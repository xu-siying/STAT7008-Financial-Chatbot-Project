from transformers import GPT2LMHeadModel, GPT2Tokenizer

def gpt_based_prediction(context):
    """
    Generate potential follow-up questions using GPT-2, constrained by the given context.
    """
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    model = GPT2LMHeadModel.from_pretrained('gpt2')
    
    # Structured prompt for better predictions
    prompt = (
        f"Context: {context}\n\n"
        "Based on the above context, what are 3 relevant follow-up questions the user might ask?\n"
        "1."
    )
    
    # Generate predictions
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(
        inputs,
        max_length=100,
        do_sample=True,
        temperature=0.4,
        top_p=0.9,
        repetition_penalty=1.1
    )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Extract the questions list
    follow_up_questions = response.split("\n")
    filtered_questions = [q.strip() for q in follow_up_questions if q.strip() and q[0].isdigit()]
    
    
    return filtered_questions  # Return top 3 questions
