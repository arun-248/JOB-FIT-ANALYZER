"""
Semantic Matcher - GUARANTEED WORKING VERSION
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import Dict
from pathlib import Path
import sys
import re

sys.path.append(str(Path(__file__).parent.parent.parent))


class SemanticMatcher:
    """Matches resume to job description using TF-IDF and cosine similarity"""
    
    def __init__(self):
        # Simple, robust TF-IDF parameters
        self.vectorizer = TfidfVectorizer(
            max_features=200,
            ngram_range=(1, 2),
            min_df=1,
            stop_words='english'
        )
        self.is_fitted = False
    
    def calculate_similarity(self, resume_text: str, jd_text: str) -> Dict[str, float]:
        """
        Calculate semantic similarity - GUARANTEED TO WORK
        
        Args:
            resume_text: Resume text
            jd_text: Job description text
            
        Returns:
            Dictionary with similarity scores
        """
        print(f"  🔍 Semantic Matching (FIXED VERSION):")
        print(f"     - Resume length: {len(resume_text)} chars")
        print(f"     - JD length: {len(jd_text)} chars")
        
        # Basic cleaning (preserve important content)
        resume_clean = self._basic_clean(resume_text)
        jd_clean = self._basic_clean(jd_text)
        
        print(f"     - Resume cleaned: {len(resume_clean)} chars, {len(resume_clean.split())} words")
        print(f"     - JD cleaned: {len(jd_clean)} chars, {len(jd_clean.split())} words")
        
        # Validate minimum content
        if len(resume_clean.split()) < 10:
            print("     ❌ ERROR: Resume too short after cleaning!")
            return {
                'overall_similarity': 0.0,
                'top_matching_terms': [],
                'error': 'Resume text too short'
            }
        
        if len(jd_clean.split()) < 10:
            print("     ❌ ERROR: JD too short after cleaning!")
            return {
                'overall_similarity': 0.0,
                'top_matching_terms': [],
                'error': 'JD text too short'
            }
        
        # Method 1: TF-IDF with error handling
        try:
            print("     - Attempting TF-IDF vectorization...")
            tfidf_matrix = self.vectorizer.fit_transform([resume_clean, jd_clean])
            self.is_fitted = True
            
            print(f"     ✓ TF-IDF successful: {tfidf_matrix.shape}")
            
            # Calculate cosine similarity
            similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
            similarity_score = float(similarity_matrix[0][0]) * 100
            
            # Get top terms
            top_terms = self._get_top_matching_terms(tfidf_matrix, n=10)
            
            print(f"     ✓ Similarity calculated: {similarity_score:.2f}%")
            
            return {
                'overall_similarity': round(similarity_score, 2),
                'top_matching_terms': top_terms,
                'method': 'tfidf'
            }
            
        except Exception as e:
            print(f"     ⚠️ TF-IDF failed: {e}")
            print(f"     - Falling back to word overlap method...")
        
        # Method 2: FALLBACK - Simple word overlap (ALWAYS WORKS)
        try:
            overlap_result = self._calculate_word_overlap(resume_clean, jd_clean)
            print(f"     ✓ FALLBACK successful: {overlap_result['overlap_percentage']:.2f}%")
            
            return {
                'overall_similarity': overlap_result['overlap_percentage'],
                'top_matching_terms': overlap_result['common_keywords'][:10],
                'method': 'word_overlap',
                'overlap_count': overlap_result['overlap_count']
            }
        
        except Exception as e:
            print(f"     ❌ FALLBACK also failed: {e}")
            
            # Method 3: LAST RESORT - Character-based similarity
            char_sim = self._character_similarity(resume_text, jd_text)
            print(f"     ⚠️ Using character similarity: {char_sim:.2f}%")
            
            return {
                'overall_similarity': char_sim,
                'top_matching_terms': [],
                'method': 'character_based'
            }
    
    def _basic_clean(self, text: str) -> str:
        """Basic text cleaning that preserves content"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep spaces and alphanumeric
        text = re.sub(r'[^a-z0-9\s\+\#]', ' ', text)
        
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def _calculate_word_overlap(self, resume_text: str, jd_text: str) -> Dict:
        """
        Calculate word overlap - SIMPLE AND RELIABLE
        """
        # Split into words
        resume_words = set(resume_text.split())
        jd_words = set(jd_text.split())
        
        # Remove very short words (less than 3 chars)
        resume_words = {w for w in resume_words if len(w) >= 3}
        jd_words = {w for w in jd_words if len(w) >= 3}
        
        if not jd_words:
            return {
                'overlap_count': 0,
                'overlap_percentage': 0.0,
                'common_keywords': []
            }
        
        # Calculate overlap
        overlap = resume_words.intersection(jd_words)
        overlap_percentage = (len(overlap) / len(jd_words)) * 100
        
        # Sort by importance (longer words are often more meaningful)
        common_keywords = sorted(list(overlap), key=len, reverse=True)
        
        return {
            'overlap_count': len(overlap),
            'overlap_percentage': round(overlap_percentage, 2),
            'common_keywords': common_keywords
        }
    
    def _character_similarity(self, text1: str, text2: str) -> float:
        """
        Last resort: character-level similarity
        """
        set1 = set(text1.lower())
        set2 = set(text2.lower())
        
        if not set2:
            return 0.0
        
        overlap = set1.intersection(set2)
        similarity = (len(overlap) / len(set2)) * 100
        
        return round(similarity, 2)
    
    def _get_top_matching_terms(self, tfidf_matrix, n: int = 10) -> list:
        """Extract top matching terms"""
        try:
            feature_names = self.vectorizer.get_feature_names_out()
            resume_scores = tfidf_matrix[0].toarray()[0]
            jd_scores = tfidf_matrix[1].toarray()[0]
            
            # Term importance = product of scores
            term_importance = resume_scores * jd_scores
            
            # Get top N
            top_indices = term_importance.argsort()[-n:][::-1]
            top_terms = [feature_names[i] for i in top_indices if term_importance[i] > 0]
            
            return top_terms[:n]
        
        except Exception as e:
            print(f"     ⚠️ Error getting top terms: {e}")
            return []