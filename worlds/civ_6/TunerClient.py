from logging import Logger
import socket

ADDRESS = "127.0.0.1"
PORT = 4318

CLIENT_PREFIX = "APSTART:"
CLIENT_POSTFIX = ":APEND"


def decode_mixed_string(data):
    return ''.join(chr(b) if 32 <= b < 127 else '?' for b in data)


class TunerException(Exception):
    pass


class TunerTimeoutException(TunerException):
    pass


class TunerErrorException(TunerException):
    pass


class TunerConnectionException(TunerException):
    pass


class TunerClient:
    """Interfaces with Civilization via the tuner socket"""
    logger: Logger

    def __init__(self, logger):
        self.logger = logger

    def __parse_response(self, response: str) -> str:
        """Parses the response from the tuner socket"""
        split = response.split(CLIENT_PREFIX)
        if len(split) > 1:
            start = split[1]
            end = start.split(CLIENT_POSTFIX)[0]
            return end
        elif  "ERR:" in response:
            raise TunerErrorException(response.replace("?", ""))
        else:
            return ""

    def send_game_command(self, command_string: str):
        """Small abstraction that prefixes a command with GameCore.Game."""
        return self.send_command("GameCore.Game." + command_string)

    def send_command(self, command_string: str):
        """Send a raw commannd"""
        self.logger.debug("Sending Command: " + command_string)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        b_command_string = command_string.encode('utf-8')
        # Send data to the server
        command_prefix = b"CMD:0:"
        delimiter = b"\x00"
        full_command =  b_command_string
        message = command_prefix + full_command + delimiter
        message_length = len(message).to_bytes(1, byteorder='little')

        # game expects this to be added before any command that is sent, indicates payload size
        message_header = message_length + b"\x00\x00\x00\x03\x00\x00\x00"
        data = message_header + command_prefix + full_command + delimiter

        server_address = (ADDRESS, PORT)
        try:
            sock.connect(server_address)
            sock.sendall(data)

            sock.settimeout(.5)

            # big enough to handle get_checked_locations_response
            received_data = sock.recv(1024 * 4)
            data = decode_mixed_string(received_data)
            self.logger.debug('Received:')
            self.logger.debug(data)
            return self.__parse_response(data)

        except socket.timeout:
            self.logger.debug('Timeout occurred while receiving data')
            raise TunerTimeoutException()
        except Exception as e:
            self.logger.debug('Error occurred while receiving data')
            # check if No connection could be made is present in the error message
            if "No connection could be made" in str(e):
                raise TunerConnectionException(e)
            else:
                raise TunerErrorException(e)
        finally:
            sock.close()