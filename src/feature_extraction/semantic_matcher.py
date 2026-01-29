"""
Semantic Matcher - Matches resume to job description using TF-IDF
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import Dict, Tuple
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.config import TFIDF_PARAMS
from src.preprocessing.text_cleaner import TextCleaner


class SemanticMatcher:
    """Matches resume to job description using TF-IDF and cosine similarity"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(**TFIDF_PARAMS)
        self.text_cleaner = TextCleaner()
        self.is_fitted = False
    
    def calculate_similarity(self, resume_text: str, jd_text: str) -> Dict[str, float]:
        """
        Calculate semantic similarity between resume and JD
        
        Args:
            resume_text: Resume text
            jd_text: Job description text
            
        Returns:
            Dictionary with similarity scores
        """
        # Clean texts
        resume_clean = self.text_cleaner.clean_text(resume_text)
        jd_clean = self.text_cleaner.clean_text(jd_text)
        
        # Fit vectorizer and transform
        try:
            tfidf_matrix = self.vectorizer.fit_transform([resume_clean, jd_clean])
            self.is_fitted = True
        except Exception as e:
            print(f"⚠ TF-IDF error: {e}")
            return {'overall_similarity': 0.0, 'top_matching_terms': []}
        
        # Calculate cosine similarity
        similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        overall_similarity = similarity_matrix[0][0]
        
        # Get top matching terms
        top_terms = self._get_top_matching_terms(tfidf_matrix, n=10)
        
        return {
            'overall_similarity': round(float(overall_similarity) * 100, 2),
            'top_matching_terms': top_terms
        }
    
    def _get_top_matching_terms(self, tfidf_matrix, n: int = 10) -> list:
        """Extract top matching terms between resume and JD"""
        try:
            # Get feature names
            feature_names = self.vectorizer.get_feature_names_out()
            
            # Get TF-IDF scores for both documents
            resume_scores = tfidf_matrix[0].toarray()[0]
            jd_scores = tfidf_matrix[1].toarray()[0]
            
            # Calculate term importance (product of both scores)
            term_importance = resume_scores * jd_scores
            
            # Get top N terms
            top_indices = term_importance.argsort()[-n:][::-1]
            top_terms = [feature_names[i] for i in top_indices if term_importance[i] > 0]
            
            return top_terms[:n]
        
        except Exception as e:
            print(f"⚠ Error extracting top terms: {e}")
            return []
    
    def get_keyword_overlap(self, resume_text: str, jd_text: str) -> Dict:
        """Calculate keyword overlap between resume and JD"""
        resume_words = set(self.text_cleaner.clean_text(resume_text).split())
        jd_words = set(self.text_cleaner.clean_text(jd_text).split())
        
        # Remove stopwords
        resume_words = {w for w in resume_words if w not in self.text_cleaner.stopwords}
        jd_words = {w for w in jd_words if w not in self.text_cleaner.stopwords}
        
        overlap = resume_words.intersection(jd_words)
        
        overlap_percentage = len(overlap) / len(jd_words) * 100 if jd_words else 0
        
        return {
            'overlap_count': len(overlap),
            'overlap_percentage': round(overlap_percentage, 2),
            'common_keywords': list(overlap)[:20]
        }


# Test
if __name__ == "__main__":
    from src.preprocessing.pdf_parser import PDFParser
    
    parser = PDFParser()
    matcher = SemanticMatcher()
    
    resume_path = Path(__file__).parent.parent.parent / "data" / "raw" / "sample_resume.txt"
    jd_path = Path(__file__).parent.parent.parent / "data" / "raw" / "sample_job_description.txt"
    
    if resume_path.exists() and jd_path.exists():
        resume_text = parser.parse(resume_path)
        jd_text = parser.parse(jd_path)
        
        similarity = matcher.calculate_similarity(resume_text, jd_text)
        overlap = matcher.get_keyword_overlap(resume_text, jd_text)
        
        print("✓ Semantic Matching Results:")
        print(f"  Overall similarity: {similarity['overall_similarity']}%")
        print(f"  Keyword overlap: {overlap['overlap_percentage']}%")
        print(f"  Top matching terms: {', '.join(similarity['top_matching_terms'][:5])}")
    else:
        print("⚠ Test files not found")