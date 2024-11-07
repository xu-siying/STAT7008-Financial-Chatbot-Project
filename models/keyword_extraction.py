from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models import Word2Vec, LdaModel

def tfidf_keyword_extraction(documents):
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(documents)
    keywords = vectorizer.get_feature_names_out()
    return keywords

def word2vec_embedding(documents):
    model = Word2Vec(documents, vector_size=100, window=5, min_count=1, workers=4)
    return model

def lda_topic_modeling(documents, num_topics=5):
    lda_model = LdaModel(documents, num_topics=num_topics)
    return lda_model
