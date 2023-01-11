import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from sklearn.metrics.pairwise import euclidean_distances


scope = "user-library-read playlist-modify-private"

OAuth = SpotifyOAuth(scope = scope,
                     redirect_uri = "http://localhost:5000/callback",
                     client_id = "b0e79083aa874b3aaaff8fd4403db555",
                     client_secret = "f9b839d489bc4c968fc65098e07ad907")

client_credentials_manager = SpotifyClientCredentials(client_id = "b0e79083aa874b3aaaff8fd4403db555", 
                                                      client_secret = "f9b839d489bc4c968fc65098e07ad907")

sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

dataset = pd.read_csv("musicas_agrupadas.csv")


# Primeira Função - Busca músicas recomendadas com base na música atual.
def buscar_recomendacoes(nome_musica: str):
    
    # Encontrando o grupo cluster da música atual
    cluster_alvo = list(dataset[dataset['musica'] == nome_musica]['grupo_cluster'])[0]
    
    # Buscando todas as músicas pertencentes ao mesmo grupo cluster
    musicas_recomendadas = list(dataset[dataset['grupo_cluster'] == cluster_alvo]['musica'])

    print(musicas_recomendadas)


buscar_recomendacoes('Shape of You')