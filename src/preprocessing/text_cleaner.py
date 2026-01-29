"""
Text Cleaner - Cleans and normalizes text
"""

import re
from typing import List


class TextCleaner:
    """Handles text cleaning and normalization"""
    
    def __init__(self):
        self.stopwords = self._load_stopwords()
    
    def _load_stopwords(self) -> set:
        """Load common English stopwords"""
        return {
            'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your',
            'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she',
            'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their',
            'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
            'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an',
            'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of',
            'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
            'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
            'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once'
        }
    
    def clean_text(self, text: str) -> str:
        """
        Basic text cleaning
        
        Args:
            text: Raw text
            
        Returns:
            Cleaned text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep some punctuation
        text = re.sub(r'[^\w\s\.\,\-\+\#]', '', text)
        
        return text.strip()
    
    def remove_stopwords(self, text: str) -> str:
        """
        Remove stopwords from text
        
        Args:
            text: Cleaned text
            
        Returns:
            Text without stopwords
        """
        words = text.split()
        filtered_words = [word for word in words if word not in self.stopwords]
        return ' '.join(filtered_words)
    
    def extract_years(self, text: str) -> List[int]:
        """
        Extract year mentions from text
        
        Args:
            text: Text containing dates
            
        Returns:
            List of years found
        """
        year_pattern = r'\b(19|20)\d{2}\b'
        years = re.findall(year_pattern, text)
        return [int(year) for year in years]
    
    def normalize_skill_name(self, skill: str) -> str:
        """
        Normalize skill names for consistent matching
        
        Args:
            skill: Raw skill name
            
        Returns:
            Normalized skill name
        """
        skill = skill.strip().title()
        
        # Handle common variations
        skill_mappings = {
            'Tensorflow': 'TensorFlow',
            'Pytorch': 'PyTorch',
            'Scikit-Learn': 'Scikit-learn',
            'Fastapi': 'FastAPI',
            'Javascript': 'JavaScript',
            'Typescript': 'TypeScript',
            'Mongodb': 'MongoDB',
            'Mysql': 'MySQL',
            'Postgresql': 'PostgreSQL',
            'Numpy': 'NumPy',
            'Scipy': 'SciPy'
        }
        
        return skill_mappings.get(skill, skill)


# Test
if __name__ == "__main__":
    cleaner = TextCleaner()
    
    sample = "I have 5+ YEARS of experience with Python, TensorFlow, and Machine Learning!!!"
    
    print("Original:", sample)
    print("Cleaned:", cleaner.clean_text(sample))
    print("Without stopwords:", cleaner.remove_stopwords(cleaner.clean_text(sample)))
    print("Years:", cleaner.extract_years(sample))
    print("✓ Text cleaner working")