from multiprocessing import context
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pinecone
import random
from models.dialogue_prediction import gpt_based_prediction

class Chatbot:
    def __init__(self, gpt_model_name="gpt2-large", pinecone_index=None, embedding_model_name="all-MiniLM-L6-v2"):
        # Initialize GPT-2 tokenizer and generator
        self.tokenizer = GPT2Tokenizer.from_pretrained(gpt_model_name)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.gpt_generator = GPT2LMHeadModel.from_pretrained(gpt_model_name)
        self.gpt_generator.config.pad_token_id = self.tokenizer.pad_token_id
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer(embedding_model_name)
        
        # Pinecone index for knowledge retrieval
        self.pinecone_index = pinecone_index

    def get_random_welcome_message(self):
        """Return a random welcome message."""
        welcome_messages = [
            "Hello! I'm your financial assistant. How can I help you today?",
            "Welcome! I’m here to assist with your financial queries.",
            "Hi there! Ready to answer your questions about investments, loans, and savings."
        ]
        return random.choice(welcome_messages)
    
    
    def retrieve_relevant_info(self, query):
        """
        Retrieve the most relevant information from Pinecone based on the query.
        """
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query).tolist()
    
        # Query Pinecone
        try:
            results = self.pinecone_index.query(vector=query_embedding, top_k=1, include_metadata=True)

            if "matches" in results and len(results["matches"]) > 0:
                best_match = results["matches"][0]
                # Safely retrieve metadata
                metadata = best_match.get("metadata", {})
                title = metadata.get("title", "No Title Available")
                summary = metadata.get("summary", "No summary available.")
                url = metadata.get("url", None)
            
                # Structure the context for GPT-2
                context = (
                    f"Relevant Information:\n"
                    f"Title: {title}\n"
                    f"Details: {summary}\n"
                )
                return title, context, url
            else:
                # Return consistent "no results" values
                return None, "I couldn't find relevant information in the knowledge base.", None
        except Exception as e:
            # Handle unexpected errors
            print(f"Error querying Pinecone: {e}")
            return None, "An error occurred while retrieving information.", None

    # def retrieve_relevant_info(self, query):
    #     """
    #     Retrieve the most relevant information from Pinecone based on the query.
    #     """
    #     # Generate query embedding
    #     query_embedding = self.embedding_model.encode(query).tolist()
    
    #     # Query Pinecone
    #     results = self.pinecone_index.query(vector=query_embedding, top_k=1, include_metadata=True)

    #     if "matches" in results and len(results["matches"]) > 0:
    #         best_match = results["matches"][0]
    #         metadata = best_match["metadata"]
    #         title = metadata.get("title", "No Title Available")
    #         summary = metadata.get("summary", "No summary available.")
    #         url = metadata.get("url", None)
    #         # Structure the context for GPT-2
    #         context = (
    #             f"Relevant Information:\n"
    #             f"Title: {title}\n"
    #             f"Details: {summary}\n"
    #         )
    #         return title, summary, url
    #     else:
    #         return None, "I couldn't find relevant information in the knowledge base.", None


    # def truncate_context(self, context, max_tokens=512):
    #     """
    #     Truncate the context to fit within a specified number of tokens.
    #     """
    #     tokenized_context = self.tokenizer(context, truncation=True, max_length=max_tokens, return_tensors="pt")
    #     return self.tokenizer.decode(tokenized_context["input_ids"][0], skip_special_tokens=True)

    
    def generate_response(self, query, context):
        """
        Generate a detailed response using GPT-2.
        """
        # Prepare input for GPT-2
        input_text = f"{context}\nQuestion: {query}\nAnswer:"
        inputs = self.tokenizer(input_text, return_tensors="pt", padding=True, truncation=True, max_length=1024)
    
        response_ids = self.gpt_generator.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_new_tokens=100,  # Generate up to 100 tokens
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.1
        )
    
        response = self.tokenizer.decode(response_ids[0], skip_special_tokens=True)
        return response.strip()



    def process_query(self, query, is_first_time=False):
        """
        Process a user query and generate a detailed response.
        """
        # Welcome message for first-time users
        if is_first_time:
            return self.get_random_welcome_message()

        # Retrieve relevant context from Pinecone
        title, context, url = self.retrieve_relevant_info(query)

        # Check if context is informative
        if url == None:
            return (
                f"Your question about '{query}' is interesting. Unfortunately, "
                f"I couldn't find detailed information in my knowledge base. "
                "Could you provide more specifics or try rephrasing your question?"
            )

        # Generate a response using GPT-2 with the provided context
        response = self.generate_response(query, context)
        print(response)
        if "Answer:" in response:
            response = response.split("Answer:")[-1].strip()
        # Append the URL at the end of the response
        final_response = f"{response}."
        print(final_response)
        
        if url and url != "No URL available.":
            final_response += f"\n\nFor more details,  visit: <a href=\"{url}\" target=\"_blank\">{title}</a>."
            
        # Predict possible follow-up questions
        next_questions = gpt_based_prediction(f"Question: {query}")

        # Format the next questions for the response
        if next_questions:
            formatted_questions = "\n".join(f"{q}" for q in next_questions)
            final_response += f"\n\nNext possible questions you might ask: \n{formatted_questions}"
       
    
        return final_response

