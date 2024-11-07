from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertModel, BertTokenizer
import torch

def cosine_similarity_matching(query_vector, knowledge_base_vectors):
    similarities = cosine_similarity(query_vector, knowledge_base_vectors)
    return similarities

def siamese_network_similarity(text1, text2):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')
    inputs1 = tokenizer(text1, return_tensors="pt")
    inputs2 = tokenizer(text2, return_tensors="pt")
    output1 = model(**inputs1)
    output2 = model(**inputs2)
    similarity = torch.cosine_similarity(output1.last_hidden_state.mean(dim=1),
                                         output2.last_hidden_state.mean(dim=1))
    return similarity
