from PIL import Image
import os

def convert_to_jpeg(input_path, output_path):
    original_image = Image.open(input_path)

    # Convert to RGB if not already in RGB mode
    if original_image.mode != 'RGB':
        original_image = original_image.convert('RGB')

    # Save the converted image as JPEG
    output_path_jpeg = output_path.replace('.png', '.jpg')
    original_image.save(output_path_jpeg, format='JPEG', quality=95)

    return output_path_jpeg

def reduce_image_size(input_path, output_path, target_size_kb):
    # Convert the image to JPEG before further processing
    input_path_jpeg = convert_to_jpeg(input_path, 'temp_image.jpg')

    original_image = Image.open(input_path_jpeg)

    # Get original size and calculate ratio
    original_width, original_height = original_image.size
    original_size = os.path.getsize(input_path_jpeg)
    ratio = original_width / original_height

    while original_size > target_size_kb * 1024:
        # Reduce image size while maintaining the aspect ratio
        reduced_width = original_width - 5  # Adjust the reduction amount as needed
        reduced_height = int(reduced_width / ratio)

        # Resize image using BICUBIC interpolation or other method
        resized_image = original_image.resize((reduced_width, reduced_height), Image.Resampling.BICUBIC)

        # Save the resized image in JPEG format with quality setting
        resized_image.save(output_path, format='JPEG', quality=70)

        # Print details for the current iteration
        # print(
        #     f"Iteration: Width={reduced_width}, Height={reduced_height}, Size={os.path.getsize(output_path) / 1024:.2f} KB")

        # Update variables for the next iteration
        original_image = resized_image
        original_width, original_height = resized_image.size
        original_size = os.path.getsize(output_path)

    # print(f"Final Image size: {os.path.getsize(output_path) / 1024:.2f} KB")

    return output_path
