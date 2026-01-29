"""
Main Pipeline - Orchestrates the entire analysis
"""

from typing import Dict, Union
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from src.preprocessing.pdf_parser import PDFParser
from src.preprocessing.section_detector import SectionDetector
from src.preprocessing.text_cleaner import TextCleaner
from src.feature_extraction.skill_extractor import SkillExtractor
from src.feature_extraction.experience_analyzer import ExperienceAnalyzer
from src.feature_extraction.semantic_matcher import SemanticMatcher
from src.models.skill_gap_classifier import SkillGapClassifier
from src.models.scoring_engine import ScoringEngine


class CandidateIntelligencePipeline:
    """Main pipeline that orchestrates all components"""
    
    def __init__(self):
        # Initialize all components
        self.pdf_parser = PDFParser()
        self.section_detector = SectionDetector()
        self.text_cleaner = TextCleaner()
        self.skill_extractor = SkillExtractor()
        self.experience_analyzer = ExperienceAnalyzer()
        self.semantic_matcher = SemanticMatcher()
        self.skill_gap_classifier = SkillGapClassifier()
        self.scoring_engine = ScoringEngine()
        
        # Load or train skill gap model
        self.skill_gap_classifier.load_model()
    
    def analyze(self, resume_path: Union[str, Path], 
                jd_path: Union[str, Path]) -> Dict:
        """
        Run complete analysis pipeline
        
        Args:
            resume_path: Path to resume file
            jd_path: Path to job description file
            
        Returns:
            Complete analysis report
        """
        print("🔄 Starting analysis pipeline...")
        
        # Step 1: Parse documents
        print("  1/6 Parsing documents...")
        resume_text = self.pdf_parser.parse(resume_path)
        jd_text = self.pdf_parser.parse(jd_path)
        
        # Step 2: Detect sections
        print("  2/6 Detecting sections...")
        resume_sections = self.section_detector.detect_sections(resume_text)
        contact_info = self.section_detector.extract_contact_info(resume_text)
        
        # Step 3: Extract skills
        print("  3/6 Extracting skills...")
        resume_skills = self.skill_extractor.extract_skills(resume_text)
        jd_skills = self.skill_extractor.extract_skills(jd_text)
        
        # Step 4: Analyze experience
        print("  4/6 Analyzing experience...")
        experience_analysis = self._analyze_experience(resume_sections)
        
        # Step 5: Calculate semantic similarity
        print("  5/6 Calculating similarity...")
        similarity = self.semantic_matcher.calculate_similarity(resume_text, jd_text)
        
        # Step 6: Generate scores and recommendations
        print("  6/6 Generating recommendations...")
        skill_match = self._calculate_skill_match(resume_skills, jd_skills)
        skill_gaps = self._identify_skill_gaps(resume_skills, jd_skills)
        
        # Calculate component scores
        experience_score = self._score_experience(experience_analysis)
        education_score = self._score_education(resume_sections)
        learning_potential = self._calculate_learning_potential(skill_gaps)
        
        # Generate final score
        final_result = self.scoring_engine.calculate_final_score(
            skill_match_score=skill_match['match_percentage'],
            experience_score=experience_score,
            semantic_similarity=similarity['overall_similarity'],
            education_score=education_score,
            learning_potential=learning_potential
        )
        
        # Compile complete report
        report = {
            'candidate_info': contact_info,
            'overall_score': final_result['final_score'],
            'recommendation': final_result['recommendation'],
            'confidence': final_result['confidence'],
            'skill_analysis': {
                'total_skills_found': sum(len(skills) for skills in resume_skills.values()),
                'match_percentage': skill_match['match_percentage'],
                'matched_skills': skill_match['matched_skills'],
                'missing_skills': skill_gaps,
                'by_category': self.skill_extractor.get_skill_summary(resume_skills)
            },
            'experience_analysis': experience_analysis,
            'semantic_similarity': similarity,
            'component_scores': final_result['component_scores'],
            'strengths': self.scoring_engine.generate_strengths(final_result['component_scores']),
            'top_gaps': self.scoring_engine.generate_gaps(skill_gaps, top_n=5)
        }
        
        print("✅ Analysis complete!\n")
        return report
    
    def _analyze_experience(self, sections: Dict) -> Dict:
        """Analyze experience section"""
        if 'experience' in sections:
            return self.experience_analyzer.analyze_experience(sections['experience'])
        return {
            'total_years': 0.0,
            'seniority_level': 'entry',
            'number_of_roles': 0
        }
    
    def _calculate_skill_match(self, resume_skills: Dict, jd_skills: Dict) -> Dict:
        """Calculate skill match percentage"""
        # Flatten all skills
        resume_skill_names = set()
        for category_skills in resume_skills.values():
            for skill_data in category_skills:
                resume_skill_names.add(skill_data['skill'].lower())
        
        jd_skill_names = set()
        for category_skills in jd_skills.values():
            for skill_data in category_skills:
                jd_skill_names.add(skill_data['skill'].lower())
        
        # Calculate match
        matched = resume_skill_names.intersection(jd_skill_names)
        match_percentage = (len(matched) / len(jd_skill_names) * 100) if jd_skill_names else 0
        
        return {
            'match_percentage': round(match_percentage, 2),
            'matched_skills': list(matched),
            'total_jd_skills': len(jd_skill_names),
            'total_resume_skills': len(resume_skill_names)
        }
    
    def _identify_skill_gaps(self, resume_skills: Dict, jd_skills: Dict) -> list:
        """Identify missing skills and predict learning difficulty"""
        resume_skill_names = set()
        for category_skills in resume_skills.values():
            for skill_data in category_skills:
                resume_skill_names.add(skill_data['skill'].lower())
        
        gaps = []
        for category, category_skills in jd_skills.items():
            for skill_data in category_skills:
                skill_name = skill_data['skill']
                if skill_name.lower() not in resume_skill_names:
                    # Predict difficulty
                    prediction = self.skill_gap_classifier.predict_difficulty(
                        has_base=0,  # Simplified - could be improved
                        skill_similarity=0.5,
                        domain_overlap=0.6
                    )
                    
                    gaps.append({
                        'skill': skill_name,
                        'category': category,
                        'difficulty': prediction['difficulty'],
                        'learning_days': prediction['estimated_learning_days']
                    })
        
        return gaps
    
    def _score_experience(self, experience_analysis: Dict) -> float:
        """Score experience (0-100)"""
        years = experience_analysis['total_years']
        
        # Simple scoring: 0 years = 0, 5+ years = 100
        score = min(years / 5 * 100, 100)
        return round(score, 2)
    
    def _score_education(self, sections: Dict) -> float:
        """Score education relevance (0-100)"""
        if 'education' not in sections:
            return 50.0  # Neutral score
        
        education_text = sections['education'].lower()
        
        # Look for relevant keywords
        relevant_keywords = [
            'computer science', 'engineering', 'data science',
            'machine learning', 'artificial intelligence', 'statistics',
            'mathematics', 'technology'
        ]
        
        matches = sum(1 for keyword in relevant_keywords if keyword in education_text)
        
        # Score based on matches
        score = min(50 + (matches * 10), 100)
        return round(score, 2)
    
    def _calculate_learning_potential(self, skill_gaps: list) -> float:
        """Calculate learning potential (0-100)"""
        if not skill_gaps:
            return 100.0  # No gaps = perfect
        
        # Average difficulty (inverse)
        difficulty_scores = {'easy': 100, 'medium': 60, 'hard': 30}
        
        total_score = sum(difficulty_scores.get(gap['difficulty'], 60) for gap in skill_gaps)
        avg_score = total_score / len(skill_gaps)
        
        return round(avg_score, 2)


# Test the complete pipeline
if __name__ == "__main__":
    pipeline = CandidateIntelligencePipeline()
    
    resume_path = Path(__file__).parent.parent / "data" / "raw" / "sample_resume.txt"
    jd_path = Path(__file__).parent.parent / "data" / "raw" / "sample_job_description.txt"
    
    if resume_path.exists() and jd_path.exists():
        report = pipeline.analyze(resume_path, jd_path)
        
        print("=" * 60)
        print("CANDIDATE INTELLIGENCE REPORT")
        print("=" * 60)
        print(f"\nOverall Score: {report['overall_score']}/100")
        print(f"Recommendation: {report['recommendation']}")
        print(f"Confidence: {report['confidence']}")
        
        print(f"\n📊 Component Scores:")
        for component, score in report['component_scores'].items():
            print(f"  {component}: {score}/100")
        
        print(f"\n💪 Strengths:")
        for strength in report['strengths']:
            print(f"  ✓ {strength}")
        
        print(f"\n📚 Top Skill Gaps:")
        for gap in report['top_gaps'][:3]:
            print(f"  ⚠ {gap['skill']} ({gap['difficulty']}, ~{gap['learning_days']} days)")
    else:
        print("⚠ Sample files not found")