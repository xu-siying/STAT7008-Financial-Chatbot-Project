from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer
from nltk.tokenize import sent_tokenize, word_tokenize


class NLTKTokenizer:
    def __init__(self, language="english"):
        self.language = language

    def to_sentences(self, text):
        """Tokenize text into sentences."""
        return sent_tokenize(text)

    def to_words(self, text):
        """Tokenize text into words."""
        return word_tokenize(text)


def summarize_content(content, num_sentences=2):
    """
    Summarize the given content into a specified number of sentences.
    """
    # Use the custom NLTK-based tokenizer
    parser = PlaintextParser.from_string(content, NLTKTokenizer())
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return " ".join(str(sentence) for sentence in summary)

