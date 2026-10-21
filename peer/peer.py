# A minimal P2P peer. It can listen for connections, or send a PING to another peer.
#
# Usage:
#   python -m peer.peer listen <port>
#   python -m peer.peer ping <host> <port>

import socket
import sys

from peer import messages


def run_listener(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", port))
    server.listen()
    print(f"listening on port {port}")

    while True:
        connection, address = server.accept()
        handle_connection(connection)
        connection.close()


# Greet a connected peer, then answer its messages until it disconnects.
def handle_connection(connection):
    messages.send(connection, {"type": "HELLO"})
    while True:
        try:
            message = messages.receive(connection)
        except (ConnectionError, OSError):
            break
        print(f"received {message['type']}")
        if message["type"] == "PING":
            messages.send(connection, {"type": "PONG"})


def run_pinger(host, port):
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((host, port))

    greeting = messages.receive(connection)
    print(f"received {greeting['type']}")

    messages.send(connection, {"type": "HELLO"})
    messages.send(connection, {"type": "PING"})

    reply = messages.receive(connection)
    print(f"received {reply['type']}")

    connection.close()


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "listen":
        run_listener(int(sys.argv[2]))
    elif len(sys.argv) == 4 and sys.argv[1] == "ping":
        run_pinger(sys.argv[2], int(sys.argv[3]))
    else:
        print("usage:")
        print("  python -m peer.peer listen <port>")
        print("  python -m peer.peer ping <host> <port>")


if __name__ == "__main__":
    main()