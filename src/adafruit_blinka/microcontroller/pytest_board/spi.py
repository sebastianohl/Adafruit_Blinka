# SPDX-FileCopyrightText: 2024 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""SPI class for a generic agnostic board."""

# from .rp2040_u2if import rp2040_u2if

import socket
import os

from threading import Thread, Event
from queue import Queue
from select import select
import json
import base64

break_threads = Event()


def spi_socket(incoming, outgoing, thread_fd, index):
    # Set the path for the Unix socket
    socket_path = f'/tmp/SPI{index}'

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

    print('Server is listening for incoming connections...')
    while not break_threads.is_set():
        # accept connections
        r, w, x = select([server, thread_fd], [], [], 1)
        if server in r:
            connection, client_address = server.accept()

            try:
                print('Connection from', str(connection).split(", ")[0][-4:])

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
                        incoming.put(data)

                    if thread_fd in r:
                        thread_fd.recv(100)  # clear pipe
                        while not outgoing.empty():
                            #print("send data")
                            data = json.dumps({
                                "data":
                                base64.b64encode(outgoing.get()).decode()
                            })
                            connection.sendall(data.encode())
            except:
                print("lost connection")
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
class SPI:
    """SPI Base Class for a generic agnostic board."""

    MSB = 0

    def __init__(self, index, *, baudrate=100000):
        self._index = index
        self._frequency = baudrate

        self._incoming = Queue()
        self._outgoing = Queue()
        # Create a socket pair using Unix domain protocol
        (self._child_fd, self._thread_fd) = socket.socketpair(socket.AF_UNIX)

        self._thread = Thread(target=spi_socket,
                              args=(
                                  self._incoming,
                                  self._outgoing,
                                  self._thread_fd,
                                  index,
                              ))
        self._thread.start()

    def __del__(self):
        break_threads.set()
        self._child_fd.send("shutdown".encode())
        self._thread.join()

    # pylint: disable=too-many-arguments,unused-argument
    def init(
        self,
        baudrate=1000000,
        polarity=0,
        phase=0,
        bits=8,
        firstbit=MSB,
        sck=None,
        mosi=None,
        miso=None,
    ):
        """Initialize the Port"""
        self._frequency = baudrate

    # pylint: enable=too-many-arguments

    @property
    def frequency(self):
        """Return the current frequency"""
        return self._frequency

    # pylint: disable=unnecessary-pass
    def write(self, buf, start=0, end=None):
        """Write data from the buffer to SPI"""
        if buf is None or len(buf) < 1:
            return
        if end is None:
            end = len(buf)

        self._outgoing.put(buf[start:end])
        self._child_fd.send("data is here".encode())

    # pylint: disable=unnecessary-pass
    def readinto(self, buf, start=0, end=None, write_value=0):
        """Read data from SPI and into the buffer"""

        if buf is None or len(buf) < 1:
            return
        if end is None:
            end = len(buf)

        self._outgoing.put([write_value] * (end - start))
        self._child_fd.send("data is here".encode())
        data = self._incoming.get()
        for i in range(end - start):  # 'readinto' the given buffer
            buf[start + i] = data[i]

    # pylint: disable=too-many-arguments, unnecessary-pass
    def write_readinto(self,
                       buffer_out,
                       buffer_in,
                       out_start=0,
                       out_end=None,
                       in_start=0,
                       in_end=None):
        """Perform a half-duplex write from buffer_out and then
        read data into buffer_in
        """

        if buffer_out is None or buffer_in is None:
            return
        if len(buffer_out) < 1 or len(buffer_in) < 1:
            return
        if out_end is None:
            out_end = len(buffer_out)
        if in_end is None:
            in_end = len(buffer_in)
        if out_end - out_start != in_end - in_start:
            raise RuntimeError("Buffer slices must be of equal length.")

        self._outgoing.put(list(buffer_out[out_start:out_end + 1]))
        self._child_fd.send("data is here".encode())
        data = self._incoming.get()
        for i in range((in_end - in_start)):
            buffer_in[i + in_start] = data[i]
