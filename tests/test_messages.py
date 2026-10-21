import socket
import unittest

from peer import messages


class TestMessages(unittest.TestCase):
    def setUp(self):
        self.a, self.b = socket.socketpair()

    def tearDown(self):
        self.a.close()
        self.b.close()

    def test_round_trip(self):
        messages.send(self.a, {"type": "PING"})
        self.assertEqual(messages.receive(self.b), {"type": "PING"})

    def test_message_with_fields(self):
        sent = {"type": "HELLO", "node_id": "n1", "port": 5000}
        messages.send(self.a, sent)
        self.assertEqual(messages.receive(self.b), sent)


if __name__ == "__main__":
    unittest.main()