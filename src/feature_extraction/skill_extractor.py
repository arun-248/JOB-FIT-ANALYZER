"""
Skill Extraction Engine
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Set
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.config import SKILL_TAXONOMY_PATH, MIN_SKILL_CONFIDENCE


class SkillExtractor:
    """Extracts skills from text using taxonomy matching"""
    
    def __init__(self):
        self.skill_taxonomy = self._load_skill_taxonomy()
        self.all_skills = self._flatten_skills()
    
    def _load_skill_taxonomy(self) -> Dict:
        """Load skill taxonomy from JSON file"""
        if not SKILL_TAXONOMY_PATH.exists():
            print(f"⚠ Skill taxonomy not found at {SKILL_TAXONOMY_PATH}")
            return {}
        
        with open(SKILL_TAXONOMY_PATH, 'r') as f:
            return json.load(f)
    
    def _flatten_skills(self) -> Set[str]:
        """Create a flat set of all skills for quick lookup"""
        all_skills = set()
        for category, skills in self.skill_taxonomy.items():
            all_skills.update([skill.lower() for skill in skills])
        return all_skills
    
    def extract_skills(self, text: str) -> Dict[str, List[Dict]]:
        """
        Extract skills from text with confidence scores
        
        Args:
            text: Resume or JD text
            
        Returns:
            Dictionary with skill categories and extracted skills
        """
        text_lower = text.lower()
        extracted_skills = {}
        
        # Extract by category
        for category, skill_list in self.skill_taxonomy.items():
            category_skills = []
            
            for skill in skill_list:
                skill_lower = skill.lower()
                
                # Check if skill is mentioned
                if skill_lower in text_lower:
                    # Count occurrences
                    count = text_lower.count(skill_lower)
                    
                    # Extract context
                    context = self._extract_context(text, skill)
                    
                    # Calculate confidence
                    confidence = min(0.5 + (count * 0.1), 1.0)
                    
                    category_skills.append({
                        'skill': skill,
                        'count': count,
                        'confidence': round(confidence, 2),
                        'context': context[:100]
                    })
            
            if category_skills:
                category_skills.sort(key=lambda x: x['confidence'], reverse=True)
                extracted_skills[category] = category_skills
        
        return extracted_skills
    
    def _extract_context(self, text: str, skill: str, window: int = 50) -> str:
        """Extract context around skill mention"""
        text_lower = text.lower()
        skill_lower = skill.lower()
        
        pos = text_lower.find(skill_lower)
        if pos == -1:
            return ""
        
        start = max(0, pos - window)
        end = min(len(text), pos + len(skill) + window)
        
        return text[start:end]
    
    def get_skill_summary(self, extracted_skills: Dict) -> Dict:
        """Generate summary statistics"""
        total_skills = sum(len(skills) for skills in extracted_skills.values())
        
        summary = {
            'total_skills': total_skills,
            'categories_found': len(extracted_skills),
            'by_category': {}
        }
        
        for category, skills in extracted_skills.items():
            summary['by_category'][category] = {
                'count': len(skills),
                'top_skills': [s['skill'] for s in skills[:5]]
            }
        
        return summary
    
    def extract_skill_years(self, text: str, skill: str) -> float:
        """Attempt to extract years of experience for a skill"""
        patterns = [
            rf'(\d+)\s*(?:years?|yrs?)\s+(?:of\s+)?{skill}',
            rf'{skill}\s*\((\d+)\s*(?:years?|yrs?)\)',
            rf'{skill}.*?(\d+)\s*(?:years?|yrs?)'
        ]
        
        text_lower = text.lower()
        skill_lower = skill.lower()
        
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                return float(match.group(1))
        
        return 0.0


# Test
if __name__ == "__main__":
    from src.preprocessing.pdf_parser import PDFParser
    
    extractor = SkillExtractor()
    parser = PDFParser()
    
    resume_path = Path(__file__).parent.parent.parent / "data" / "raw" / "sample_resume.txt"
    
    if resume_path.exists():
        text = parser.parse(resume_path)
        skills = extractor.extract_skills(text)
        summary = extractor.get_skill_summary(skills)
        
        print("✓ Skill Extraction Results:")
        print(f"Total skills: {summary['total_skills']}")
        print(f"Categories: {summary['categories_found']}")
        
        for category, data in summary['by_category'].items():
            print(f"\n{category} ({data['count']} skills):")
            print(f"  Top: {', '.join(data['top_skills'])}")
    else:
        print("⚠ Test file not found")