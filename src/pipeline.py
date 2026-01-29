"""
Main Pipeline - WITH ADVANCED RECOMMENDATIONS ENGINE INTEGRATED
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
from src.models.recommendation_engine import RecommendationEngine  # NEW!


class CandidateIntelligencePipeline:
    """Main pipeline with ADVANCED RECOMMENDATIONS"""
    
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
        self.recommendation_engine = RecommendationEngine()  # NEW!
        
        # Load or train skill gap model
        try:
            self.skill_gap_classifier.load_model()
        except:
            print("⚠️ Skill gap model not loaded")
    
    def analyze(self, resume_path: Union[str, Path], 
                jd_path: Union[str, Path]) -> Dict:
        """
        Run complete analysis pipeline WITH ADVANCED RECOMMENDATIONS
        """
        print("🔄 Starting ADVANCED analysis pipeline...")
        
        # Step 1: Parse documents
        print("  1/7 Parsing documents...")
        resume_text = self.pdf_parser.parse(resume_path)
        jd_text = self.pdf_parser.parse(jd_path)
        
        print(f"     - Resume: {len(resume_text)} chars")
        print(f"     - JD: {len(jd_text)} chars")
        
        # Step 2: Detect sections
        print("  2/7 Detecting sections...")
        resume_sections = self.section_detector.detect_sections(resume_text)
        contact_info = self.section_detector.extract_contact_info(resume_text)
        
        # Step 3: Extract skills
        print("  3/7 Extracting skills...")
        resume_skills = self.skill_extractor.extract_skills(resume_text)
        jd_skills = self.skill_extractor.extract_skills(jd_text)
        
        # Step 4: Analyze experience (BOTH resume AND JD)
        print("  4/7 Analyzing experience...")
        resume_experience = self._analyze_experience(resume_sections, resume_text)
        jd_experience = self._detect_required_experience(jd_text)
        
        print(f"     - Candidate: {resume_experience['total_years']} years, {resume_experience['seniority_level']}")
        print(f"     - Required: {jd_experience['required_years']} years, {jd_experience['required_level']}")
        
        # Step 5: Calculate semantic similarity
        print("  5/7 Calculating similarity...")
        similarity = self.semantic_matcher.calculate_similarity(resume_text, jd_text)
        print(f"     - Similarity: {similarity.get('overall_similarity', 0)}%")
        
        # Step 6: Generate scores
        print("  6/7 Generating scores...")
        skill_match = self._calculate_skill_match(resume_skills, jd_skills)
        skill_gaps = self._identify_skill_gaps(resume_skills, jd_skills)
        
        experience_score = self._score_experience_intelligent(
            resume_experience, 
            jd_experience
        )
        
        education_score = self._score_education(resume_sections)
        learning_potential = self._calculate_learning_potential(skill_gaps)
        
        # Generate final score
        final_result = self.scoring_engine.calculate_final_score(
            skill_match_score=skill_match['match_percentage'],
            experience_score=experience_score,
            semantic_similarity=similarity.get('overall_similarity', 0),
            education_score=education_score,
            learning_potential=learning_potential
        )
        
        # Step 7: Generate ADVANCED RECOMMENDATIONS (NEW!)
        print("  7/7 Generating advanced recommendations...")
        advanced_recommendations = self.recommendation_engine.generate_comprehensive_recommendations(
            overall_score=final_result['final_score'],
            component_scores=final_result['component_scores'],
            skill_analysis={
                'total_skills_found': sum(len(skills) for skills in resume_skills.values()),
                'match_percentage': skill_match['match_percentage'],
                'matched_skills': skill_match['matched_skills'],
                'missing_skills': skill_gaps,
                'by_category': self.skill_extractor.get_skill_summary(resume_skills)
            },
            experience_analysis=resume_experience,
            jd_text=jd_text,
            resume_text=resume_text,
            required_experience=jd_experience
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
            'experience_analysis': resume_experience,
            'required_experience': jd_experience,
            'semantic_similarity': similarity,
            'component_scores': final_result['component_scores'],
            'strengths': self.scoring_engine.generate_strengths(final_result['component_scores']),
            'top_gaps': self.scoring_engine.generate_gaps(skill_gaps, top_n=5),
            
            # NEW: ADVANCED RECOMMENDATIONS
            'advanced_recommendations': advanced_recommendations
        }
        
        print("✅ Advanced analysis complete!\n")
        return report
    
    def _analyze_experience(self, sections: Dict, full_text: str) -> Dict:
        """Analyze experience section"""
        if 'experience' in sections and sections['experience']:
            return self.experience_analyzer.analyze_experience(sections['experience'])
        
        print("     ⚠️ No experience section, analyzing full text...")
        result = self.experience_analyzer.analyze_experience(full_text)
        
        if result['total_years'] == 0:
            result['is_fresher'] = True
            print("     ✓ Detected as FRESHER candidate")
        
        return result
    
    def _detect_required_experience(self, jd_text: str) -> Dict:
        """Detect required experience from job description"""
        jd_lower = jd_text.lower()
        
        fresher_keywords = [
            'fresher', 'freshers', 'entry level', 'entry-level',
            'no experience required', '0 years', '0-1 years',
            'recent graduate', 'new graduate', 'graduate trainee',
            'internship', 'trainee', 'beginner'
        ]
        
        is_fresher_role = any(keyword in jd_lower for keyword in fresher_keywords)
        
        if is_fresher_role:
            print("     ✓ Detected as FRESHER/ENTRY-LEVEL role")
            return {
                'required_years': 0,
                'required_level': 'entry',
                'is_fresher_role': True
            }
        
        import re
        
        year_patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)\s+(?:of\s+)?(?:experience|exp)',
            r'(?:minimum|min|at least)\s+(\d+)\s*(?:years?|yrs?)',
            r'(\d+)\s*[-–]\s*(\d+)\s*(?:years?|yrs?)'
        ]
        
        required_years = 0
        for pattern in year_patterns:
            matches = re.findall(pattern, jd_lower)
            if matches:
                if isinstance(matches[0], tuple):
                    required_years = max(required_years, int(matches[0][0]))
                else:
                    required_years = max(required_years, int(matches[0]))
        
        required_level = 'entry'
        if any(word in jd_lower for word in ['senior', 'lead', 'principal', 'architect']):
            required_level = 'senior'
            if required_years == 0:
                required_years = 5
        elif any(word in jd_lower for word in ['mid', 'intermediate', 'associate']):
            required_level = 'mid'
            if required_years == 0:
                required_years = 3
        elif any(word in jd_lower for word in ['junior']):
            required_level = 'junior'
            if required_years == 0:
                required_years = 1
        
        return {
            'required_years': required_years,
            'required_level': required_level,
            'is_fresher_role': False
        }
    
    def _score_experience_intelligent(self, resume_exp: Dict, jd_exp: Dict) -> float:
        """INTELLIGENT experience scoring"""
        candidate_years = resume_exp['total_years']
        required_years = jd_exp['required_years']
        
        is_fresher_role = jd_exp.get('is_fresher_role', False)
        is_fresher_candidate = resume_exp.get('is_fresher', False) or candidate_years < 0.5
        
        print(f"     🎯 Experience Scoring:")
        print(f"        - Candidate: {candidate_years} years")
        print(f"        - Required: {required_years} years")
        
        if is_fresher_role and is_fresher_candidate:
            print(f"        ✓ PERFECT MATCH: Fresher + Fresher role = 100")
            return 100.0
        
        if is_fresher_role and not is_fresher_candidate:
            score = max(70, 100 - (candidate_years * 5))
            print(f"        ⚠️ Overqualified for fresher role: {score}")
            return round(score, 2)
        
        if not is_fresher_role and is_fresher_candidate and required_years > 2:
            score = 20.0
            print(f"        ⚠️ Underqualified: Fresher for {required_years}+ role = {score}")
            return score
        
        if required_years == 0:
            score = min(candidate_years * 10, 80)
        elif candidate_years >= required_years:
            excess = candidate_years - required_years
            if excess <= 2:
                score = 100.0
            elif excess <= 5:
                score = 95.0
            else:
                score = 85.0
        else:
            shortage = required_years - candidate_years
            penalty = shortage * 15
            score = max(30, 100 - penalty)
        
        print(f"        ✓ Experience score: {score}")
        return round(score, 2)
    
    def _calculate_skill_match(self, resume_skills: Dict, jd_skills: Dict) -> Dict:
        """Calculate skill match percentage"""
        resume_skill_names = set()
        for category_skills in resume_skills.values():
            for skill_data in category_skills:
                resume_skill_names.add(skill_data['skill'].lower())
        
        jd_skill_names = set()
        for category_skills in jd_skills.values():
            for skill_data in category_skills:
                jd_skill_names.add(skill_data['skill'].lower())
        
        if not jd_skill_names:
            return {
                'match_percentage': 0,
                'matched_skills': [],
                'total_jd_skills': 0,
                'total_resume_skills': len(resume_skill_names)
            }
        
        matched = resume_skill_names.intersection(jd_skill_names)
        match_percentage = (len(matched) / len(jd_skill_names) * 100)
        
        return {
            'match_percentage': round(match_percentage, 2),
            'matched_skills': list(matched),
            'total_jd_skills': len(jd_skill_names),
            'total_resume_skills': len(resume_skill_names)
        }
    
    def _identify_skill_gaps(self, resume_skills: Dict, jd_skills: Dict) -> list:
        """Identify missing skills"""
        resume_skill_names = set()
        for category_skills in resume_skills.values():
            for skill_data in category_skills:
                resume_skill_names.add(skill_data['skill'].lower())
        
        gaps = []
        for category, category_skills in jd_skills.items():
            for skill_data in category_skills:
                skill_name = skill_data['skill']
                if skill_name.lower() not in resume_skill_names:
                    try:
                        prediction = self.skill_gap_classifier.predict_difficulty(
                            has_base=0,
                            skill_similarity=0.5,
                            domain_overlap=0.6
                        )
                        difficulty = prediction.get('difficulty', 'medium')
                        learning_days = prediction.get('estimated_learning_days', 60)
                    except:
                        difficulty = 'medium'
                        learning_days = 60
                    
                    gaps.append({
                        'skill': skill_name,
                        'category': category,
                        'difficulty': difficulty,
                        'learning_days': learning_days
                    })
        
        return gaps
    
    def _score_education(self, sections: Dict) -> float:
        """Score education relevance"""
        if 'education' not in sections:
            return 50.0
        
        education_text = sections['education'].lower()
        
        relevant_keywords = [
            'computer science', 'engineering', 'data science',
            'machine learning', 'artificial intelligence', 'statistics',
            'mathematics', 'technology', 'information technology'
        ]
        
        matches = sum(1 for keyword in relevant_keywords if keyword in education_text)
        score = min(50 + (matches * 10), 100)
        return round(score, 2)
    
    def _calculate_learning_potential(self, skill_gaps: list) -> float:
        """Calculate learning potential"""
        if not skill_gaps:
            return 100.0
        
        difficulty_scores = {'easy': 100, 'medium': 60, 'hard': 30}
        total_score = sum(difficulty_scores.get(gap['difficulty'], 60) for gap in skill_gaps)
        avg_score = total_score / len(skill_gaps)
        
        return round(avg_score, 2)