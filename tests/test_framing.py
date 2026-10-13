import socket
import unittest

from peer.framing import FrameError, encode, read_message


class TestFraming(unittest.TestCase):
    def setUp(self):
        self.a, self.b = socket.socketpair()

    def tearDown(self):
        self.a.close()
        self.b.close()

    def test_round_trip(self):
        self.a.sendall(encode(b"hello"))
        self.assertEqual(read_message(self.b), b"hello")

    def test_two_messages_sent_together(self):
        self.a.sendall(encode(b"first") + encode(b"second"))
        self.assertEqual(read_message(self.b), b"first")
        self.assertEqual(read_message(self.b), b"second")

    def test_corrupted_payload_is_rejected(self):
        frame = bytearray(encode(b"hello"))
        frame[-1] ^= 0xFF  # flip the last byte
        self.a.sendall(bytes(frame))
        with self.assertRaises(FrameError):
            read_message(self.b)


if __name__ == "__main__":
    unittest.main()