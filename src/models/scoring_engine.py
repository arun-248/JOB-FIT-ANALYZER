"""
Scoring Engine - Aggregates all scores into final recommendation
"""

from typing import Dict, List
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.config import SCORING_WEIGHTS, MATCH_THRESHOLDS


class ScoringEngine:
    """Aggregates all analysis into final candidate score"""
    
    def __init__(self):
        self.weights = SCORING_WEIGHTS
        self.thresholds = MATCH_THRESHOLDS
    
    def calculate_final_score(self, 
                             skill_match_score: float,
                             experience_score: float,
                             semantic_similarity: float,
                             education_score: float,
                             learning_potential: float) -> Dict:
        """
        Calculate weighted final score
        
        Args:
            skill_match_score: Skill match percentage (0-100)
            experience_score: Experience match score (0-100)
            semantic_similarity: TF-IDF similarity (0-100)
            education_score: Education relevance score (0-100)
            learning_potential: Learning potential score (0-100)
            
        Returns:
            Dictionary with final score and recommendation
        """
        # Normalize all scores to 0-1 range
        normalized_scores = {
            'skill_match': skill_match_score / 100,
            'experience': experience_score / 100,
            'semantic_similarity': semantic_similarity / 100,
            'education': education_score / 100,
            'learning_potential': learning_potential / 100
        }
        
        # Calculate weighted score
        final_score = sum(
            normalized_scores[key] * self.weights[key]
            for key in self.weights.keys()
        ) * 100
        
        # Generate recommendation
        recommendation = self._get_recommendation(final_score)
        
        # Calculate confidence
        confidence = self._calculate_confidence(normalized_scores)
        
        return {
            'final_score': round(final_score, 2),
            'recommendation': recommendation,
            'confidence': confidence,
            'component_scores': {
                'skill_match': round(skill_match_score, 2),
                'experience': round(experience_score, 2),
                'semantic_similarity': round(semantic_similarity, 2),
                'education': round(education_score, 2),
                'learning_potential': round(learning_potential, 2)
            }
        }
    
    def _get_recommendation(self, score: float) -> str:
        """Get hiring recommendation based on score"""
        if score >= self.thresholds['strong_match']:
            return "Strong Match - Highly Recommended"
        elif score >= self.thresholds['potential_match']:
            return "Potential Match - Consider for Interview"
        elif score >= self.thresholds['weak_match']:
            return "Weak Match - Requires Significant Training"
        else:
            return "Not Recommended - Significant Skill Gaps"
    
    def _calculate_confidence(self, scores: Dict[str, float]) -> str:
        """Calculate confidence level in the recommendation"""
        # Calculate variance in scores
        score_values = list(scores.values())
        mean_score = sum(score_values) / len(score_values)
        variance = sum((x - mean_score) ** 2 for x in score_values) / len(score_values)
        
        # Low variance = high confidence
        if variance < 0.05:
            return "High"
        elif variance < 0.15:
            return "Medium"
        else:
            return "Low"
    
    def generate_strengths(self, component_scores: Dict[str, float], top_n: int = 5) -> List[str]:
        """Generate list of candidate strengths"""
        strengths = []
        
        scores = component_scores
        
        if scores['skill_match'] >= 70:
            strengths.append("Strong technical skill match with job requirements")
        
        if scores['experience'] >= 70:
            strengths.append("Relevant work experience in similar roles")
        
        if scores['semantic_similarity'] >= 70:
            strengths.append("Resume content closely aligns with job description")
        
        if scores['education'] >= 70:
            strengths.append("Strong educational background for the role")
        
        if scores['learning_potential'] >= 70:
            strengths.append("High learning potential for missing skills")
        
        return strengths[:top_n]
    
    def generate_gaps(self, missing_skills: List[Dict], top_n: int = 3) -> List[Dict]:
        """
        Generate prioritized list of skill gaps
        
        Args:
            missing_skills: List of missing skills with difficulty
            top_n: Number of gaps to highlight
            
        Returns:
            List of prioritized gaps
        """
        # Sort by difficulty (hard skills first)
        difficulty_order = {'hard': 3, 'medium': 2, 'easy': 1}
        
        sorted_gaps = sorted(
            missing_skills,
            key=lambda x: difficulty_order.get(x.get('difficulty', 'medium'), 2),
            reverse=True
        )
        
        return sorted_gaps[:top_n]


# Test
if __name__ == "__main__":
    engine = ScoringEngine()
    
    # Test scoring
    result = engine.calculate_final_score(
        skill_match_score=75,
        experience_score=60,
        semantic_similarity=80,
        education_score=85,
        learning_potential=70
    )
    
    print("✓ Scoring Engine Test:")
    print(f"  Final Score: {result['final_score']}")
    print(f"  Recommendation: {result['recommendation']}")
    print(f"  Confidence: {result['confidence']}")
    
    # Test strengths
    strengths = engine.generate_strengths(result['component_scores'])
    print(f"\n  Strengths:")
    for strength in strengths:
        print(f"    - {strength}")