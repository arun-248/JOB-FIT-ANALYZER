"""
Experience Analyzer - Analyzes work experience from resume
"""

import re
from datetime import datetime
from typing import Dict, List, Tuple
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.preprocessing.text_cleaner import TextCleaner


class ExperienceAnalyzer:
    """Analyzes work experience and calculates years"""
    
    def __init__(self):
        self.text_cleaner = TextCleaner()
    
    def analyze_experience(self, experience_text: str) -> Dict:
        """
        Analyze experience section
        
        Args:
            experience_text: Experience section from resume
            
        Returns:
            Dictionary with experience analysis
        """
        # Extract years
        years = self.text_cleaner.extract_years(experience_text)
        
        # Calculate total experience
        total_years = self._calculate_total_years(years)
        
        # Detect seniority level
        seniority = self._detect_seniority(experience_text, total_years)
        
        # Count roles
        roles = self._count_roles(experience_text)
        
        return {
            'total_years': total_years,
            'seniority_level': seniority,
            'number_of_roles': roles,
            'years_mentioned': years
        }
    
    def _calculate_total_years(self, years: List[int]) -> float:
        """Calculate total years of experience from year mentions"""
        if not years:
            return 0.0
        
        current_year = datetime.now().year
        
        # If we have pairs of years (start-end)
        if len(years) >= 2:
            # Simple heuristic: latest year - earliest year
            max_year = max(years)
            min_year = min(years)
            
            # Cap max year at current year
            max_year = min(max_year, current_year)
            
            return float(max_year - min_year)
        
        # If only one year mentioned
        if len(years) == 1:
            return float(current_year - years[0])
        
        return 0.0
    
    def _detect_seniority(self, text: str, years: float) -> str:
        """Detect seniority level from text and years"""
        text_lower = text.lower()
        
        # Keyword-based detection
        if any(word in text_lower for word in ['senior', 'lead', 'principal', 'architect']):
            return 'senior'
        elif any(word in text_lower for word in ['junior', 'associate', 'trainee']):
            return 'junior'
        elif 'intern' in text_lower:
            return 'entry'
        
        # Years-based detection
        if years >= 5:
            return 'senior'
        elif years >= 3:
            return 'mid'
        elif years >= 1:
            return 'junior'
        else:
            return 'entry'
    
    def _count_roles(self, text: str) -> int:
        """Count number of roles/positions"""
        # Look for common job title indicators
        role_indicators = [
            r'\n[A-Z][a-z]+\s+(Engineer|Developer|Analyst|Scientist|Manager|Intern)',
            r'\n[A-Z][a-z]+\s+[A-Z][a-z]+\s+(Engineer|Developer)',
        ]
        
        count = 0
        for pattern in role_indicators:
            matches = re.findall(pattern, text)
            count += len(matches)
        
        # Minimum 1 role if experience section exists
        return max(count, 1)
    
    def extract_key_achievements(self, experience_text: str, top_n: int = 3) -> List[str]:
        """
        Extract key achievements from experience
        
        Args:
            experience_text: Experience section text
            top_n: Number of achievements to extract
            
        Returns:
            List of achievement strings
        """
        # Look for bullet points or achievement indicators
        achievement_patterns = [
            r'[-•]\s*([^-•\n]{20,150})',  # Bullet points
            r'(Achieved|Improved|Increased|Decreased|Led|Built|Developed)\s+([^.\n]{20,150})',
        ]
        
        achievements = []
        
        for pattern in achievement_patterns:
            matches = re.findall(pattern, experience_text)
            for match in matches:
                if isinstance(match, tuple):
                    achievement = ' '.join(match).strip()
                else:
                    achievement = match.strip()
                
                if achievement and len(achievement) > 20:
                    achievements.append(achievement)
        
        # Return top N unique achievements
        unique_achievements = list(dict.fromkeys(achievements))
        return unique_achievements[:top_n]


# Test
if __name__ == "__main__":
    from src.preprocessing.pdf_parser import PDFParser
    from src.preprocessing.section_detector import SectionDetector
    
    parser = PDFParser()
    detector = SectionDetector()
    analyzer = ExperienceAnalyzer()
    
    resume_path = Path(__file__).parent.parent.parent / "data" / "raw" / "sample_resume.txt"
    
    if resume_path.exists():
        text = parser.parse(resume_path)
        sections = detector.detect_sections(text)
        
        if 'experience' in sections:
            exp_analysis = analyzer.analyze_experience(sections['experience'])
            achievements = analyzer.extract_key_achievements(sections['experience'])
            
            print("✓ Experience Analysis:")
            print(f"  Total years: {exp_analysis['total_years']}")
            print(f"  Seniority: {exp_analysis['seniority_level']}")
            print(f"  Roles: {exp_analysis['number_of_roles']}")
            print(f"\n  Key achievements:")
            for i, ach in enumerate(achievements, 1):
                print(f"    {i}. {ach[:80]}...")
        else:
            print("⚠ No experience section found")
    else:
        print("⚠ Test file not found")