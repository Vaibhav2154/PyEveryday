import qrcode as qr
import os
import sys
import cv2
from PIL import Image


class QR_Toolkit():
    def __init__(self):
        pass

    def generate_qr(self, url, filename="QR_code.png"):
        try:
            img = qr.make(f"{url}")
            img.save(filename)
        except Exception as e:
            print(f"Error generating QR code: {e}")

    def scan_qr(self, img_path):
        try:
            if not os.path.exists(img_path):
                print(f"File does not exist: {img_path}")
                return
            
            img = cv2.imread(img_path)

            if img is None:
                print(f"Could not read image: {img_path}")
                return

            detector = cv2.QRCodeDetector()
            data, points, _ = detector.detectAndDecode(img)

            if points is not None and data:
                print(f"Decoded QR Data: {data}")
                return data
            else:
                print("No QR code found in the image.")
                return

        except Exception as e:
            print(f"Failed to scan QR code: {e}")

def print_usage():
    print("Usage: python qr_toolkit.py <command> [args]")
    print("Commands:")
    print("  generate <text_or_url> [filename]       - Generate a QR code")
    print("  scan <image_path>                       - Scan a QR code from image")
    print("  help                                    - Show this help message")

if __name__ == "__main__":
    qr_tool = QR_Toolkit()

    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "generate":
        if len(sys.argv) < 3:
            print("Usage: generate <text_or_url> [filename]")
            sys.exit(1)
        
        data = sys.argv[2]
        filename = sys.argv[3] if len(sys.argv) >= 4 else "QR_code.png"
        qr_tool.generate_qr(data, filename)

    elif command == "scan":
        if len(sys.argv) < 3:
            print("Usage: scan <image_path>")
            sys.exit(1)

        image_path = sys.argv[2]
        qr_tool.scan_qr(image_path)

    elif command == "help":
        print_usage()

    else:
        print(f"Unknown command: '{command}'")
        print_usage()

