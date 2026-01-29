"""
Advanced Recommendation Engine - Makes Job Fit Analyzer ENTERPRISE-LEVEL
This should go in: src/models/recommendation_engine.py
"""

from typing import Dict, List
import re


class RecommendationEngine:
    """Generates actionable recommendations for candidates"""
    
    def __init__(self):
        # Industry benchmarks
        self.benchmarks = {
            'entry': {'avg_score': 65, 'top_10': 85, 'top_25': 75},
            'junior': {'avg_score': 70, 'top_10': 88, 'top_25': 80},
            'mid': {'avg_score': 75, 'top_10': 90, 'top_25': 83},
            'senior': {'avg_score': 80, 'top_10': 93, 'top_25': 87}
        }
    
    def generate_comprehensive_recommendations(
        self,
        overall_score: float,
        component_scores: Dict,
        skill_analysis: Dict,
        experience_analysis: Dict,
        jd_text: str,
        resume_text: str,
        required_experience: Dict
    ) -> Dict:
        """Generate all recommendation categories - MAIN METHOD"""
        
        level = required_experience.get('required_level', 'entry')
        
        # Get missing skills list
        missing_skills = skill_analysis.get('missing_skills', [])
        
        return {
            'keyword_suggestions': self._generate_keywords(jd_text, resume_text, skill_analysis),
            'job_specific': self._generate_job_specific(jd_text, required_experience, component_scores),
            'resume_rewrites': self._generate_rewrites(skill_analysis, experience_analysis, jd_text),
            'projects': self._generate_projects(missing_skills),
            'benchmark': self._generate_benchmark(overall_score, level, skill_analysis),
            'roadmap': self._generate_roadmap(component_scores, skill_analysis, overall_score, level)
        }
    
    def _generate_keywords(self, jd_text: str, resume_text: str, skill_analysis: Dict) -> Dict:
        """Generate missing keyword suggestions"""
        jd_lower = jd_text.lower()
        resume_lower = resume_text.lower()
        
        important = [
            'machine learning', 'deep learning', 'nlp', 'api development',
            'docker', 'kubernetes', 'tensorflow', 'pytorch', 'aws', 'gcp',
            'rest api', 'fastapi', 'flask', 'scikit-learn', 'pandas'
        ]
        
        missing = [kw for kw in important if kw in jd_lower and kw not in resume_lower]
        present = [kw for kw in important if kw in jd_lower and kw in resume_lower]
        
        return {
            'missing_keywords': missing[:8],
            'present_keywords': present[:8],
            'recommendations': [f"Add '{kw}' in Summary or Skills section" for kw in missing[:5]]
        }
    
    def _generate_job_specific(self, jd_text: str, required_exp: Dict, scores: Dict) -> Dict:
        """Job-specific recommendations"""
        jd_lower = jd_text.lower()
        is_fresher = required_exp.get('is_fresher_role', False)
        
        actions = []
        
        if is_fresher:
            actions.append("Emphasize 3-4 strong academic projects with live demos")
            actions.append("Highlight hands-on learning and technical skills")
            actions.append("Add GitHub links to all projects")
        
        if 'deployment' in jd_lower or 'production' in jd_lower:
            actions.append("Add projects with Docker deployment and live APIs")
        
        if 'nlp' in jd_lower:
            actions.append("Build NLP projects: Text Classification or Sentiment Analysis")
        
        # Get skill_match from component_scores
        skill_score = 0
        for key, value in scores.items():
            if 'skill' in key.lower():
                skill_score = value
                break
        
        if skill_score < 70:
            actions.append("URGENT: Learn top 3 missing skills within 2-4 weeks")
        
        return {
            'is_fresher_role': is_fresher,
            'priority_actions': actions,
            'match_assessment': self._assess_match(skill_score, is_fresher)
        }
    
    def _assess_match(self, skill_score: float, is_fresher: bool) -> str:
        """Assess job match quality"""
        if is_fresher and skill_score >= 80:
            return "EXCELLENT FIT - Strong candidate, apply with confidence!"
        elif skill_score >= 75:
            return "GOOD FIT - You meet most requirements"
        else:
            return "MODERATE FIT - Build 1-2 more relevant projects"
    
    def _generate_rewrites(self, skills: Dict, exp: Dict, jd_text: str) -> Dict:
        """Resume rewrite suggestions"""
        is_fresher = exp.get('total_years', 0) < 1
        matched = skills.get('matched_skills', [])
        top_skills = ', '.join(matched[:4]) if matched else 'Python, Machine Learning, NLP'
        total_skills = skills.get('total_skills_found', 10)
        
        if is_fresher:
            summary = f"Results-driven Entry AI/ML professional with foundation in Machine Learning and NLP. Experience with {top_skills}. Built {total_skills}+ technical projects demonstrating hands-on expertise. Passionate about applying AI to solve real-world problems."
        else:
            years = exp.get('total_years', 3)
            level = exp.get('seniority_level', 'mid').title()
            summary = f"{level}-level AI/ML Engineer with {years}+ years in ML systems. Expert in {top_skills}. Proven track record in building production-grade ML applications across various domains."
        
        return {
            'summary_rewrite': summary,
            'quick_tips': [
                'Add exact job title from JD to your summary',
                'Lead with 3 most relevant skills from JD',
                'Include metrics: "94% accuracy", "1000+ users", "20% improvement"',
                'Use active verbs: Developed → Engineered, Built → Architected',
                'Add "Technologies:" tag at end of each project description'
            ]
        }
    
    def _generate_projects(self, missing_skills: List) -> Dict:
        """Project recommendations"""
        projects = []
        
        # Convert missing_skills to list of skill dicts if not already
        if not missing_skills:
            missing_skills = []
        
        # Check for NLP gaps
        nlp_found = False
        for skill in missing_skills:
            skill_name = skill.get('skill', '') if isinstance(skill, dict) else str(skill)
            if 'nlp' in skill_name.lower() or 'spacy' in skill_name.lower() or 'nltk' in skill_name.lower():
                nlp_found = True
                break
        
        if nlp_found:
            projects.append({
                'name': 'Text Similarity & Document Clustering System',
                'skills': ['spaCy', 'NLTK', 'TF-IDF', 'Scikit-learn'],
                'time': '2-3 weeks',
                'difficulty': 'Intermediate'
            })
        
        # Check for deployment gaps
        deploy_found = False
        for skill in missing_skills:
            skill_name = skill.get('skill', '') if isinstance(skill, dict) else str(skill)
            if 'docker' in skill_name.lower() or 'api' in skill_name.lower() or 'fastapi' in skill_name.lower():
                deploy_found = True
                break
        
        if deploy_found:
            projects.append({
                'name': 'ML Model API with FastAPI & Docker',
                'skills': ['FastAPI', 'Docker', 'Model Deployment', 'REST API'],
                'time': '1-2 weeks',
                'difficulty': 'Intermediate'
            })
        
        # Always add a general ML project
        projects.append({
            'name': 'End-to-End ML Pipeline with Deployment',
            'skills': ['Scikit-learn', 'Pandas', 'Streamlit', 'GitHub'],
            'time': '2 weeks',
            'difficulty': 'Beginner-Intermediate'
        })
        
        return {
            'recommended_projects': projects[:3],
            'quick_wins': [
                {'name': 'Interactive Data Dashboard with Streamlit', 'time': '3-5 days'},
                {'name': 'REST API with FastAPI', 'time': '5-7 days'},
                {'name': 'GitHub Portfolio Cleanup', 'time': '1-2 days'}
            ]
        }
    
    def _generate_benchmark(self, score: float, level: str, skills: Dict) -> Dict:
        """Benchmark comparison"""
        benchmark = self.benchmarks.get(level, self.benchmarks['entry'])
        
        if score >= benchmark['top_10']:
            percentile = 90
            summary = "EXCEPTIONAL - Top 10% of candidates!"
        elif score >= benchmark['top_25']:
            percentile = 75
            summary = "STRONG - Top 25% of candidates"
        elif score >= benchmark['avg_score']:
            percentile = 50
            summary = "ABOVE AVERAGE - Better than half of candidates"
        else:
            percentile = 30
            summary = "BELOW AVERAGE - Improvements needed"
        
        return {
            'your_score': round(score, 1),
            'average_score': benchmark['avg_score'],
            'top_25_score': benchmark['top_25'],
            'percentile': percentile,
            'summary': summary,
            'insights': self._generate_insights(score, percentile, skills)
        }
    
    def _generate_insights(self, score: float, percentile: int, skills: Dict) -> List[str]:
        """Competitive insights"""
        insights = []
        
        if percentile >= 75:
            insights.append("You're highly competitive! Apply with confidence")
            insights.append("Your profile is stronger than 75% of candidates")
        elif percentile >= 50:
            insights.append("You're competitive. A strong cover letter is recommended")
            insights.append("Consider adding 1-2 more relevant projects")
        else:
            insights.append("Build 1-2 more targeted projects to become competitive")
            insights.append("Focus on acquiring the top 3 missing skills")
        
        match_pct = skills.get('match_percentage', 0)
        if match_pct < 70:
            insights.append(f"Your skill match is {match_pct}% - aim for 75%+ for better chances")
        
        return insights
    
    def _generate_roadmap(self, scores: Dict, skills: Dict, current: float, level: str) -> Dict:
        """Improvement roadmap"""
        benchmark = self.benchmarks.get(level, self.benchmarks['entry'])
        target = benchmark['top_25']
        gap = max(0, target - current)
        
        return {
            'current_score': round(current, 1),
            'target_score': target,
            'score_gap': round(gap, 1),
            'phase_1': {
                'title': 'Week 1-2: Quick Wins',
                'actions': [
                    'Update resume with missing keywords from job description',
                    'Rewrite professional summary to match role',
                    'Add quantifiable metrics to all projects (accuracy, users, impact)',
                    'Reorganize skills section by relevance to this role'
                ],
                'impact': '+5-10 points'
            },
            'phase_2': {
                'title': 'Week 3-6: Skill Building',
                'actions': [
                    'Learn top 3 missing critical skills',
                    'Build 1 comprehensive project showcasing new skills',
                    'Deploy project with live demo and API',
                    'Write a technical blog post explaining your project'
                ],
                'impact': '+10-15 points'
            },
            'phase_3': {
                'title': 'Week 7-12: Portfolio Expansion',
                'actions': [
                    'Build 2-3 additional domain-specific projects',
                    'Contribute to 1-2 open-source ML projects',
                    'Complete a relevant certification (AWS, Google Cloud, etc.)',
                    'Network with ML professionals on LinkedIn/Twitter'
                ],
                'impact': '+15-20 points'
            }
        }