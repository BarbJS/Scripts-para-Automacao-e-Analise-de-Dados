# conversor_vendas.py

import csv  # Importa o módulo para trabalhar com arquivos CSV.
import json  # Importa o módulo para trabalhar com dados no formato JSON.
import os  # Importa o módulo para interagir com o sistema operacional, como manipular caminhos de arquivos.
import xml.etree.ElementTree as ET  # Importa o módulo para criar e manipular arquivos XML.
from datetime import datetime  # Importa a classe datetime para trabalhar com datas e horas.
from xml.dom import minidom  # Importa o minidom para formatar (pretty-print) o XML.

def processar_vendas(caminho_arquivo_txt):
    """
    Lê um arquivo TXT de vendas, processa os dados e retorna uma lista de dicionários.
    """
    vendas = []
    # Captura a data e hora atual para o campo 'data_importacao'
    data_importacao = datetime.now()  # Pega a data e hora exatas do momento da execução.
    # Formata a data de importação para o padrão brasileiro
    data_importacao_formatada = data_importacao.strftime('%d/%m/%Y')  # Formata a data para o formato Dia/Mês/Ano.

    # Abre o arquivo de texto no modo de leitura ('r') com codificação 'utf-8' para suportar caracteres especiais.
    with open(caminho_arquivo_txt, mode='r', encoding='utf-8') as arquivo_txt:  
        leitor_csv = csv.reader(arquivo_txt)  # Cria um leitor de CSV para iterar sobre as linhas do arquivo.
        for linha in leitor_csv:  # Itera sobre cada linha do arquivo de vendas.
            # Extração e limpeza dos dados de cada linha
            id_produto = int(linha[0])  # Converte o primeiro elemento (ID do produto) para um número inteiro.
            nome_produto = linha[1].strip()  # Pega o segundo elemento (nome) e remove espaços em branco extras.
            quantidade = int(linha[2])  # Converte o terceiro elemento (quantidade) para um número inteiro.
            preco_unitario = float(linha[3])  # Converte o quarto elemento (preço) para um número de ponto flutuante.
            # Converte a string da data da venda para um objeto datetime
            data_venda = datetime.strptime(linha[4].strip(), '%Y-%m-%d')  # Converte a string de data (Ano-Mês-Dia) para um objeto datetime.

            # Cria um dicionário para armazenar os dados processados da venda.
            venda = {
                "id_produto": id_produto,  # Armazena o ID do produto.
                "nome_produto": nome_produto,  # Armazena o nome do produto.
                "quantidade": quantidade,  # Armazena a quantidade vendida.
                "preco_unitario": preco_unitario,  # Armazena o preço por unidade.
                # Etapa 3: Formata a data da venda para o padrão brasileiro
                "data_venda": data_venda.strftime('%d/%m/%Y'),  # Formata o objeto data_venda para o formato Dia/Mês/Ano.
                # Etapa 2 e 3: Adiciona e formata a data de importação
                "data_importacao": data_importacao_formatada  # Adiciona a data de importação já formatada.
            }
            vendas.append(venda)  # Adiciona o dicionário da venda atual à lista de vendas.
    return vendas  # Retorna a lista completa de vendas processadas.

def criar_arquivo_json(vendas, caminho_arquivo_json):
    """
    Cria um arquivo JSON a partir de uma lista de dicionários de vendas.
    """
    # Abre o arquivo de destino no modo de escrita ('w') com codificação 'utf-8'.
    with open(caminho_arquivo_json, 'w', encoding='utf-8') as arquivo_json:  
        # 'indent=4' para formatar o arquivo e torná-lo legível
        # 'ensure_ascii=False' para garantir a correta gravação de caracteres especiais
        json.dump(vendas, arquivo_json, indent=4, ensure_ascii=False)  # Converte a lista de vendas para JSON e a salva no arquivo.

def criar_arquivo_xml(vendas, caminho_arquivo_xml):
    """
    Cria um arquivo XML a partir de uma lista de dicionários de vendas.
    """
    # Cria o elemento raiz do XML
    root = ET.Element("vendas")  # O elemento principal que conterá todas as vendas.

    for venda_dict in vendas:  # Itera sobre cada dicionário de venda na lista.
        # Cria um elemento 'venda' para cada item na lista
        venda_elem = ET.SubElement(root, "venda")  # Cria um nó <venda> dentro do nó <vendas>.
        # Adiciona os dados da venda como sub-elementos de 'venda'
        for chave, valor in venda_dict.items():  # Itera sobre os pares chave-valor do dicionário (ex: 'id_produto': 1).
            child = ET.SubElement(venda_elem, chave)  # Cria um sub-elemento (ex: <id_produto>).
            child.text = str(valor)  # Define o texto do sub-elemento (ex: <id_produto>1</id_produto>).

    # Formata o XML para uma melhor legibilidade (pretty print)
    xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")  # Converte a árvore XML para string e a formata com indentação.

    # Abre o arquivo de destino no modo de escrita ('w') com codificação 'utf-8'.
    with open(caminho_arquivo_xml, "w", encoding='utf-8') as arquivo_xml:  
        arquivo_xml.write(xml_str)  # Escreve a string XML formatada no arquivo.

# --- Execução Principal ---
if __name__ == "__main__":  # Bloco de código que só executa quando o script é rodado diretamente.
    # Encontra o diretório onde o script está sendo executado.
    diretorio_script = os.path.dirname(os.path.abspath(__file__))  # Obtém o caminho absoluto do diretório do script.
    
    # Cria o caminho completo para o arquivo de entrada.
    arquivo_entrada = os.path.join(diretorio_script, 'vendas.txt')  # Junta o caminho do diretório com o nome do arquivo de entrada.

    if not os.path.exists(arquivo_entrada):  # Verifica se o arquivo de entrada realmente existe.
        print(f"Erro: O arquivo '{arquivo_entrada}' não foi encontrado.")  # Exibe uma mensagem de erro se o arquivo não for encontrado.
    else:  # Se o arquivo existir, continua a execução.
        # Processa os dados do arquivo de texto
        dados_vendas = processar_vendas(arquivo_entrada)  # Chama a função para ler e processar o arquivo de vendas.
        
        # --- ALTERAÇÃO AQUI: Define os nomes dos arquivos de saída no mesmo diretório do script ---
        arquivo_saida_json = os.path.join(diretorio_script, 'vendas.json')  # Define o caminho completo para o arquivo JSON de saída.
        arquivo_saida_xml = os.path.join(diretorio_script, 'vendas.xml')  # Define o caminho completo para o arquivo XML de saída.
        # --- FIM DA ALTERAÇÃO ---
        
        # Cria os arquivos de saída
        criar_arquivo_json(dados_vendas, arquivo_saida_json)  # Chama a função para criar o arquivo JSON.
        criar_arquivo_xml(dados_vendas, arquivo_saida_xml)  # Chama a função para criar o arquivo XML.
        
        # Exibe mensagens de sucesso informando onde os arquivos foram salvos.
        print(f"Conversão concluída com sucesso!")  
        print(f"Arquivo JSON gerado em: {arquivo_saida_json}")  
        print(f"Arquivo XML gerado em: {arquivo_saida_xml}")  