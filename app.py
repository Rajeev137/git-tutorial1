from flask import Flask, render_template, request, redirect, url_for, session
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from googleapiclient.discovery import build

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Spotify API credentials
SPOTIPY_CLIENT_ID = '84446d7814e9418aafdac3893a1c0d2e'
SPOTIPY_CLIENT_SECRET = 'dfd13f3f10ac473abfeb8a4f4b68d478'
SPOTIPY_REDIRECT_URI = 'https://0c61-103-167-195-87.ngrok-free.app/callback'

# YouTube API credentials
YOUTUBE_API_KEY = 'AIzaSyBO45gofMhl8vnFZeKQn60gCfC10_2XFlA'

# Create Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope="playlist-read-private"))

# Create YouTube client
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    # Redirect users to Spotify login page
    return redirect(url_for('spotify_login'))

@app.route('/spotify_login')
def spotify_login():
    # Redirect users to Spotify login URL
    auth_url = sp.auth_manager.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    # Handle Spotify callback after user login
    code = request.args.get('code')
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET,redirect_uri=SPOTIPY_REDIRECT_URI,scope="playlist-read-private"))
    token_info = sp.auth_manager.get_access_token(code)
    playlists = sp.current_user_playlists()
    return render_template('search.html', playlists=playlists)
    #return redirect(url_for('spotify_search'))

@app.route('/spotify_search')
def spotify_search():
    # Fetch user's Spotify playlists and display them in the frontend
    playlists = sp.current_user_playlists()
    return render_template('search.html', playlists=playlists)

@app.route('/youtube_search/<playlist_id>')
def youtube_search(playlist_id):
    # Search songs on YouTube for a given Spotify playlist ID
    playlist_tracks = sp.playlist_tracks(playlist_id)
    video_urls = []
    for track in playlist_tracks['items']:
        search_query = f"{track['track']['name']} {track['track']['artists'][0]['name']} official music video"
        search_response = youtube.search().list(q=search_query, part='snippet', type='video', maxResults=1).execute()
        if search_response['items']:
            video_urls.append(f"https://www.youtube.com/watch?v={search_response['items'][0]['id']['videoId']}")
    return render_template('results.html', video_urls=video_urls)




if __name__ == '__main__':
    app.run(debug=True)
