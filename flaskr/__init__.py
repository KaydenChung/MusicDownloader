# Library Imports
import os
import yt_dlp
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

# Creating Flask App
app = Flask(__name__)

# Get Keys from Environment Variables
load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

# Function to Search Videos
def searchVideo(search):
    # Placeholder
    return [{'title': search, 'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'}]

# Function Download Video
def downloadVideo(url, filename):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': filename,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Flask App Handling
@app.route('/')
def index():
    return render_template('index.html')

# Search POST Request
@app.route('/search', methods=['POST'])
def search():
    search = request.form['search']
    results = searchVideo(search)
    return jsonify(results)

# Download POST Request
@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    filename = 'output.mp3'
    downloadVideo(url, filename)
    return jsonify({'status': 'success', 'file': filename})

# Main
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
