# interpretador_dados.py

# --- Bloco de Importações ---
# Importa a biblioteca 'logging' para criar um registro (log) de eventos e erros durante a execução.
import logging
# Importa a biblioteca matplotlib.pyplot para personalização de gráficos, apelidada como 'plt'.
import matplotlib.pyplot as plt
# Importa a biblioteca 'os' para interagir com o sistema operacional e para manipular caminhos de arquivos.
import os
# Importa a biblioteca pandas, essencial para manipulação e análise de dados, apelidada como 'pd'.
import pandas as pd
# Importa a biblioteca seaborn para criação de gráficos estatísticos mais atraentes, apelidada como 'sns'.
import seaborn as sns
# Importa o módulo 'stats' da biblioteca scipy para realizar cálculos estatísticos, como a correlação.
from scipy import stats


# --- Definição das Funções ---

def configurar_logging(diretorio_base):
    """Configura o arquivo de log para registrar as operações."""
    # Constrói o caminho completo para o arquivo de log, garantindo que ele seja salvo no mesmo diretório do script.
    caminho_log = os.path.join(diretorio_base, "registro.log")
    # Inicia a configuração básica do logging.
    logging.basicConfig(
        # Define o nível mínimo de mensagem a ser registrado (INFO captura tudo, de informações a erros).
        level=logging.INFO,
        # Define o formato da mensagem de log, incluindo data/hora, nível (INFO, ERROR) e a mensagem.
        format='%(asctime)s - %(levelname)s - %(message)s',
        # Define os "manipuladores", ou seja, para onde as mensagens de log serão enviadas.
        handlers=[
            # Envia o log para um arquivo, com codificação 'utf-8' para suportar caracteres especiais.
            logging.FileHandler(caminho_log, encoding='utf-8'),
            # Envia o log também para o console (terminal) onde o script é executado.
            logging.StreamHandler()
        ]
    )

def main():
    """Função principal para executar todo o processo de análise de dados."""
    # Obtém o caminho absoluto da pasta onde o script está localizado. Isso torna o script portátil.
    diretorio_script = os.path.dirname(os.path.abspath(__file__))
    # Chama a função para configurar e iniciar o sistema de logging.
    configurar_logging(diretorio_script)
    
    # Registra o início do processo no arquivo de log e no console.
    logging.info("--- INICIANDO PROCESSO DE ANÁLISE DE DADOS DE CLIENTES ---")
    
    # Constrói os caminhos completos e seguros para os arquivos de entrada (CSV e JSON).
    caminho_csv = os.path.join(diretorio_script, 'clientes.csv')
    caminho_json = os.path.join(diretorio_script, 'compras.json')
    
    # Inicia um bloco 'try...except' para capturar e tratar possíveis erros durante a execução.
    try:
        # --- Etapa 1: Leitura dos arquivos ---
        # Registra a tentativa de leitura do arquivo CSV.
        logging.info(f"Lendo arquivo CSV de: {caminho_csv}")
        # Usa o pandas para ler o arquivo CSV e carregá-lo em um DataFrame.
        df_clientes = pd.read_csv(caminho_csv)
        
        # Registra a tentativa de leitura do arquivo JSON.
        logging.info(f"Lendo arquivo JSON de: {caminho_json}")
        # Lê o arquivo JSON e, em seguida, renomeia uma coluna para padronizar o nome.
        df_compras = pd.read_json(caminho_json).rename(columns={'Pontuacao_Satisfacao': 'Pontuação_Satisfação'})
        
        # --- Etapa 2: Junção dos DataFrames ---
        # Registra a operação de junção dos dados.
        logging.info("Juntando os dados dos arquivos CSV e JSON.")
        # Usa a função 'merge' do pandas para combinar os dois DataFrames.
        # A junção é feita usando a coluna 'ID_Cliente' como chave comum.
        df = pd.merge(df_clientes, df_compras, on="ID_Cliente")
        
        # Registra que a preparação dos dados foi concluída com sucesso.
        logging.info("Dados consolidados com sucesso. Iniciando análises e geração de gráficos.")
        
        # --- Bloco de Análise e Visualização ---
        
        # Calcula estatísticas descritivas (média, desvio padrão, etc.) do DataFrame consolidado.
        summary_stats = df.describe()
        # Registra as estatísticas no log. '.to_string()' formata o output para melhor leitura.
        logging.info("Estatísticas descritivas geradas:\n" + summary_stats.to_string())
        
        # --- Gráfico 1: Histograma de Idade ---
        # Cria uma nova figura para o gráfico com um tamanho específico.
        plt.figure(figsize=(10, 6))
        # Usa o seaborn para criar um histograma da coluna 'Idade', com 10 barras (bins) e uma linha de densidade (kde).
        sns.histplot(df['Idade'], bins=10, kde=True)
        # Define o título e os rótulos dos eixos do gráfico.
        plt.title('Distribuição de Idade dos Clientes')
        plt.xlabel('Idade')
        plt.ylabel('Contagem')
        # Constrói o caminho completo para salvar a imagem do gráfico.
        caminho_grafico1 = os.path.join(diretorio_script, 'grafico_distribuicao_idade.png')
        # Salva a figura gerada como um arquivo PNG no caminho especificado.
        plt.savefig(caminho_grafico1)
        # Fecha a figura atual para liberar a memória do sistema antes de criar a próxima.
        plt.close()
        # Registra que o gráfico foi salvo com sucesso.
        logging.info(f"Gráfico de distribuição de idade salvo em: {caminho_grafico1}")
        
        # --- Gráfico 2: Gráfico de Dispersão ---
        plt.figure(figsize=(10, 6))
        # Cria um gráfico de dispersão (scatterplot) para analisar a relação entre 'Idade' e 'Pontuação_Satisfação'.
        # 'hue' colore os pontos com base no 'Salario', e 'size' ajusta o tamanho dos pontos com base no 'Valor_Gasto'.
        sns.scatterplot(data=df, x='Idade', y='Pontuação_Satisfação', hue='Salario', size='Valor_Gasto', palette='coolwarm', sizes=(50, 500))
        plt.title('Dispersão: Idade vs. Satisfação por Salário e Valor Gasto')
        plt.xlabel('Idade')
        plt.ylabel('Índice de Satisfação')
        caminho_grafico2 = os.path.join(diretorio_script, 'grafico_dispersao.png')
        plt.savefig(caminho_grafico2)
        plt.close()
        logging.info(f"Gráfico de dispersão salvo em: {caminho_grafico2}")

        # --- Análise de Correlação ---
        # Calcula a correlação de Pearson entre 'Idade' e 'Pontuação_Satisfação'.
        correlation, p_value = stats.pearsonr(df['Idade'], df['Pontuação_Satisfação'])
        # Registra o resultado da correlação no log.
        logging.info(f"Análise de Correlação (Idade vs. Satisfação): Correlação={correlation:.2f}, Valor-p={p_value:.4f}")
        # Imprime o resultado também no console para visualização imediata.
        print(f'Correlação: {correlation:.2f}')
        print(f'Valor-p: {p_value:.4f}')

        # --- Gráfico 3: Box Plot ---
        plt.figure(figsize=(12, 7))
        # Cria uma nova coluna 'Faixa_Etaria' agrupando as idades em categorias para um boxplot mais claro.
        df['Faixa_Etaria'] = pd.cut(df['Idade'], bins=[20, 30, 40, 50], labels=['20-30', '31-40', '41-50'])
        # Cria um boxplot para visualizar a distribuição da 'Pontuação_Satisfação' em cada 'Faixa_Etaria'.
        sns.boxplot(data=df, x='Faixa_Etaria', y='Pontuação_Satisfação')
        plt.title('Box Plot: Satisfação por Faixa Etária')
        plt.xlabel('Faixa Etária')
        plt.ylabel('Índice de Satisfação')
        caminho_grafico3 = os.path.join(diretorio_script, 'grafico_boxplot_satisfacao.png')
        plt.savefig(caminho_grafico3)
        plt.close()
        logging.info(f"Gráfico de Box Plot salvo em: {caminho_grafico3}")

    # --- Etapa 5: Tratamento de Erros ---
    # Captura o erro específico que ocorre se um arquivo de entrada não for encontrado.
    except FileNotFoundError as e:
        logging.error(f"ERRO: Arquivo não encontrado. Verifique se os arquivos 'clientes.csv' e 'compras.json' estão no diretório correto. Detalhe: {e}")
    # Captura o erro que ocorre se o script não tiver permissão de leitura ou escrita na pasta.
    except PermissionError as e:
        logging.error(f"ERRO: Sem permissão para ler os arquivos de entrada ou salvar os gráficos/log. Verifique as permissões da pasta. Detalhe: {e}")
    # Captura o erro que ocorre se uma coluna essencial (ex: 'ID_Cliente') não for encontrada nos arquivos.
    except KeyError as e:
        logging.error(f"ERRO: Uma coluna esperada não foi encontrada nos arquivos de dados. Verifique os nomes das colunas. Detalhe: {e}")
    # Captura qualquer outro tipo de erro inesperado que possa ocorrer.
    except Exception as e:
        logging.error(f"Ocorreu um erro inesperado durante a execução: {e}")
    # O bloco 'finally' é executado sempre, independentemente de ter ocorrido um erro ou não.
    finally:
        # Registra a finalização do processo.
        logging.info("--- PROCESSO DE ANÁLISE FINALIZADO ---")

# --- Ponto de Entrada do Script ---
# A condição 'if __name__ == "__main__"' garante que a função 'main()' só será executada
# quando o script for rodado diretamente (e não quando for importado por outro script).
if __name__ == "__main__":
    main()