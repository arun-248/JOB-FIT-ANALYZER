"""
Configuration file for Job Fit Analyzer
Contains all settings, paths, and hyperparameters
"""

from pathlib import Path
import re

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
SRC_DIR = BASE_DIR / "src"

# Data paths
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SKILL_TAXONOMY_PATH = DATA_DIR / "skill_taxonomy.json"
SKILL_RELATIONSHIPS_PATH = DATA_DIR / "skill_relationships.csv"

# Model paths  
SKILL_GAP_MODEL_PATH = MODELS_DIR / "skill_gap_classifier_v1.pkl"
TFIDF_VECTORIZER_PATH = MODELS_DIR / "tfidf_vectorizer_v1.pkl"
MODEL_REGISTRY_PATH = MODELS_DIR / "model_registry.json"

# Ensure directories exist
for directory in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, MODELS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Model hyperparameters
SKILL_GAP_CLASSIFIER_PARAMS = {
    "n_estimators": 100,
    "max_depth": 10,
    "min_samples_split": 5,
    "random_state": 42
}

# TF-IDF parameters
TFIDF_PARAMS = {
    "max_features": 500,
    "ngram_range": (1, 2),
    "min_df": 1,
    "max_df": 0.8
}

# Scoring weights
SCORING_WEIGHTS = {
    "skill_match": 0.40,
    "experience": 0.25,
    "semantic_similarity": 0.20,
    "education": 0.10,
    "learning_potential": 0.05
}

# Match thresholds
MATCH_THRESHOLDS = {
    "strong_match": 75,
    "potential_match": 60,
    "weak_match": 45
}

# Section detection patterns
SECTION_PATTERNS = {
    "experience": re.compile(r"(experience|work history|employment|professional experience)", re.IGNORECASE),
    "education": re.compile(r"(education|academic|qualification|degree)", re.IGNORECASE),
    "skills": re.compile(r"(skills|technical skills|core competencies|expertise)", re.IGNORECASE),
    "projects": re.compile(r"(projects|portfolio|work samples)", re.IGNORECASE),
    "certifications": re.compile(r"(certifications|certificates|training)", re.IGNORECASE)
}

# Skill extraction settings
MIN_SKILL_CONFIDENCE = 0.6
SKILL_CONTEXT_WINDOW = 20

# Experience levels (in years)
EXPERIENCE_LEVELS = {
    "entry": (0, 1),
    "junior": (1, 3),
    "mid": (3, 5),
    "senior": (5, 100)
}

# Difficulty to learning days mapping
DIFFICULTY_TO_DAYS = {
    "easy": 30,
    "medium": 60,
    "hard": 120
}

print(f"✓ Config loaded successfully")