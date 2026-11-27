import hashlib
from pathlib import Path
import json

def calculate_sha256(file_path, chunk_size=4096):
    if type(chunk_size) != int or chunk_size <= 0:
        raise ValueError("Chunk size must be a positive integer")

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)

            if not chunk:
                break

            sha256.update(chunk)

    return sha256.hexdigest()

def generate_manifest(directory_path):
    directory = Path(directory_path)

    files = []

    for file in sorted(directory.iterdir()):
        if file.is_file():
            files.append({"filename": file.name,
                          "size": file.stat().st_size,
                          "sha256": calculate_sha256(file)})

    return {"files": files}


def save_manifest(manifest, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=4)

if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent

    manifest_ = generate_manifest(project_root / "test_data" / "originals")
    save_manifest(manifest_, project_root / "test_data" / "manifest.json")