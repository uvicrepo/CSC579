"""Message framing for the peer program.

Each frame on the wire is:
    4 bytes   length of the rest of the frame (big-endian)
    32 bytes  SHA-256 hash of the payload
    N bytes   payload
"""

import hashlib
import struct

HEADER = struct.Struct(">I")
HASH_SIZE = 32
MAX_FRAME = 1_000_000  # reject anything larger than 1 MB


class FrameError(Exception):
    """The frame is too large or its hash does not match."""


def encode(payload: bytes) -> bytes:
    """Wrap a payload in a frame."""
    digest = hashlib.sha256(payload).digest()
    return HEADER.pack(HASH_SIZE + len(payload)) + digest + payload


def read_exact(sock, n: int) -> bytes:
    """Read exactly n bytes from a socket."""
    data = b""
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise ConnectionError("connection closed")
        data += chunk
    return data


def read_message(sock) -> bytes:
    """Read one frame from a socket and return its payload."""
    (length,) = HEADER.unpack(read_exact(sock, HEADER.size))
    if length < HASH_SIZE or length > MAX_FRAME:
        raise FrameError(f"bad frame length {length}")
    body = read_exact(sock, length)
    digest, payload = body[:HASH_SIZE], body[HASH_SIZE:]
    if hashlib.sha256(payload).digest() != digest:
        raise FrameError("hash mismatch")
    return payload