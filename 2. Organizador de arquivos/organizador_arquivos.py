# organizador_arquivos.py

# --- Bloco de Importações ---
# Importa a biblioteca 'logging' para criar um registro (log) de todas as operações e erros que ocorrem durante a execução.
import logging
# Importa a biblioteca 'os' para interagir com o sistema operacional, como criar pastas e manipular caminhos de arquivos.
import os
# Importa a biblioteca 'shutil' que oferece operações de alto nível em arquivos, como mover arquivos de um local para outro.
import shutil
# Importa a classe 'datetime' da biblioteca 'datetime' para trabalhar com datas e horas, como obter a data de criação de um arquivo.
from datetime import datetime

# --- Definição das Funções ---

def configurar_logging(diretorio_base):
    """Configura o arquivo de log para registrar as operações."""
    # Constrói o caminho completo onde o arquivo de log será salvo, juntando o diretório base com o nome 'registro.log'.
    caminho_log = os.path.join(diretorio_base, "registro.log")
    # Configura o sistema de logging.
    logging.basicConfig(
        # Define o nível mínimo de mensagem a ser registrado (INFO captura informações gerais, avisos e erros).
        level=logging.INFO,
        # Define o formato de cada linha de log, incluindo data/hora, nível da mensagem e a mensagem em si.
        format='%(asctime)s - %(levelname)s - %(message)s',
        # Define os "manipuladores" de log, ou seja, para onde as mensagens de log serão enviadas.
        handlers=[
            # FileHandler: envia as mensagens para o arquivo 'registro.log' com codificação UTF-8.
            logging.FileHandler(caminho_log, encoding='utf-8'),
            # StreamHandler: envia as mensagens também para o console (terminal) onde o script está sendo executado.
            logging.StreamHandler()
        ]
    )

def obter_mapeamento_pastas():
    """Retorna um dicionário que mapeia extensões de arquivos para pastas de destino e tipos de mídia."""
    # Cria e retorna um dicionário. A chave é a extensão do arquivo (ex: '.jpg').
    # O valor é uma tupla contendo o nome da pasta de destino e o tipo de mídia para o novo nome do arquivo.
    return {
        # Mapeamento para Imagens
        '.jpg': ('Imagens', 'Imagem'),
        '.jpeg': ('Imagens', 'Imagem'),
        '.png': ('Imagens', 'Imagem'),
        '.gif': ('Imagens', 'Imagem'),
        '.bmp': ('Imagens', 'Imagem'),
        '.svg': ('Imagens', 'Imagem'),
        # Mapeamento para Vídeos
        '.mp4': ('Vídeos', 'Vídeo'),
        '.mov': ('Vídeos', 'Vídeo'),
        '.avi': ('Vídeos', 'Vídeo'),
        '.mkv': ('Vídeos', 'Vídeo'),
        # Mapeamento para Documentos
        '.doc': ('Documentos', 'Documento'),
        '.docx': ('Documentos', 'Documento'),
        '.pdf': ('Documentos', 'Documento'),
        '.txt': ('Documentos', 'Documento'),
        # Mapeamento para Apresentações
        '.ppt': ('Apresentações', 'Apresentação'),
        '.pptx': ('Apresentações', 'Apresentação'),
    }

def organizar_arquivos(diretorio_origem, diretorio_base):
    """
    Organiza e renomeia arquivos do diretório de origem para subpastas no diretório base.
    """
    # Obtém o dicionário de mapeamento de extensões para pastas.
    mapeamento = obter_mapeamento_pastas()
    # Inicializa um dicionário vazio para contar os arquivos por tipo e data, garantindo identificadores únicos.
    contadores = {}

    # Itera sobre cada nome de arquivo/pasta encontrado dentro do diretório de origem.
    for nome_arquivo in os.listdir(diretorio_origem):
        # Constrói o caminho completo para o arquivo atual.
        caminho_antigo = os.path.join(diretorio_origem, nome_arquivo)

        # Verifica se o caminho atual é um arquivo. Se for um diretório, pula para o próximo item.
        if not os.path.isfile(caminho_antigo):
            continue

        # Inicia um bloco 'try...except' para tratar possíveis erros durante o processamento de um arquivo.
        try:
            # Divide o nome do arquivo em nome base e extensão (ex: 'relatorio', '.docx').
            _, extensao = os.path.splitext(nome_arquivo)
            # Converte a extensão para letras minúsculas para garantir que '.JPG' e '.jpg' sejam tratados da mesma forma.
            extensao = extensao.lower()

            # Verifica se a extensão do arquivo atual existe como chave no dicionário de mapeamento.
            if extensao in mapeamento:
                # Se existir, obtém o nome da pasta de destino e o tipo de mídia associados à extensão.
                pasta_destino, tipo_media = mapeamento[extensao]
                # Constrói o caminho completo para a pasta de destino (ex: 'C:/Projeto/Imagens').
                caminho_pasta_destino = os.path.join(diretorio_base, pasta_destino)

                # Cria a pasta de destino, caso ela ainda não exista. 'exist_ok=True' evita erros se a pasta já existir.
                os.makedirs(caminho_pasta_destino, exist_ok=True)

                # Obtém o timestamp (número de segundos desde uma data de referência) da data de criação do arquivo.
                timestamp_criacao = os.path.getctime(caminho_antigo)
                # Converte o timestamp para um objeto de data e hora legível.
                data_criacao = datetime.fromtimestamp(timestamp_criacao)
                # Formata o objeto de data para o padrão brasileiro dia-mês-ano (ex: '15-10-2025').
                data_formatada = data_criacao.strftime('%d-%m-%Y')

                # Cria uma chave única para o contador baseada na data e no tipo de mídia (ex: '15-10-2025_Imagem').
                chave_contador = f"{data_formatada}_{tipo_media}"
                
                # Obtém o valor atual do contador para essa chave (ou 0 se não existir) e adiciona 1.
                contadores[chave_contador] = contadores.get(chave_contador, 0) + 1
                # Armazena o novo número do contador como o identificador único do arquivo.
                identificador_unico = contadores[chave_contador]

                # Monta a string do novo nome do arquivo no formato padrão.
                # '{identificador_unico:03d}' formata o número para ter sempre 3 dígitos com zeros à esquerda (ex: 1 -> 001).
                novo_nome = f"{data_formatada}_{tipo_media}_{identificador_unico:03d}{extensao}"
                # Constrói o caminho completo de destino para o arquivo com o novo nome.
                caminho_novo = os.path.join(caminho_pasta_destino, novo_nome)
                
                # Loop de verificação para o caso (muito raro) de um arquivo com o mesmo nome já existir.
                while os.path.exists(caminho_novo):
                    # Registra um aviso no log informando sobre a duplicata.
                    logging.warning(f"Nome duplicado encontrado: {caminho_novo}. Tentando novo identificador.")
                    # Incrementa o identificador para tentar o próximo número (ex: 001 -> 002).
                    identificador_unico += 1
                    # Atualiza o contador global para que o próximo arquivo do mesmo tipo não repita este número.
                    contadores[chave_contador] = identificador_unico
                    # Recria o novo nome e o novo caminho com o identificador atualizado.
                    novo_nome = f"{data_formatada}_{tipo_media}_{identificador_unico:03d}{extensao}"
                    caminho_novo = os.path.join(caminho_pasta_destino, novo_nome)

                # Move o arquivo do seu local original para o novo local com o novo nome.
                shutil.move(caminho_antigo, caminho_novo)
                # Registra uma mensagem de sucesso no log informando a operação realizada.
                logging.info(f"'{nome_arquivo}' movido e renomeado para '{caminho_novo}'")

            else:
                # Se a extensão do arquivo não estiver no mapeamento, registra um aviso e o arquivo é ignorado.
                logging.warning(f"Arquivo '{nome_arquivo}' ignorado: extensão '{extensao}' não mapeada.")

        # Captura erros específicos que podem ocorrer.
        except PermissionError:
            # Se o script não tiver permissão para ler/mover o arquivo, registra um erro.
            logging.error(f"Erro de permissão ao tentar mover o arquivo '{nome_arquivo}'. Verifique as permissões.")
        except FileNotFoundError:
            # Se o arquivo for deletado durante a execução, registra um erro.
            logging.error(f"Arquivo '{nome_arquivo}' não encontrado. Pode ter sido movido ou deletado durante a execução.")
        except Exception as e:
            # Captura qualquer outro erro inesperado, registra a mensagem de erro e continua o script.
            logging.error(f"Ocorreu um erro inesperado ao processar '{nome_arquivo}': {e}")


# --- Bloco de Execução Principal ---
# Este bloco só é executado quando o script é rodado diretamente.
if __name__ == "__main__":
    # Obtém o caminho absoluto da pasta onde o script 'organizador_arquivos.py' está localizado.
    diretorio_base_script = os.path.dirname(os.path.abspath(__file__))
    
    # Chama a função para configurar o logging, garantindo que o 'registro.log' seja criado no mesmo diretório.
    configurar_logging(diretorio_base_script)
    
    # Define o nome da pasta que contém os arquivos a serem organizados.
    pasta_origem_nome = "exemplos_arquivos"
    # Constrói o caminho completo para a pasta de origem.
    caminho_origem = os.path.join(diretorio_base_script, pasta_origem_nome)

    # Registra o início da execução no log.
    logging.info("--- INICIANDO SCRIPT DE ORGANIZAÇÃO DE ARQUIVOS ---")

    # Verifica se o caminho de origem é de fato um diretório existente.
    if os.path.isdir(caminho_origem):
        # Se o diretório existir, chama a função principal para iniciar o processo de organização.
        organizar_arquivos(caminho_origem, diretorio_base_script)
        # Registra a finalização bem-sucedida do processo.
        logging.info("--- SCRIPT DE ORGANIZAÇÃO FINALIZADO ---")
    else:
        # Se o diretório não for encontrado, registra uma mensagem de erro crítica e encerra o script.
        logging.error(f"A pasta de origem '{caminho_origem}' não foi encontrada. Verifique o nome e a localização da pasta.")