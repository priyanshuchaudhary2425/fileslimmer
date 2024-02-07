import os
import fitz  # PyMuPDF
from PIL import Image


def convert_pdf_to_jpeg(pdf_path):
    """
    Converts a PDF file to JPEG images and deletes them after 5 minutes.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        list: A list of image file paths.
    """
    output_dir = os.path.splitext(pdf_path)[0] + '_images'
    os.makedirs(output_dir, exist_ok=True)

    pdf_document = fitz.open(pdf_path)
    image_paths = []
    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        image = page.get_pixmap()
        image_path = os.path.join(output_dir, f"page_{page_number + 1}.jpg")
        image_pil = Image.frombytes("RGB", [image.width, image.height], image.samples)
        image_pil.save(image_path, format='JPEG', quality=95)
        image_paths.append(image_path)

    pdf_document.close()

    return image_paths


def convert_pdf_to_png(pdf_path):
    """
    Converts a PDF file to PNG images and deletes them after 5 minutes.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        list: A list of image file paths.
    """
    output_dir = os.path.splitext(pdf_path)[0] + '_images'
    os.makedirs(output_dir, exist_ok=True)

    pdf_document = fitz.open(pdf_path)
    image_paths = []
    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        image = page.get_pixmap(alpha=False)  # Disable alpha channel for PNG
        image_path = os.path.join(output_dir, f"page_{page_number + 1}.png")

        # Convert Pixmap to PIL image
        image_pil = Image.frombytes("RGB", [image.width, image.height], image.samples)

        # Save PIL image as PNG
        image_pil.save(image_path, format='PNG')
        image_paths.append(image_path)

    pdf_document.close()

    return image_paths



def jpeg_to_png(input_path, output_path):
    """
    Converts JPEG image to PNG format.

    Parameters:
        input_path (str): Path to the input JPEG image.
        output_path (str): Path to save the output PNG image.
    """
    try:
        with Image.open(input_path) as img:
            img.save(output_path, "PNG")
        print(f"JPEG to PNG conversion successful. Image saved at {output_path}")
    except Exception as e:
        print(f"Error converting JPEG to PNG: {e}")

def png_to_jpeg(input_path, output_path):
    """
    Converts PNG image to JPEG format.

    Parameters:
        input_path (str): Path to the input PNG image.
        output_path (str): Path to save the output JPEG image.
    """
    try:
        with Image.open(input_path) as img:
            img.convert("RGB").save(output_path, "JPEG")
        print(f"PNG to JPEG conversion successful. Image saved at {output_path}")
    except Exception as e:
        print(f"Error converting PNG to JPEG: {e}")
