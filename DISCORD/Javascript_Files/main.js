const { Client, GatewayIntentBits, Partials } = require('discord.js');
const client = new Client({ intents: [GatewayIntentBits.Guilds], partials: [Partials.Channel] });

//const Discord = require('discord.js');
const fs = require('fs');
const TOKEN = 'OTc2OTUxMzcwODE0OTg0MjUy.GGbHEH.hsa8gU8PheJbW4jV1ffg4ahWaS8FWYU8tvYuII';
//const bot = new Discord.Client();

const PREFIX = "!";

client.on('ready', () =>{
    console.log("SPOTBOT: ON");
})

client.on('message', msg =>{
    //splits up the message into an array
    let args = msg.content.substring(PREFIX.length).split(" ");
    //Gets the ! from the message 
    switch(args[0]){
        case 'ping': //name of the command
            msg.reply("pong");
        break;
    }

})

client.login(TOKEN);