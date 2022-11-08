
var redirectUri = "http://localhost:8888/callback"; // change this your value
var client_id = "a08383e569fd4d9d9f06812485b72a86";
var client_secret = "63008b05ef5949d8b23c151e4c0e0a82";
const AUTHORIZE = "https://accounts.spotify.com/authorize"

function onPageLoad(){

}





function requestAuthorization(){    
    client_id = document.getElementById("clientId").value;
    client_secret = document.getElementById("clientSecret").value;
    localStorage.setItem("client_id", client_id);
    localStorage.setItem("client_secret", client_secret); // In a real app you should not expose your client_secret to the user

    let url = AUTHORIZE;
    url += "?client_id=" + client_id;
    url + "&response_type=code";
    url += "&redirect_uri=" + encodeURI(redirect_uri);
    url + "&show_dialog=true";
    url += "&scope=user-read-private user-read-email user-modify-playback-state user-read-playback-position user-library-read streaming user-read-playback-state user-read-recently-played playlist-read-private";
    window.location.href = url; // Show Spotify's authorization screen
}