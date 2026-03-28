import os
import PyPDF2
import re
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# This file stores the raw text extracted from your physics PDFs
KNOWLEDGE_BASE = "knowledge.txt"

@app.route('/')
def home():
    """Renders the main search interface."""
    return render_template('index.html')

@app.route('/admin')
def admin():
    """Secure Admin Panel: Only accessible via /admin?pw=1234"""
    #
    password = request.args.get('pw')
    if password == "1234": # This matches your requested secret code
        return render_template('admin.html')
    else:
        return "Access Denied: You do not have permission to view this page.", 403

@app.route('/upload', methods=['POST'])
def upload_file():
    """Processes uploaded PDFs and saves text to the knowledge base."""
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    if file and file.filename.endswith('.pdf'):
        try:
            #
            reader = PyPDF2.PdfReader(file)
            text_content = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text_content += extracted + " "
            
            # Save the extracted text so the AI can "memorize" it
            with open(KNOWLEDGE_BASE, "a", encoding="utf-8") as f:
                f.write(text_content + "\n")
            return "SUCCESS: PDF content has been memorized."
        except Exception as e:
            return f"ERROR: Could not process PDF: {str(e)}"
    
    return "INVALID: Please upload a valid PDF file."

@app.route('/get_dimension')
def get_answer():
    """Searches the knowledge base for the user's physics query."""
    query = request.args.get('query', '').lower()
    
    if not os.path.exists(KNOWLEDGE_BASE):
        return jsonify(success=False, formula="I haven't learned anything yet. Upload a PDF first.")

    if not query:
        return jsonify(success=False, formula="Please enter a question.")

    with open(KNOWLEDGE_BASE, "r", encoding="utf-8") as f:
        content = f.read()

    # Search logic: Finds the sentence with the keyword and 2 sentences after it for context
    #
    pattern = rf"([^.]*?{re.escape(query)}[^.]*\.[^.]*\.[^.]*\.)"
    match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)

    if match:
        # Clean up newlines and extra spaces for a smooth typing effect
        clean_answer = ' '.join(match.group(1).split())
        return jsonify(success=True, formula=clean_answer)
    
    return jsonify(success=False, formula="I couldn't find that specific information in my memory.")

if __name__ == "__main__":
    # Render uses the 'PORT' environment variable; default to 5000 for local testing
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
