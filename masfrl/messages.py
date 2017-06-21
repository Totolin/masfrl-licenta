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
    return str(message) + symbols['end']


def decode_message(message):
    message = message.replace(symbols['end'], '')
    return eval(message)


def stream_stop(chunk):
    if not chunk:
        return True
    return True if symbols['end'] in chunk else False
