from sklearn.feature_extraction.text import TfidfVectorizer

def extract_keywords(content, top_n=5):
    """
    Extract top N keywords from the content using TF-IDF.
    
    content: Text content of the article.
    top_n: Number of keywords to extract.
    """
    # Initialize the vectorizer
    vectorizer = TfidfVectorizer(stop_words="english", max_features=top_n)
    tfidf_matrix = vectorizer.fit_transform([content])
    keywords = vectorizer.get_feature_names_out()
    return list(keywords)


