import struct


class Communication:

    def __init__(self, sock):
        self._sock = sock

    def send(self, message_str):
        message_bytes = message_str.encode("utf-8")
        size_prefix = struct.pack("!I", len(message_bytes))
        self._sock.sendall(size_prefix)
        self._sock.sendall(message_bytes)

    def recv_message_str(self):

        size_buffer = b""
        while len(size_buffer) != 4:
            recv_ret = self._sock.recv(4 - len(size_buffer))
            if len(recv_ret) == 0:
                raise Exception("socket disconnected")
            size_buffer += recv_ret
        size = struct.unpack("!I", size_buffer)

        message_buffer = b""
        while len(message_buffer) != size[0]:
            recv_ret = self._sock.recv(size[0] - len(message_buffer))
            if len(recv_ret) == 0:
                raise Exception("socket disconnected")
            message_buffer += recv_ret
        return message_buffer.decode("utf-8", errors="ignore")
