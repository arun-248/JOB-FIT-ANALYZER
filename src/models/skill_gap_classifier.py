"""
Skill Gap Classifier - Predicts learning difficulty for missing skills
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.config import (
    SKILL_RELATIONSHIPS_PATH,
    SKILL_GAP_MODEL_PATH,
    SKILL_GAP_CLASSIFIER_PARAMS,
    DIFFICULTY_TO_DAYS
)


class SkillGapClassifier:
    """Classifies learning difficulty for skill gaps"""
    
    def __init__(self):
        self.model = None
        self.label_encoder = LabelEncoder()
        self.feature_columns = ['has_base', 'skill_similarity', 'domain_overlap']
        self.is_trained = False
    
    def train(self, save_model: bool = True):
        """
        Train the skill gap classifier
        
        Args:
            save_model: Whether to save the trained model
        """
        # Load training data
        if not SKILL_RELATIONSHIPS_PATH.exists():
            raise FileNotFoundError(f"Training data not found: {SKILL_RELATIONSHIPS_PATH}")
        
        df = pd.read_csv(SKILL_RELATIONSHIPS_PATH)
        
        # Prepare features
        X = df[self.feature_columns]
        y = df['difficulty']
        
        # Encode labels
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=0.2, random_state=42
        )
        
        # Train model
        self.model = RandomForestClassifier(**SKILL_GAP_CLASSIFIER_PARAMS)
        self.model.fit(X_train, y_train)
        
        # Evaluate
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        
        print(f"✓ Model trained successfully")
        print(f"  Train accuracy: {train_score:.2%}")
        print(f"  Test accuracy: {test_score:.2%}")
        
        self.is_trained = True
        
        # Save model
        if save_model:
            self.save_model()
    
    def predict_difficulty(self, has_base: int, skill_similarity: float, 
                          domain_overlap: float) -> dict:
        """
        Predict learning difficulty for a skill gap
        
        Args:
            has_base: Whether candidate has prerequisite skill (0 or 1)
            skill_similarity: Similarity to known skills (0-1)
            domain_overlap: Domain overlap (0-1)
            
        Returns:
            Dictionary with prediction and confidence
        """
        if self.model is None:
            self.load_model()
        
        # Prepare features
        features = np.array([[has_base, skill_similarity, domain_overlap]])
        
        # Predict
        prediction_encoded = self.model.predict(features)[0]
        prediction_proba = self.model.predict_proba(features)[0]
        
        # Decode prediction
        difficulty = self.label_encoder.inverse_transform([prediction_encoded])[0]
        confidence = float(max(prediction_proba))
        
        # Get learning days
        learning_days = DIFFICULTY_TO_DAYS.get(difficulty, 60)
        
        return {
            'difficulty': difficulty,
            'confidence': round(confidence, 2),
            'estimated_learning_days': learning_days
        }
    
    def save_model(self):
        """Save trained model to disk"""
        if self.model is None:
            raise ValueError("No model to save. Train the model first.")
        
        # Ensure models directory exists
        SKILL_GAP_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        # Save model and label encoder
        model_data = {
            'model': self.model,
            'label_encoder': self.label_encoder,
            'feature_columns': self.feature_columns
        }
        
        joblib.dump(model_data, SKILL_GAP_MODEL_PATH)
        print(f"✓ Model saved to {SKILL_GAP_MODEL_PATH}")
    
    def load_model(self):
        """Load trained model from disk"""
        if not SKILL_GAP_MODEL_PATH.exists():
            print(f"⚠ Model not found. Training new model...")
            self.train()
            return
        
        model_data = joblib.load(SKILL_GAP_MODEL_PATH)
        
        self.model = model_data['model']
        self.label_encoder = model_data['label_encoder']
        self.feature_columns = model_data['feature_columns']
        self.is_trained = True
        
        print(f"✓ Model loaded from {SKILL_GAP_MODEL_PATH}")


# Test and train
if __name__ == "__main__":
    classifier = SkillGapClassifier()
    
    # Train the model
    classifier.train()
    
    # Test prediction
    print("\n✓ Testing predictions:")
    
    # Test case 1: Has prerequisite, high similarity
    result1 = classifier.predict_difficulty(1, 0.9, 0.95)
    print(f"  Case 1 (easy): {result1}")
    
    # Test case 2: No prerequisite, low similarity
    result2 = classifier.predict_difficulty(0, 0.3, 0.4)
    print(f"  Case 2 (hard): {result2}")
    
    # Test case 3: Medium case
    result3 = classifier.predict_difficulty(1, 0.6, 0.7)
    print(f"  Case 3 (medium): {result3}")