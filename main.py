from scanner import scan_file

def main():
    file_path = input("Enter path to the file: ")

    try:
        signatures = scan_file(file_path, chunk_size=16)

        for signature, offsets in signatures.items():
            print(f"Signature -{signature}- found at positions: {str(offsets)}")

    except FileNotFoundError:
        print("File not found")


if __name__ == "__main__":
    main()

