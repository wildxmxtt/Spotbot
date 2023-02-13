import json
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import base64


def sendOff():
    pgrm_signature = "playlist_update.py: "

    #opens the setup.json file
    with open("setup.json", 'r') as info:
        data = json.load(info)
        playlist_link = (data['playlist_link']) 
        client_id = (data['client_id'])
        client_secret = (data['client_secret'])
    open('spotify.json', 'w+').close() #clears old token info if there is any

    file1 = open("spotify.json", "a") #prepares file to be written to 

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

    #This function keep the user from having to get a new token manually every hour
    def refesh_the_token(): 
            #This code was made possible by https://www.youtube.com/watch?v=-FsFT6OwE1A 
            #Notable timestamps 10:14, 40:25

            auth_client = client_id + ":" + client_secret
            auth_encode = 'Basic ' + base64.b64encode(auth_client.encode()).decode()

            headers = {
                'Authorization': auth_encode,
                }

            data = {
                'grant_type' : 'refresh_token',
                'refresh_token' : refresh_token
                }

            response = requests.post('https://accounts.spotify.com/api/token', data=data, headers=headers) #sends request off to spotify

            if(response.status_code == 200): #checks if request was valid
                print(pgrm_signature + "The request to went through we got a status 200; Spotify token refreshed")
                response_json = response.json()
                new_expire = response_json['expires_in']
                print(pgrm_signature + "the time left on new token is: "+ str(new_expire / 60) + "min") #says how long
                return response_json["access_token"]
            else:
                print(pgrm_signature + "ERROR! The response we got was: "+ str(response))
                return TOKEN #last ditch to try and make it work if TOKEN varaible is still active

        
    now = int(time.time())#gets the current time 

    is_expried = expires_at - now < 60 #checks to see if the token is expired, is a boolean variable

    time_left = expires_at - now #finds out how much time is left on the token

    print(pgrm_signature + "the time left on orginial token is: "+ str(time_left / 60) + "min")
    if(is_expried): #if token is expried, get a new token with the refresh token
        sp = spotipy.Spotify(auth=refesh_the_token())#Refreshes the token from now on after 
    else:
        sp = spotipy.Spotify(auth=TOKEN) #creates object that interacts with spotify api; uses the first token generated; token only last 1 hour

    #chop playlist link into uri format
    #replace x, with y
    #Ex: line.replace(x,y)
    fline = playlist_link.replace("https://open.spotify.com/playlist/", "")#deletes first part of the link
    PLAYLISTID = fline.split("?", 1)[0]
    #PLAYLISTID = (fline.split("?si")[0]) #cuts off exess info from the link

    tracks = ["blankfaketrack"] #needed to have one space in the array
    file = open("uri.txt", "r") #open uri text file
    rline = file.readlines()
        
    #loops through the entire file and only adds one songs at a time to the array
    for line in reversed(list(rline)):
        if "spotify:track:" in line:
            tracks[0] = (line.strip()) #adds to the first element over and over again
            sp.playlist_add_items(playlist_id=PLAYLISTID, items=[tracks][0]) #adds to the actual playlist
    f = open('uri.txt', 'r+')
    f.truncate(0) 
    return "Playlist update request was sent and went through!"
 

#sendOff() used to debug file
