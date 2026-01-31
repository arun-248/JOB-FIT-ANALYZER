"""
Interview Question Generator - FINAL WORKING VERSION
All bugs fixed, generates unique questions
"""

import re
from typing import List, Dict


class InterviewQuestionGenerator:
    
    def generate_questions(
        self, 
        resume_skills: Dict[str, List[Dict]], 
        experience_data: Dict,
        jd_text: str,
        resume_text: str = "",
        top_n: int = 10
    ) -> Dict[str, List[Dict]]:
        """Generate unique questions per resume"""
        
        print("\n[QUESTION GEN] === STARTING ===")
        print(f"[QUESTION GEN] Resume text: {len(resume_text)} chars")
        print(f"[QUESTION GEN] Skills categories: {list(resume_skills.keys())}")
        
        # Clean text
        cleaned_text = self._clean_resume_text(resume_text)
        
        # Extract content
        projects = self._extract_projects(cleaned_text)
        
        years = experience_data.get('total_years', 0)
        seniority = experience_data.get('seniority_level', 'entry')
        
        print(f"[QUESTION GEN] Years: {years}, Seniority: {seniority}")
        print(f"[QUESTION GEN] Projects found: {len(projects)}")
        
        all_questions = {
            'verification_questions': [],
            'depth_questions': [],
            'practical_questions': [],
            'red_flag_questions': []
        }
        
        # 1. VERIFICATION
        if projects:
            all_questions['verification_questions'] = self._questions_from_projects(projects, years)
        else:
            all_questions['verification_questions'] = self._questions_from_skills(resume_skills, years)
        
        # 2. DEPTH  
        all_questions['depth_questions'] = self._create_depth_questions(resume_skills, seniority, years)
        
        # 3. PRACTICAL
        all_questions['practical_questions'] = self._create_practical_questions(resume_skills, years)
        
        # 4. RED FLAGS
        if years < 1 and projects:
            red_flags = self._check_for_red_flags(projects, years)
            if red_flags:
                all_questions['red_flag_questions'] = red_flags
        
        print(f"[QUESTION GEN] Generated: {len(all_questions['verification_questions'])} verification, {len(all_questions['depth_questions'])} depth, {len(all_questions['practical_questions'])} practical")
        
        return all_questions
    
    def _clean_resume_text(self, text: str) -> str:
        """Clean junk"""
        if not text:
            return ""
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)
        text = re.sub(r'\b\d{10}\b', '', text)
        for char in ['§', 'ï', '¨', '©', '®', '™', '\x00']:
            text = text.replace(char, '')
        text = re.sub(r'\s+', ' ', text)
        return text
    
    def _extract_projects(self, text: str) -> List[str]:
        """Extract actual projects"""
        text_lower = text.lower()
        
        project_start = -1
        for keyword in ['projects', 'project work', 'academic projects']:
            idx = text_lower.find(keyword)
            if idx != -1:
                project_start = idx
                break
        
        if project_start == -1:
            return []
        
        project_end = len(text)
        for keyword in ['education', 'qualification', 'skills', 'certifications']:
            idx = text_lower.find(keyword, project_start + 20)
            if idx != -1 and idx < project_end:
                project_end = idx
        
        project_section = text[project_start:project_end]
        projects = []
        lines = project_section.split('\n')
        
        current_project = []
        for line in lines:
            line = line.strip()
            
            if 'project' in line.lower() and len(line) < 30:
                continue
            if re.search(r'\d{4}\s*[-–]\s*\d{4}', line):
                continue
            if any(word in line.lower() for word in ['university', 'college', 'cgpa', '%']):
                continue
            
            if re.match(r'^[\d\.\-\*•]+\s', line) and len(line) > 25:
                if current_project:
                    projects.append(' '.join(current_project))
                current_project = [line]
            elif len(line) > 10 and current_project:
                current_project.append(line)
        
        if current_project:
            projects.append(' '.join(current_project))
        
        cleaned = []
        for proj in projects:
            proj = re.sub(r'^[\d\.\-\*•]+\s*', '', proj)
            if len(proj) > 30:
                cleaned.append(proj)
        
        return cleaned[:5]
    
    def _questions_from_projects(self, projects: List[str], years: float) -> List[Dict]:
        """Questions from projects"""
        questions = []
        
        templates = [
            "Walk me through the architecture of your {name}. What were the main technical challenges?",
            "Regarding your {name} - what was the most difficult bug you encountered and how did you solve it?",
            "Explain your specific role in {name}. What components did you personally build?"
        ]
        
        for i, project in enumerate(projects[:3]):
            words = project.split()[:10]
            name = ' '.join(words)
            
            q = templates[i % len(templates)].format(name=name)
            
            questions.append({
                'question': q,
                'skill_tested': 'Project Work',
                'type': 'verification',
                'difficulty': 'medium',
                'purpose': f'Verify project: "{project[:60]}..."'
            })
        
        return questions[:3]
    
    def _questions_from_skills(self, skills: Dict, years: float) -> List[Dict]:
        """Fallback to skills"""
        questions = []
        
        all_skills = []
        for category, skill_list in skills.items():
            for skill_data in skill_list[:3]:
                all_skills.append(skill_data['skill'])
        
        for skill in all_skills[:3]:
            if years >= 3:
                q = f"With {int(years)} years, what's an advanced {skill} technique you've used?"
            elif years >= 1:
                q = f"Describe a real project where you used {skill}. What challenges did you face?"
            else:
                q = f"Walk me through your {skill} knowledge. What have you built with it?"
            
            questions.append({
                'question': q,
                'skill_tested': skill,
                'type': 'verification',
                'difficulty': 'easy' if years < 1 else 'medium',
                'purpose': f'Assess {skill} experience'
            })
        
        return questions[:3]
    
    def _create_depth_questions(self, skills: Dict, seniority: str, years: float) -> List[Dict]:
        """Depth questions"""
        questions = []
        
        if years >= 5 or seniority in ['senior', 'lead']:
            level = 'senior'
        elif years >= 2:
            level = 'mid'
        else:
            level = 'entry'
        
        # Get ALL skills from all categories
        all_skills = []
        for category, skill_list in skills.items():
            for skill_data in skill_list:
                all_skills.append(skill_data['skill'])
        
        print(f"[DEPTH Q] All skills: {all_skills[:10]}")
        
        depth_qs = {
            'python': {
                'senior': "Explain Python's GIL and when you'd use multiprocessing vs threading.",
                'mid': "What's the difference between deep copy and shallow copy?",
                'entry': "Explain list comprehensions. When are they useful?"
            },
            'machine learning': {
                'senior': "How do you handle data drift in production ML models?",
                'mid': "Explain overfitting and how to prevent it.",
                'entry': "What's the difference between classification and regression?"
            },
            'sql': {
                'senior': "Explain query execution plans and optimization strategies.",
                'mid': "What's the difference between INNER JOIN and LEFT JOIN?",
                'entry': "What are primary and foreign keys?"
            },
            'tensorflow': {
                'senior': "Explain TensorFlow's execution graph and eager execution modes.",
                'mid': "How do you prevent overfitting in TensorFlow models?",
                'entry': "What's the difference between Sequential and Functional API?"
            },
            'pytorch': {
                'senior': "Explain PyTorch's autograd and how gradients are computed.",
                'mid': "What's the difference between .detach() and .clone()?",
                'entry': "What are tensors and how do they differ from NumPy arrays?"
            },
            'docker': {
                'senior': "Explain multi-stage builds and layer caching optimization.",
                'mid': "What's the difference between CMD and ENTRYPOINT?",
                'entry': "What's the difference between containers and VMs?"
            },
            'aws': {
                'senior': "Design a highly available architecture using AWS services.",
                'mid': "What's the difference between EC2 and Lambda?",
                'entry': "What are the main AWS compute services?"
            },
            'react': {
                'senior': "Explain React's reconciliation algorithm and fiber architecture.",
                'mid': "What's the difference between useState and useReducer?",
                'entry': "What are props and state?"
            }
        }
        
        for skill in all_skills[:3]:
            skill_lower = skill.lower()
            
            question_text = None
            for key, levels in depth_qs.items():
                if key in skill_lower:
                    question_text = levels.get(level, levels.get('mid'))
                    break
            
            if not question_text:
                if level == 'senior':
                    question_text = f"What's an advanced {skill} pattern that most developers miss?"
                elif level == 'mid':
                    question_text = f"Explain a complex problem you solved using {skill}."
                else:
                    question_text = f"What are the key concepts in {skill}?"
            
            questions.append({
                'question': question_text,
                'skill_tested': skill,
                'type': 'depth',
                'difficulty': level,
                'purpose': f'Test {level}-level {skill} understanding'
            })
            
            print(f"[DEPTH Q] Q{len(questions)}: {question_text[:60]}...")
        
        return questions[:3]
    
    def _create_practical_questions(self, skills: Dict, years: float) -> List[Dict]:
        """Practical questions based on THEIR skills"""
        questions = []
        
        # Get ALL skills
        all_skills = []
        for category, skill_list in skills.items():
            for skill_data in skill_list:
                all_skills.append(skill_data['skill'])
        
        print(f"[PRACTICAL Q] All skills for practical: {all_skills[:10]}")
        
        for i, skill in enumerate(all_skills[:3]):
            skill_lower = skill.lower()
            
            if 'python' in skill_lower:
                q = f"Optimize a Python script processing 1M records taking 10 minutes. What's your approach?"
            elif 'machine learning' in skill_lower or 'ml' in skill_lower:
                q = f"Your ML model: 95% accuracy in training, 60% in production. How do you debug?"
            elif 'tensorflow' in skill_lower or 'pytorch' in skill_lower:
                q = f"Your {skill} model needs to run on edge devices with limited memory. How do you optimize?"
            elif 'sql' in skill_lower or 'database' in skill_lower:
                q = f"Optimize a {skill} query scanning 10M rows taking 30 seconds."
            elif 'docker' in skill_lower:
                q = f"A Docker container works locally but crashes in production. Debug process?"
            elif 'aws' in skill_lower or 'azure' in skill_lower or 'gcp' in skill_lower or 'cloud' in skill_lower:
                q = f"Design {skill} deployment handling 50K requests/minute. What services?"
            elif 'react' in skill_lower or 'javascript' in skill_lower:
                q = f"A {skill} app is slow as data grows. How identify performance issues?"
            elif 'flask' in skill_lower or 'fastapi' in skill_lower or 'django' in skill_lower:
                q = f"Build {skill} microservice integrating 3 APIs. How handle failures?"
            elif 'nlp' in skill_lower:
                q = f"Design NLP pipeline processing 1000 documents/second. Architecture?"
            elif 'git' in skill_lower:
                q = f"Your team of 5 uses Git. How handle merge conflicts and code reviews?"
            elif 'linux' in skill_lower:
                q = f"Production Linux server running out of memory. Diagnose and fix?"
            else:
                # Different question for each position
                variants = [
                    f"Design production system using {skill} needing 99.9% uptime.",
                    f"Integrate {skill} into microservices with 10+ services.",
                    f"Use {skill} to solve performance bottleneck in high-traffic app."
                ]
                q = variants[i % len(variants)]
            
            questions.append({
                'question': q,
                'skill_tested': skill,
                'type': 'practical',
                'difficulty': 'medium',
                'purpose': f'Test practical {skill} application'
            })
            
            print(f"[PRACTICAL Q] Q{i+1} for {skill}: {q[:60]}...")
        
        # Fallback if no skills
        if len(questions) == 0:
            questions = [
                {'question': "Design real-time data processing system. Architecture?", 'skill_tested': 'System Design', 'type': 'practical', 'difficulty': 'medium', 'purpose': 'Test design'},
                {'question': "Deploy app handling variable load. Ensure scalability?", 'skill_tested': 'Architecture', 'type': 'practical', 'difficulty': 'medium', 'purpose': 'Test scalability'},
                {'question': "Monitor and debug production system. Your process?", 'skill_tested': 'DevOps', 'type': 'practical', 'difficulty': 'medium', 'purpose': 'Test production'}
            ]
        
        return questions[:3]
    
    def _check_for_red_flags(self, projects: List[str], years: float) -> List[Dict]:
        """Check red flags"""
        flags = []
        
        if years < 1:
            advanced = ['architecture', 'scalable', 'distributed', 'microservices', 'production']
            
            for project in projects:
                if any(kw in project.lower() for kw in advanced):
                    flags.append({
                        'question': f"You mention advanced work with {years} years. Describe team size, your role, and who mentored you.",
                        'skill_tested': 'Experience',
                        'type': 'red_flag',
                        'difficulty': 'hard',
                        'purpose': 'Verify advanced claims',
                        'red_flag': 'Entry-level claiming advanced work'
                    })
                    break
        
        return flags[:2]