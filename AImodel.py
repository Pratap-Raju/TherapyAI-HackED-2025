import pandas as pd
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    # Call your chatbot function here
    response = therapy_ai(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# Load the CSV file into a DataFrame
df = pd.read_csv("C:/Users/kolpr/Desktop/reddit_text-davinci-002.csv")

# Remove duplicates
df = df.drop_duplicates()

# Remove rows with missing values
df = df.dropna()

# API Configuration
API_KEY = "AIzaSyB2T-tr8FGgIF976scv2dU7zUz5dTLgzXQ"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Memory to retain conversation history
conversation_history = []

# Example function to send data to Gemini
def send_to_gemini(prompt):
    response = model.generate_content(prompt)
    return response.text

# Define a system prompt
system_prompt = """
You are a compassionate and empathetic therapist. Provide supportive and non-judgmental responses to the user's concerns.
"""

# Combine system prompt with user input
def therapy_ai(user_input):
    # Add user input to conversation history
    conversation_history.append(f":User  {user_input}")
    
    # Create a full prompt with conversation history
    full_prompt = f"{system_prompt}\n" + "\n".join(conversation_history) + f"\nTherapist:"
    
    # Get the response from the model
    response = send_to_gemini(full_prompt)
    
    # Add the response to conversation history
    conversation_history.append(f"Therapist: {response}")
    
    return response

# Example: Formatting for fine-tuning
formatted_data = []
for index, row in df.iterrows():
    input_text = row["prompt"]
    output_text = row["completion"]
    formatted_data.append({"prompt": input_text, "completion": output_text})

formatted_data = [
    {"prompt": "I feel really anxious today.", "completion": "I'm sorry to hear that. Let's talk about what's causing your anxiety."},
    {"prompt": "I can't stop overthinking.", "completion": "Overthinking can be overwhelming. Try focusing on one thing at a time."},
    # Add more examples
]


# Main loop for user interaction
while True:
    user_input = input("What's your distress (type 'exit' to quit): ")
    if user_input.lower() == 'exit':
        break
    response = therapy_ai(user_input)
    print(response)

# Optionally, you can save the conversation history to a file
with open("conversation_history.txt", "w") as f:
    for line in conversation_history:
        f.write(line + "\n")