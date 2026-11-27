import json
import pytest

from scripts.generate_manifest import (
    calculate_sha256,
    generate_manifest,
    save_manifest
)


def test_calculate_sha256(tmp_path):
    file_path = tmp_path / "test.bin"
    file_path.write_bytes(b"abc")

    expected = (
        "ba7816bf8f01cfea414140de5dae2223"
        "b00361a396177a9cb410ff61f20015ad"
    )

    assert calculate_sha256(file_path) == expected


@pytest.mark.parametrize("chunk_size", [1, 2, 4, 4096])
def test_sha256_independent_of_chunk_size(tmp_path, chunk_size):
    file_path = tmp_path / "test.bin"
    file_path.write_bytes(b"abc")

    assert calculate_sha256(file_path, chunk_size) == (
        "ba7816bf8f01cfea414140de5dae2223"
        "b00361a396177a9cb410ff61f20015ad"
    )


def test_generate_manifest(tmp_path):
    file_path = tmp_path / "test.bin"
    file_path.write_bytes(b"abc")

    result = generate_manifest(tmp_path)

    assert result == {
        "files": [
            {
                "filename": "test.bin",
                "size": 3,
                "sha256": (
                    "ba7816bf8f01cfea414140de5dae2223"
                    "b00361a396177a9cb410ff61f20015ad"
                )
            }
        ]
    }


def test_empty_directory(tmp_path):
    assert generate_manifest(tmp_path) == {"files": []}


def test_manifest_ignores_subdirectories(tmp_path):
    (tmp_path / "subdirectory").mkdir()

    assert generate_manifest(tmp_path) == {"files": []}


def test_save_manifest(tmp_path):
    manifest = {"files": []}
    output_path = tmp_path / "manifest.json"

    save_manifest(manifest, output_path)

    with open(output_path, "r", encoding="utf-8") as f:
        result = json.load(f)

    assert result == manifest


@pytest.mark.parametrize("chunk_size", [0, -1, 1.5, "16", None, True])
def test_invalid_chunk_size(tmp_path, chunk_size):
    file_path = tmp_path / "test.bin"
    file_path.write_bytes(b"abc")

    with pytest.raises(ValueError):
        calculate_sha256(file_path, chunk_size)