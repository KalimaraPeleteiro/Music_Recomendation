import spotipy
import pandas as pd
import matplotlib.pyplot as plt
from skimage import io
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

    # Buscando músicas pertencentes ao mesmo grupo
    musicas_recomendadas = dataset[dataset['grupo_cluster'] == cluster_alvo][['0', '1', 'musica']]
    	
	# Coletando os valores espaciais no cluster (x e y)
    x_musicas_recomendadas = list(dataset[dataset['musica']==nome_musica]['0'])[0]
    y_musicas_recomendadas = list(dataset[dataset['musica']==nome_musica]['1'])[0]

    # Calculando as distâncias para a música-alvo
    distancias = euclidean_distances(musicas_recomendadas[['0', '1']], [[x_musicas_recomendadas, 
                                                                     y_musicas_recomendadas]])
    musicas_recomendadas['id'] = dataset['id']
    musicas_recomendadas['distancias'] = distancias

    # Ordenando o dataset com as nove músicas mais próximas do nosso alvo no espaço amostral
    # Ou seja, as mais semelhantes daquelas que estão no mesmo grupo clusteer
    dataset_recomendacao = musicas_recomendadas.sort_values('distancias').head(10)
    
    # Extraindo os ids das músicas
    lista_de_ids = list(dataset_recomendacao['id'])
    return lista_de_ids


# Dado os ids das músicas em busca, iremos buscar seus álbuns e seus nomes
def extrator_info(lista_de_ids):
    urls = []
    nomes = []

    for item in lista_de_ids:
        musica = sp.track(item) # Buscando pela API do Spotify
        urls.append(musica["album"]["images"][1]["url"])
        nomes.append(musica["name"])
    
    return nomes, urls


# Dado os nomes e as imagens das músicas recomendadas, cria um gráfico com as imagens para visualização
def visualizador_musicas(nomes, urls):
    
    plt.figure(figsize=(15,10))
    columns = 5
    for i, u in enumerate(urls):
        ax = plt.subplot(len(urls) // columns + 1, columns, i + 1)
        imagem = io.imread(u)
        plt.imshow(imagem)
        ax.get_yaxis().set_visible(False)
        plt.xticks(color = 'w', fontsize = 0.1)
        plt.yticks(color = 'w', fontsize = 0.1) 
        plt.xlabel(nomes[i], fontsize = 8)
        plt.tight_layout(h_pad=2, w_pad=0)
        plt.subplots_adjust(wspace=None, hspace=None)
        plt.tick_params(bottom = False)
        plt.grid(visible=None)
    plt.show()


# Função Geral
def recomendador(musica_alvo):
    lista_ids = buscar_recomendacoes(musica_alvo)
    lista_nomes, lista_urls = extrator_info(lista_ids)
    visualizador_musicas(lista_nomes, lista_urls)


recomendador('Shape of You')