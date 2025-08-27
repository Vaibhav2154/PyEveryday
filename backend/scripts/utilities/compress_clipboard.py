import zipfile
import pyperclip
import os
import sys
import time


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class FileUtility:

    @staticmethod
    def compress_files(files, output_zip=None):
        
        valid_files = []
        for f in files:
            if os.path.exists(f):
                valid_files.append(f)
            else:
                print(f"{Colors.WARNING}⚠️  Path not found: {f}{Colors.ENDC}")

        if not valid_files:
            raise FileNotFoundError("No valid files or folders provided to compress.")

        
        if output_zip is None:
            if len(valid_files) == 1:
                name = os.path.basename(valid_files[0])
                output_zip = os.path.splitext(name)[0] + ".zip"
            else:
                output_zip = "archive.zip"

        
        all_files = []
        for path in valid_files:
            if os.path.isfile(path):
                all_files.append((path, os.path.basename(path)))
            elif os.path.isdir(path):
                for root, _, files_in_dir in os.walk(path):
                    for file in files_in_dir:
                        full_path = os.path.join(root, file)
                        arcname = os.path.relpath(full_path, os.path.dirname(path))
                        all_files.append((full_path, arcname))

        total = len(all_files)
        print(f"{Colors.OKBLUE}📦 Compressing {total} item(s) into '{output_zip}'{Colors.ENDC}")

        
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for idx, (full_path, arcname) in enumerate(all_files, 1):
                zipf.write(full_path, arcname=arcname)
                progress = int((idx / total) * 30)
                bar = '🟩' * progress + '⬜' * (30 - progress)
                print(f"\r[{bar}] {idx}/{total} files", end="")
                time.sleep(0.01)

        print(f"\n{Colors.OKGREEN}✅ Compression completed!{Colors.ENDC}")
        return output_zip

    @staticmethod
    def copy_to_clipboard(text):
        pyperclip.copy(text)
        print(f"{Colors.OKCYAN}📋 Copied to clipboard: '{text}'{Colors.ENDC}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"{Colors.BOLD}Usage: python compress_clipboard.py <command> [args]{Colors.ENDC}")
        print("Commands:")
        print("  compress <file/folder1> [file/folder2 ...] [output_zip]   - Compress files/folders")
        print("  copy <text>                                               - Copy text to clipboard")
        sys.exit(1)

    command = sys.argv[1]

    try:
        if command == "compress":
            if len(sys.argv) < 3:
                print("Usage: compress <file/folder1> [file/folder2 ...] [output_zip]")
                sys.exit(1)

            *paths, last_arg = sys.argv[2:]
            output_zip = None
            if len(paths) >= 1 and last_arg.lower().endswith(".zip"):
                output_zip = last_arg
            else:
                paths.append(last_arg)

            zip_file = FileUtility.compress_files(paths, output_zip)
            FileUtility.copy_to_clipboard(zip_file)

        elif command == "copy":
            if len(sys.argv) < 3:
                print("Usage: copy <text>")
                sys.exit(1)

            text = " ".join(sys.argv[2:])
            FileUtility.copy_to_clipboard(text)

        else:
            print(f"{Colors.FAIL}❌ Unknown command: {command}{Colors.ENDC}")

    except Exception as e:
        print(f"{Colors.FAIL}⚠️  Error: {e}{Colors.ENDC}")

