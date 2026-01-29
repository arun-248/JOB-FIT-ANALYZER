"""
Section Detector - Identifies sections in resume text
"""

import re
from typing import Dict
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.config import SECTION_PATTERNS


class SectionDetector:
    """Detects and extracts structured sections from resume text"""
    
    def __init__(self):
        self.section_patterns = SECTION_PATTERNS
    
    def detect_sections(self, text: str) -> Dict[str, str]:
        """
        Detect and extract sections from resume text
        
        Args:
            text: Full resume text
            
        Returns:
            Dictionary with section names as keys and content as values
        """
        text = text.strip()
        sections = {}
        
        # Find all section headers and their positions
        section_positions = []
        
        for section_name, pattern in self.section_patterns.items():
            matches = list(pattern.finditer(text))
            for match in matches:
                section_positions.append({
                    'name': section_name,
                    'start': match.start(),
                    'header_end': match.end()
                })
        
        # Sort by position
        section_positions.sort(key=lambda x: x['start'])
        
        # Extract content for each section
        for i, section in enumerate(section_positions):
            start = section['header_end']
            
            # End is the start of next section or end of text
            end = section_positions[i + 1]['start'] if i + 1 < len(section_positions) else len(text)
            
            content = text[start:end].strip()
            
            # Store the first occurrence of each section type
            if section['name'] not in sections:
                sections[section['name']] = content
        
        # If no sections found, treat entire text as general content
        if not sections:
            sections['general'] = text
        
        return sections
    
    def extract_contact_info(self, text: str) -> Dict[str, str]:
        """
        Extract contact information
        
        Args:
            text: Resume text
            
        Returns:
            Dictionary with contact information
        """
        contact_info = {}
        
        # Email pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, text)
        if email_match:
            contact_info['email'] = email_match.group()
        
        # Phone pattern
        phone_pattern = r'[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,5}[-\s\.]?[0-9]{1,5}'
        phone_match = re.search(phone_pattern, text)
        if phone_match:
            contact_info['phone'] = phone_match.group()
        
        # LinkedIn
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        linkedin_match = re.search(linkedin_pattern, text, re.IGNORECASE)
        if linkedin_match:
            contact_info['linkedin'] = linkedin_match.group()
        
        # GitHub
        github_pattern = r'github\.com/[\w-]+'
        github_match = re.search(github_pattern, text, re.IGNORECASE)
        if github_match:
            contact_info['github'] = github_match.group()
        
        return contact_info


# Test
if __name__ == "__main__":
    from src.preprocessing.pdf_parser import PDFParser
    
    parser = PDFParser()
    detector = SectionDetector()
    
    resume_path = Path(__file__).parent.parent.parent / "data" / "raw" / "sample_resume.txt"
    
    if resume_path.exists():
        text = parser.parse(resume_path)
        sections = detector.detect_sections(text)
        contact = detector.extract_contact_info(text)
        
        print("✓ Detected sections:")
        for section_name, content in sections.items():
            print(f"  - {section_name}: {len(content)} characters")
        
        print("\n✓ Contact info:")
        for key, value in contact.items():
            print(f"  - {key}: {value}")
    else:
        print("⚠ Test file not found")