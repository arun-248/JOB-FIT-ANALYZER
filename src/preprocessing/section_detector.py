"""
Section Detector - Identifies sections in resume text (FIXED VERSION)
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
        # Enhanced section patterns with more variations
        self.section_patterns = {
            "experience": re.compile(
                r"(work\s+experience|professional\s+experience|experience|employment\s+history|"
                r"work\s+history|career\s+history|employment|professional\s+background|"
                r"relevant\s+experience|job\s+history)",
                re.IGNORECASE
            ),
            "education": re.compile(
                r"(education|academic\s+background|qualifications?|degrees?|"
                r"academic\s+qualifications|educational\s+background)",
                re.IGNORECASE
            ),
            "skills": re.compile(
                r"(skills|technical\s+skills|core\s+competencies|expertise|"
                r"key\s+skills|competencies|technical\s+expertise|proficiencies)",
                re.IGNORECASE
            ),
            "projects": re.compile(
                r"(projects|portfolio|work\s+samples|key\s+projects|"
                r"notable\s+projects|project\s+experience)",
                re.IGNORECASE
            ),
            "certifications": re.compile(
                r"(certifications?|certificates?|training|licenses?|"
                r"professional\s+certifications|credentials)",
                re.IGNORECASE
            ),
            "summary": re.compile(
                r"(summary|professional\s+summary|profile|objective|"
                r"career\s+objective|about\s+me|personal\s+statement)",
                re.IGNORECASE
            )
        }
    
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
                    'header_end': match.end(),
                    'header_text': match.group()
                })
        
        # Sort by position
        section_positions.sort(key=lambda x: x['start'])
        
        # DEBUG: Print found sections
        print(f"  🔍 DEBUG: Found {len(section_positions)} section headers:")
        for sec in section_positions:
            print(f"     - {sec['name']}: '{sec['header_text']}' at position {sec['start']}")
        
        # Extract content for each section
        for i, section in enumerate(section_positions):
            start = section['header_end']
            
            # End is the start of next section or end of text
            end = section_positions[i + 1]['start'] if i + 1 < len(section_positions) else len(text)
            
            content = text[start:end].strip()
            
            # Store the first occurrence of each section type
            if section['name'] not in sections:
                sections[section['name']] = content
                print(f"     ✓ Extracted {section['name']}: {len(content)} chars")
        
        # FALLBACK: If no sections found, try to identify experience by keywords
        if 'experience' not in sections and len(text) > 100:
            print("  ⚠️  No 'experience' section found, trying fallback detection...")
            # Look for date patterns (likely experience section)
            date_pattern = r'\b(20\d{2}|19\d{2})\s*[-–—]\s*(20\d{2}|19\d{2}|present|current)\b'
            date_matches = list(re.finditer(date_pattern, text, re.IGNORECASE))
            
            if date_matches:
                # Assume experience section starts before first date
                exp_start = max(0, date_matches[0].start() - 200)
                # And ends after last date or at 50% of text
                exp_end = min(len(text), date_matches[-1].end() + 500)
                sections['experience'] = text[exp_start:exp_end].strip()
                print(f"     ✓ FALLBACK: Extracted experience by date pattern: {len(sections['experience'])} chars")
        
        # If still no sections found, treat entire text as general content
        if not sections:
            sections['general'] = text
            print("  ⚠️  No sections detected, using entire text as 'general'")
        
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