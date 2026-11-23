from scanner import scan

def test_png_signature():
    expected_result = {"PNG": [100], "PDF": [], "JPEG": []}

    data = b"\x00" * 100 + b"\x89PNG\r\n\x1a\n"

    actual_result = scan(data)

    assert expected_result == actual_result

def test_empty_data():
    expected_result = {"PNG": [], "PDF": [], "JPEG": []}

    data = b""

    actual_result = scan(data)

    assert expected_result == actual_result

def test_multiple_signatures():
    expected_result = {"PNG": [100], "PDF": [190], "JPEG": [158]}

    data = b"\x00" * 100 + b"\x89PNG\r\n\x1a\n" + b"\x00" * 50 + b"\xff\xd8" + b"\x00" * 30 + b"%PDF-"

    actual_result = scan(data)

    assert expected_result == actual_result

def test_multiple_same_signatures():
    expected_result = {"PNG": [0, 18], "PDF": [], "JPEG": []}

    data = b"\x89PNG\r\n\x1a\n" + b"\x00" * 10 + b"\x89PNG\r\n\x1a\n"

    actual_result = scan(data)

    assert expected_result == actual_result