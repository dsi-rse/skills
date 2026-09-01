# Factor checklist: security

Only report reachable issues — a pattern-match without a path from untrusted input is noise.

- Injection: SQL/NoSQL built by string concat or format; shell/`exec`/`eval` with user data; template injection.
- Input handling: validation at the trust boundary, not deep inside; deserialization of untrusted data (pickle, yaml.load, unbounded JSON).
- AuthN/AuthZ: new endpoints — who can call them? Object-level checks (IDOR): does the handler verify the caller owns the resource, or only that they're logged in?
- Secrets: hardcoded keys/passwords/tokens, secrets in logs or error messages, secrets in test fixtures that look real.
- Web: XSS via unescaped output / innerHTML / dangerouslySetInnerHTML; CSRF on state-changing endpoints; open redirects; SSRF from user-supplied URLs.
- Crypto & randomness: homegrown crypto, non-CSPRNG for tokens, weak hashing for passwords.
- Dependencies: new packages — are they well-known? Pinned? Any typosquat-looking names?
- Data exposure: PII in logs, overly broad API responses, stack traces to clients.
- Report with the attack path: input source → sink. If you can't trace one, mark confidence accordingly.
