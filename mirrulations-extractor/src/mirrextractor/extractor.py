from datetime import datetime
import os
import time
import io
import pdfminer
import pdfminer.high_level
import pikepdf
from mirrcore.path_generator import PathGenerator


class Extractor:
    """
    Class containing methods to extract text from files.
    """
    @staticmethod
    def extract_text(attachment_path, save_path):
        """
        This method takes a complete path to an attachment and determines
        which type of extraction will take place.
        *Note* save_path is for later use when saving the extracted text
        Parameters
        ----------
        attachment_path : str
            the complete file path for the attachment that is being extracted
            ex. /path/to/pdf/attachment_1.pdf
        save_path : str
            the complete path to store the extract text
            ex. /path/to/text/attachment_1.txt
        """
        # gets the type of the attachment file
        #   (ex. /path/to/pdf/attachment_1.pdf -> pdf)
        file_type = attachment_path[attachment_path.rfind('.')+1:]
        if file_type.endswith('pdf'):
            print(f"Extracting text from {attachment_path}")
            Extractor._extract_pdf(attachment_path, save_path)
        else:
            print(f"FAILURE: attachment doesn't have appropriate extension \
            {attachment_path}")

    @staticmethod
    def make_save_path(path):
        """
        This method takes a complete path to a pdf and makes
        the save path based on paramters in that path.
        Parameters
        ----------
        path : str
            the complete file path for the attachment that is being extracted
            ex. /path/to/pdf/attachment_1.pdf
        """
        return path.replace('binary', 'text') \
            .replace('comments_attachments',
                     'comments_extracted_text/pdfminer') \
            .replace('.pdf', '_extracted.txt')

    @staticmethod
    def _extract_pdf(attachment_path, save_path):
        """
        This method takes a complete path to a pdf and stores
        the extracted text in the save_path.
        *Note* If a file exists at save_path, it will be overwritten.
        Parameters
        ----------
        attachment_path : str
            the complete file path for the attachment that is being extracted
            ex. /path/to/pdf/attachment_1.pdf
        save_path : str
            the complete path to store the extract text
            ex. /path/to/text/attachment_1.txt
        """
        try:
            pdf = pikepdf.open(attachment_path)
        except pikepdf.PdfError:
            try:
                pdf = pikepdf.open(attachment_path, recover=True)
            except pikepdf.PdfError:
                print(f"FAILURE: failed to open {attachment_path}")
                return
        pdf_bytes = io.BytesIO()
        pdf.save(pdf_bytes, linearize=True)
        text = pdfminer.high_level.extract_text(pdf_bytes)
        # Save the extracted text to a file
        with open(save_path, "w", encoding="utf-8") as out_file:
            out_file.write(text)
        print(f"SUCCESS: Saved pdf at {save_path}")


if __name__ == '__main__':
    now = datetime.now()
    while True:
        for (root, dirs, files) in os.walk('/data'):
            for file in files:
                # Checks for pdfs
                if not file.endswith('pdf'):
                    continue
                complete_path = os.path.join(root, file)
                output_path = "/data/data/" + \
                    PathGenerator.make_attachment_save_path(complete_path)
                if not output_path.is_file():
                    start_time = time.time()
                    Extractor.extract_text(complete_path, output_path)
                    print(f"Time taken to extract text from {complete_path}"
                          f" is {start_time - time.time()} seconds")
        # sleep for a hour
        current_time = now.strftime("%H:%M:%S")
        print(f"Sleeping for an hour : started at {current_time}")
        time.sleep(3600)