"""
Experience Analyzer - Analyzes work experience from resume (FIXED VERSION)
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
        print(f"  🔍 DEBUG Experience Analysis:")
        print(f"     - Input length: {len(experience_text)} chars")
        
        # Extract years using multiple methods
        years = self._extract_years_improved(experience_text)
        print(f"     - Years found: {years}")
        
        # Calculate total experience
        total_years = self._calculate_total_years(years, experience_text)
        print(f"     - Total years calculated: {total_years}")
        
        # Detect seniority level
        seniority = self._detect_seniority(experience_text, total_years)
        
        # Count roles
        roles = self._count_roles(experience_text)
        
        result = {
            'total_years': total_years,
            'seniority_level': seniority,
            'number_of_roles': roles,
            'years_mentioned': years
        }
        
        print(f"     ✓ Experience analysis complete: {total_years} years, {seniority} level")
        return result
    
    def _extract_years_improved(self, text: str) -> List[int]:
        """Enhanced year extraction with multiple patterns"""
        years = []
        
        # Pattern 1: Standard 4-digit years (1990-2099)
        year_pattern = r'\b(19\d{2}|20[0-2]\d)\b'
        year_matches = re.findall(year_pattern, text)
        years.extend([int(y) for y in year_matches])
        
        # Pattern 2: Explicit year mentions like "5 years", "3+ years"
        exp_years_pattern = r'(\d+)\+?\s*(?:years?|yrs?)\s+(?:of\s+)?(?:experience|exp)'
        exp_matches = re.findall(exp_years_pattern, text, re.IGNORECASE)
        if exp_matches:
            # These are direct year counts, not calendar years
            # Use current year as reference
            current_year = datetime.now().year
            for exp_years in exp_matches:
                years.append(current_year - int(exp_years))
        
        # Remove duplicates and sort
        years = sorted(list(set(years)))
        
        return years
    
    def _calculate_total_years(self, years: List[int], text: str) -> float:
        """Calculate total years of experience from year mentions"""
        print(f"       > Calculating from years: {years}")
        
        # Method 1: Look for explicit year mentions first
        exp_pattern = r'(\d+\.?\d*)\+?\s*(?:years?|yrs?)\s+(?:of\s+)?(?:experience|exp)'
        exp_matches = re.findall(exp_pattern, text, re.IGNORECASE)
        
        if exp_matches:
            # Found explicit mention like "5 years of experience"
            total = max([float(y) for y in exp_matches])
            print(f"       > Found explicit: {total} years")
            return round(total, 1)
        
        # Method 2: Calculate from date ranges
        if not years or len(years) < 1:
            print(f"       > No years found, returning 0")
            return 0.0
        
        current_year = datetime.now().year
        
        # If we have pairs of years (start-end dates)
        if len(years) >= 2:
            # Find all date ranges
            date_ranges = []
            i = 0
            while i < len(years) - 1:
                start_year = years[i]
                end_year = years[i + 1] if i + 1 < len(years) else current_year
                
                # Validate range
                if start_year <= end_year and end_year <= current_year:
                    duration = end_year - start_year
                    if 0 <= duration <= 50:  # Reasonable range
                        date_ranges.append(duration)
                i += 2
            
            if date_ranges:
                # Sum all ranges (overlaps are ignored for simplicity)
                total = sum(date_ranges)
                print(f"       > Calculated from ranges: {total} years")
                return round(float(total), 1)
            
            # Fallback: latest - earliest
            max_year = min(max(years), current_year)
            min_year = min(years)
            total = max_year - min_year
            print(f"       > Fallback (max-min): {total} years")
            return round(float(total), 1)
        
        # If only one year mentioned, assume it's start year
        if len(years) == 1:
            year = min(years[0], current_year)
            total = current_year - year
            print(f"       > Single year, current-year: {total} years")
            return round(float(total), 1)
        
        return 0.0
    
    def _detect_seniority(self, text: str, years: float) -> str:
        """Detect seniority level from text and years"""
        text_lower = text.lower()
        
        # Keyword-based detection
        if any(word in text_lower for word in ['senior', 'lead', 'principal', 'architect', 'staff', 'expert']):
            return 'senior'
        elif any(word in text_lower for word in ['junior', 'associate', 'trainee', 'assistant']):
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
            r'\n\s*[A-Z][a-z]+\s+(Engineer|Developer|Analyst|Scientist|Manager|Intern|Consultant)',
            r'\n\s*[A-Z][a-z]+\s+[A-Z][a-z]+\s+(Engineer|Developer|Analyst)',
            r'\n\s*•\s*[A-Z][a-z]+\s+(Engineer|Developer|Analyst|Scientist|Manager)',
        ]
        
        count = 0
        for pattern in role_indicators:
            matches = re.findall(pattern, text)
            count += len(matches)
        
        # Also count date ranges as indicators of separate roles
        date_pattern = r'\b(19\d{2}|20[0-2]\d)\s*[-–—]\s*(19\d{2}|20[0-2]\d|present|current)\b'
        date_ranges = re.findall(date_pattern, text, re.IGNORECASE)
        count = max(count, len(date_ranges))
        
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
            r'(Achieved|Improved|Increased|Decreased|Led|Built|Developed|Created|Implemented|Designed)\s+([^.\n]{20,150})',
        ]
        
        achievements = []
        
        for pattern in achievement_patterns:
            matches = re.findall(pattern, experience_text, re.IGNORECASE)
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