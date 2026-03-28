import os
import PyPDF2
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# This text file will act as the "memory" for your AI
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
        try:
            reader = PyPDF2.PdfReader(file)
            text_content = ""
            for page in reader.pages:
                text_content += page.extract_text() + "\n"
            
            # This saves the PDF text into your knowledge base
            with open(KNOWLEDGE_BASE, "a", encoding="utf-8") as f:
                f.write(text_content)
            return "PDF Memorized! You can now ask questions on the home page."
        except Exception as e:
            return f"Error processing PDF: {str(e)}"
    return "Please upload a valid PDF file."

@app.route('/get_dimension')
def get_answer():
    query = request.args.get('query', '').lower()
    if not os.path.exists(KNOWLEDGE_BASE):
        return jsonify(success=False, formula="I haven't learned anything yet. Upload a PDF in Admin.")

    with open(KNOWLEDGE_BASE, "r", encoding="utf-8") as f:
        content = f.read()

    # Search logic: find the paragraph containing your question
    # This looks for the word (like 'pressure') and takes the surrounding text
    import re
    # This finds the sentence containing your keyword
    sentences = re.split(r'(?<=[.!?]) +', content)
    relevant_sentences = [s for s in sentences if query in s.lower()]

    if relevant_sentences:
        # Show the first 2 sentences found
        answer = " ".join(relevant_sentences[:2])
        return jsonify(success=True, formula=answer)
    
    return jsonify(success=False, formula="I couldn't find information about that in my memory.")

if __name__ == "__main__":
    app.run(debug=True)
    
