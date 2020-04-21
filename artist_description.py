import streamlit as st
import os
import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials

# Credentials
cid = 'your_client_id'
secret = 'your_client_secret'

#cid = os.environ.get("SPOTIPY_CLIENT_ID")
#secret = os.environ.get("SPOTIPY_CLIENT_SECRET")

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

def main():
	st.sidebar.subheader('Saiba tudo sobre o seu artista favorito no Spotify! \nConfira popularidade, número de seguidores e músicas mais tocadas.\n')

	name_input = st.sidebar.text_input('Digite o nome do artista:') 

	st.sidebar.markdown('[GitHub](https://github.com/mariromildo)')

	if name_input:
		result = sp.search(q='artist:' + name_input, type='artist')
		result_id = result['artists']['items'][0]['id']
		query = 'spotify:artist:' + result_id
		artist = sp.artist(query)

		# Artist infos
		name = artist['name']
		genres = artist['genres'][0]
		popularity = artist['popularity']
		followers = artist['followers']['total']
		image = artist['images'][0]['url']

		st.header(name)
		st.write('**Gênero musical:**', genres)
		st.write('**Popularidade:**', popularity)
		st.write('**Seguidores no Spotify:**', followers)
		st.image(image, width=200)
		st.write('__________________________________________________________')

		# Top 3 track infos
		top_tracks = sp.artist_top_tracks(query)['tracks']
		st.header('Top tracks')

		for track in range(3):
			music_name = top_tracks[track]['name']
			album = top_tracks[track]['album']['name']
			album_image = top_tracks[track]['album']['images'][track]['url']
			preview = top_tracks[track]['preview_url']
			feat = top_tracks[track]['artists']
			feat_name = [] 
			for i in range(len(feat)):
				feat_name.append(feat[i]['name'])

			if len(feat_name) > 0:
				feat_name.remove(name)

			st.write('**Música:**', music_name)
			if len(feat_name) > 0: # Returning featured artists only when the value isn't the searched artist name
				st.write('**Participação:**', ', '.join(str(p) for p in feat_name))

			st.write('**Album:**', album)
			st.image(album_image, width=200) # track audio preview
			st.audio(preview)
			st.write('__________________________________________________________')

if __name__ == '__main__':
	main()