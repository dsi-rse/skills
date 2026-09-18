# Resources: hardware, parallelism, and shepherding

## 1. Probe before you plan

Do this in Phase 1, before estimating anything. Report what you find to the user and ask them to
confirm.

```
nproc                                   # logical cores
lscpu | grep -E 'Model name|Socket|Core|Thread'
free -g                                 # RAM
df -h <the output volume>               # disk space where models/artifacts will go
nvidia-smi                              # GPU model, total and free VRAM, current utilization
```

Adapt for the platform (`sysctl -n hw.ncpu` and `vm_stat` on macOS; `nvidia-smi` is absent on Apple
silicon, where the relevant question is unified-memory size).

Then probe the software, which matters just as much:

- Which Python/R environment is active, and which one *should* be? Repos often specify one.
- Which frameworks are installed, at which versions?
- **Is the installed build actually GPU-capable?** A CPU-only wheel on a machine with a GPU is a
  classic silent disaster: everything runs, nothing errors, and the campaign takes twenty times
  longer than planned. Check it explicitly — query the framework for device availability and run a
  one-line tensor operation on the device. Do not infer it from `nvidia-smi` alone.
- Is another user or job already using the GPU? Check current utilization and memory before
  assuming it is yours.

Record all of this in the durable documentation. It is what makes the timings interpretable later.

## 2. Use the whole machine

**A single-threaded, CPU-only search on a multi-core box with a GPU is a bug.** Concretely:

**Tree-based models** parallelize across trees and are usually the easy case: give them the core
count. But if you are *also* running several configurations concurrently, divide — `n_workers ×
threads_per_worker ≈ n_cores`. Oversubscription is worse than either extreme, because the threads
fight over cache. Watch for libraries that read `OMP_NUM_THREADS` or equivalent and quietly grab
every core regardless of what you asked for; set the environment variable explicitly per worker.

**Neural networks on a single GPU** are usually GPU-serial: train one model at a time and focus on
keeping the GPU busy rather than on parallelizing across models.

- data-loader worker processes: roughly `n_cores - 2`
- pinned memory and prefetching enabled
- mixed precision (AMP / bf16) — frequently close to a 2× speedup with no measurable accuracy cost,
  and it should be on unless you have a reason
- batch size as large as VRAM allows, with the learning rate scaled to match
- if the models are small and VRAM is plentiful, running two or three training processes
  concurrently on one GPU can raise utilization substantially — measure it rather than assuming
  either way

**Watch for the data pipeline being the bottleneck.** If GPU utilization sits at 30% while all your
CPU cores are pinned, you are not training — you are decoding JPEGs. See §3.

**Independent configurations are embarrassingly parallel** across CPU cores. Prefer process-level
parallelism over threads for anything holding the GIL.

**Set the thread/worker counts as explicit, logged parameters**, not as library defaults, so the
timings in the ledger mean something.

## 3. Precompute what is constant

**This is usually the single biggest speedup available, and it is easy to miss.**

Any transformation that is *identical across every configuration in the search* should be computed
once, cached to disk, and loaded thereafter:

- text embeddings, when the encoder is fixed
- frozen-backbone image features, when the backbone and the input preprocessing are fixed
- decoded, resized, normalized image tensors (memory-mapped arrays or a shard format)
- masked, cropped, canonically rotated images, when those preprocessing choices are fixed
- joins, feature engineering, and any expensive derived columns
- the fold assignment itself

A sweep over a hundred MLP heads on cached embeddings takes minutes; the same sweep re-encoding the
text each time takes hours and produces identical results.

**The caveat:** cache only what is genuinely constant. If the input representation is itself a
search axis (`search-space.md` §1), cache each *variant* separately, keyed by a hash of the
preprocessing configuration, so you never silently mix them. Include that key in the cache filename
and in the ledger.

**Memory ceilings.** Estimate `n_examples × n_features × bytes_per_value` before loading, compare to
available RAM, and if it doesn't fit, memory-map or stream. Cap the worker count by
`RAM / peak_bytes_per_worker`, not by core count — an OOM kill twelve hours in is unrecoverable
unless you checkpointed. Watch for loader workers each holding a full copy of the dataset.

## 4. Long runs and shepherding

### Mechanics

- **Run detached, with a log file.** `nohup`, `tmux`, a systemd unit, or a background process with
  its output redirected. Never hold a multi-hour campaign inside a single foreground tool call — you
  lose the ability to check on it, and you lose everything if the session drops.
- **Log with timestamps.** Every configuration start and finish, its score, its elapsed time, the
  running total, and an ETA for the round. Flush or line-buffer, or the log will be empty exactly
  when you need it.
- **Checkpoint after every configuration.** Append its ledger row, save its artifacts, and make
  restart resume from the ledger rather than re-running completed work. A crash should cost one
  configuration, not the campaign.
- **Make the runner idempotent**: on start, read the ledger and skip anything already recorded as
  complete.
- **Fail loudly per configuration, softly per campaign.** One configuration crashing should record
  an error row and move to the next, not abort the run. But a *pattern* of crashes should stop
  everything and get your attention.

### The shepherding loop

On the cadence agreed at intake (roughly every twenty minutes is reasonable for a long unattended
run), verify:

1. **Something is running.** The process exists.
2. **Utilization matches expectation.** CPU busy for tree models, GPU busy for neural ones. Idle
   cores during a supposedly parallel sweep, or a 5%-utilized GPU during training, is a **bug to
   investigate**, not a thing to wait out. It is the most common way a campaign quietly takes four
   times as long as it should.
3. **The log advanced** since the previous check. A live process making no progress is a hang —
   deadlocked workers, a stalled network mount, an exhausted data loader.
4. **Nothing is blocked waiting for input.** A prompt nobody will answer is an all-night stall.
5. **Disk is not filling.** Checkpoints, logs, and cached tensors accumulate fast.
6. **Memory is stable.** A steadily climbing resident set means a leak and a coming OOM.

**When something has died:** read the log, diagnose the actual cause, fix it, resume from the
checkpoint, and **record the incident in the durable documentation** — what failed, why, what
changed, and how much time it cost. Then check whether the same failure could affect configurations
still queued.

**Do not paper over repeated failures.** Three crashes in the same place is a bug in the harness,
not bad luck, and continuing to restart it wastes the budget.

## 5. Fail fast

Before committing the budget, exercise **every branch** of the search space at tiny scale — a
handful of examples, one epoch, the smallest sizes, one fold. Include:

- every model family and every input representation in the enumeration
- the metric computation, on a case with a known answer
- the model **save and load round-trip**, verified to reproduce a prediction
- the ledger write and the resume-from-ledger path
- the **final-model code path**, which by construction runs only once, at the end, when a failure is
  most expensive

Then time a realistic configuration from each family at full scale and size the rounds from those
measurements (`protocol.md` §8). If the measurements contradict the plan's estimates, revise the
plan and say so.

*A crash fourteen hours in, on a code path nobody ran, is the most expensive failure mode in this
entire workflow.* Ten minutes of smoke testing is the highest-return time in the campaign.
