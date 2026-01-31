"""
Skill Depth Analyzer - KILLER FEATURE #3
Analyzes HOW someone knows a skill (not just IF they know it)
This goes beyond keyword matching to understand DEPTH
"""

import re
from typing import Dict, List, Tuple
from datetime import datetime


class SkillDepthAnalyzer:
    """
    Analyzes skill depth by examining:
    1. Evidence Strength (how skill is mentioned)
    2. Context Quality (theory vs hands-on vs production)
    3. Experience Duration (how long they've used it)
    4. Proof Points (projects, metrics, specific tools)
    
    This is what separates "mentioned Python" from "3 years production Python"
    """
    
    def __init__(self):
        # Context quality indicators
        self.context_indicators = {
            'theory': [
                'learned', 'studied', 'familiar with', 'knowledge of',
                'understanding of', 'coursework', 'academic', 'theoretical'
            ],
            'hands_on': [
                'used', 'worked with', 'implemented', 'built', 'developed',
                'created', 'project', 'assignment', 'practice'
            ],
            'production': [
                'deployed', 'production', 'live', 'scaled', 'optimized',
                'maintained', 'enterprise', 'client', 'commercial', 'industry',
                'released', 'shipped', 'real-world', 'business'
            ]
        }
        
        # Experience level indicators
        self.experience_indicators = {
            'beginner': ['basic', 'learning', 'beginner', 'introductory', 'fundamental'],
            'intermediate': ['intermediate', 'working knowledge', 'practical', 'applied'],
            'advanced': ['advanced', 'expert', 'proficient', 'extensive', 'mastery'],
            'expert': ['expert', 'specialist', 'architect', 'lead', 'principal']
        }
        
        # Proof point patterns
        self.proof_patterns = {
            'metrics': r'\b(\d+(?:\.\d+)?(?:%|x|times|\s*(?:percent|users|requests|accuracy|improvement)))\b',
            'duration': r'\b(\d+(?:\.\d+)?)\s*(?:years?|yrs?|months?|mos?)\b',
            'scale': r'\b(\d+[KMB]?)\s*(?:users?|requests?|records?|rows?)\b',
            'technologies': r'(?:using|with|via)\s+([A-Z][a-zA-Z0-9\s,]+)',
        }
    
    def analyze_skill_depth(
        self, 
        skill: str, 
        full_text: str,
        context_window: str = None
    ) -> Dict:
        """
        Comprehensive depth analysis for a single skill
        
        Returns:
            {
                'skill': str,
                'evidence_strength': 0-5 stars,
                'context_quality': 'theory'|'hands_on'|'production',
                'experience_level': 'beginner'|'intermediate'|'advanced'|'expert',
                'proof_points': {...},
                'depth_score': 0-100,
                'explanation': str
            }
        """
        
        # Get context if not provided
        if context_window is None:
            context_window = self._extract_skill_context(skill, full_text, window=200)
        
        # 1. Analyze evidence strength
        evidence_strength = self._calculate_evidence_strength(skill, full_text, context_window)
        
        # 2. Determine context quality
        context_quality = self._determine_context_quality(context_window)
        
        # 3. Determine experience level
        experience_level = self._determine_experience_level(context_window)
        
        # 4. Extract proof points
        proof_points = self._extract_proof_points(context_window)
        
        # 5. Calculate overall depth score
        depth_score = self._calculate_depth_score(
            evidence_strength, 
            context_quality, 
            experience_level, 
            proof_points
        )
        
        # 6. Generate explanation
        explanation = self._generate_depth_explanation(
            skill,
            evidence_strength,
            context_quality,
            experience_level,
            proof_points
        )
        
        return {
            'skill': skill,
            'evidence_strength': evidence_strength,
            'context_quality': context_quality,
            'experience_level': experience_level,
            'proof_points': proof_points,
            'depth_score': depth_score,
            'explanation': explanation,
            'context_snippet': context_window[:150]
        }
    
    def _extract_skill_context(self, skill: str, full_text: str, window: int = 200) -> str:
        """Extract context around skill mentions"""
        text_lower = full_text.lower()
        skill_lower = skill.lower()
        
        # Find all occurrences
        contexts = []
        pos = 0
        while True:
            pos = text_lower.find(skill_lower, pos)
            if pos == -1:
                break
            
            start = max(0, pos - window)
            end = min(len(full_text), pos + len(skill) + window)
            contexts.append(full_text[start:end])
            
            pos += len(skill)
        
        # Return the longest/most detailed context
        return max(contexts, key=len) if contexts else ""
    
    def _calculate_evidence_strength(
        self, 
        skill: str, 
        full_text: str, 
        context: str
    ) -> int:
        """
        Calculate evidence strength (0-5 stars)
        Based on: frequency, context detail, specificity
        """
        
        # Count mentions
        mentions = full_text.lower().count(skill.lower())
        
        # Base score from mentions
        if mentions >= 5:
            base_score = 5
        elif mentions >= 3:
            base_score = 4
        elif mentions >= 2:
            base_score = 3
        else:
            base_score = 2
        
        # Boost for detailed context
        if len(context) > 150:
            base_score = min(5, base_score + 1)
        
        # Boost for specific details (numbers, tools, etc.)
        if re.search(r'\d+', context):
            base_score = min(5, base_score + 1)
        
        return base_score
    
    def _determine_context_quality(self, context: str) -> str:
        """
        Determine quality of experience: theory < hands_on < production
        """
        context_lower = context.lower()
        
        # Score each level
        scores = {}
        for level, indicators in self.context_indicators.items():
            score = sum(1 for indicator in indicators if indicator in context_lower)
            scores[level] = score
        
        # Return highest scoring level
        if scores['production'] > 0:
            return 'production'
        elif scores['hands_on'] > 0:
            return 'hands_on'
        elif scores['theory'] > 0:
            return 'theory'
        else:
            return 'hands_on'  # Default assumption
    
    def _determine_experience_level(self, context: str) -> str:
        """
        Determine experience level: beginner < intermediate < advanced < expert
        """
        context_lower = context.lower()
        
        # Check for explicit level indicators
        for level, indicators in self.experience_indicators.items():
            if any(indicator in context_lower for indicator in indicators):
                return level
        
        # Check for years of experience
        years_match = re.search(r'(\d+)\s*(?:years?|yrs?)', context_lower)
        if years_match:
            years = int(years_match.group(1))
            if years >= 5:
                return 'expert'
            elif years >= 3:
                return 'advanced'
            elif years >= 1:
                return 'intermediate'
            else:
                return 'beginner'
        
        return 'intermediate'  # Default
    
    def _extract_proof_points(self, context: str) -> Dict:
        """
        Extract concrete proof points:
        - Metrics (94% accuracy, 2x improvement)
        - Duration (3 years)
        - Scale (1M users)
        - Technologies (TensorFlow, AWS)
        """
        
        proof_points = {
            'metrics': [],
            'duration': [],
            'scale': [],
            'technologies': []
        }
        
        for point_type, pattern in self.proof_patterns.items():
            matches = re.findall(pattern, context, re.IGNORECASE)
            if matches:
                # Clean and deduplicate
                cleaned = list(set([m if isinstance(m, str) else m[0] for m in matches]))
                proof_points[point_type] = cleaned[:5]  # Limit to 5 per type
        
        return proof_points
    
    def _calculate_depth_score(
        self, 
        evidence_strength: int,
        context_quality: str,
        experience_level: str,
        proof_points: Dict
    ) -> int:
        """
        Calculate overall depth score (0-100)
        
        Weighted combination of:
        - Evidence strength (30%)
        - Context quality (30%)
        - Experience level (25%)
        - Proof points (15%)
        """
        
        # Evidence strength score (0-30)
        evidence_score = (evidence_strength / 5) * 30
        
        # Context quality score (0-30)
        context_scores = {'theory': 15, 'hands_on': 22, 'production': 30}
        context_score = context_scores[context_quality]
        
        # Experience level score (0-25)
        level_scores = {'beginner': 10, 'intermediate': 17, 'advanced': 22, 'expert': 25}
        level_score = level_scores[experience_level]
        
        # Proof points score (0-15)
        total_proof_points = sum(len(points) for points in proof_points.values())
        proof_score = min(total_proof_points * 3, 15)
        
        total_score = evidence_score + context_score + level_score + proof_score
        
        return round(total_score)
    
    def _generate_depth_explanation(
        self,
        skill: str,
        evidence_strength: int,
        context_quality: str,
        experience_level: str,
        proof_points: Dict
    ) -> str:
        """
        Generate human-readable explanation of depth assessment
        """
        
        # Evidence strength explanation
        strength_desc = {
            5: "Strong evidence",
            4: "Good evidence",
            3: "Moderate evidence",
            2: "Limited evidence",
            1: "Minimal evidence"
        }
        
        # Context quality explanation
        context_desc = {
            'production': "production/commercial environment",
            'hands_on': "hands-on projects/implementations",
            'theory': "theoretical/academic context"
        }
        
        # Experience level description
        level_desc = {
            'expert': "Expert-level proficiency",
            'advanced': "Advanced skills",
            'intermediate': "Intermediate working knowledge",
            'beginner': "Beginner-level familiarity"
        }
        
        explanation = f"{strength_desc.get(evidence_strength, 'Some evidence')} of {skill} usage in {context_desc[context_quality]}. "
        explanation += f"{level_desc[experience_level]}. "
        
        # Add proof points if available
        if proof_points['duration']:
            explanation += f"Experience duration: {', '.join(proof_points['duration'])}. "
        
        if proof_points['metrics']:
            explanation += f"Measurable results: {', '.join(proof_points['metrics'][:2])}. "
        
        if proof_points['technologies']:
            explanation += f"Used with: {', '.join(proof_points['technologies'][:3])}."
        
        return explanation.strip()
    
    def analyze_all_skills(
        self, 
        skills_dict: Dict[str, List[Dict]], 
        full_text: str
    ) -> Dict[str, Dict]:
        """
        Analyze depth for all extracted skills
        
        Args:
            skills_dict: {category: [{'skill': name, 'count': n, ...}, ...]}
            full_text: Full resume text
        
        Returns:
            {skill_name: depth_analysis, ...}
        """
        
        depth_analyses = {}
        
        for category, skill_list in skills_dict.items():
            for skill_data in skill_list:
                skill = skill_data['skill']
                context = skill_data.get('context', '')
                
                analysis = self.analyze_skill_depth(skill, full_text, context)
                depth_analyses[skill] = analysis
        
        return depth_analyses
    
    def get_top_skills_by_depth(
        self, 
        depth_analyses: Dict[str, Dict], 
        top_n: int = 5
    ) -> List[Dict]:
        """
        Get top N skills by depth score
        Useful for highlighting strongest skills
        """
        
        # Sort by depth score
        sorted_skills = sorted(
            depth_analyses.items(),
            key=lambda x: x[1]['depth_score'],
            reverse=True
        )
        
        return [
            {
                'skill': skill,
                'depth_score': analysis['depth_score'],
                'evidence_strength': analysis['evidence_strength'],
                'context_quality': analysis['context_quality'],
                'explanation': analysis['explanation']
            }
            for skill, analysis in sorted_skills[:top_n]
        ]
    
    def compare_skill_depth(
        self,
        candidate_depth: Dict[str, Dict],
        required_skills: List[str]
    ) -> List[Dict]:
        """
        Compare candidate's skill depth against required skills
        
        Returns list with depth match for each required skill
        """
        
        comparisons = []
        
        for required_skill in required_skills:
            # Find closest match in candidate skills
            best_match = None
            best_score = 0
            
            for candidate_skill, depth_analysis in candidate_depth.items():
                if required_skill.lower() in candidate_skill.lower() or \
                   candidate_skill.lower() in required_skill.lower():
                    if depth_analysis['depth_score'] > best_score:
                        best_match = candidate_skill
                        best_score = depth_analysis['depth_score']
            
            if best_match:
                comparisons.append({
                    'required_skill': required_skill,
                    'candidate_skill': best_match,
                    'depth_score': best_score,
                    'context_quality': candidate_depth[best_match]['context_quality'],
                    'match_quality': 'strong' if best_score >= 70 else 'moderate' if best_score >= 40 else 'weak',
                    'explanation': candidate_depth[best_match]['explanation']
                })
            else:
                comparisons.append({
                    'required_skill': required_skill,
                    'candidate_skill': None,
                    'depth_score': 0,
                    'context_quality': None,
                    'match_quality': 'missing',
                    'explanation': f'{required_skill} not found in resume'
                })
        
        return comparisons