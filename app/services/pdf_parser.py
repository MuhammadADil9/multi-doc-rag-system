from PyPDF2 import PdfReader
from typing import Optional
import os
from pathlib import Path



class PdfParsingError(Exception):
    pass


class PDFParser:

    """Extract text from PDF file."""

    @staticmethod
    def extract_text(pdf_path: str) -> str:
        """ Extract all text from PDF file.

        Args:
            path to pdf file 
        
        Returns:
             extracted text from pdf file
        """
        
        if not os.path.exists(pdf_path):
            raise PdfParsingError(f"file {pdf_path} does not exist")

        file = PdfReader(pdf_path)
        pages = file.pages
        print(len(pages))
        data = ""

        try:
            for page in pages:
                data += page.extract_text()
        except PdfParsingError as e:
            print(f"PdfParsingError :- {e} ")
            raise e("Corrupted file") 
        finally:
            print("\nCompleted processing of file")


    @staticmethod
    def validate_file(pdf_file:str, max_size:int) -> list[bool, Optional[str]]:
        """ Validate the PDF file.

        Args:
            pdf_file: path to pdf file
            max_size: maximum size of pdf file
        
        Returns:
            list of boolean and optional string
        """
        
        if not os.path.exists(pdf_path):
            raise PdfParsingError(f"file {pdf_path} does not exist")

        file_path = Path(pdf_file)
        file_name = file_name


# where does that path of pdf came from ? like will we store pdf file in here within project, like the point where how os.path will figure out if file exist or not

# pdfreader > object of file
# we got list of pagess through pages property of object 
# then we looped over it to get the data

# while reading the file how we would capture if file was corrupted or not ?