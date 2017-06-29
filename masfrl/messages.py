"""
    Module used to store common messages and methods related to messages.
    Used by both MASFRL-Slave and MASFRL-Master, when communicating over socket.
"""


client = {
    "send_work": {
        "type": "response",
        "content": "work"
    }
}

server = {
    "work": {
        "type": "work",
        "content": ""
    },
    "request_work": {
        "type": "request",
        "content": "work"
    }
}

symbols = {
    "end": "END"
}


def encode_message(message):
    """
    Encodes a message to be sent over the socket.
    Adds a terminal symbol for the other end to stop
    :param message: String representation of the message
    :return: Encoded message
    """
    return str(message) + symbols['end']


def decode_message(message):
    """
    Decodes a message received from a socket connection
    Removes terminal message used to stop byte transfers.
    :param message: Encoded message
    :return: Decoded message
    """
    message = message.replace(symbols['end'], '')
    return eval(message)


def stream_stop(chunk):
    """
    Determines if the byte chunk contains standard terminal symbol
    :param chunk: Byte chunk received 
    :return: True if chunk contains terminal symbol
    """
    if not chunk:
        return True
    return True if symbols['end'] in chunk else False
