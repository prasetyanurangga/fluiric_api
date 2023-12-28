import azapi
from spotify import Spotify
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
async def root():
    return {"hello": "world"}

@app.get("/get_lyrics_spotify/{track_id}")
async def get_lyrics_spotify(track_id: str):
    # Example usage:
    sp_dc = ''

    spotify = Spotify(sp_dc)
    spotify.check_token_expire()
    lyrics_data = spotify.get_lyrics(track_id)
    # Return lyrics as JSON response
    return JSONResponse(content=lyrics_data)

@app.get("/get_lyrics_az/{title}")
async def get_lyrics_az(title: str):
    # Initialize AZlyrics API
    API = azapi.AZlyrics('google', accuracy=0.5)
    API.title = title

    # Get lyrics
    lyrics = API.getLyrics()

    # Convert lyrics to an array of strings (one string per line)
    lyrics_array = lyrics.splitlines()

    # Return lyrics as JSON response
    return JSONResponse(content={"title": title, "lyrics": lyrics_array})