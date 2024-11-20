import re
from nltk.corpus import stopwords

def normalize_text(content):
    """
    Normalize the article content.
    
    content: Text content of the article.
    Returns: Cleaned and normalized text.
    """
    stop_words = set(stopwords.words("english"))

    # Lowercase the text
    content = content.lower()

    # Remove special characters and numbers
    content = re.sub(r"[^a-z\s]", "", content)

    # Remove stopwords
    content = " ".join(word for word in content.split() if word not in stop_words)

    return content


