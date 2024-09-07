# Library Imports
import os
import spotipy
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from spotipy.oauth2 import SpotifyClientCredentials

# Creating Flask App
app = Flask(__name__)

# Get Keys from Environment Variables
load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

# Authentication
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

# Search Track Method
def searchTrack(name):
    results = sp.search(q=f'track:{name}', type='track', limit=1)
    tracks = results['tracks']['items']
    if tracks:
        track = tracks[0]
        return {
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'album': track['album']['name'],
            'url': track['external_urls']['spotify']
        }
    else:
        return None

# Flask App Handling
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/search', methods=['POST'])
def search():
    name = request.form['name']
    result = searchTrack(name)
    if result:
        return jsonify(result)
    else:
        return jsonify({'error': 'Track Not found'})

# Main
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
