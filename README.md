# Spotbot2
*Made with python 3.10.9 , Make sure you have this installed !*
A discord bot that scrapes users spotifylinks from a set channel and automatically adds those songs to a set spotify playlist.

**This readME file is meant to be looked at with the Image_refrences.pdf found in this repo**

How to setup:
1. Go to https://developer.spotify.com/dashboard/ refimage1 in image_refrences.pdf 
    
    a. Press Login
    
    b. Create App (refimage2)
    
    c. Copy and paste the corrosponging client id and client secret in their respective places in setup.json (refimage3)
    
    d. select Edit Settings and fillout fields detailed in (refimage4)
    
 2. Go to https://discord.com/developers/
    
    a. Create a new application (refimage5)
    
    b. Go to the bot tab > select create bot 
    
    c. Press reset access token (refimage6) and paste that token in "discord_token" : "place token here" in setup.json
    
    d. Copy and past access token into setup.json
    
    e. Turn on switches just like refimage7
    
    f. In the sidebar, you'll find the OAuth2 go to general and place http://localhost:5000/callback in redirecturi (refimage8)
    
    g. In the sidebar, go to URL Genreator. Fill out feilds just like refimage 9 & 10
    
    h. Invite the bot to the server you want it to run in
    
    i. Grab the link to the chat you want the bot to run in; right click on a discord channel and select copyID (refimage11)
    
    j. Paste the ID you recieved in the "discord_channel" : "place playlist link here" inside of the setup.json file

3. Get spotify playlist link that the bot will add to
    
    a.Add that link into setup.json in the correct field ex:"https://open.spotify.com/playlist/0XM....8226c884a3d" (needs to be a playlist you made on your own personal spotify account)
    
    
4. All fields in setup.json should be filled out and look like refimage12

5. Install requrements.txt to your machine 
  
  a. pip install -r requirements.txt in your terminal

6. Run app.py (only needs to be done once)
    a. flask run in your terminal
    
    b. Go to https://localhost:5000
    
    c. Login with your spotify username and password
    
    d. Once logged in on the webpage you should get the number of songs in the playlist you placed in setup.json refimage(13 & 15)
    
    e. Ctrl + c in terminal (app.py will never need to be ran again)
    
 7. Run spotbot.py
    
    (If you dont have past songs you want to grab skip steps b and c and set the grabpast flag to 1 in setup.json or else it will break the code)
    
    a.Once in the terminal it reads "spotbot.py: SpotifyBot: ON" (refimage16)
    
    b.Type [!grabPast] in the channel you specified in step 2j; This will grab all past spotify links sent in the chat **If you want to run this command and you have more than 500000 messages in your chat go to *line 62* in spotbot.py and increase the number as much as needed** 
    
    c. Once [!grabPast] is ran you should see it act like refrence (image18), grabpast can only be ran once, if this needs to be changed go to the setup.json file and set the flag back to 0 instead of 1

8. Now when songs are sent to the channel it will automatically send them to spotify! (refimage 20 & 21)

Enjoy!
