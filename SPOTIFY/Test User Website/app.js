// Imports
const express = require('express')
const app = express()
const port = 8888
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


app.listen(port, () => console.info(`App listening on port ${port}`))