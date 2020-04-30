import json
import requests
from collections import Counter
import base64
#import thread
#from ratelimit import limits, sleep_and_retry

production=1




def req_auth():
    if production:
        callback_url="https://livelist-42.herokuapp.com/form/".replace('/','%2F')
    else:
        callback_url="http://localhost:5000/form/".replace('/','%2F')
    scope="playlist-modify-private"
    client_id="008bb528a0ef4cb8aa389d7bf1c937d5"
    response_type="code"
    url = "https://accounts.spotify.com/authorize?client_id="+client_id+"&redirect_uri="+callback_url+"&scope="+scope+"&response_type="+response_type+"&show_dialog=true"

    payload = {}
    headers= {}

    return url

def get_code():
    if production:
        callback_url="https://livelist-42.herokuapp.com/form/".replace('/','%2F')
    else:
        callback_url="http://localhost:5000/form/".replace('/','%2F')
    scope="playlist-modify-private"
    client_id="008bb528a0ef4cb8aa389d7bf1c937d5"
    response_type='code'
    url = "https://accounts.spotify.com/authorize?client_id="+client_id+"&redirect_uri="+callback_url+"&scope="+scope+"&response_type="+response_type+"&show_dialog=true"

    return url

def get_token(auth_code):

    url = "https://accounts.spotify.com/api/token"

    if production:
        redirect_url="https%3A//livelist-42%2Eherokuapp%2Ecom/form/"
    else:
        redirect_url='http%3A//localhost%3A5000/form/'
    payload = 'grant_type=authorization_code&code='+auth_code+'&redirect_uri='+redirect_url
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Basic MDA4YmI1MjhhMGVmNGNiOGFhMzg5ZDdiZjFjOTM3ZDU6ZmU0ZjA5ZTMzZjEzNDUxZWJkZDM0YWMwMGQzZTk5ZTY='
    }
    response = requests.request("POST", url, headers=headers, data = payload)
    if response.status_code==200:
        response=response.json()
    else:
        exit(response.status_code)

    access_token='Bearer '+response['access_token']
    refresh_token=response['refresh_token']
    return access_token

def call_setlistfm(mbid):
    apikey= '2SM-gNCWYjzW7hHnjpIfa6K5FOHDkK1S8zj5'

    url="https://api.setlist.fm/rest/1.0/artist/"+mbid+"/setlists?p=1"
    payload = {}
    headers = {
        'Accept': 'application/json',
        'x-api-key': apikey
    }
    response=requests.request("GET", url, headers=headers, data = payload)
    data=response.json()
    return data
    
def get_songs(data,num_concerts=5,max_songs=20,date=0):
    setlists=data['setlist']
    list_of_songs=[]
    for i in range(num_concerts):
        setlist=setlists[i]
        for _set in setlist['sets']['set']:
            for song in _set['song']:
                list_of_songs.append(song['name'])
                #print(song['name'])
    res = [key for key, value in Counter(list_of_songs).most_common()]
    return res

def get_access_token_client_credentials():
    client_id='008bb528a0ef4cb8aa389d7bf1c937d5'
    client_secret='fe4f09e33f13451ebdd34ac00d3e99e6'
    data=client_id+':'+client_secret
    encoded_client_id_secret = base64.b64encode(data.encode('utf-8'))


    url = "https://accounts.spotify.com/api/token"

    payload = 'grant_type=client_credentials'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Basic '+str(encoded_client_id_secret,'utf-8')
    }

    response = requests.request("POST", url, headers=headers, data = payload).json()
    access_token=response['access_token']
    return access_token

def search_song(access_token, platform, song):
    try:
        if platform=='Spotify':
            url="https://api.spotify.com/v1/search?q="+song.replace(' ','+')+"&type=track&market=US"
            payload = {}
            headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'Authorization': 'Bearer '+access_token
            }

            response = requests.request("GET", url, headers=headers, data = payload)
            if (response.status_code!=200):
                print('Not 200')
            #print(type(response))
            data=response.json()
    #        print(data['tracks'])
            if data['tracks']['items'][0]['name']==song:
                # print('True')
                # print(song)
                uri=data['tracks']['items'][0]['uri']
                # print(data['tracks']['items'][0]['uri'])
                return (1,uri)
            else:
                # print('False')
                # print(song)
                # print('Not the exact song')
                return (0,song)
    except:
        print('error')
        print(data)
        return 2

def get_spotify_song_uris(setlistfm_songlist, platform):
    access_token=get_access_token_client_credentials()
    found_songs=[]
    not_found_songs=[]
    for song in setlistfm_songlist:
        res=search_song(access_token, platform, song)
        if res!=2:    
            print(res)
            if res[0]:
                found_songs.append(res[1])
            else:
                not_found_songs.append(res[1])
    return (found_songs,not_found_songs)

def create_playlist(access_token, playlist_name, platform, songlist):
    if platform=='Spotify':
        
        url = "https://api.spotify.com/v1/me"

        payload = {}
        headers = {
        'Authorization': access_token
        }
        print('#############')
        print(access_token)
        response = requests.request("GET", url, headers=headers, data = payload)
        if response.status_code==200:
            response = response.json()
        else:
            for (key,value) in response.json().items():
                print(key,response)
            exit(response.status_code)
        user_id=response["id"]

        url = "https://api.spotify.com/v1/users/"+user_id+"/playlists"

        payload = {'name' : playlist_name,'public' : 'false'}
        payload=json.dumps(payload)
        headers = {
        'Content-Type': 'application/json',
        'Authorization': access_token
        }

        response = requests.request("POST", url, headers=headers, data = payload)
        if response.status_code==201:
            response = response.json()
        else:
            for (key,value) in response.json().items():
                print(key,response)
            exit(response.status_code)
        playlist_id=response['id']

        uris = ','
        uris = uris.join(songlist)
        uris = uris.replace(':','%3A')
        url = "https://api.spotify.com/v1/playlists/"+playlist_id+"/tracks"+"?uris="+uris
        print(json.dumps(songlist))
        print(access_token)
        print(url)
        payload = {}
        headers = {
        #'Content-Type': 'application/json',
        'Authorization': access_token
        }
        response = requests.request("POST", url, headers=headers, data = payload)
        if response.status_code==201:
            response = response.json()
        else:
            print(payload)
            print(response)
            exit(response.status_code)