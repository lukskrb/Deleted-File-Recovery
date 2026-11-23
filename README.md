# Deleted-File-Recovery

A Python-based digital forensics project focused on recovering
deleted PNG, JPEG, and PDF files from FAT32 disk images.

## Current functionality

- Binary signature scanning for PNG, JPEG, and PDF
- Detection of signature offsets
- Automated tests using pytest

## Usage

Run the scanner:

    python main.py

Enter the path to a binary file when prompted.

## Tests

    python -m pytest

## Project status

Work in progress. File recovery, FAT32 parsing, file validation,
and fragmented file reconstruction are planned features.