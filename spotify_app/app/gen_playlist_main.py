import app.API_Calls as api

def gen_playlist(platform,mbid,playlist_name,code,num_concerts,max_songs,date):
    data=api.call_setlistfm(mbid)
    res=api.get_songs(data,num_concerts,max_songs,date)
    access_token=api.get_token(code)
    song_uris=api.get_spotify_song_uris(res,platform)[0]
    api.create_playlist(access_token,playlist_name,platform,song_uris)
