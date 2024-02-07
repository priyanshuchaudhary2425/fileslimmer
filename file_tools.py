import PyPDF2

def lock_pdf(input_pdf_path, output_pdf_path, password):
    try:
        with open(input_pdf_path, 'rb') as input_file, open(output_pdf_path, 'wb') as output_file:
            pdf_reader = PyPDF2.PdfReader(input_file)
            pdf_writer = PyPDF2.PdfWriter()
            for page_num in range(len(pdf_reader.pages)):
                pdf_writer.add_page(pdf_reader.pages[page_num])
            pdf_writer.encrypt(password)
            pdf_writer.write(output_file)
        print(f"PDF locked successfully and saved as {output_pdf_path}")
    except Exception as e:
        print(f"Error: {e}")


import PyPDF2

def unlock_pdf(input_pdf_path, output_pdf_path, password):
    try:
        with open(input_pdf_path, 'rb') as input_file, open(output_pdf_path, 'wb') as output_file:
            pdf_reader = PyPDF2.PdfReader(input_file)
            if pdf_reader.is_encrypted:
                pdf_reader.decrypt(password)
            pdf_writer = PyPDF2.PdfWriter()
            for page_num in range(len(pdf_reader.pages)):
                pdf_writer.add_page(pdf_reader.pages[page_num])
            pdf_writer.write(output_file)
        print(f"PDF unlocked successfully and saved as {output_pdf_path}")
    except Exception as e:
        print(f"Error: {e}")




