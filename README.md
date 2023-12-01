# ETL de dados da API do Spotify

## Ferramentas usadas:

---

- Python
    - boto3
    - spotipy
    - json
    - OS

## Visão Geral:

---

Esse projeto foi desenvolvido com o propósito de treinar minhas técnicas de programação com a linguagem python e sua conectividade com o serviço S3 da AWS utilizando a biblioteca **boto3**, além de explorar a biblioteca **OS** para gerenciamento dos diretórios.

## Atividade:

---

Utilizando a biblioteca **spotipy**, crie uma conexão com sua conta spotify e extraia os dados das músicas salvas. Com o resultado extraído, extraía as features de cada música. O resultado dessas duas operações devem ser armazenadas em arquivos JSON seguindo a seguinte organização:

- **Arquivo 1 - data_raw.json:** track_name, track_id, album_name, release_date, album_id, artists, artists_id
- **Arquivo 2 - dados_tracks_feature.json:** id, danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, type, duration_ms, time_signature
- **Arquivo 3 - artists_info.json:** artists, artists_id
- **Arquivo 4 - albuns_info.json:** album_id, album_name
- **Arquivo 5 - tracks_info.json:** track_name, track_id, album_id

Após tratar os dados e transformá-los nos quatro arquivos propostos, faça o Upload dos arquivos para um bucket S3 AWS.

> Os arquivos podem ser encontrados na pasta [data](https://github.com/LevyRamalho/etl-spotify/tree/main/data)

## Passo a Passo da extração de dados - Arquivo [extract_data.py](https://github.com/LevyRamalho/etl-spotify/blob/main/extract_data.py)

---

1. **Conexão com o Spotify:**

A função `spotify_connection()` busca as credenciais armazenadas como variáveis de ambiente usando a biblioteca **OS** e cria uma conexão com o Spotify usando `SpotifyOAuth` da biblioteca **spotipy**. Essa função retorna a conexão que será usada como argumentos de outras funções.

2. **Extraindo os dados das músicas salvas:**

A função `get_spotify_data()` recebe como argumento a conexão e busca os dados das músicas salvas utilizando a função `current_user_saved_tracks` da biblioteca **spotipy**. A função organiza os dados que desejo dentro de uma lista de dicionários, armazena esses dados como arquivo JSON intitulado data_raw.json e salva o arquivo na pasta **data**

3. **Extração da features das músicas:**

A função `get_tracks_features()` busca as features de cada música. Essa função recebe como argumento a conexão com o spotify e os dados das músicas extraídas pela função get_spotify_data(). A função se encarrega de salvar o dados em um arquivo JSON intitulado de dados_tracks_feature.json.

4. **Organizar arquivo com os dados de Artistas:**

Para extrair as informações de artistas e criar o arquivo artists_info.json foi criado a função `extract_artists_info()`. Essa função recebe como argumento os dados extraídos do Spotify e o file_path

> file_path Local que será armazenado o arquivo JSON resultado dessa função.
> 

5. Organizar arquivo com os dados de Álbuns:

Para extrair as informações de álbuns e criar o arquivo albuns_info.json foi criado a função `extract_albuns_info()`. Essa função recebe como argumento os dados extraídos do Spotify e o file_path

> file_path Local que será armazenado o arquivo JSON resultado dessa função.
> 

6. **Organizar arquivo com os dados de Música:**

Para extrair as informações de Música e criar o arquivo tracks_info.json foi criado a função `extract_tracks_info()`. Essa função recebe como argumento os dados extraídos do Spotify e o file_path

> file_path Local que será armazenado o arquivo JSON resultado dessa função.


## Passo a Passo da carga de dados no bucket - Arquivo [load_on_S3.py](https://github.com/LevyRamalho/etl-spotify/blob/main/load_on_S3.py)

---

1. **Criar conexão com o Serviço S3 da AWS:**

A função `conn_S3()` cria uma conexão com o serviço S3 do AWS usando a função `boto3.client` da biblioteca **boto3**. Essa função retorna a variável de conexão que será usada em outras funções.

2. **Criar bucket, caso ele não exista:**

A função `create_bucket()` é chamada caso a função que fará o upload dos arquivos identificar que o bucket não existe no S3. Essa função recebe como parâmetros a conexão com o S3 e o nome do bucket e retorna TRUE se o bucket for criado ou FALSE se ocorrer falhas.

3. **Upload dos arquivos no S3:**

Para realizar a atividade de subir os arquivos no S3, criei a função `upload_files_onS3()` que recebe como parâmetro o nome do bucket, o caminho da pasta com os arquivos que desejo subir no S3 e o nome da pasta que deve ser criada no S3.
A função primeiro verifica se o bucket já está criado no S3, em caso negativo a função chama a create_bucket() e logo depois, usando a biblioteca **OS**, a função percorre todos os arquivos existentes no diretório passado como parêmetro usando `os.listdir(folder_path)` e verifica se são arquivos utilizando `os.path.isfile(file_path)`, em caso de serem arquivos a função utiliza a `.put_object()` da biblioteca **boto** para fazer o upload dos arquivos no bucket e pasta desejado.

> file_path é uma variável contendo o caminho do arquivo usando o recurso ´os.path.join(folder_path, file_name)´ da biblioteca OS
