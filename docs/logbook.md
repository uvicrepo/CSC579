# Project Logbook

How Bot Behaviour Affects Structure-Based Detection of P2P Botnets

CSC579, Fall 2026

This logbook records the work done on the project, in date order. Each entry lists what was done, what was tested, and what comes next.

---

## 2026-10-13

### Done

- Added `peer/framing.py`. It wraps each message with a 4-byte length prefix and a SHA-256 hash, and reads one complete message back from a connection. Messages with a wrong hash are rejected. Frames larger than 1 MB are also rejected.
- Added `tests/test_framing.py` with three tests using Python's built-in unittest module.

### Tested

Command: `python3 -m unittest -v tests.test_framing`

Result: 3 tests ran, all passed.

1. A message comes through unchanged.
2. Two messages sent together are read back as two separate messages.
3. A message with one changed byte is rejected.

### Notes

- The length prefix and SHA-256 check come from the peer program spec in the definition document.
- The tests use a socket pair inside one program, not two separate programs on a real port.
- A message arriving in pieces is not really tested yet.

### Next

Two peers on local ports exchanging HELLO, PING, and PONG.