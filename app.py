from flask import Flask, request, url_for, session, redirect, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import json
from datetime import datetime

#This code was made yt video https://www.youtube.com/watch?v=1TYyX8soQ8M&list=PLhYNDxVvF4oXa9ihs8WCzEriZsCF3Pp7A&index=3

app = Flask(__name__)

#random string to sign the session 
app.secret_key = "Sidhsfweiuofi8e983284bsCSCzkmlabs278a"
app.config['SESSION_COOKIE_NAME'] = 'Matts_Cookie'
TOKEN_INFO = "token_info"

#gets info from setup file
with open('setup.json', 'r') as setupf:
    data = json.load(setupf)
    client_id = (data['client_id'])
    client_secret = (data['client_secret'])
    PLAYLISTID = (data['playlist_link'])


@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url) 


@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth() #must make a new one everytime
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info #saving the token info in the session

    return redirect(url_for('getTracks', _external=True)) #sends us to the getTracks Page


#Returning the lenght of the given spotify playlist to avoid an error
@app.route('/getTracks')
def getTracks():
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        redirect(url_for('login', _external=False))
    #USING THE TOKEN
    sp = spotipy.Spotify(auth=token_info['access_token'])
    #playlist_id, items
    #URI PASSED IN HERE
    count = 0
    all_songs = []
    count = 0
    while True:
        items = sp.playlist_items(playlist_id=PLAYLISTID, limit=50, offset=count * 50)['items']
        count += 1
        all_songs += items
        if(len(items) < 50):
            break
    spotifyRQ1  = str(len(all_songs))
    print( "The amount of songs in the playlist are: " + spotifyRQ1)
    print("TIMESTAMP:" + str(datetime.now()))
    print("SPOTIFY REQUEST WENT THROUGH!!!! ")
    return spotifyRQ1

#this function will get us a new token if ours expires 
#also ensures that there is token data & if there is not it will
#redirect the user back to the login page
def get_token():
    token_info = session.get(TOKEN_INFO, None) #gets the value
    if not token_info:
        raise "execpetion"
    now = int(time.time())

    is_expried = token_info['expires_at'] - now < 60

    if(is_expried):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        
    return token_info


#creates oatuh object
def create_spotify_oauth():
    return SpotifyOAuth(
    client_id,
    client_secret,
    redirect_uri = url_for('redirectPage', _external=True), # Auto gernates this in the url_for http://localhost:5000/callback
    scope = 'playlist-modify-public user-library-read' )    