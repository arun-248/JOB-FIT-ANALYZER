import nltk
import spacy

# Download NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except:
    pass

# Download spaCy model
try:
    spacy.cli.download("en_core_web_sm")
except:
    pass