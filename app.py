import os
import PyPDF2
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# This file will store all the text from your uploaded PDFs
KNOWLEDGE_BASE = "knowledge.txt"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file and file.filename.endswith('.pdf'):
        reader = PyPDF2.PdfReader(file)
        text_content = ""
        for page in reader.pages:
            text_content += page.extract_text() + "\n"
        
        # Save the "memorized" text to a file
        with open(KNOWLEDGE_BASE, "a", encoding="utf-8") as f:
            f.write(text_content)
        return "Book Memorized Successfully! You can now ask questions."
    return "Please upload a valid PDF."

@app.route('/get_dimension') # Keeping same route name for your JS
def get_answer():
    query = request.args.get('query', '').lower()
    if not os.path.exists(KNOWLEDGE_BASE):
        return jsonify(success=False, formula="No knowledge base found. Upload a PDF first.")

    with open(KNOWLEDGE_BASE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Simple logic: Find sentences that contain your keyword
    results = []
    for line in lines:
        if query in line.lower():
            results.append(line.strip())

    if results:
        # Returns the first 3 relevant lines found in the PDF
        answer = " ".join(results[:3])
        return jsonify(success=True, formula=answer)
    
    return jsonify(success=False, formula="I couldn't find that in the uploaded material.")

if __name__ == "__main__":
    app.run(debug=True)
    
if __name__ == '__main__':
    # Render provides a PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
  
