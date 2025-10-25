# gestor_qualidade.py

# --- Bloco de Importações ---
# Importa a biblioteca 'logging' para criar um registro (log) de todas as operações, avisos e erros.
import logging
# Importa a biblioteca 'matplotlib.pyplot' para criar e personalizar gráficos.
import matplotlib.pyplot as plt
# Importa a biblioteca 'os' para interagir com o sistema operacional e manipular caminhos de arquivos.
import os
# Importa a biblioteca 'pandas' para manipulação e análise de dados, especialmente com sua estrutura de DataFrame.
import pandas as pd
# Importa a biblioteca 're' para trabalhar com expressões regulares, usada aqui para extrair informações dos nomes dos arquivos.
import re
# Importa a biblioteca 'seaborn' para criar visualizações estatísticas mais elaboradas e esteticamente agradáveis.
import seaborn as sns
# Importa a classe 'datetime' para trabalhar com datas e horas, usada para registrar o momento da geração dos relatórios.
from datetime import datetime

# --- Definição das Funções ---

def configurar_logging(diretorio_base):
    """Configura o arquivo de log para registrar as operações e erros."""
    # Constrói o caminho completo para o arquivo de log, garantindo que ele seja salvo no mesmo diretório do script.
    caminho_log = os.path.join(diretorio_base, "registro.log")
    # Inicia a configuração básica do logging.
    logging.basicConfig(
        # Define o nível mínimo de mensagem a ser registrado (INFO captura tudo, de informações a erros).
        level=logging.INFO,
        # Define o formato da mensagem de log, incluindo data/hora, nível da mensagem e a própria mensagem.
        format='%(asctime)s - %(levelname)s - %(message)s',
        # Define os "manipuladores", ou seja, para onde as mensagens de log serão enviadas.
        handlers=[
            # FileHandler: envia as mensagens para o arquivo 'registro.log' com codificação UTF-8.
            logging.FileHandler(caminho_log, encoding='utf-8'),
            # StreamHandler: envia as mensagens também para o console (terminal) durante a execução.
            logging.StreamHandler()
        ]
    )

def carregar_parametros(caminho_parametros):
    """Lê o arquivo de parâmetros de qualidade e o transforma em um dicionário estruturado para fácil consulta."""
    # Inicializa um dicionário vazio para armazenar os parâmetros.
    parametros = {}
    # Bloco try/except para tratar erros de arquivo não encontrado ou de leitura.
    try:
        # Abre o arquivo de parâmetros em modo de leitura ('r').
        with open(caminho_parametros, 'r', encoding='utf-8') as f:
            # Variável para rastrear o produto que está sendo lido no momento.
            produto_atual = None
            # Itera sobre cada linha do arquivo.
            for linha in f:
                # Remove espaços em branco do início e do fim da linha.
                linha = linha.strip()
                # Pula linhas vazias.
                if not linha:
                    continue
                
                # Se a linha define um novo produto, atualiza a variável 'produto_atual'.
                if linha.startswith('PRODUTO:'):
                    produto_atual = linha.split(':')[1].strip()
                    # Cria uma nova entrada no dicionário para este produto.
                    parametros[produto_atual] = {}
                # Se a linha contém um parâmetro (chave: valor) e já estamos dentro de um bloco de produto.
                elif ':' in linha and produto_atual:
                    # Divide a linha em chave (ex: 'ph') e valor (ex: '6.5-7.5').
                    chave, valor = linha.split(':', 1)
                    chave = chave.strip()
                    valor = valor.strip()
                    # Se o valor representa uma faixa (contém '-'), armazena como 'min' e 'max'.
                    if '-' in valor:
                        min_val, max_val = map(float, valor.split('-'))
                        parametros[produto_atual][chave] = {'min': min_val, 'max': max_val}
                    # Se for um valor único, armazena como 'max' (ex: viscosidade_max).
                    else:
                        parametros[produto_atual][chave] = {'max': float(valor)}
        # Registra o sucesso da operação no log.
        logging.info("Parâmetros de qualidade carregados com sucesso.")
        # Retorna o dicionário com os parâmetros.
        return parametros
    # Trata o erro caso o arquivo de parâmetros não seja encontrado.
    except FileNotFoundError:
        logging.error(f"Arquivo de parâmetros não encontrado em '{caminho_parametros}'.")
        return None
    # Trata outros possíveis erros durante a leitura do arquivo.
    except Exception as e:
        logging.error(f"Erro ao ler ou processar o arquivo de parâmetros: {e}")
        return None

def processar_dados_laboratorio(diretorio_dados):
    """Lê todos os arquivos CSV do laboratório, normaliza os dados e os consolida em um único DataFrame."""
    # Dicionário para agregar os dados de múltiplos arquivos antes de criar o DataFrame final.
    dados_consolidados = {}
    
    # Itera sobre todos os arquivos na pasta de dados do laboratório.
    for nome_arquivo in os.listdir(diretorio_dados):
        # Processa apenas os arquivos que terminam com '.csv'.
        if not nome_arquivo.endswith('.csv'):
            continue
            
        # Constrói o caminho completo para o arquivo CSV.
        caminho_arquivo = os.path.join(diretorio_dados, nome_arquivo)
        # Bloco try/except para tratar erros no processamento de um arquivo individual.
        try:
            # Lê o arquivo CSV usando pandas.
            df = pd.read_csv(caminho_arquivo)
            # Normaliza os nomes das colunas para minúsculas e remove espaços para facilitar o acesso.
            df.columns = [col.lower().strip() for col in df.columns]
            
            # Renomeia diferentes variações de colunas de ID para um padrão único 'lote_id'.
            df.rename(columns={'id_lote': 'lote_id', 'lote': 'lote_id'}, inplace=True)

            # Verifica se o arquivo tem uma coluna de ID de lote; se não, pula o arquivo.
            if 'lote_id' not in df.columns:
                logging.warning(f"Arquivo '{nome_arquivo}' ignorado: não contém uma coluna de ID de lote.")
                continue

            # Usa expressão regular para extrair o tipo de teste (visco, ph, etc.) do nome do arquivo.
            tipo_teste_match = re.search(r'^(visco|ph|densidade)', nome_arquivo, re.IGNORECASE)
            if not tipo_teste_match:
                logging.warning(f"Não foi possível determinar o tipo de teste para o arquivo '{nome_arquivo}'.")
                continue
            
            # Obtém o nome do teste normalizado (ex: 'visco').
            tipo_teste = tipo_teste_match.group(1).lower()
            # Encontra o nome da coluna que contém o valor do teste (ex: 'valor_ph', 'viscosidade').
            nome_coluna_valor = next((col for col in df.columns if tipo_teste in col), None)

            # Se não encontrar uma coluna de valor, pula o arquivo.
            if not nome_coluna_valor:
                logging.warning(f"Não foi possível encontrar a coluna de valor para o teste '{tipo_teste}' no arquivo '{nome_arquivo}'.")
                continue

            # Itera sobre as linhas do DataFrame do arquivo atual.
            for _, row in df.iterrows():
                lote_id = row['lote_id']
                valor = row[nome_coluna_valor]
                # Se o lote ainda não está no dicionário consolidado, cria uma nova entrada.
                if lote_id not in dados_consolidados:
                    dados_consolidados[lote_id] = {'lote_id': lote_id}
                # Adiciona o resultado do teste atual ao dicionário do lote.
                dados_consolidados[lote_id][tipo_teste] = valor
            
            # Registra o sucesso no processamento do arquivo.
            logging.info(f"Arquivo '{nome_arquivo}' processado com sucesso.")

        # Trata qualquer erro que possa ocorrer durante o processamento do arquivo.
        except Exception as e:
            logging.error(f"Erro ao processar o arquivo '{nome_arquivo}': {e}")
            
    # Se nenhum dado foi consolidado, retorna um DataFrame vazio.
    if not dados_consolidados:
        logging.warning("Nenhum dado de lote foi consolidado.")
        return pd.DataFrame()

    # Converte o dicionário de dados consolidados em um DataFrame do pandas.
    return pd.DataFrame(list(dados_consolidados.values()))

def analisar_conformidade(df_dados, parametros):
    """Compara os dados consolidados com os parâmetros de qualidade e identifica não conformidades."""
    # Lista para armazenar os resultados da análise.
    resultados = []
    # Itera sobre cada lote no DataFrame de dados consolidados.
    for _, lote in df_dados.iterrows():
        lote_id = lote['lote_id']
        # Extrai o código do produto do ID do lote (ex: 'SXT' de 'SXT-101A').
        codigo_produto_match = re.search(r'^([A-Z]+)', lote_id)
        if not codigo_produto_match:
            logging.warning(f"Não foi possível extrair o código do produto do lote '{lote_id}'.")
            continue
            
        # Mapeamento para converter o código extraído no nome completo do produto.
        mapa_codigos = {'SXT': 'SHAMPOO_XT', 'CND': 'CONDICIONADOR_Y', 'SBZ': 'SABONETE_Z'}
        codigo = codigo_produto_match.group(1)
        nome_produto = mapa_codigos.get(codigo)
        
        # Se o produto não for reconhecido ou não tiver parâmetros, pula o lote.
        if not nome_produto or nome_produto not in parametros:
            logging.warning(f"Lote '{lote_id}' ignorado: produto '{nome_produto}' sem parâmetros de qualidade definidos.")
            continue

        # Obtém os parâmetros específicos para este produto.
        param_produto = parametros[nome_produto]
        
        # Itera sobre cada teste realizado para o lote.
        for teste, valor_medido in lote.items():
            # Pula a coluna 'lote_id' e valores nulos.
            if teste == 'lote_id' or pd.isna(valor_medido):
                continue

            # Normaliza o nome do teste para corresponder às chaves do dicionário de parâmetros.
            teste_param = 'viscosidade' if 'visco' in teste else teste
            
            # Verifica se existe um parâmetro definido para este teste.
            if teste_param in param_produto:
                padrao = param_produto[teste_param]
                # Assume que o lote está conforme por padrão.
                status = "Conforme"
                observacao = ""
                
                # Verifica se o valor está abaixo do mínimo permitido.
                if 'min' in padrao and valor_medido < padrao['min']:
                    status = "NÃO CONFORME"
                    observacao = f"Abaixo do mínimo ({padrao['min']})"
                # Verifica se o valor está acima do máximo permitido.
                if 'max' in padrao and valor_medido > padrao['max']:
                    status = "NÃO CONFORME"
                    observacao = f"Acima do máximo ({padrao['max']})"
                
                # Adiciona o resultado detalhado da análise à lista de resultados.
                resultados.append({
                    'lote_id': lote_id,
                    'produto': nome_produto,
                    'teste': teste.upper(),
                    'valor_medido': valor_medido,
                    'status': status,
                    'observacao': observacao
                })
    # Converte a lista de resultados em um DataFrame.
    return pd.DataFrame(resultados)

def gerar_relatorios_e_estatisticas(df_analise, diretorio_base):
    """Gera os relatórios textuais (CSV, TXT) e o arquivo de estatísticas descritivas."""
    # Bloco try/except para tratar erros de escrita de arquivos.
    try:
        # --- Relatório 1: CSV com todos os resultados do turno ---
        caminho_consolidado = os.path.join(diretorio_base, 'relatorio_consolidado_turno.csv')
        # Salva o DataFrame de análise em um arquivo CSV, usando ';' como separador e ',' como decimal.
        df_analise.to_csv(caminho_consolidado, index=False, sep=';', decimal=',')
        logging.info(f"Relatório consolidado salvo em: {caminho_consolidado}")

        # --- Relatório 2: TXT apenas com as não conformidades ---
        df_nao_conformes = df_analise[df_analise['status'] == 'NÃO CONFORME']
        caminho_nao_conformes = os.path.join(diretorio_base, 'relatorio_nao_conformes.txt')
        # Abre o arquivo de texto para escrita.
        with open(caminho_nao_conformes, 'w', encoding='utf-8') as f:
            # Escreve o cabeçalho do relatório.
            f.write("RELATÓRIO DE NÃO CONFORMIDADES - CONTROLE DE QUALIDADE\n")
            f.write(f"Data de Geração: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write("="*60 + "\n\n")

            # Se não houver não conformidades, escreve uma mensagem informativa.
            if df_nao_conformes.empty:
                f.write("Nenhuma não conformidade encontrada no período.\n")
            # Se houver, itera sobre cada uma e a formata no arquivo.
            else:
                for _, linha in df_nao_conformes.iterrows():
                    f.write(f"LOTE: {linha['lote_id']} (Produto: {linha['produto']})\n")
                    f.write(f"  - TESTE: {linha['teste']}\n")
                    f.write(f"  - VALOR MEDIDO: {linha['valor_medido']}\n")
                    f.write(f"  - OBSERVAÇÃO: {linha['observacao']}\n\n")
        logging.info(f"Relatório de não conformidades salvo em: {caminho_nao_conformes}")

        # --- ETAPA 1 (NOVA): Geração do arquivo de estatísticas descritivas ---
        # Agrupa os dados por produto e teste, e calcula estatísticas (contagem, média, desvio padrão, etc.).
        estatisticas = df_analise.groupby(['produto', 'teste'])['valor_medido'].describe()
        caminho_estatisticas = os.path.join(diretorio_base, 'estatisticas_produtos.txt')
        # Abre o arquivo de estatísticas para escrita.
        with open(caminho_estatisticas, 'w', encoding='utf-8') as f:
            f.write("ESTATÍSTICAS DESCRITIVAS POR PRODUTO E TIPO DE TESTE\n")
            f.write(f"Data de Geração: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write("="*70 + "\n\n")
            # Escreve a tabela de estatísticas no arquivo.
            f.write(estatisticas.to_string())
        logging.info(f"Arquivo de estatísticas salvo em: {caminho_estatisticas}")

    # Trata erros de permissão ao tentar salvar os arquivos.
    except PermissionError:
        logging.error("Erro de permissão ao tentar salvar os relatórios. Verifique as permissões da pasta.")
    # Trata outros erros inesperados.
    except Exception as e:
        logging.error(f"Erro inesperado ao gerar relatórios ou estatísticas: {e}")

def gerar_graficos(df_analise, parametros, diretorio_base):
    """Gera os gráficos de dispersão e boxplot para análise visual dos dados."""
    # Registra o início da geração de gráficos.
    logging.info("Iniciando a geração de gráficos...")
    
    # Define paletas de cores para manter a consistência visual entre os gráficos.
    cores_testes = {'PH': 'gold', 'DENSIDADE': 'blue', 'VISCO': 'purple'}
    cores_produtos = {'SHAMPOO_XT': 'blue', 'SABONETE_Z': 'green', 'CONDICIONADOR_Y': 'yellow'}

    # --- ETAPAS 2 e 3 (NOVAS): Gráficos de Dispersão por Produto ---
    # Obtém a lista de produtos únicos que foram analisados.
    produtos_unicos = df_analise['produto'].unique()
    # Itera sobre cada produto para criar um gráfico de dispersão separado.
    for produto in produtos_unicos:
        # Filtra o DataFrame para conter apenas os dados do produto atual.
        df_produto = df_analise[df_analise['produto'] == produto]
        
        # Obtém os testes realizados para este produto específico.
        testes_no_produto = df_produto['teste'].unique()
        # Cria uma figura com subplots; o número de subplots depende de quantos testes foram feitos.
        fig, axes = plt.subplots(len(testes_no_produto), 1, figsize=(15, 6 * len(testes_no_produto)), sharex=True)
        # Garante que 'axes' seja sempre uma lista, mesmo que haja apenas um subplot.
        if len(testes_no_produto) == 1: axes = [axes]
        
        # Define um título geral para a figura.
        fig.suptitle(f'Análise de Dispersão de Lotes - {produto}', fontsize=16, y=0.95)

        # Itera sobre cada teste para criar seu respectivo subplot.
        for i, teste in enumerate(testes_no_produto):
            df_teste = df_produto[df_produto['teste'] == teste]
            ax = axes[i]
            
            # Cria o gráfico de dispersão (scatterplot) no subplot correspondente.
            sns.scatterplot(data=df_teste, x='lote_id', y='valor_medido', ax=ax, color=cores_testes.get(teste, 'black'), s=100, label='Medição')
            # Rotaciona os rótulos do eixo X (nomes dos lotes) para evitar sobreposição.
            ax.tick_params(axis='x', rotation=45)
            # Define o título e os rótulos do subplot.
            ax.set_title(f'Análise de {teste}')
            ax.set_ylabel('Valor Medido')
            ax.grid(True, linestyle='--', alpha=0.6)

            # --- ETAPA 4 (NOVA): Adiciona linhas de Mínimo e Máximo ---
            param_teste = 'viscosidade' if 'VISCO' in teste else teste.lower()
            # Verifica se existem parâmetros definidos para este teste e produto.
            if produto in parametros and param_teste in parametros[produto]:
                limites = parametros[produto][param_teste]
                # Se houver um limite mínimo, desenha uma linha horizontal vermelha.
                if 'min' in limites:
                    ax.axhline(y=limites['min'], color='red', linestyle='--', label=f'Mínimo ({limites["min"]})')
                # Se houver um limite máximo, desenha uma linha horizontal vermelha.
                if 'max' in limites:
                    ax.axhline(y=limites['max'], color='red', linestyle='--', label=f'Máximo ({limites["max"]})')
            # Adiciona a legenda ao subplot.
            ax.legend()

        # Ajusta o layout para evitar que o título principal sobreponha os subplots.
        plt.tight_layout(rect=[0, 0, 1, 0.93])
        # Constrói o nome do arquivo de saída e salva o gráfico.
        caminho_grafico = os.path.join(diretorio_base, f'dispersao_{produto}.png')
        plt.savefig(caminho_grafico)
        # Fecha a figura para liberar memória.
        plt.close(fig)
        logging.info(f"Gráfico de dispersão para '{produto}' salvo em: {caminho_grafico}")

    # --- ETAPAS 2 e 3 (NOVAS): Gráficos Boxplot por Tipo de Análise ---
    # Obtém a lista de todos os tipos de testes realizados.
    testes_unicos = df_analise['teste'].unique()
    # Itera sobre cada tipo de teste para criar um gráfico boxplot.
    for teste in testes_unicos:
        # Cria uma nova figura para o boxplot.
        plt.figure(figsize=(10, 7))
        # Filtra o DataFrame para conter apenas os dados do teste atual.
        df_teste = df_analise[df_analise['teste'] == teste]

        # Cria o gráfico boxplot, mostrando a distribuição dos valores por produto.
        ax = sns.boxplot(data=df_teste, x='produto', y='valor_medido', palette=cores_produtos)
        # Define o título e os rótulos do gráfico.
        plt.title(f'Box Plot de Resultados - {teste}', fontsize=16)
        plt.xlabel('Tipo de Produto')
        plt.ylabel('Valor Medido')

        # --- ETAPA 4 (NOVA): Adiciona linhas de Mínimo e Máximo ao Boxplot ---
        param_teste = 'viscosidade' if 'VISCO' in teste else teste.lower()
        # Itera sobre os produtos no eixo X para desenhar suas respectivas linhas de limite.
        for i, produto in enumerate(ax.get_xticklabels()):
            nome_produto = produto.get_text()
            if nome_produto in parametros and param_teste in parametros[nome_produto]:
                limites = parametros[nome_produto][param_teste]
                # Desenha as linhas de limite na largura da caixa do boxplot.
                if 'min' in limites:
                    plt.hlines(limites['min'], i - 0.4, i + 0.4, color='red', linestyle='--', label='Limite Mín/Máx' if i==0 else "")
                if 'max' in limites:
                    plt.hlines(limites['max'], i - 0.4, i + 0.4, color='red', linestyle='--')
        
        # Bloco para garantir que a legenda "Limite Mín/Máx" apareça apenas uma vez no gráfico.
        handles, labels = plt.gca().get_legend_handles_labels()
        if labels:
            by_label = dict(zip(labels, handles))
            plt.legend(by_label.values(), by_label.keys())

        # Constrói o nome do arquivo e salva o gráfico boxplot.
        caminho_grafico = os.path.join(diretorio_base, f'boxplot_{teste}.png')
        plt.savefig(caminho_grafico)
        # Fecha a figura para liberar memória.
        plt.close()
        logging.info(f"Gráfico boxplot para '{teste}' salvo em: {caminho_grafico}")

# --- Bloco de Execução Principal ---
# A condição 'if __name__ == "__main__"' garante que o código abaixo só será executado
# quando o script for rodado diretamente (e não quando importado por outro script).
if __name__ == "__main__":
    # Obtém o caminho absoluto da pasta onde o script está localizado.
    diretorio_script = os.path.dirname(os.path.abspath(__file__))
    # Inicia e configura o sistema de logging.
    configurar_logging(diretorio_script)

    # Registra o início da execução do script.
    logging.info("--- INICIANDO SCRIPT DE GESTÃO DE QUALIDADE ---")

    # Define o nome da pasta onde os dados de entrada estão.
    pasta_dados_nome = "dados_laboratorio"
    # Constrói o caminho completo para a pasta de dados.
    caminho_dados = os.path.join(diretorio_script, pasta_dados_nome)
    
    # Verifica se a pasta de dados realmente existe.
    if not os.path.isdir(caminho_dados):
        logging.error(f"A pasta de dados '{caminho_dados}' não foi encontrada. Verifique a estrutura de pastas.")
    else:
        # Constrói o caminho para o arquivo de parâmetros.
        caminho_params = os.path.join(caminho_dados, 'parametros_qualidade.txt')
        # Carrega os parâmetros de qualidade.
        parametros_qualidade = carregar_parametros(caminho_params)

        # Se os parâmetros foram carregados com sucesso, continua o processo.
        if parametros_qualidade:
            # Processa os arquivos do laboratório e consolida os dados.
            df_dados_brutos = processar_dados_laboratorio(caminho_dados)
            # Se dados foram encontrados e processados, continua.
            if not df_dados_brutos.empty:
                # Realiza a análise de conformidade.
                df_resultado_analise = analisar_conformidade(df_dados_brutos, parametros_qualidade)
                # Gera os relatórios textuais e o arquivo de estatísticas.
                gerar_relatorios_e_estatisticas(df_resultado_analise, diretorio_script)
                # Gera os gráficos para análise visual.
                gerar_graficos(df_resultado_analise, parametros_qualidade, diretorio_script)

    # Registra a finalização do script.
    logging.info("--- SCRIPT DE GESTÃO DE QUALIDADE FINALIZADO ---")