# pdf_reader.py
import pyttsx3
import PyPDF2
import docx
import os

def find_file_path(filename, search_dirs=None):
    if search_dirs is None:
        search_dirs = [
            os.path.join(os.path.expanduser("~"), "Desktop"),
            os.path.join(os.path.expanduser("~"), "Documents"),
            os.path.join(os.path.expanduser("~"), "Downloads"),
            "D:/", "C:/"
        ]

    filename_lower = filename.lower()
    for directory in search_dirs:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if filename_lower in file.lower() and (file.endswith('.pdf') or file.endswith('.docx')):
                    return os.path.join(root, file)
    return None

def read_document(filename):
    file_path = find_file_path(filename)
    if not file_path:
        return f"❌ File '{filename}' not found."

    engine = pyttsx3.init()
    text = ""

    if file_path.endswith('.pdf'):
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
    elif file_path.endswith('.docx'):
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + '\n'

    if not text.strip():
        return "⚠️ File is empty or unreadable."

    engine.say(text)
    engine.runAndWait()

    return f"✅ Finished reading: {os.path.basename(file_path)}"
