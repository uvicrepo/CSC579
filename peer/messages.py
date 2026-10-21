import json

from peer import framing

# Turn messages into bytes and back, using the framing layer.

def send(sock, message):
    data = json.dumps(message).encode("utf-8")
    sock.sendall(framing.encode(data))


def receive(sock):
    data = framing.read_message(sock)
    return json.loads(data.decode("utf-8"))