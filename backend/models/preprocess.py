import re
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)  # remove extra spaces/newlines
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)  # remove punctuation
    text = ' '.join([word for word in text.split() if word not in stop_words])
    return text
