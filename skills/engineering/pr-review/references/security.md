# Factor checklist: security

Report an issue only if untrusted input can reach it. A risky-looking pattern with no path from outside input isn't a finding.

- Injection: SQL or NoSQL queries built by string concatenation or formatting; `exec`, `eval`, or shell commands that include user data; template injection.
- Input handling: does the code validate input at the trust boundary, not deep inside? Does it deserialize untrusted data (pickle, `yaml.load`, unbounded JSON)?
- Authentication and authorization: who can call each new endpoint? Does the handler check that the caller owns the requested resource, or only that they're logged in? Checking only the login is an insecure direct object reference (IDOR).
- Secrets: hardcoded keys, passwords, or tokens; secrets in logs or error messages; real-looking secrets in test fixtures.
- Web: cross-site scripting (XSS) through unescaped output, `innerHTML`, or `dangerouslySetInnerHTML`; cross-site request forgery (CSRF) on endpoints that change state; open redirects; server-side request forgery (SSRF) from user-supplied URLs.
- Crypto and randomness: homegrown crypto, tokens from a random generator that isn't cryptographically secure, weak password hashing.
- Dependencies: are new packages well known and pinned? Do any names look like typosquats of popular packages?
- Data exposure: personal data in logs, API responses that return more than the caller needs, stack traces sent to clients.
- Attack path: report the route from the input source to the vulnerable code (the sink). If you can't trace one, lower your stated confidence.
