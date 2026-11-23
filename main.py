from scanner import scan

def main():
    file_path = input("Enter path to the file: ")

    try:
        with open(file_path, 'rb') as file:
            data = file.read()

        signatures = scan(data)
        for signature, offsets in signatures.items():
            print("Signature -" + signature + "- found at positions: " + str(offsets))

    except FileNotFoundError:
        print("File not found")


if __name__ == "__main__":
    main()

