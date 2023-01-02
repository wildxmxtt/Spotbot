import json
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth



def sendOff():

    with open("setup.json", 'r') as info:
        data = json.load(info)
        PLAYLISTID = (data['playlist_link'])

    open('spotify.json', 'w+').close()

    file1 = open("spotify.json", "a")



    file2 = open(".cache", "r+")
    rline2 = file2.readlines()
    for line in rline2:
        content = line

        file1.write(content)
        
    file1.close()

    with open("spotify.json", 'r') as info:
        data = json.load(info)
        TOKEN = (data['access_token'])
        refresh_token = (data['refresh_token'])
        expires_at = (data['expires_at'])

    ##########################################
    #refresh the token 
    
    def refesh_the_token():
        now = int(time.time())

        is_expried = expires_at - now < 60

        if(is_expried):
            sp_oauth = SpotifyOAuth.create_spotify_oauth()
            token_info = sp_oauth.refresh_access_token(refresh_token)
            print(token_info)

    refesh_the_token()
    ##########################################

    sp = spotipy.Spotify(auth=TOKEN)
        #playlist_id, items
        #URI PASSED IN HERE


    tracks = ["blankfaketrack"] #needed to have one space in the array
    #PLAYLISTID = "7tOjWDfeKSWc3cV19aTX1m"
    count = 0
    file = open("uri.txt", "r") #open uri text file
    rline = file.readlines()
        
    #loops through the entire file and only adds one songs at a time to the array
    for line in rline:
        if "spotify:track:" in line:
            tracks[0] = (line.strip()) #adds to the first element over and over again
            sp.playlist_add_items(playlist_id=PLAYLISTID, items=[tracks][0])
    print("Request was sent and went through!")
    return "Request was sent and went through!"
    #res = requests.post(url=playlistUrl, headers=headers, uris=uri, playlistId=playlistId)    


sendOff()