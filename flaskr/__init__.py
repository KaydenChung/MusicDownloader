# Library Imports
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
import os
import requests
import json
import yt_dlp

# Creating Flask App
app = Flask(__name__)

# Get Keys from Environment Variables
load_dotenv()
API_KEY = os.getenv('API_KEY')  

# Function to Search Videos
def searchVideo(search):

    query = search.replace(" ","%")
    url = f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&q={query}&key={API_KEY}&maxResults=5"
    
    response = requests.get(url)
    results = response.json()

    if 'items' not in results:
        return None
    
    videoID = results['items'][0]['id']['videoId']
    videoTitle = results['items'][0]['snippet']['title']
    videoURL = f"https://www.youtube.com/watch?v={videoID}"
    
    return {'title': videoTitle, 'url': videoURL}

# Function to Download Audio
def downloadAudio(videoURL):

    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': '/opt/homebrew/bin/',
        'keepvideo': False,
        'outtmpl': 'downloads/%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info_dict = ydl.extract_info(videoURL, download=True)
        filename = ydl.prepare_filename(info_dict).replace('.webm', '.mp3').replace('.m4a', '.mp3')
    
    return filename

# Flask Route for Index Page
@app.route('/')
def index():
    return render_template('index.html')

# Search POST Request
@app.route('/search', methods=['POST'])
def search():
    query = request.form['search']
    result = searchVideo(query)
    if result:
        return jsonify({'status': 'success', 'video': result})
    else:
        return jsonify({'status': 'error', 'message': 'No video found'})

# Download POST Request
@app.route('/download', methods=['POST'])
def download():
    videoURL = request.form['url']
    try:
        filename = downloadAudio(videoURL)
        return jsonify({'status': 'success', 'file': filename})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# Main
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
