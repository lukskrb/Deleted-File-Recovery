from scanner import scan_file
import pytest

png = b"\x89PNG\r\n\x1a\n"
data_ = b"\x00" * 13 + png

def test_signature_crosses_chunk_boundary(tmp_path):
    file_path = tmp_path / "test.bin"
    file_path.write_bytes(data_)

    result = scan_file(file_path, chunk_size=16)

    assert result["PNG"] == [13]

def test_signature_spans_multiple_chunks(tmp_path):
    file_path = tmp_path / "test.bin"
    file_path.write_bytes(data_)

    result = scan_file(file_path, chunk_size=2)

    assert result["PNG"] == [13]

def test_multiple_signatures_across_chunks(tmp_path):
    png = b"\x89PNG\r\n\x1a\n"
    jpeg = b"\xff\xd8"
    pdf = b"%PDF-"

    data = (
        b"\x00" * 13
        + png
        + b"\x00" * 10
        + jpeg
        + b"\x00" * 10
        + pdf
    )

    file_path = tmp_path / "multiple.bin"
    file_path.write_bytes(data)

    result = scan_file(file_path, chunk_size=16)

    assert result["PNG"] == [13]
    assert result["JPEG"] == [31]
    assert result["PDF"] == [43]


def test_no_duplicate_signatures(tmp_path):
    jpeg = b"\xff\xd8"

    data = jpeg + b"\x00" * 6 + jpeg

    file_path = tmp_path / "duplicates.bin"
    file_path.write_bytes(data)

    result = scan_file(file_path, chunk_size=4)

    assert result["JPEG"] == [0, 8]


def test_empty_file(tmp_path):
    file_path = tmp_path / "empty.bin"
    file_path.write_bytes(b"")

    result = scan_file(file_path, chunk_size=16)

    assert result == {
        "PNG": [],
        "PDF": [],
        "JPEG": []
    }

@pytest.mark.parametrize("chunk_size", [0, -1, -100, 1.5, "16", None, True])
def test_invalid_chunk_size(tmp_path, chunk_size):
    file_path = tmp_path / "test.bin"
    file_path.write_bytes(b"\x89PNG\r\n\x1a\n")

    with pytest.raises(ValueError):
        scan_file(file_path, chunk_size=chunk_size)