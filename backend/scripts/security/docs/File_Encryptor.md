# File Encryptor - README

## Overview
The File Encryptor is a secure, robust Python utility designed to encrypt and decrypt files using the Fernet symmetric encryption algorithm. This tool helps protect sensitive files from unauthorized access by encrypting them with a strong key.

## Features
- **Strong encryption**: Uses Fernet symmetric encryption (AES-128 in CBC mode with PKCS7 padding)
- **Multiple file support**: Encrypts/decrypts multiple files and folders in one operation
- **File type filtering**: Supports common document, image, and video formats
- **Backup protection**: Creates temporary backups during operations to prevent data loss
- **Detailed logging**: Maintains operation logs for auditing and troubleshooting
- **Error handling**: Comprehensive error handling and reporting

## Supported File Types
- Documents: `.pdf`, `.txt`, `.doc`, `.docx`, `.ppt`, `.pptx`, `.xls`, `.xlsx`
- Images: `.jpg`, `.jpeg`, `.png`, `.gif`
- Videos: `.mp4`, `.avi`, `.mov`, `.mkv`
- Archives: `.zip`, `.rar`, `.7z`

## Usage

### Command Line
```bash
# Encrypt files and/or folders
python file_encryptor.py encrypt document.pdf images/ downloads/

# Decrypt files using specific key
python file_encryptor.py decrypt document.pdf --key /path/to/key.key

# View help
python file_encryptor.py --help
```

### As a Library
```python
from scripts.security.file_encryptor import encrypt_files, decrypt_files

# Encrypt files
results = encrypt_files(["document.pdf", "images/"])

# Decrypt files with specific key
key = load_key("my_key.key")
results = decrypt_files(["document.pdf"], key=key)
```

## Key Management
- When encrypting files for the first time, a new key is generated and saved as `key.key`
- **IMPORTANT**: Keep your key file safe! Without it, encrypted files cannot be recovered
- For decryption, you must provide the same key used for encryption

## Security Notes
1. The encryption key is stored locally - protect it appropriately
2. Files larger than 100MB are skipped to prevent memory issues
3. The script creates temporary backups during operations to prevent data loss

## Integration with PyEveryday
This script is part of the PyEveryday automation toolkit and can be accessed through:
1. Command line interface
2. PyEveryday web interface under the Security category
3. As an importable module in other Python scripts

---

**Remember:** Always keep your encryption key safe. Without it, your encrypted files cannot be recovered.