from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments

import openai

def fine_tune_gpt_generator(train_data):
    """Fine-tune GPT model to generate responses based on context."""
    model = GPT2LMHeadModel.from_pretrained("gpt2")

    training_args = TrainingArguments(
        output_dir="./gpt_results",
        per_device_train_batch_size=4,
        num_train_epochs=3,
        logging_dir="./gpt_logs",
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_data,
    )

    trainer.train()
    return model


# Initialize OpenAI API with your API key
openai.api_key = 'your_openai_api_key'

def generate_gpt3_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",  # Specify GPT-3 model
        prompt=prompt,
        max_tokens=50,
        temperature=0.7,
        top_p=0.9
    )
    return response.choices[0].text.strip()


def generate_response(query, context, model, tokenizer):
    # prompt = f"{context} {query}"
    # return generate_gpt3_response(prompt)
    # Limit context length to focus on the most relevant information
    input_text = f"{context} {query}"[:300]  # Limit the combined length of context and query
    inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)
    
    response_ids = model.generate(
        inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_length=100,
        do_sample=True,
        temperature=0.6,
        top_p=0.9,
        repetition_penalty=1.2,  # Reduces the likelihood of repetitive text
        pad_token_id=tokenizer.pad_token_id,
        eos_token_id=tokenizer.eos_token_id
    )
    
    # Decode and return the response
    response = tokenizer.decode(response_ids[0], skip_special_tokens=True)
    
    # Filter and refine the response
    response = refine_response(response)
    return response

# Helper function to refine the response
def refine_response(response):
    # Remove repeated phrases or cut off text after an incoherent sentence if needed
    response = response.split(" If ")[0]  # Example refinement to cut off irrelevant parts
    return response.strip()