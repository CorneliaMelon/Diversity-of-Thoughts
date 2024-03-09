import openai


openai.api_key = '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'

def is_semantically_similar_gpt4(text1, text2):
    completion = openai.ChatCompletion.create(
           model="gpt-4",
           messages=[
                  {"role": "system", "content": "You are a helpful Assistant. Your task is to check whether two texts are semantically equal. You are only allowed to answer with 'Yes' or 'No'. "},
                  {"role": "user", "content": f"Are the following two texts semantically equal?\n\nText 1: {text1}\n\nText 2: {text2}\n\nAnswer with 'Yes' or 'No'."}
                  ]
                  )
    
    response = completion.choices[0].message['content']
    return 1 if response.lower() == 'yes' else 0

# Test
text1 = "Solve the equation 2x + 3 = 15."
text2 = "Find the value of x in 2x + 3 = 15."
result = is_semantically_similar_gpt4(text1, text2)
print(f"Semantic Similarity: {result}") 
