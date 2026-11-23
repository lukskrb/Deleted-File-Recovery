FILE_SIGNATURES = {
    "PNG": b"\x89PNG\r\n\x1a\n",
    "PDF": b"%PDF-",
    "JPEG": b"\xff\xd8",
}

def find_signatures(data, signature):
    offset = data.find(signature)
    offsets = []

    while offset != -1:
        offsets.append(offset)
        offset = data.find(signature, offset + 1)

    return offsets

def scan(data):
    signatures = {}

    for format_name, signature in FILE_SIGNATURES.items():
        offsets = find_signatures(data, signature)
        signatures[format_name] = offsets

    return signatures