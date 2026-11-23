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

def scan_file(file_path, chunk_size=4096):
    if type(chunk_size) != int or chunk_size <= 0:
        raise ValueError("Chunk size must be positive and not 0")

    already_checked = 0
    overlap_size = max(len(sig) for sig in FILE_SIGNATURES.values()) - 1
    prev_tail = b""

    all_signatures = {name: [] for name in FILE_SIGNATURES}

    with open(file_path, 'rb') as file:
        while True:
            data = file.read(chunk_size)

            if not data:
                break

            combined_data = prev_tail + data
            signatures = scan(combined_data)

            combined_start = already_checked - len(prev_tail)

            for sign, offsets in signatures.items():
                for offset in offsets:

                    signature_length = len(FILE_SIGNATURES[sign])
                    absolute_offset = offset + combined_start

                    if absolute_offset + signature_length > already_checked:
                        all_signatures[sign].append(absolute_offset)

            #print(f"Offset {already_checked}, Length {len(data)}")
            already_checked = already_checked + len(data)

            prev_tail = combined_data[-overlap_size:]
    return all_signatures