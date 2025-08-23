from PIL import Image, ImageFilter, ImageEnhance
import os
import sys

class ImageProcessor:
    def __init__(self):
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp']
    
    def resize_image(self, input_path, output_path, size, keep_aspect=True):
        try:
            with Image.open(input_path) as img:
                if keep_aspect:
                    img.thumbnail(size, Image.Resampling.LANCZOS)
                else:
                    img = img.resize(size, Image.Resampling.LANCZOS)
                
                img.save(output_path, optimize=True, quality=95)
                print(f"Resized {input_path} to {output_path}")
                return True
        except Exception as e:
            print(f"Error resizing image: {e}")
            return False
    
    def convert_format(self, input_path, output_path, format=None):
        try:
            with Image.open(input_path) as img:
                if img.mode == 'RGBA' and format and format.upper() in ['JPEG', 'JPG']:
                    img = img.convert('RGB')
                
                if format:
                    img.save(output_path, format=format.upper(), optimize=True, quality=95)
                else:
                    img.save(output_path, optimize=True, quality=95)
                
                print(f"Converted {input_path} to {output_path}")
                return True
        except Exception as e:
            print(f"Error converting image: {e}")
            return False
    
    def crop_image(self, input_path, output_path, box):
        try:
            with Image.open(input_path) as img:
                cropped = img.crop(box)
                cropped.save(output_path, optimize=True, quality=95)
                print(f"Cropped {input_path} to {output_path}")
                return True
        except Exception as e:
            print(f"Error cropping image: {e}")
            return False
    
    def rotate_image(self, input_path, output_path, angle):
        try:
            with Image.open(input_path) as img:
                rotated = img.rotate(angle, expand=True)
                rotated.save(output_path, optimize=True, quality=95)
                print(f"Rotated {input_path} by {angle} degrees")
                return True
        except Exception as e:
            print(f"Error rotating image: {e}")
            return False
    
    def apply_filter(self, input_path, output_path, filter_type):
        try:
            with Image.open(input_path) as img:
                if filter_type == 'blur':
                    filtered = img.filter(ImageFilter.BLUR)
                elif filter_type == 'sharpen':
                    filtered = img.filter(ImageFilter.SHARPEN)
                elif filter_type == 'edge_enhance':
                    filtered = img.filter(ImageFilter.EDGE_ENHANCE)
                elif filter_type == 'emboss':
                    filtered = img.filter(ImageFilter.EMBOSS)
                elif filter_type == 'contour':
                    filtered = img.filter(ImageFilter.CONTOUR)
                else:
                    print(f"Unknown filter: {filter_type}")
                    return False
                
                filtered.save(output_path, optimize=True, quality=95)
                print(f"Applied {filter_type} filter to {input_path}")
                return True
        except Exception as e:
            print(f"Error applying filter: {e}")
            return False
    
    def adjust_brightness(self, input_path, output_path, factor):
        try:
            with Image.open(input_path) as img:
                enhancer = ImageEnhance.Brightness(img)
                enhanced = enhancer.enhance(factor)
                enhanced.save(output_path, optimize=True, quality=95)
                print(f"Adjusted brightness of {input_path} by factor {factor}")
                return True
        except Exception as e:
            print(f"Error adjusting brightness: {e}")
            return False
    
    def adjust_contrast(self, input_path, output_path, factor):
        try:
            with Image.open(input_path) as img:
                enhancer = ImageEnhance.Contrast(img)
                enhanced = enhancer.enhance(factor)
                enhanced.save(output_path, optimize=True, quality=95)
                print(f"Adjusted contrast of {input_path} by factor {factor}")
                return True
        except Exception as e:
            print(f"Error adjusting contrast: {e}")
            return False
    
    def create_thumbnail(self, input_path, output_path, size=(128, 128)):
        try:
            with Image.open(input_path) as img:
                img.thumbnail(size, Image.Resampling.LANCZOS)
                base_name = os.path.splitext(output_path)[0]
                thumb_path = f"{base_name}_thumb.jpg"
                img.save(thumb_path, 'JPEG', optimize=True, quality=90)
                print(f"Created thumbnail: {thumb_path}")
                return True
        except Exception as e:
            print(f"Error creating thumbnail: {e}")
            return False
    
    def get_image_info(self, input_path):
        try:
            with Image.open(input_path) as img:
                info = {
                    'filename': os.path.basename(input_path),
                    'format': img.format,
                    'mode': img.mode,
                    'size': img.size,
                    'width': img.width,
                    'height': img.height,
                    'has_transparency': img.mode in ('RGBA', 'LA') or 'transparency' in img.info
                }
                
                if hasattr(img, '_getexif') and img._getexif():
                    info['has_exif'] = True
                else:
                    info['has_exif'] = False
                
                return info
        except Exception as e:
            print(f"Error getting image info: {e}")
            return None
    
    def batch_resize(self, input_dir, output_dir, size, keep_aspect=True):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        processed = 0
        for filename in os.listdir(input_dir):
            if any(filename.lower().endswith(ext) for ext in self.supported_formats):
                input_path = os.path.join(input_dir, filename)
                output_path = os.path.join(output_dir, filename)
                
                if self.resize_image(input_path, output_path, size, keep_aspect):
                    processed += 1
        
        print(f"Batch resize completed: {processed} images processed")
        return processed
    
    def batch_convert(self, input_dir, output_dir, output_format):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        processed = 0
        for filename in os.listdir(input_dir):
            if any(filename.lower().endswith(ext) for ext in self.supported_formats):
                input_path = os.path.join(input_dir, filename)
                base_name = os.path.splitext(filename)[0]
                output_filename = f"{base_name}.{output_format.lower()}"
                output_path = os.path.join(output_dir, output_filename)
                
                if self.convert_format(input_path, output_path, output_format):
                    processed += 1
        
        print(f"Batch conversion completed: {processed} images processed")
        return processed

def create_test_image():
    img = Image.new('RGB', (800, 600), color='lightblue')
    img.save('test_image.png')
    print("Test image created: test_image.png")

if __name__ == "__main__":
    processor = ImageProcessor()
    
    if len(sys.argv) < 2:
        print("Usage: python image_processor.py <command> [args]")
        print("Commands:")
        print("  resize <input> <output> <width> <height>")
        print("  convert <input> <output> <format>")
        print("  crop <input> <output> <x1> <y1> <x2> <y2>")
        print("  rotate <input> <output> <angle>")
        print("  filter <input> <output> <filter_type>")
        print("  brightness <input> <output> <factor>")
        print("  contrast <input> <output> <factor>")
        print("  thumbnail <input> <output>")
        print("  info <input>")
        print("  batch_resize <input_dir> <output_dir> <width> <height>")
        print("  batch_convert <input_dir> <output_dir> <format>")
        print("  create_test")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "resize":
        if len(sys.argv) < 6:
            print("Usage: resize <input> <output> <width> <height>")
            sys.exit(1)
        
        input_path = sys.argv[2]
        output_path = sys.argv[3]
        width = int(sys.argv[4])
        height = int(sys.argv[5])
        
        processor.resize_image(input_path, output_path, (width, height))
    
    elif command == "convert":
        if len(sys.argv) < 5:
            print("Usage: convert <input> <output> <format>")
            sys.exit(1)
        
        processor.convert_format(sys.argv[2], sys.argv[3], sys.argv[4])
    
    elif command == "crop":
        if len(sys.argv) < 8:
            print("Usage: crop <input> <output> <x1> <y1> <x2> <y2>")
            sys.exit(1)
        
        input_path = sys.argv[2]
        output_path = sys.argv[3]
        box = (int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]))
        
        processor.crop_image(input_path, output_path, box)
    
    elif command == "rotate":
        if len(sys.argv) < 5:
            print("Usage: rotate <input> <output> <angle>")
            sys.exit(1)
        
        processor.rotate_image(sys.argv[2], sys.argv[3], float(sys.argv[4]))
    
    elif command == "filter":
        if len(sys.argv) < 5:
            print("Usage: filter <input> <output> <filter_type>")
            print("Filters: blur, sharpen, edge_enhance, emboss, contour")
            sys.exit(1)
        
        processor.apply_filter(sys.argv[2], sys.argv[3], sys.argv[4])
    
    elif command == "brightness":
        if len(sys.argv) < 5:
            print("Usage: brightness <input> <output> <factor>")
            sys.exit(1)
        
        processor.adjust_brightness(sys.argv[2], sys.argv[3], float(sys.argv[4]))
    
    elif command == "contrast":
        if len(sys.argv) < 5:
            print("Usage: contrast <input> <output> <factor>")
            sys.exit(1)
        
        processor.adjust_contrast(sys.argv[2], sys.argv[3], float(sys.argv[4]))
    
    elif command == "thumbnail":
        if len(sys.argv) < 4:
            print("Usage: thumbnail <input> <output>")
            sys.exit(1)
        
        processor.create_thumbnail(sys.argv[2], sys.argv[3])
    
    elif command == "info":
        if len(sys.argv) < 3:
            print("Usage: info <input>")
            sys.exit(1)
        
        info = processor.get_image_info(sys.argv[2])
        if info:
            print(f"\nImage Information:")
            print(f"Filename: {info['filename']}")
            print(f"Format: {info['format']}")
            print(f"Mode: {info['mode']}")
            print(f"Size: {info['width']} x {info['height']} pixels")
            print(f"Has transparency: {info['has_transparency']}")
            print(f"Has EXIF data: {info['has_exif']}")
    
    elif command == "batch_resize":
        if len(sys.argv) < 6:
            print("Usage: batch_resize <input_dir> <output_dir> <width> <height>")
            sys.exit(1)
        
        input_dir = sys.argv[2]
        output_dir = sys.argv[3]
        width = int(sys.argv[4])
        height = int(sys.argv[5])
        
        processor.batch_resize(input_dir, output_dir, (width, height))
    
    elif command == "batch_convert":
        if len(sys.argv) < 5:
            print("Usage: batch_convert <input_dir> <output_dir> <format>")
            sys.exit(1)
        
        processor.batch_convert(sys.argv[2], sys.argv[3], sys.argv[4])
    
    elif command == "create_test":
        create_test_image()
    
    else:
        print("Unknown command")
