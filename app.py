import os
import sqlite3
from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)

# This ensures the database is created in the right place on Render
DB_PATH = os.path.join(os.path.dirname(__file__), 'physics.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Table for formulas
    c.execute('CREATE TABLE IF NOT EXISTS dimensions (quantity TEXT PRIMARY KEY, formula TEXT)')
    # Table for tracking what users search
    c.execute('CREATE TABLE IF NOT EXISTS search_logs (query TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_dimension')
def get_dimension():
    query = request.args.get('query', '').lower().strip()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Log the search
    c.execute('INSERT INTO search_logs (query) VALUES (?)', (query,))
    # Search for the formula
    c.execute('SELECT formula FROM dimensions WHERE quantity=?', (query,))
    result = c.fetchone()
    conn.commit()
    conn.close()
    
    if result:
        return jsonify({"success": True, "formula": result[0]})
    return jsonify({"success": False, "message": "Not found"})

@app.route('/admin')
def admin():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT query, timestamp FROM search_logs ORDER BY timestamp DESC LIMIT 20')
    logs = c.fetchall()
    c.execute('SELECT * FROM dimensions')
    data = c.fetchall()
    conn.close()
    return render_template('admin.html', logs=logs, data=data)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if file:
        lines = file.read().decode('utf-8').splitlines()
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        for line in lines:
            if ":" in line:
                q, f = line.split(":", 1)
                c.execute('INSERT OR REPLACE INTO dimensions VALUES (?, ?)', (q.strip().lower(), f.strip()))
        conn.commit()
        conn.close()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    # Render provides a PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
  
