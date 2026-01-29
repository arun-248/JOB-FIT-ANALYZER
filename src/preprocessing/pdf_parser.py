"""
PDF Parser - Extracts text from PDF and text files
"""

import fitz  # PyMuPDF
from pathlib import Path
from typing import Union


class PDFParser:
    """Handles PDF and text file parsing"""
    
    def __init__(self):
        self.supported_pdf = ['.pdf']
        self.supported_text = ['.txt']
    
    def parse(self, file_path: Union[str, Path]) -> str:
        """
        Parse file and extract text
        
        Args:
            file_path: Path to PDF or text file
            
        Returns:
            Extracted text
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        suffix = file_path.suffix.lower()
        
        if suffix in self.supported_pdf:
            return self._parse_pdf(file_path)
        elif suffix in self.supported_text:
            return self._parse_text(file_path)
        else:
            raise ValueError(f"Unsupported file format: {suffix}")
    
    def _parse_pdf(self, file_path: Path) -> str:
        """Extract text from PDF"""
        try:
            doc = fitz.open(file_path)
            text = ""
            
            for page in doc:
                text += page.get_text()
            
            doc.close()
            return text.strip()
        
        except Exception as e:
            raise Exception(f"Error parsing PDF: {str(e)}")
    
    def _parse_text(self, file_path: Path) -> str:
        """Read text file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            raise Exception(f"Error reading text file: {str(e)}")


# Test
if __name__ == "__main__":
    parser = PDFParser()
    test_file = Path(__file__).parent.parent.parent / "data" / "raw" / "sample_resume.txt"
    
    if test_file.exists():
        text = parser.parse(test_file)
        print(f"✓ Parsed {len(text)} characters")
        print(f"Preview: {text[:150]}...")
    else:
        print("⚠ Test file not found")