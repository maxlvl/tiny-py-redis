class ConnectionBuffer:
    def __init__(self, connection):
        self.connection = connection
        self.buffer = b''

    def read(self, buffersize):
        if len(self.buffer) < buffersize:
            data = self.connection.recv(1024)
            if not data:
                return None
            self.buffer += data

            data, self.buffer = self.buffer[:buffersize], self.buffer[buffersize:]
            return data


    def read_until_delimiter(self, delimiter):
        while delimiter not in self.buffer:
            data = self.connection.recv(1024)

            if not data:
                return None # socket closed

            self.buffer += data
            # TODO: look into bytearray partition https://en.wikiversity.org/wiki/Python_Concepts/Bytes_objects_and_Bytearrays
            data_before_delimiter, delimiter, self.buffer = self.buffer.partition(delimiter)
            return data_before_delimiter

class Parser:
    def __init__(self, connection):
        self.connection = ConnectionBuffer(connection)

    def decode(self):
        data_type_byte = self.connection.read(1)

        # this is an array command
        if data_type_byte == b"*":
            return self.decode_array()


    def decode_array(self):
        result = []
        array_length = int(self.connection.read_until_delimiter(b"\r\n"))

        for _ in range(array_length):
            result.append(self.decode())

        return result


