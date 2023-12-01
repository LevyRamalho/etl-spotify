import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import os

def spotify_connection():
    """Criar conexão com a API Spotify
        :return sp: Conexão com o spotify
    """

    # Resga as credenciais de acesso das variaveis de ambiente
    client_id = os.environ.get('SPOTIFY_CLIENT_ID')
    client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri="https://www.google.com.br/",
                                               scope="user-library-read"))
    return sp

def get_spotify_data(file_path, sp):
    print('Extraindo dados da API do spotify e salvando em formato JSON')
    # Fazendo a conexão com o Spotify
    
    table_raw = []
    offset = 0
    limit = 50

    while True:
            # Extrai via API as músicas salvas - A propriedade offset garantirá que puxe todos os dados da API
            results = sp.current_user_saved_tracks(limit=limit, offset=offset)

            # Itera sobre cada item de results
        
            for item in results['items']:
                track_info = item['track']
                # Extraio as informações que preciso
                data_raw = {
                    'track_name': track_info['name'],
                    'track_id': track_info['id'],
                    'album_name': track_info['album']['name'],
                    'release_date': track_info['album']['release_date'],
                    'album_id' :  track_info['album']['id'],
                    'artists': [artist['name'] for artist in track_info['artists']],
                    'artists_id': [artist['id'] for artist in track_info['artists']]
                }

                table_raw.append(data_raw)

            # Verifica se existem mais páginas de dados. Em caso positivo, atualiza o offset e o loop segue.
            if results['next']:
                offset += limit
            else:
                break

    # # Salva os dados em arquivo JSON
    with open(f'{file_path}\data_raw.json', 'w', encoding='utf-8') as jp:
            js = json.dumps(table_raw, indent=4)
            jp.write(js) 

    return table_raw

# Extração da features de cada música 
def get_tracks_features(data, file_path, sp):
    print('Extraindo as Features das músicas e salvando em formato JSON')
    ids = []
    for entry in data:
        ids.append(entry['track_id'])

    audio_feature_list = []
    audio_feature = []
    index = 0

    while index < len(ids):
        audio_feature += sp.audio_features(ids[index:index + 50])
        index += 50
        audio_feature_dic = {
            'id' : audio_feature[0]['key'],
            'danceability': audio_feature[0]['danceability'],
            'energy': audio_feature[0]['energy'],
            'key': audio_feature[0]['key'],
            'loudness': audio_feature[0]['loudness'],
            'mode': audio_feature[0]['mode'],
            'speechiness': audio_feature[0]['speechiness'],
            'acousticness': audio_feature[0]['acousticness'],
            'instrumentalness': audio_feature[0]['instrumentalness'],
            'liveness': audio_feature[0]['liveness'],
            'valence': audio_feature[0]['valence'],
            'tempo': audio_feature[0]['tempo'],
            'type': audio_feature[0]['type'],
            'duration_ms': audio_feature[0]['duration_ms'],
            'time_signature': audio_feature[0]['time_signature']
        }
        audio_feature_list.append(audio_feature_dic)
    # Salvando em arquivo json
    with open(f'{file_path}\dados_tracks_feature.json','w') as json_file:
        json.dump(audio_feature_list, json_file, indent=4)

# Extração das informações de música 
def extract_tracks_info(data, file_path):
    print('Extraindo informações de Músicas e salvando em formato JSON')

    #Criando uma lista para conter os obejtos finais
    tracks_info = []

    for entry in data:
        track_info = {
            "track_name": entry['track_name'],
            "track_id": entry['track_id'],
            "album_id": entry['album_id']
        }

        tracks_info.append(track_info)
    # Salvando em arquivo JSON
    with open(os.path.join(file_path,'tracks_info.json'), 'w') as json_file:
        json.dump(tracks_info,json_file, indent=4)
    
def extract_artists_info(data, file_path):
    print('Extraindo informações de Artistas e salvando em formato JSON')
    # Criando uma lista para conter os objetos finais
    artists_info = []

    # Iterando sobre cada elemento do JSON original
    for entry in data:
        # Iterando sobre os artistas e seus IDs correspondentes
        for i in range(len(entry['artists'])):
            artist_info = {
                "artists_id": entry['artists_id'][i],
                "artists": entry['artists'][i]
            }
            # Adicionando as informações do artista à lista final
            artists_info.append(artist_info)

    # Removendo os duplicados utilizando a técnica de converter cada elemento da lista de dicionários para tuple e voltando para lista de dicionários
    artists_info = [dict(t) for t in {tuple(d.items()) for d in artists_info}]

    # Salvando as informações dos artistas em um novo arquivo JSON
    with open(os.path.join(file_path, 'artists_info.json'), 'w') as json_file:
        json.dump(artists_info, json_file, indent=4)

# Extração da informçãoes de audios
def extract_albums_info(data, file_path):
    print('Extraindo informações dos Albuns e salvando em formato JSON')
    albuns_info = []

    # Interando sobre cada elemento do JSON original
    for entry in data:
        # Resgantando as informações que quero
        album_info = {
            "album_name": entry['album_name'],
            "album_id": entry['album_id'],
            "release_date": entry['release_date']
        }
        # Colocando cada dicionário dentro de uma lista
        albuns_info.append(album_info)
    # Como muitas músicas pertencem a um mesmo album acabamos tendo mais de uma ocorrência de um mesmo album. 
    # Para eviatar repetições usei a estratégia abaixo
    albuns_info = [dict(t) for t in {tuple(d.items()) for d in albuns_info}] 

    # Salvando em arquivo JSON
    with open(os.path.join(file_path, 'albuns_info.json'),'w') as json_file:
        json.dump(albuns_info, json_file, indent=4)

# Organizando os PATH dos arquivos
path = os.getcwd()
folder_name = 'data'
file_path = os.path.join(path, folder_name)

# Obter Conexão com spotify
sp_conn = spotify_connection()

# Obtendo dados do Spotify
spotify_data = get_spotify_data(file_path, sp_conn)


# Obtendo as features de cada Música
get_tracks_features(spotify_data,file_path, sp_conn)

# Extrair informações de tracks, artistas e álbuns
extract_tracks_info(spotify_data,file_path)
extract_artists_info(spotify_data,file_path)
extract_albums_info(spotify_data,file_path)