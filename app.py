from flask import Flask, render_template, request, jsonify
from transformers import pipeline
import torch

app = Flask(__name__)

# Load your model (adjust based on what model you're using)
generator = pipeline('text-generation', model='gpt2')  # or your specific model

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.json['prompt']
    
    # Generate text
    result = generator(
        prompt,
        max_length=100,
        temperature=0.7,
        do_sample=True
    )
    
    return jsonify({'text': result[0]['generated_text']})

if __name__ == '__main__':
    app.run(debug=True)