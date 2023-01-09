# Spotbot2
A discord bot that scrapes users spotifylinks from a set channel and automatically adds those songs to a set spotify playlist.

How to setup:
. Go to https://developer.spotify.com/dashboard/ refimage1 in image_refrences.pdf 
    .Press Login
    .Create App refimage2
    .Copy and paste the corrosponging client id and client secret in their respective places in setup.json refimage3
    .select Edit Settings and fillout fields detailed in refimage4
    
 .Go to https://discord.com/developers/
    .Create a new application refimage5
    .Go to the bot tab > select create bot 
    .Press reset access token refimage6
    .Copy and past access token into setup.json
    .In the sidebar, you'll find the OAuth2 URL Generator go to general and place http://localhost:5000/callback in redirecturi
    
    
 
. Fill out all fields in setup.json, grabpast should be 0 already
. Install requrements.txt to your machine 
  a. pip install -r requirements.txt in your terminal
.
. Run app.py
    a. flask run in your terminal
. Go to https://localhost:5000


INSTRUCTIONS WHEN BOT IS ACTIVE:
###
!grabpast must be ran first 
songs will then be added once a new song is sent to the chat 
after that grabpast will be disabled 
###



#Make requriements.json file
#Make bash file??
#Ensure token refresh works, if not find new soloution
#Rename tst.py to something more fitting or just put it in main.py 
#Make github page look pretty
