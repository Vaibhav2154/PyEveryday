import os
import sys
import logging
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from datetime import datetime
from typing import List, Tuple, Dict, Union, Any, Optional
import argparse
import getpass

# Allowed file extensions - you can customize this
ALLOWED_EXTENSIONS = {".pdf", ".ppt", ".pptx", ".jpg", ".jpeg", ".png", ".gif", 
                      ".mp4", ".avi", ".mov", ".mkv", ".txt", ".doc", ".docx",
                      ".xls", ".xlsx", ".zip", ".rar", ".7z"}

# Maximum file size to prevent memory issues (100MB)
MAX_FILE_SIZE = 100 * 1024 * 1024

# Configure logging
def setup_logging():
    """Setup logging configuration"""
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(
        filename='encryption_log.txt',
        level=logging.INFO,
        format=log_format,
        encoding='utf-8'
    )
    
    # Also add console handler for important messages
    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)

class FileEncryptionError(Exception):
    """Custom exception for file encryption errors"""
    pass

class KeyManagementError(Exception):
    """Custom exception for key management errors"""
    pass

def log_operation_start(operation: str):
    """Log the start of an encryption/decryption operation"""
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"{'='*20} {operation.upper()} OPERATION STARTED at {start_time} {'='*20}")

def log_operation_end(operation: str, status: str = "COMPLETED"):
    """Log the end of an encryption/decryption operation"""
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"{'='*20} {operation.upper()} OPERATION {status} at {end_time} {'='*20}")

def generate_key_from_password(password: str, salt: bytes = None) -> Tuple[bytes, bytes]:
    """Generate a key from a password using PBKDF2"""
    try:
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt
    except Exception as e:
        raise KeyManagementError(f"Failed to generate key from password: {str(e)}")

def generate_key(key_path: str = "key.key") -> bytes:
    """Generate a new encryption key if one doesn't exist"""
    try:
        if os.path.exists(key_path):
            logging.warning(f"Key file already exists at {key_path}. Using existing key.")
            return load_key(key_path)
        
        key = Fernet.generate_key()
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(key_path) if os.path.dirname(key_path) else '.', exist_ok=True)
        
        with open(key_path, "wb") as f:
            f.write(key)
        
        logging.info(f"Generated new encryption key at {key_path}")
        print(f"✓ New encryption key generated and saved to: {key_path}")
        print("⚠️  IMPORTANT: Keep this key file safe! Without it, you cannot decrypt your files.")
        return key
        
    except PermissionError:
        error_msg = f"Permission denied: Cannot write key file at {key_path}"
        logging.error(error_msg)
        raise KeyManagementError(error_msg)
    except Exception as e:
        error_msg = f"Failed to generate encryption key: {str(e)}"
        logging.error(error_msg)
        raise KeyManagementError(error_msg)

def load_key(key_path: str = "key.key") -> bytes:
    """Load the encryption key from file with enhanced error handling"""
    try:
        if not os.path.exists(key_path):
            error_msg = f"Encryption key not found at {key_path}"
            logging.error(error_msg)
            raise KeyManagementError(error_msg)
        
        with open(key_path, "rb") as f:
            key = f.read()
        
        # Validate key format
        try:
            Fernet(key)
        except ValueError:
            error_msg = f"Invalid key format in {key_path}"
            logging.error(error_msg)
            raise KeyManagementError(error_msg)
        
        logging.info(f"Loaded encryption key from {key_path}")
        return key
        
    except PermissionError:
        error_msg = f"Permission denied: Cannot read key file at {key_path}"
        logging.error(error_msg)
        raise KeyManagementError(error_msg)
    except Exception as e:
        error_msg = f"Failed to load encryption key: {str(e)}"
        logging.error(error_msg)
        raise KeyManagementError(error_msg)

def collect_supported_files(paths: List[str]) -> Tuple[List[str], List[str], List[str]]:
    """Collect files with supported extensions from given paths"""
    supported, unsupported, errors = [], [], []
    
    for path in paths:
        try:
            if not os.path.exists(path):
                errors.append(f"Path does not exist: {path}")
                continue
                
            if os.path.isdir(path):
                for root_dir, _, files in os.walk(path):
                    for file in files:
                        try:
                            fpath = os.path.join(root_dir, file)
                            file_ext = os.path.splitext(file)[1].lower()
                            
                            if file_ext in ALLOWED_EXTENSIONS:
                                supported.append(fpath)
                            else:
                                unsupported.append(fpath)
                        except Exception as e:
                            errors.append(f"Error processing file {file}: {str(e)}")
                            
            elif os.path.isfile(path):
                file_ext = os.path.splitext(path)[1].lower()
                if file_ext in ALLOWED_EXTENSIONS:
                    supported.append(path)
                else:
                    unsupported.append(path)
            else:
                errors.append(f"Path is not a file or directory: {path}")
                
        except Exception as e:
            errors.append(f"Error processing path {path}: {str(e)}")
    
    return supported, unsupported, errors

def check_file_size(file_path: str) -> bool:
    """Check if file size is within limits"""
    try:
        file_size = os.path.getsize(file_path)
        return file_size <= MAX_FILE_SIZE
    except OSError as e:
        logging.warning(f"Cannot check size of {file_path}: {str(e)}")
        return False

def encrypt_file(file_path: str, key: bytes) -> Dict[str, Any]:
    """Encrypt a single file and return status with enhanced error handling"""
    result = {
        "file": os.path.basename(file_path),
        "full_path": file_path,
        "status": "success", 
        "message": "File encrypted successfully"
    }
    
    try:
        # Check file accessibility
        if not os.access(file_path, os.R_OK | os.W_OK):
            result["status"] = "error"
            result["message"] = "Insufficient file permissions (need read/write access)"
            return result
        
        # Check file size
        if not check_file_size(file_path):
            result["status"] = "error"
            result["message"] = f"File too large (max {MAX_FILE_SIZE // (1024*1024)}MB)"
            return result
        
        fernet = Fernet(key)
        
        with open(file_path, "rb") as f:
            content = f.read()
            
            # Check if file is empty
            if len(content) == 0:
                result["status"] = "skipped"
                result["message"] = "File is empty"
                return result
            
            try:
                # Check if already encrypted
                fernet.decrypt(content)
                result["status"] = "skipped"
                result["message"] = "File already encrypted"
                return result
            except InvalidToken:
                # File is not encrypted, proceed with encryption
                pass
        
        # Create backup (optional - you might want to make this configurable)
        backup_path = file_path + ".backup"
        try:
            import shutil
            shutil.copy2(file_path, backup_path)
        except Exception as e:
            logging.warning(f"Could not create backup for {file_path}: {str(e)}")
        
        # Encrypt and write file
        try:
            encrypted = fernet.encrypt(content)
            with open(file_path, "wb") as f:
                f.write(encrypted)
            
            logging.info(f"Encrypted: {file_path}")
            return result
            
        except Exception as e:
            # Restore from backup if encryption fails
            if os.path.exists(backup_path):
                try:
                    shutil.move(backup_path, file_path)
                except Exception as restore_error:
                    logging.error(f"Failed to restore backup for {file_path}: {str(restore_error)}")
            
            result["status"] = "error"
            result["message"] = f"Encryption failed: {str(e)}"
            return result
        finally:
            # Clean up backup file if it exists
            if os.path.exists(backup_path):
                try:
                    os.remove(backup_path)
                except Exception:
                    pass
                    
    except Exception as e:
        result["status"] = "error"
        result["message"] = f"Unexpected error: {str(e)}"
        logging.error(f"Error encrypting {file_path}: {e}")
        return result

def decrypt_file(file_path: str, key: bytes) -> Dict[str, Any]:
    """Decrypt a single file and return status with enhanced error handling"""
    result = {
        "file": os.path.basename(file_path),
        "full_path": file_path,
        "status": "success", 
        "message": "File decrypted successfully"
    }
    
    try:
        # Check file accessibility
        if not os.access(file_path, os.R_OK | os.W_OK):
            result["status"] = "error"
            result["message"] = "Insufficient file permissions (need read/write access)"
            return result
        
        fernet = Fernet(key)
        
        with open(file_path, "rb") as f:
            content = f.read()
            
            # Check if file is empty
            if len(content) == 0:
                result["status"] = "error"
                result["message"] = "File is empty"
                return result
            
            try:
                # Try to decrypt
                decrypted = fernet.decrypt(content)
            except InvalidToken:
                result["status"] = "error"
                result["message"] = "File is not encrypted or uses a different key"
                return result
                
        # Create backup
        backup_path = file_path + ".backup"
        try:
            import shutil
            shutil.copy2(file_path, backup_path)
        except Exception as e:
            logging.warning(f"Could not create backup for {file_path}: {str(e)}")
        
        # Write decrypted content
        try:
            with open(file_path, "wb") as f:
                f.write(decrypted)
            
            logging.info(f"Decrypted: {file_path}")
            return result
            
        except Exception as e:
            # Restore from backup if decryption fails
            if os.path.exists(backup_path):
                try:
                    shutil.move(backup_path, file_path)
                except Exception as restore_error:
                    logging.error(f"Failed to restore backup for {file_path}: {str(restore_error)}")
            
            result["status"] = "error"
            result["message"] = f"Decryption failed: {str(e)}"
            return result
        finally:
            # Clean up backup file
            if os.path.exists(backup_path):
                try:
                    os.remove(backup_path)
                except Exception:
                    pass
                    
    except Exception as e:
        result["status"] = "error"
        result["message"] = f"Unexpected error: {str(e)}"
        logging.error(f"Error decrypting {file_path}: {e}")
        return result

def encrypt_files(file_paths: List[str], key: bytes = None, key_path: str = "key.key") -> Dict[str, Any]:
    """Encrypt multiple files and return results with enhanced error handling"""
    log_operation_start("Encryption")
    
    try:
        if key is None:
            key = generate_key(key_path)
        
        supported, unsupported, path_errors = collect_supported_files(file_paths)
        
        results = {
            "status": "success",
            "supported_count": len(supported),
            "unsupported_count": len(unsupported),
            "path_errors": path_errors,
            "unsupported_files": [os.path.basename(f) for f in unsupported[:10]],  # Limit output
            "results": []
        }
        
        if not supported and not path_errors:
            results["status"] = "warning"
            results["message"] = "No supported files found to encrypt"
            log_operation_end("Encryption", "COMPLETED WITH WARNINGS")
            return results
        
        if path_errors:
            results["status"] = "warning"
            results["message"] = "Operation completed with some path errors"
        
        # Process files
        for file_path in supported:
            result = encrypt_file(file_path, key)
            results["results"].append(result)
        
        # Count results
        successful = len([r for r in results["results"] if r["status"] == "success"])
        skipped = len([r for r in results["results"] if r["status"] == "skipped"])
        errors = len([r for r in results["results"] if r["status"] == "error"])
        
        results["successful"] = successful
        results["skipped"] = skipped
        results["errors"] = errors
        
        operation_status = "COMPLETED"
        if errors > 0 or path_errors:
            operation_status = "COMPLETED WITH ERRORS"
        elif skipped > 0:
            operation_status = "COMPLETED WITH WARNINGS"
            
        log_operation_end("Encryption", operation_status)
        return results
        
    except Exception as e:
        error_msg = f"Encryption operation failed: {str(e)}"
        logging.error(error_msg)
        log_operation_end("Encryption", "FAILED")
        return {
            "status": "error",
            "message": error_msg,
            "supported_count": 0,
            "unsupported_count": 0,
            "results": []
        }

def decrypt_files(file_paths: List[str], key: bytes = None, key_path: str = "key.key") -> Dict[str, Any]:
    """Decrypt multiple files and return results with enhanced error handling"""
    log_operation_start("Decryption")
    
    try:
        if key is None:
            key = load_key(key_path)
        
        supported, _, path_errors = collect_supported_files(file_paths)
        
        results = {
            "status": "success",
            "supported_count": len(supported),
            "path_errors": path_errors,
            "results": []
        }
        
        if not supported and not path_errors:
            results["status"] = "warning"
            results["message"] = "No supported files found to decrypt"
            log_operation_end("Decryption", "COMPLETED WITH WARNINGS")
            return results
        
        if path_errors:
            results["status"] = "warning"
            results["message"] = "Operation completed with some path errors"
        
        # Process files
        for file_path in supported:
            result = decrypt_file(file_path, key)
            results["results"].append(result)
        
        # Count results
        successful = len([r for r in results["results"] if r["status"] == "success"])
        errors = len([r for r in results["results"] if r["status"] == "error"])
        
        results["successful"] = successful
        results["errors"] = errors
        
        operation_status = "COMPLETED"
        if errors > 0 or path_errors:
            operation_status = "COMPLETED WITH ERRORS"
            
        log_operation_end("Decryption", operation_status)
        return results
        
    except Exception as e:
        error_msg = f"Decryption operation failed: {str(e)}"
        logging.error(error_msg)
        log_operation_end("Decryption", "FAILED")
        return {
            "status": "error",
            "message": error_msg,
            "supported_count": 0,
            "results": []
        }

def display_results(results: Dict[str, Any], operation: str):
    """Display results in a user-friendly format"""
    print(f"\n{'='*50}")
    print(f"{operation.upper()} RESULTS")
    print(f"{'='*50}")
    
    if results["status"] == "error":
        print(f"❌ Operation failed: {results['message']}")
        return
    
    if "supported_count" in results:
        print(f"📁 Supported files found: {results['supported_count']}")
    
    if "unsupported_count" in results and results["unsupported_count"] > 0:
        print(f"⚡ Unsupported files skipped: {results['unsupported_count']}")
        if results["unsupported_files"]:
            print("   Sample unsupported files:")
            for file in results["unsupported_files"][:5]:
                print(f"     - {file}")
            if len(results["unsupported_files"]) > 5:
                print(f"     ... and {len(results['unsupported_files']) - 5} more")
    
    if "path_errors" in results and results["path_errors"]:
        print(f"⚠️  Path errors encountered: {len(results['path_errors'])}")
        for error in results["path_errors"][:3]:
            print(f"   - {error}")
        if len(results["path_errors"]) > 3:
            print(f"   ... and {len(results['path_errors']) - 3} more")
    
    if "successful" in results:
        print(f"✅ Successful: {results['successful']}")
    
    if "skipped" in results and results["skipped"] > 0:
        print(f"🔶 Skipped: {results['skipped']}")
    
    if "errors" in results and results["errors"] > 0:
        print(f"❌ Errors: {results['errors']}")
        
        # Show some error details
        error_files = [r for r in results["results"] if r["status"] == "error"]
        print("\nError details (first 3):")
        for error in error_files[:3]:
            print(f"   - {error['file']}: {error['message']}")
    
    if results.get("message"):
        print(f"\n💡 Note: {results['message']}")
    
    print(f"{'='*50}\n")

def main():
    """Main function with enhanced CLI interface"""
    setup_logging()
    
    parser = argparse.ArgumentParser(
        description="File Encryptor/Decryptor - PyEveryday (Enhanced)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s encrypt document.pdf images/ downloads/
  %(prog)s decrypt document.pdf --key /secure/path/key.key
  %(prog)s encrypt . --key my_key.key
        """
    )
    
    parser.add_argument("action", choices=["encrypt", "decrypt"], 
                       help="Action to perform: encrypt or decrypt files")
    parser.add_argument("paths", nargs="+", 
                       help="Files or folders to process")
    parser.add_argument("--key", default="key.key",
                       help="Path to key file (default: key.key)")
    parser.add_argument("--password", action="store_true",
                       help="Use password-based encryption (experimental)")
    
    args = parser.parse_args()
    
    try:
        if args.action == "encrypt":
            print("🔒 Starting encryption process...")
            results = encrypt_files(args.paths, key_path=args.key)
        else:
            print("🔓 Starting decryption process...")
            results = decrypt_files(args.paths, key_path=args.key)
        
        display_results(results, args.action)
        
        # Exit with appropriate code
        if results["status"] == "error" or results.get("errors", 0) > 0:
            sys.exit(1)
        else:
            sys.exit(0)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user.")
        logging.info("Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Critical error: {str(e)}")
        logging.critical(f"Critical error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()