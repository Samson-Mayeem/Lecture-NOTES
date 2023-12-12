import hashlib
import os
import sqlite3
from flask import Flask, render_template, request, g, send_file

app = Flask(__name__)
app.config['DATABASE'] = 'your_database.db'
app.config['UPLOAD_FOLDER'] = 'uploads'  # Specify a folder for temporary file storage

# Function to get the database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    return db

# Function to create the database tables
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# Teardown function to close the database connection
@app.teardown_appcontext
def close_db(error):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Initialize the database tables
init_db()

# Route to handle the main page
@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT hash FROM files')
    file_hashes = [row[0] for row in cursor.fetchall()]

    # Generate download links for each file hash
    download_links = [f'/download/{file_hash}' for file_hash in file_hashes]

    return render_template('index.html', download_link=None, download_links=download_links)

# Route to handle file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    download_link = None  # Initialize download_link variable

    if file:
        filename = file.filename
        file_contents = file.read()

        # Perform your file processing and database operations here
        # For example, calculate the SHA256 hash of the file
        sha256_hash = hashlib.sha256(file_contents).hexdigest()

        # Insert into the database
        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO files (filename, content, hash) VALUES (?, ?, ?)', (filename, file_contents, sha256_hash))
        db.commit()

        # Generate a download link for the uploaded file
        download_link = f'/download/{sha256_hash}'

    # Render the template with the download_link variable
    return render_template('index.html', download_link=download_link)

# Route to handle file download
@app.route('/download/{file_hash}', methods=['GET'])
def download_file(file_hash):
    # Retrieve the file details from the database using the hash
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT filename, content FROM files WHERE hash = ?', (file_hash,))
    result = cursor.fetchone()

    if result:
        filename, file_contents = result
        # Create a temporary file or use an appropriate file path
        temp_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Save the file to the temporary path
        with open(temp_file_path, 'wb') as temp_file:
            temp_file.write(file_contents)

        # Send the file as an attachment
        return send_file(temp_file_path, attachment_filename=filename, as_attachment=True)

    return "File not found"

if __name__ == '__main__':
    app.run(debug=True)

