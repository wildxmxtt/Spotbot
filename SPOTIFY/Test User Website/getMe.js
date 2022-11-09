const fs = require('fs');
const fsPromises = require('fs').promises;
var SpotifyWebApi = require('spotify-web-api-node');

var TOKEN = 'BLANK_AWAITING_TOKEN'
var REFRESH_TOKEN = 'BLANK_AWAITING_TOKEN'

const spotifyApi = new SpotifyWebApi();
const {tokens} = require('./app.js');

//Gets the tokens from their respected files and sets their vaules 

async function accessG() {
  var pre_token;
  fs.readFile('Spotbot2\SPOTIFY\Test User Website\access_token.txt', 'utf8', (err, data) => {
    if (err) {
      console.error(err);
      return;
    }
    pre_token = data;
    console.log("Asynchronous read: " + data.toString());
  });
  
  let final_token = await pre_token;
  return final_token;
}
accessG();






  if(TOKEN == 'BLANK_AWAITING_TOKEN'){
    TOKEN = accessG();
    spotifyApi.setAccessToken(tokens.access.toString());
  }


  function getMyData() {
    (async () => {
      const me = await spotifyApi.getMe();
      // console.log(me.body);
      getUserPlaylists(me.body.id);
    })().catch(e => {
      console.error(e);
    });
  }


  async function getUserPlaylists(userName) {
    const data = await spotifyApi.getUserPlaylists(userName)
  
    console.log("---------------+++++++++++++++++++++++++")
    let playlists = []
  
    for (let playlist of data.body.items) {
      console.log(playlist.name + " " + playlist.id)
      
      let tracks = await getPlaylistTracks(playlist.id, playlist.name);
      // console.log(tracks);
  
      const tracksJSON = { tracks }
      let data = JSON.stringify(tracksJSON);
      fs.writeFileSync(playlist.name+'.json', data);
    }
  }
  getMyData();


  /*
async function refreshG() {
    try {
      const data = await fs.readFile('refresh_token.txt', { encoding: 'utf8' });
      REFRESH_TOKEN = data.toString();
      console.log(data);
    } catch (err) {
      console.log(err);
    }
  }
  refreshG();
*/