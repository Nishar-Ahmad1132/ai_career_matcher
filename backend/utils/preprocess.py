import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords', quiet=True)

def clean_text(text: str) -> str:
    """Cleans and normalizes text for embedding."""
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)  # collapse whitespace
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # remove special chars
    stop_words = set(stopwords.words('english'))
    text = ' '.join([w for w in text.split() if w not in stop_words])
    return text
