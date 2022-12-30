from flask import Flask, request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import DISCORD.Discord_main as dm #aiaised as dm

app = Flask(__name__)


#random string to sign the session 
app.secret_key = "Sidhsfweiuofi8e983284bsCSCzkmlabs278a"
app.config['SESSION_COOKIE_NAME'] = 'Matts_Cookie'
#token_info = ""
TOKEN_INFO = "token_info"


#a session is where we store data about a users session, prevents reloggin in
#setting up endpoints
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


#this will add to a users playlist
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
    tracks = ["spotify:track:2id8E4WvczfKHB4LHI7Np3"]
    PLAYLISTID = "7tOjWDfeKSWc3cV19aTX1m"
    sp.playlist_add_items(playlist_id=PLAYLISTID, items=[tracks][0])
    print("SPOTIFY REQUEST WENT THROUGH!!!! " + tracks[0] + " Was added")

    #Returning the lenght of a playlist to avoid an error
    


###

#This code works go to 14:00 on this yt video https://www.youtube.com/watch?v=1TYyX8soQ8M&list=PLhYNDxVvF4oXa9ihs8WCzEriZsCF3Pp7A&index=3
#Code is from here ^^

###

    all_songs = []
    count = 0
    while True:
        items = sp.playlist_items(playlist_id=PLAYLISTID, limit=50, offset=count * 50)['items']
        count += 1
        all_songs += items
        if(len(items) < 50):
            break
    print("This track:" + tracks[0] + " is now the " + str(len(all_songs)) + " Song in the playlist")
    return str(len(all_songs))
    #return str(sp.current_user_saved_tracks(limit=50, offset=0)['items'][0])#this returns the first saved track

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


def create_spotify_oauth():
    return SpotifyOAuth(
    client_id = 'a08383e569fd4d9d9f06812485b72a86',
    client_secret = '63008b05ef5949d8b23c151e4c0e0a82',
    redirect_uri = url_for('redirectPage', _external=True), # Auto gernates this in the url_for http://localhost:5000/callback
    scope = 'playlist-modify-public user-library-read' )