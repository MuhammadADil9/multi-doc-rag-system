from PyPDF2 import PdfReader
from typing import Optional, Tuple
from config import settings
from pathlib import Path
from logging import getLogger
import os
logger = getLogger(__name__)


# Exception class
class PdfParsingError(Exception):
    pass


# PDF parser and validator class
class PDFParser:

    """
    > Extract text from PDF file.
    > Validate the incoming file.
    """

    @staticmethod
    def extract_text(pdf_path: str) -> str:
        """
        Extract all text from a PDF file.
        """
        try:
            reader = PdfReader(pdf_path)
            pages = reader.pages
            logger.info(f"Number of pages: {len(pages)}")

            text = ""
            for index, page in enumerate(pages, start=1):

                if "/XObject" in page["/Resources"]:
                    raise PdfParsingError(f"PDF {pdf_path} contains images and cannot be parsed.")
                
                page_text = page.extract_text()

                if page_text: 
                    text += page_text

            if not text.strip():
                raise PdfParsingError(f"PDF contains no extractable text (may be image-only)")
            return text

        except Exception as e:
            raise PdfParsingError(f"Failed to extract text from {pdf_path}: {e}")

        finally:
            print(f"Completed processing of file: {pdf_path}")


    @staticmethod
    def validate_file(pdf_file: str, max_size: int) -> None:
        """
        Validate a PDF file.

        Checks:
        - File exists
        - File is a PDF
        - File is readable
        - File size is > 0 and within max_size limit
        """
        file_path = Path(pdf_file)

        
        if not file_path.exists():
            raise PdfParsingError(f"File {file_path} does not exist.")

        
        if file_path.suffix.lower() != ".pdf":
            raise PdfParsingError(f"Provided file {file_path.name} is not a PDF.")

        
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        if file_size_mb == 0:
            raise PdfParsingError(f"PDF {file_path.name} is empty or corrupted.")
        if file_size_mb > max_size:
            raise PdfParsingError(f"PDF size {file_size_mb:.2f}MB exceeds {max_size}MB limit.")

        
        
        PdfReader(file_path)
        raise PdfParsingError(f"PDF {file_path.name} cannot be read or is corrupted.")





# So far what we did ? 

# We followed single responsibility principle. 
# We created a file that will help us in parsing pdfs. 
# File contain two functions. 
# First function responsibility 
# > open a file
# > grab the text out of it
# > returns a string


# Second function responsibility 
# > validate file existance. 
# > make sure it is a pdf
# > make sure it is neither zero mb in size nor it is greater than defined limit 
# > make sure it is openable 
 
# Takeaways 
# > SRP
# > Flow planning 
# > use of try and exceptions