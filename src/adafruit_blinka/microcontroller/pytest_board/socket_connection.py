# SPDX-FileCopyrightText: 2025 Sebastian Ohl
#
# SPDX-License-Identifier: MIT
"""socket connection for test service"""

import socket
import os

from threading import Thread, Event
from queue import Queue
from select import select
import json
import base64

break_threads = Event()


def spi_socket(incoming, outgoing, thread_fd, socket_path):
    # remove the socket file if it already exists
    try:
        os.unlink(socket_path)
    except OSError:
        if os.path.exists(socket_path):
            raise

    # Create the Unix socket server
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(socket_path)
    server.listen(1)
    server.setblocking(True)

    print(f'Server is listening for incoming connections on {socket_path}...')
    while not break_threads.is_set():
        # accept connections
        r, w, x = select([server, thread_fd], [], [], 1)
        if server in r:
            connection, client_address = server.accept()

            try:
                print(
                    f'Connection from {str(connection).split(", ")[0][-4:]} to {socket_path}'
                )

                # receive data from the client
                while not break_threads.is_set():
                    r, w, x = select([connection, thread_fd], [], [], 1.0)
                    if break_threads.is_set():
                        break
                    elif connection in r:
                        # print('Received data')
                        data = connection.recv(100000)
                        if not data:
                            break
                        incoming.put(json.loads(data))

                    if thread_fd in r:
                        thread_fd.recv(100)  # clear pipe
                        while not outgoing.empty():
                            #print("send data")
                            data = json.dumps(outgoing.get())
                            connection.sendall(data.encode())
            except:
                print(f"lost connection on {socket_path}")
            finally:
                # close the connection
                connection.close()

        if thread_fd in r:  # clear old data
            thread_fd.recv(100)  # clear pipe
            while not outgoing.empty():
                outgoing.get()

    # remove the socket file
    os.unlink(socket_path)

    print(f"shutting down socket {socket_path}")


# pylint: disable=protected-access, no-self-use
class SocketConnection:
    """Socket Connection Base Class for testing service."""

    def __init__(self, socket_path: str):
        self._socket_path = socket_path

        self._incoming = Queue()
        self._outgoing = Queue()
        # Create a socket pair using Unix domain protocol
        (self._child_fd, self._thread_fd) = socket.socketpair(socket.AF_UNIX)

        self._thread = Thread(target=spi_socket,
                              args=(
                                  self._incoming,
                                  self._outgoing,
                                  self._thread_fd,
                                  self._socket_path,
                              ))
        self._thread.start()

    def __del__(self):
        break_threads.set()
        self._child_fd.send("shutdown".encode())
        self._thread.join()

    # pylint: disable=unnecessary-pass
    def _send_packet(self, packet):
        """Write data via socket"""

        self._outgoing.put(packet)
        self._child_fd.send("data is here".encode())

    # pylint: disable=unnecessary-pass
    def _receive_packet(self):
        """Read data from socket, blocking if nothing available"""

        return self._incoming.get()
