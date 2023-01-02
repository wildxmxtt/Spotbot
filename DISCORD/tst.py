import json
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth



def sendOff():
    #opens the set up file
    with open("setup.json", 'r') as info:
        data = json.load(info)
        playlist_link = (data['playlist_link']) #make a comment about how to pull playlist url

    open('spotify.json', 'w+').close() #clears old token info

    file1 = open("spotify.json", "a") #preparts file to be written to 

    file2 = open(".cache", "r+")#reads the cached file 
    rline2 = file2.readlines()
    for line in rline2:
        content = line

        file1.write(content)#writes the content into the json file
        
    file1.close()

    with open("spotify.json", 'r') as info: #reads the json file that was just written to 
        data = json.load(info)
        TOKEN = (data['access_token'])
        refresh_token = (data['refresh_token'])
        expires_at = (data['expires_at'])

    ##########################################
    #refresh the token 
    
    def refesh_the_token():
        now = int(time.time())#gets the current time 

        is_expried = expires_at - now < 60 #checks to see if the token is expired

        if(is_expried): #if token is expried, get a new token with the refresh token
            sp_oauth = SpotifyOAuth.create_spotify_oauth()
            token_info = sp_oauth.refresh_access_token(refresh_token)
            print(token_info)

    refesh_the_token() 
    ##########################################

    sp = spotipy.Spotify(auth=TOKEN) #creates object that interacts with spotify api
    
        #chop playlist link into uri format

    #replace x, with y
    #line.replace(x,y)
    fline = playlist_link.replace("https://open.spotify.com/playlist/", "")#deletes first part of the link
    PLAYLISTID = (fline.split("?si")[0]) #cuts off exess info from the link
    

    tracks = ["blankfaketrack"] #needed to have one space in the array
    file = open("uri.txt", "r") #open uri text file
    rline = file.readlines()
        
    #loops through the entire file and only adds one songs at a time to the array
    for line in rline:
        if "spotify:track:" in line:
            tracks[0] = (line.strip()) #adds to the first element over and over again
            sp.playlist_add_items(playlist_id=PLAYLISTID, items=[tracks][0]) #adds to the actual playlist
    print("Request was sent and went through!")
    
    return "Request was sent and went through!"
 


#sendOff()