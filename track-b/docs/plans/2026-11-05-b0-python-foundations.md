# B0 · Python foundations for supply-chain AI applications

Adapt the teaching progression from the BFSI M0 deck and its share-purchase/
wealth examples into a preparatory Track B module. Deliver the established
Marp Markdown slide format, complete runnable `.py` snippets, and a derived
Gamma text copy. Keep the BFSI source intact.

Use tiny synthetic container-service examples. A transport quote supplies
simple arithmetic without pretending to implement PortOps demurrage tariffs.
Container records then introduce collections, control flow and returned data.
Functions, explicit checks, objects, dates, JSON and configuration prepare
learners to read B1. SQL, decorators, a local API, async calls, logs and tests
form a follow-on application bridge for B2–B4/PortOps.

All numbered snippets use the standard library and run without model access,
an API key, a database server or a previous snippet. The optional FastAPI
server declares its separate dependency command. B0 does not duplicate B1's
hosted/local model demonstrations or change the existing lockfile.

- [x] Create small scripts and a teaching/run map, with expected outputs and
  one controlled learner change per file.
- [x] Write concepts incrementally before their code illustrations, using
  the current slide styling, presenter notes and links to full runnable files.
- [x] Generate the Gamma copy from that same source and register B0 in the
  Track B indexes as preparation before B1, without changing the timetable.
- [x] Execute every script from a separate directory, verify the optional
  server contract, check source/deck links and inspect rendered slide layout.
