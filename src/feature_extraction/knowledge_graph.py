"""
Knowledge Graph Engine - KILLER FEATURE #2
Builds and analyzes skill relationship graphs to show transferable skills and learning paths
"""

import networkx as nx
from typing import Dict, List, Set, Tuple
import json


class SkillKnowledgeGraph:
    """
    Builds a knowledge graph of skills showing:
    - Prerequisites (you need X before learning Y)
    - Adjacencies (X and Y are similar)
    - Transferability (knowing X gives you Z% readiness for Y)
    
    This is what makes the system INTELLIGENT, not just keyword matching
    """
    
    def __init__(self):
        self.graph = nx.DiGraph()  # Directed graph for prerequisites
        self.similarity_graph = nx.Graph()  # Undirected for similarities
        
        # Build the knowledge base
        self._initialize_skill_relationships()
    
    def _initialize_skill_relationships(self):
        """
        Initialize skill relationships
        This is the KNOWLEDGE BASE that ChatGPT doesn't have
        """
        
        # PREREQUISITE RELATIONSHIPS (A → B means "A is prerequisite for B")
        prerequisites = {
            # Programming fundamentals
            ('Python Basics', 'Machine Learning'): 0.9,
            ('Python Basics', 'Deep Learning'): 0.9,
            ('Python Basics', 'NLP'): 0.8,
            ('Python Basics', 'Data Science'): 0.9,
            
            # Math prerequisites
            ('Linear Algebra', 'Machine Learning'): 0.7,
            ('Statistics', 'Machine Learning'): 0.8,
            ('Calculus', 'Deep Learning'): 0.6,
            ('Probability', 'Machine Learning'): 0.7,
            
            # ML progression
            ('Machine Learning', 'Deep Learning'): 0.8,
            ('Machine Learning', 'NLP'): 0.7,
            ('Machine Learning', 'Computer Vision'): 0.7,
            ('Deep Learning', 'Transformers'): 0.9,
            ('Deep Learning', 'GANs'): 0.8,
            ('NLP', 'Transformers'): 0.8,
            
            # Tools progression
            ('Python Basics', 'NumPy'): 0.9,
            ('NumPy', 'Pandas'): 0.8,
            ('Pandas', 'scikit-learn'): 0.7,
            ('scikit-learn', 'TensorFlow'): 0.6,
            ('scikit-learn', 'PyTorch'): 0.6,
            
            # Web/API
            ('Python Basics', 'Flask'): 0.7,
            ('Python Basics', 'FastAPI'): 0.7,
            ('Flask', 'REST API'): 0.8,
            ('FastAPI', 'REST API'): 0.8,
            
            # DevOps
            ('Linux', 'Docker'): 0.8,
            ('Docker', 'Kubernetes'): 0.9,
            ('Docker', 'CI/CD'): 0.7,
            
            # Cloud
            ('Python Basics', 'AWS'): 0.5,
            ('Docker', 'AWS'): 0.7,
            ('Docker', 'GCP'): 0.7,
        }
        
        for (skill_a, skill_b), strength in prerequisites.items():
            self.graph.add_edge(skill_a, skill_b, 
                              relationship='prerequisite',
                              strength=strength)
        
        # SIMILARITY RELATIONSHIPS (skills that are similar/transferable)
        similarities = {
            # Similar frameworks
            ('TensorFlow', 'PyTorch'): 0.85,
            ('TensorFlow', 'Keras'): 0.90,
            ('Flask', 'FastAPI'): 0.80,
            ('Flask', 'Django'): 0.75,
            
            # Similar concepts
            ('Machine Learning', 'Deep Learning'): 0.70,
            ('NLP', 'Computer Vision'): 0.60,
            ('Supervised Learning', 'Unsupervised Learning'): 0.65,
            
            # Similar tools
            ('NumPy', 'Pandas'): 0.75,
            ('scikit-learn', 'XGBoost'): 0.70,
            ('spaCy', 'NLTK'): 0.80,
            
            # Cloud platforms
            ('AWS', 'GCP'): 0.85,
            ('AWS', 'Azure'): 0.85,
            ('GCP', 'Azure'): 0.90,
            
            # DevOps
            ('Docker', 'Podman'): 0.90,
            ('Kubernetes', 'Docker Swarm'): 0.75,
            ('Jenkins', 'GitLab CI'): 0.80,
            
            # Databases
            ('MySQL', 'PostgreSQL'): 0.90,
            ('MongoDB', 'DynamoDB'): 0.75,
        }
        
        for (skill_a, skill_b), similarity in similarities.items():
            self.similarity_graph.add_edge(skill_a, skill_b, similarity=similarity)
        
        # SKILL CATEGORIES (for broader matching)
        self.skill_categories = {
            'ml_frameworks': ['TensorFlow', 'PyTorch', 'Keras', 'scikit-learn', 'XGBoost'],
            'nlp_tools': ['spaCy', 'NLTK', 'Transformers', 'BERT', 'GPT'],
            'web_frameworks': ['Flask', 'FastAPI', 'Django', 'Express'],
            'cloud_platforms': ['AWS', 'GCP', 'Azure'],
            'containers': ['Docker', 'Kubernetes', 'Podman'],
            'databases': ['MySQL', 'PostgreSQL', 'MongoDB', 'Redis'],
        }
    
    def calculate_readiness(
        self, 
        known_skills: List[str], 
        target_skill: str
    ) -> Dict:
        """
        Calculate how ready someone is to learn a target skill
        
        Returns readiness score (0-100%) based on:
        - Direct prerequisites met
        - Similar skills known
        - Category overlap
        
        This is INTELLIGENT analysis that keyword matching can't do
        """
        
        known_skills_normalized = [self._normalize_skill(s) for s in known_skills]
        target_normalized = self._normalize_skill(target_skill)
        
        # 1. Check direct prerequisites
        prerequisites_score = self._check_prerequisites(known_skills_normalized, target_normalized)
        
        # 2. Check similar skills
        similarity_score = self._check_similarities(known_skills_normalized, target_normalized)
        
        # 3. Check category overlap
        category_score = self._check_category_overlap(known_skills_normalized, target_normalized)
        
        # Weighted combination
        readiness = (
            prerequisites_score * 0.5 +  # Prerequisites are most important
            similarity_score * 0.35 +     # Similarity helps
            category_score * 0.15         # Category gives base familiarity
        )
        
        # Determine readiness level
        if readiness >= 80:
            level = "Excellent - Ready to start immediately"
            learning_time_weeks = 1
        elif readiness >= 60:
            level = "Good - Need 1-2 prerequisite skills"
            learning_time_weeks = 2
        elif readiness >= 40:
            level = "Moderate - Need foundational skills first"
            learning_time_weeks = 4
        elif readiness >= 20:
            level = "Low - Significant learning path required"
            learning_time_weeks = 8
        else:
            level = "Very Low - Start with fundamentals"
            learning_time_weeks = 12
        
        return {
            'readiness_score': round(readiness, 1),
            'readiness_level': level,
            'estimated_learning_weeks': learning_time_weeks,
            'breakdown': {
                'prerequisites_met': round(prerequisites_score, 1),
                'similar_skills': round(similarity_score, 1),
                'category_familiarity': round(category_score, 1)
            },
            'missing_prerequisites': self._get_missing_prerequisites(known_skills_normalized, target_normalized)
        }
    
    def _normalize_skill(self, skill: str) -> str:
        """Normalize skill name for matching"""
        # Remove common variations
        normalized = skill.lower().strip()
        
        # Map common variations
        mappings = {
            'ml': 'machine learning',
            'dl': 'deep learning',
            'ai': 'artificial intelligence',
            'py': 'python',
            'js': 'javascript',
            'tf': 'tensorflow',
            'k8s': 'kubernetes',
        }
        
        return mappings.get(normalized, normalized)
    
    def _check_prerequisites(self, known_skills: List[str], target: str) -> float:
        """Check if prerequisites are met"""
        if target not in self.graph:
            return 50.0  # Default if skill not in graph
        
        # Get all prerequisites for target
        try:
            predecessors = list(self.graph.predecessors(target))
        except:
            return 50.0
        
        if not predecessors:
            return 50.0  # No prerequisites defined
        
        # Check how many prerequisites are met
        met_prerequisites = []
        for prereq in predecessors:
            if any(prereq.lower() in known.lower() or known.lower() in prereq.lower() 
                   for known in known_skills):
                met_prerequisites.append(prereq)
        
        if not predecessors:
            return 50.0
        
        score = (len(met_prerequisites) / len(predecessors)) * 100
        return min(score, 100.0)
    
    def _check_similarities(self, known_skills: List[str], target: str) -> float:
        """Check for similar skills"""
        if target not in self.similarity_graph:
            return 30.0
        
        # Get neighbors (similar skills)
        try:
            neighbors = list(self.similarity_graph.neighbors(target))
        except:
            return 30.0
        
        if not neighbors:
            return 30.0
        
        max_similarity = 0.0
        for neighbor in neighbors:
            if any(neighbor.lower() in known.lower() or known.lower() in neighbor.lower()
                   for known in known_skills):
                similarity = self.similarity_graph[target][neighbor]['similarity']
                max_similarity = max(max_similarity, similarity)
        
        return max_similarity * 100
    
    def _check_category_overlap(self, known_skills: List[str], target: str) -> float:
        """Check if target is in same category as known skills"""
        target_lower = target.lower()
        
        # Find target's category
        target_category = None
        for category, skills in self.skill_categories.items():
            if any(target_lower in s.lower() or s.lower() in target_lower for s in skills):
                target_category = category
                break
        
        if not target_category:
            return 20.0
        
        # Check if any known skills are in same category
        category_skills = self.skill_categories[target_category]
        for known in known_skills:
            if any(known.lower() in s.lower() or s.lower() in known.lower() 
                   for s in category_skills):
                return 60.0
        
        return 20.0
    
    def _get_missing_prerequisites(self, known_skills: List[str], target: str) -> List[str]:
        """Get list of missing prerequisites"""
        if target not in self.graph:
            return []
        
        try:
            prerequisites = list(self.graph.predecessors(target))
        except:
            return []
        
        missing = []
        for prereq in prerequisites:
            if not any(prereq.lower() in known.lower() or known.lower() in prereq.lower()
                      for known in known_skills):
                missing.append(prereq)
        
        return missing
    
    def find_learning_path(
        self, 
        current_skills: List[str], 
        target_skill: str
    ) -> Dict:
        """
        Find optimal learning path from current skills to target
        Uses graph algorithms - this is ADVANCED!
        """
        
        current_normalized = [self._normalize_skill(s) for s in current_skills]
        target_normalized = self._normalize_skill(target_skill)
        
        # Find closest current skill to target
        paths = []
        for current in current_normalized:
            if current in self.graph and target_normalized in self.graph:
                try:
                    path = nx.shortest_path(self.graph, current, target_normalized)
                    paths.append(path)
                except nx.NetworkXNoPath:
                    continue
        
        if paths:
            # Get shortest path
            shortest_path = min(paths, key=len)
            
            return {
                'path_exists': True,
                'learning_sequence': shortest_path,
                'total_steps': len(shortest_path) - 1,
                'estimated_weeks': (len(shortest_path) - 1) * 2,  # 2 weeks per skill
                'next_skill_to_learn': shortest_path[1] if len(shortest_path) > 1 else target_normalized
            }
        else:
            # No direct path - recommend prerequisites
            missing_prereqs = self._get_missing_prerequisites(current_normalized, target_normalized)
            
            return {
                'path_exists': False,
                'learning_sequence': missing_prereqs + [target_normalized],
                'total_steps': len(missing_prereqs) + 1,
                'estimated_weeks': (len(missing_prereqs) + 1) * 2,
                'next_skill_to_learn': missing_prereqs[0] if missing_prereqs else target_normalized
            }
    
    def get_transferable_skills(
        self, 
        current_skills: List[str], 
        available_opportunities: List[str]
    ) -> List[Dict]:
        """
        Given current skills, find which opportunities you're most ready for
        
        This helps candidates see: "You have Python → You're 85% ready for Data Science roles"
        """
        
        readiness_analysis = []
        
        for opportunity in available_opportunities:
            readiness = self.calculate_readiness(current_skills, opportunity)
            
            readiness_analysis.append({
                'opportunity': opportunity,
                'readiness_score': readiness['readiness_score'],
                'readiness_level': readiness['readiness_level'],
                'estimated_weeks': readiness['estimated_learning_weeks'],
                'missing_skills': readiness['missing_prerequisites']
            })
        
        # Sort by readiness
        readiness_analysis.sort(key=lambda x: x['readiness_score'], reverse=True)
        
        return readiness_analysis
    
    def export_graph_data(self) -> Dict:
        """
        Export graph data for visualization
        Returns nodes and edges in format ready for D3.js or Plotly
        """
        
        nodes = []
        edges = []
        
        # Get all unique nodes
        all_nodes = set(self.graph.nodes()) | set(self.similarity_graph.nodes())
        
        for i, node in enumerate(all_nodes):
            nodes.append({
                'id': i,
                'name': node,
                'group': self._get_node_category(node)
            })
        
        # Create node name to ID mapping
        node_to_id = {node: i for i, node in enumerate(all_nodes)}
        
        # Add prerequisite edges
        for source, target in self.graph.edges():
            edges.append({
                'source': node_to_id[source],
                'target': node_to_id[target],
                'type': 'prerequisite',
                'strength': self.graph[source][target].get('strength', 0.5)
            })
        
        # Add similarity edges
        for source, target in self.similarity_graph.edges():
            edges.append({
                'source': node_to_id[source],
                'target': node_to_id[target],
                'type': 'similar',
                'similarity': self.similarity_graph[source][target].get('similarity', 0.5)
            })
        
        return {
            'nodes': nodes,
            'edges': edges
        }
    
    def _get_node_category(self, skill: str) -> int:
        """Get category ID for a skill (for visualization coloring)"""
        skill_lower = skill.lower()
        
        if any(x in skill_lower for x in ['python', 'java', 'javascript', 'programming']):
            return 1  # Programming
        elif any(x in skill_lower for x in ['machine learning', 'deep learning', 'ai', 'ml', 'dl']):
            return 2  # AI/ML
        elif any(x in skill_lower for x in ['nlp', 'computer vision', 'transformers']):
            return 3  # ML Applications
        elif any(x in skill_lower for x in ['tensorflow', 'pytorch', 'keras', 'scikit']):
            return 4  # ML Tools
        elif any(x in skill_lower for x in ['docker', 'kubernetes', 'aws', 'gcp', 'cloud']):
            return 5  # DevOps/Cloud
        elif any(x in skill_lower for x in ['flask', 'fastapi', 'django', 'api']):
            return 6  # Web/API
        elif any(x in skill_lower for x in ['math', 'statistics', 'linear', 'calculus']):
            return 7  # Math
        else:
            return 0  # Other