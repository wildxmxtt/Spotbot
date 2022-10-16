// Imports
const express = require('express')
const app = express()
const port = 8888
const fs = require('fs/promises');
var SpotifyWebApi = require('spotify-web-api-node');

//THIS GETS THE SERVER STARTED


// Static Files
app.use(express.static('public'));
// Specific folder example
app.use('/css', express.static(__dirname + 'public/css'))
app.use('/js', express.static(__dirname + 'public/js'))
// app.use('/img', express.static(__dirname + 'public/images'))



app.get('/', (req, res) => {
   res.sendFile(__dirname + '/index.html')
})


const scopes = [
   'ugc-image-upload',
   'user-read-playback-state',
   'user-modify-playback-state',
   'user-read-currently-playing',
   'streaming',
   'app-remote-control',
   'user-read-email',
   'user-read-private',
   'playlist-read-collaborative',
   'playlist-modify-public',
   'playlist-read-private',
   'playlist-modify-private',
   'user-library-modify',
   'user-library-read',
   'user-top-read',
   'user-read-playback-position',
   'user-read-recently-played',
   'user-follow-read',
   'user-follow-modify'
 ];
 
// credentials are optional
var spotifyApi = new SpotifyWebApi({
   clientId: 'a08383e569fd4d9d9f06812485b72a86',
   clientSecret: '63008b05ef5949d8b23c151e4c0e0a82',
   redirectUri: 'http://localhost:8888/callback'
 });
 
 
 app.get('/login', (req, res) => {
   res.redirect(spotifyApi.createAuthorizeURL(scopes));
 });
 
 app.get('/callback', (req, res) => {
   const error = req.query.error;
   const code = req.query.code;
   const state = req.query.state;
 
   if (error) {
     console.error('Callback Error:', error);
     res.send(`Callback Error: ${error}`);
     return;
   }
 
   spotifyApi
     .authorizationCodeGrant(code)
     .then(data => {
       const access_token = data.body['access_token'];
       const refresh_token = data.body['refresh_token'];
       const expires_in = data.body['expires_in'];
 
       spotifyApi.setAccessToken(access_token);
       spotifyApi.setRefreshToken(refresh_token);
       
       //Saves the access token into a file
       async function aTokenF() {
         try {
           const content = access_token;
           await fs.writeFile('access_token.txt', content);
         } catch (err) {
           console.log(err);
         }
       }
       aTokenF();

       //Saves the refresh token into a file
       async function rTokenF() {
         try {
           const content = refresh_token;
           await fs.writeFile('refresh_token.txt', content, {flag: 'w+'});
         } catch (err) {
           console.log(err);
         }
       }
       rTokenF();


       console.log('access_token:', access_token);
       console.log('refresh_token:', refresh_token);
 
       console.log(
         `Sucessfully retreived access token. Expires in ${expires_in} s.`
       );
       res.send('Success! You can now close the window.');

 
  
 
       setInterval(async () => {
         const data = await spotifyApi.refreshAccessToken();
         const access_token = data.body['access_token'];
 
         console.log('The access token has been refreshed!');
         console.log('access_token:', access_token);
         spotifyApi.setAccessToken(access_token);
       }, expires_in / 2 * 1000);
     })
     .catch(error => {
       console.error('Error getting Tokens:', error);
       res.send(`Error getting Tokens: ${error}`);
     });
 });

app.listen(port, () => console.info(`App listening on port ${port}`))