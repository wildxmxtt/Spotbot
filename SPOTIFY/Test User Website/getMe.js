const fs = require('fs');
const fsPromises = require('fs').promises;
var SpotifyWebApi = require('spotify-web-api-node');

var TOKEN = 'BLANK_AWAITING_TOKEN'
var REFRESH_TOKEN = 'BLANK_AWAITING_TOKEN'

const spotifyApi = new SpotifyWebApi();


//Gets the tokens from their respected files and sets their vaules 

async function accessG() {
  fs.promises.readFile("access_token.txt")
  .then(function(result) {
    console.log("TOKEN:"+result);
    return result.toString();
  })
  .catch(function(error) {
     console.log(error);
  })
}
accessG();

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

  if(TOKEN == 'BLANK_AWAITING_TOKEN'){
    TOKEN = accessG();
    spotifyApi.setAccessToken(TOKEN);
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