from discord.ext import commands
import re
import discord
from datetime import datetime
import json
import playlist_update
from os import path
#Token vaild as of 1/2/2023

pgrm_signature = "spotbot.py: "

with open("setup.json", 'r') as setupf:
    data = json.load(setupf)
    TOKEN = (data['discord_token'])
    client_id = (data['client_id'])
    client_secret = (data['client_secret'])
    playlist_link = (data['playlist_link'])
    grab_past_flag = (data['grab_past_flag'])
    discord_channel = (data['discord_channel'])


intents = discord.Intents.all()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', case_insensitive=True, intents=intents)


@bot.event
async def on_ready():
    #Lets programmer know that the bot has been activated
    print(pgrm_signature + 'SpotifyBot: ON')


#This is the help command that lets the user know all of the avaliable commands that can be used 
@bot.command()
async def hlp(ctx):
    await ctx.reply("The commands for this bot go as follows: \n" + 
    "sLink (gives the user the link to the spotify playlist) \n" + 
    "grabPast (allows for the user to grab past songs sent in a chat, this can only be ran once) \n" +
    "When a user sends a messsage in THIS CHAT the bot will analyis that message, if it is a valid spotify link it will be placed into the playlist\n" 
    )

#gives the link set in the setup.json file
@bot.command()
async def sLink(ctx):
     await ctx.reply(playlist_link)


#This is to grab the past songs that have been sent to the channel
@bot.command()
async def grabPast(ctx):
    with open("setup.json", 'r') as setupf:
        data = json.load(setupf)
        grab_past_flag = (data['grab_past_flag'])

    if(grab_past_flag) == 1: 
        await ctx.reply("grabPast has already been called. If this is a mistake please go to the setup.json file and set grab_past_flag to 0")
    else:
        word = "https://open.spotify.com/track"
        await ctx.reply("Grabbing songs now please wait until FINISHED is sent")
        channel = ctx.channel

        #MAKE SURE TO BUMP THIS LIMMIT UP TO A CRAZY NUMBER WEHN FULLY IMPLEMENTED
        messages = [messages async for messages in ctx.channel.history(limit=500)] # This is the new way to do the .flatten() commented down below.
        #messages = await ctx.channel.history(limit=500).flatten()


        await ctx.send("Grabbing & Flitering Past Messages.....")

        # to make it work with only one file, surprisingly to me all the file handling can be done in dupCheck()
        for msg in messages:
            if word in msg.content:
                dupCheck(msg.content)

                ####
                ####
                #MAKE A FLAG FOR GRABPAST, this function should only need to be ran once, make it so it used uritxt before the patch w
                #where it adds the whole text file and then the next uri, since this should be the first command you run when entering the server
                #the command should then be disabled in a way
                #####
                ####
        await ctx.send("Messages Grabbed, Process Complete, FINISHED")




@bot.event
async def on_message(msg):
    #grabs the discord channel specified in setup.json
    if msg.channel.id == discord_channel:
    #once again, all the file work can be moved over to the dupCheck() function for single file handling
        strCheck = "https://open.spotify.com/track"

        if re.search(strCheck, msg.content):
            if not "Here are all the songs" in str(msg.content): # This had to be added as the way it works, it would catch all songs comand as a new link for some reason.
                print(pgrm_signature + "Valid Spotify Link")

                checkEmoji = "☑️"
                rEmoji = "🔁" 

                test = dupCheck(msg.content)


        #Decides what emoji to add based on if it is a duplicate or not
                if(test == True):
                    await msg.add_reaction (rEmoji)
                else:
                    await msg.add_reaction(checkEmoji) 
                    print(pgrm_signature + playlist_update.sendOff())
                    update_gp_flag()
                    await msg.reply("Added to Spotify Playlist!")

        else:            
            print(pgrm_signature + "Not valid Link")
        
        await bot.process_commands(msg)



def dupCheck(link):
    string1 = link

    # opening a text files
    try:
        file = open("playlist.txt", "r") # I am changing the name to playlist as it makes more sense in my head this could be a problem later so revert if needed.
    except FileNotFoundError:
        #make it create then open the file if the file does not exits
        file = open("playlist.txt", "x")
        file.close()
        file = open("playlist.txt", "r")

    # setting flag and index to 0
    flag = 0
    index = 0

    # Loop through the file line by line
    for line in file:
        index += 1
        
        # checking string is present in line or not (also adds some error checks for constraining commas to only accept what discord displays if commas are present.)
        if string1.split(",", 1)[0] in line: 
            flag = 1
            break

        if string1.split("\n", 1)[0] in line: 
            flag = 1
            break
    
    #swap file operation to append
    file.close()
    file = open("playlist.txt", "a")


    # checking condition for string found or not
    if flag == 0:
        print(pgrm_signature + 'String', string1 , 'Not Found')
        
        songToWrite = str(link)

        if "," in songToWrite:
            songToWrite = songToWrite.split(",", 1)[0]
        
        file.write(songToWrite + "\n") # Changed to making every new song go to its own line for later reading simplicity
        print(pgrm_signature + "playlist file has been written to succesfully")
        file.close()
        uritxt(songToWrite)
        return False
    else:
        print(pgrm_signature + 'String', string1, 'Found In Line', index, ' in playlist.txt')
        # closing text file	
        print(pgrm_signature + "DUPLICATE LINK FOUND, NOT ADDED TO PLAYLIST FILE")
        file.close()
        return True


def uritxt(link):
    #opens up the setup.json file
    with open("setup.json", 'r') as setupf:
        data = json.load(setupf)
        grab_past_flag = (data['grab_past_flag']) #this will check if the grab_past_flag has been updated

    print(pgrm_signature + "Writting to uri.txt..... \n")
    
    if(grab_past_flag == 0):
        print(pgrm_signature + "Writting to uri.txt.....: \n")
        file = open("playlist.txt", "r+")
        file1 = open("uri.txt", "w+")
        count = 0
        rline = file.readlines()
    
    #chops it up into uri format
        for line in rline:
            count += 1 
            #replace x, with y
            #line.replace(x,y)
            fline = line.replace("https://open.spotify.com/track/", "spotify:track:")
            file1.write(fline.split("?si")[0] + "\n") #cuts off exess info from the uri and writes it to the file
        print(pgrm_signature + "uri.txt has been written to")
        file1.close()
        #send off here then set grabpast to 1???
    else:
        file1 = open("uri.txt", "w+")

        song = str(link)

        #chops it up into uri format
        fline = song.replace("https://open.spotify.com/track/", "spotify:track:")
        file1.write(fline.split("?si")[0] + "\n") #cuts off exess info from the uri and writes it to the file

        file1.close()
        count = 0

        #read uri text file
        file1 = open("uri.txt", "r+")
        rline1 = file1.readlines()
        for line in rline1:
            print(pgrm_signature + "Line{}: {}".format(count, line.strip()))

        file1.close()


        print(pgrm_signature + "Uri text file written to succesfully!\n")
        print(pgrm_signature + "Sending songs off to spotify")
  

#two routes for this function
#Option A figure out how to make vaild request to a server with a token 
#Option B just have the silly bot open and close new tabs to localhost5000
#We will need a basch script to make this work on linux and windows simotaniously
#The bash script neeeds to run both main.py and app.py at the same time z
#def sendOff():
    #url = "http://127.0.0.1:5000/"
    #webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open(url)
    #dt = datetime.now()
    #print(pgrm_signature + "check app.py terminal if request was succesful TIMESTAMP:" + str(dt))
    #time.sleep(10)
    #os.system("taskkill /im chrome.exe /f")
    
    
    #read uri text file
    
def update_gp_flag(): 
 ###Update grab_past_flag#####
    filename = "setup.json"
    dictObj = []

    # Check if file exists
    if path.isfile(filename) is False:
        raise Exception("File not found")
    
    # Read JSON file
    with open(filename) as fp:
        dictObj = json.load(fp)
    
        # "grab_past_flag" : 0
        dictObj.update({"grab_past_flag": 1 })
    
        with open(filename, 'w') as json_file:
            json.dump(dictObj, json_file, 
                        indent=4,  
                        separators=(',',': '))
    
        print(pgrm_signature + 'Successfully updated setup.json')
    
bot.run(TOKEN)