# Deleted-File-Recovery

A Python-based digital forensics project focused on recovering
deleted PNG, JPEG, and PDF files from FAT32 disk images.

## Current functionality

- Binary signature scanning for PNG, JPEG, and PDF
- Detection of signature offsets
- Memory-efficient chunk-based file scanning
- Detection of signatures acros chunk boundaries
- Prevention of duplicate signature detection
- SHA-256 hash calculation
- JSON manifest - containing file names, sizes, and SHA 256 hashes
- Automated tests using pytest

# Usage

## Binary signature scanner

Run the scanner:

    python main.py

Enter the path to a binary file when prompted.

## Test data manifest

Place the original test files in the test_data/originals/ directory (some are already provided).

Run the manifest generation script from the project root:

    python -m scripts.generate_manifest

The generated manifest is saved to test_data/manifest.json and will be used to evaluate file recovery accuracy.

## Tests

Run the automated tests:

    python -m pytest

## Project status

Work in progress. File recovery, FAT32 parsing, file validation,
and fragmented file reconstruction are planned features.