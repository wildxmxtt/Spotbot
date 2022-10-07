from asyncio.windows_events import NULL
from discord.ext import commands
import re
from discord import Spotify

TOKEN = 'OTc2OTUxMzcwODE0OTg0MjUy.GGbHEH.hsa8gU8PheJbW4jV1ffg4ahWaS8FWYU8tvYuII'
bot = commands.Bot(command_prefix='!', case_insensitive=True)

@bot.event
async def on_ready():
    #Lets programmer know that the bot has been activated
    print('SpotifyBot: ON')


#This is the help command that lets the user know all of the avaliable commands that can be used 
@bot.command()
async def hlp(ctx):
    await ctx.reply("The commands for this bot go as follows: \n" + "slink (gives the user the link to the spotify playlist) \n" + "sLogin (logs into the account the spotify playlist will be created in")

@bot.command()
async def sLink(ctx):
     await ctx.reply("Super cool temp link!!!11!!!!1!")


@bot.command()
async def sLogin(ctx):
     await ctx.reply("login/temp/cute/guys")

#This is the vote command it takes context (ctx) the first option (opt1) and second option (opt2)

#This is to grab the past songs that have been sent to the channel
@bot.command()
async def grabPast(ctx):
    word = "https://open.spotify.com/track"
    await ctx.reply("Grabbing songs now please wait until FINISHED is sent")
    channel = ctx.channel
    #MAKE SURE TO BUMP THIS LIMMIT UP TO A CRAZY NUMBER WEHN FULLY IMPLEMENTED
    messages = await ctx.channel.history(limit=500).flatten()
    await ctx.send("Grabbing & flitering past messages.....")
    file = open("oldLinks.txt", "a")
    file2 = open("allLinks.txt", "a")
    
    

    for msg in messages:
        if word in msg.content:
            #adds to the filter file 
            file2.write(str(msg.content) + ",")
            print("allLink file has been written to succesfully" )

            file.write(str(msg.content) + ",")
            print("message added to oldLinks.txt")
            dupCheck(msg.content)



    await ctx.send("messages grabbed, Process complete")





@bot.event
async def on_message(msg):
    strCheck = "https://open.spotify.com/track"
    if re.search(strCheck, msg.content):
        print("Valid Spotify Link")
        #Creates a file called play con (playlist converter) for the spotify API to read from
        file = open(r"allLinks.txt", "a")

        checkEmoji = "☑️"
        rEmoji = "🔁" 

        file.write(str(msg.content) + ",")

        print("allLink file has been written to succesfully" )
        test = dupCheck(msg.content)


    #Decides what emoji to add based on if it is a duplicate or not
        if(test == True):
            await msg.add_reaction (rEmoji)
        else:
            await msg.add_reaction(checkEmoji) 
        
    else:
     
        print("Not valid Link")
    
    await bot.process_commands(msg)



def dupCheck(link):
    string1 = link

    # opening a text files
    file = open("allLinks.txt", "r")
    #opens the master link files that will be sent to the spotify server
    #playCon is what actually will get sent to the server
    file2 = open("playCon.txt", "a")

    # setting flag and index to 0
    flag = 0
    index = 0

    # Loop through the file line by line
    for line in file:
        index += 1
        
        # checking string is present in line or not
        if string1 in line: 
            flag = 1
            break
                
    # checking condition for string found or not
    if flag == 0:
        print('String', string1 , 'Not Found')

        # closing text file	

        file.close()
        print("Playcon File has been written to succesfully")
        file2.write(str(link) + ",")
        return False
    else:
        print('String', string1, 'Found In Line', index)
        # closing text file	
        print("DUPLICATE LINK FOUND, NOT ADDED TO PLAYCONFILE")
        file.close()
        return True


bot.run(TOKEN)