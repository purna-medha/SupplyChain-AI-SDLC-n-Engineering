# B0 verification · 5 November 2026

## Executed material

- All **14 numbered snippets** ran independently from a temporary working
  directory with exit status zero, using standard-library Python.
- The examples were checked with both the system interpreter and the shared
  Track B Python environment.
- Eight controlled variations ran in disposable copies: four-container quote,
  changed status route, free-time boundary, unknown SQL record, unknown async
  record, named arguments/type-hint behavior, environment configuration without
  printing a key, and the deliberate missing-validation test failure.
- The test illustration initially passes both cases. Removing its positivity
  check in a temporary copy causes the zero-container test to fail as intended.
- The optional FastAPI application passed health, known/unknown container and
  documentation-route checks with TestClient. Its additional packages were
  also resolved and checked through `uv run --locked --with fastapi --with uvicorn`.
- Marp rendered the final **38 slides** to PNG. All pages were visually
  inspected on contact sheets; dense function and command slides were also
  inspected individually. Text/code fit the existing 16:9 layout.
- The derived Gamma copy has the same 38 slides and 29 code/diagram blocks,
  with configuration, presenter notes and local illustration links removed.

Source files retained the passing teaching baseline. The temporary variations
did not edit the distributed snippets. No model request, provider key, live
shipment record or capstone database was needed.

## Review

Independent review checked Python semantics, uv commands, async usage, source
links and the distinction between the illustrative transport quote and PortOps
demurrage. The f-string output explanation was added before its later use in
the function example. No other material findings remained.

## Boundaries

The quote examples enforce positivity only; type hints do not enforce integer
counts. The date example uses a fixed classroom as-of date. SQLite storage is
in memory. Async yielding is demonstrated without a network call. The optional
API was checked in process; no external server or browser session is required
for those handler checks. The API environment emitted its existing
Starlette/httpx TestClient deprecation warning; checks still passed.

These checks establish that the examples run and illustrate their stated
mechanisms, not that they implement production booking or pricing contracts.
Temporary render and execution artifacts are under
`/private/tmp/maersk-b0-verification-20261105/`.
