# Scripts para Automação e Análise de Dados

Coleção de scripts em python desenvolvidos para solucionar desafios comuns de negócios de uma empresa, focados em automação de tarefas, processamento de diferentes tipos de dados e Business Intelligence (BI).

____________

*Este repositório inclui:*

- 1 Script para conversão e manipulação de formatos de dados (TXT para XML e JSON);

- 1 Script para organização e padronização de arquivos com diferentes extensões em diretórios;

- 1 Script para análise de dados e processamento de informações de clientes e suas compras (CSV e JSON), com posterior geração de gráficos de barra, dispersão e boxplot;

- 1 Script para análise de dados e processamento de resultados de análises laboratoriais físico-químicas de lotes de produtos cosméticos, com posterior geração de relatórios e de gráficos de dispersão e boxplot;

- Implementação de logging nos 3 últimos scripts para garantir rastreabilidade e facilitar a depuração.

____________________

*Propósito*

O objetivo principal deste respositório é fornecer um conjunto de ferramentas em python que sejam práticas, eficientes e reutilizáveis; capazes de otimizar processos operacionais, organizar ativos digitais e extrair insights valiosos a partir de dados brutos. Este repositório demonstra a aplicação prática do python na automação de tarefas repetitivas, como organizar arquivos ou converter arquivos de diferentes formatos, e na análise e manipulação de dados complexa, como a correlação de dados de clientes ou o monitoramento de controle de qualidade. As soluções aqui presentes visam reduzir o esforço manual, garantir a integridade dos dados e apoiar a tomada de decisões estratégicas baseadas em evidências.

___________________

*Descrição dos Scripts*

1) Script conversor_vendas.py (Pasta 1. Conversor de vendas)
   
Descrição: Este script atua como um utilitário de ETL (Extract, Transform and Load) focado na conversão de dados de vendas. Ele é projetado para ler registros de vendas do e-commerce de uma empresa que estão armazenados em arquivos de texto simples (.txt), e convertê-los em arquivos de outros formatos para integrar o sistema de vendas com um software de gerenciamento de estoque fictício que aceita apenas extensões .xml e .json.

Modo de Uso: Baixe a pasta "1. Conversor de vendas" e a abra em seu editor de código. Altere o arquivo "vendas.txt" com as informações das suas vendas (incluindo informações como ID do produto/serviço, nome do produto/serviço, quantidade vendida, preço unitário, data da venda e data da importação) e salve. Clique com o botão direito do mouse em cima do script "conversor_vendas.py" e selecione a opção "Open in integrated terminal". Execute o script. Ao ser executado, o script processa o arquivo .txt de entrada e gera duas saídas estruturadas: 

> Um arquivo .xml (Ideal para sistemas legados ou integrações que exigem este formato); 
    
> Um arquivo .json (Ideal para APIs modernas, bancos de dados NoSQL e análise de dados).


2) Script organizar_arquivos.py (Pasta 2. Organizador de arquivos)

Descrição: Este script atua como uma ferramenta de gerenciamento de arquivos, projetada especificamente para organizar diretórios de marketing que comumente contêm uma vasta gama de extensões de arquivos.

Modo de Uso: Baixe a pasta "2. Organizador de arquivos" e a abra em seu editor de código. Insira na pasta "exemplos_arquivos" os diretórios ou arquivos que deseja organizar. Clique com o botão direito do mouse em cima do script "organizar_arquivos.py" e selecione a opção "Open in integrated terminal". Execute o script. O script varre o diretório de origem e executa as seguintes ações: 

> Criação de Pastas: Cria automaticamente novas pastas no mesmo diretório com base no tipo de extensão dos arquivos encontrados (exemplo: "PDFs", "Imagens", "Vídeos", "Documentos" etc);

> Organização dos arquivos: Move cada arquivo para a pasta correspondente à sua extensão;

> Padronização de nomes: Renomeia os arquivos movidos seguindo um formato padronizado (exemplo: 15-10-2025_Apresentação_001.pptx); 

> Crição de logging: Registra todas as operações (arquivos lidos, pastas criadas, arquivos movidos/renomeados, datas e horários) em um arquivo de log, garantindo total rastreabilidade do processo.


3) Script interpretador_dados.py (Pasta 3. Interpretador de dados)
   
Descrição: Este Script atua como um analista de dados focado em Customer Intelligence. Ele realiza a fusão e a interpretação de dados de clientes provenientes de fontes distintas para gerar insights sobre o comportamento e a satisfação do consumidor.

Modo de Uso: Baixe a pasta "3. Interpretador de dados" e a abra em seu editor de código. Insira na pasta "clientes.csv" os dados dos seus clientes (incluindo ID CLiente, Nome, Idade e Salário). Insira na pasta "compras.json" os dados dos seus clientes (incluindo ID Cliente, Produto comprado, Valor gasto e Pontuação de satisfação). Clique com o botão direito do mouse em cima do script "interpretador_dados.py" e selecione a opção "Open in integrated terminal". Execute o script. O script varre o diretório de origem e executa as seguintes ações: 

> Leitura e Processamento: Lê dados de ambos os arquivos .csv e .json;

> Compilação: Une as duas fontes de dados em um único DataFrame, correlacionando os clientes entre os arquivos;

> Visualização de Dados: Gera três gráficos distintos para facilitar a análise e a tomada de decisão. 1 Gráfico de Boxplot, para analisar a distribuição estatística da satisfação do cliente; 1 Gráfico de dispersão, para identificar possíveis correlações entre satisfação e frequência de compras; e 1 Gráfico de barras, para comparar métricas de satisfação entre diferentes segmentos de clientes;

> Criação de Logging: Cria registros detalhados de logging de todas as etapas (leitura, processamento, fusão e geração de gráficos, datas e horários).


4) Script gestor_qualidade.py (Pasta 4. Gestor da qualidade)
   
Descrição: Este Script atua como uma solução robusta para automação do Controle de Qualidade (CQ) em laboratório, especificamente voltada para a indústria de cosméticos. O script processa e analisa resultados de análises físico-químicas, conforme o lote do produto fabricado e suas especificações de limites máximos e mínimos respectivos para cada tipo de análise.

Modo de Uso: Baixe a pasta "4. Gestor da qualidade" e a abra em seu editor de código. Dentro da pasta "dados_laboratorio", abra cada arquivo.csv e altere os resultados de análise de pH, densidade e viscosidade para os 3 lotes fictícios fabricados para os produtos (Shampoo, Condicionador e Sabonete), e salve. Se necessário, altere o arquivo "parametros_qualidade.txt" com as especificações de limites máximo e mínimo que sua empresa utiliza como padrão, e salve. Clique com o botão direito do mouse em cima do script "gestor_qualidade.py" e selecione a opção "Open in integrated terminal". Execute o script. O script varre o diretório de origem e executa as seguintes ações: 

> Processamento de Dados: Lê, compila e interpreta dados de análises (pH, densidade e viscosidade) de 3 lotes diferentes fabricados naquele dia para cada tipo de produto (Shampoo, Condicionador e Sabonete Líquido);

> Verificação de Conformidade: Compara os resultados das análises com os padrões de qualidade pré-estabelecidos e classifica cada lote como "Conforme" ou "Não Conforme";

> Geração de Relatórios: Cria automaticamente três relatórios essenciais para a gestão da qualidade: 1 Relatório estatístico, que detalha dados estatísticos (média, mediana, desvio padrão, quartis e amplitude) dos produtos analisados; 1 Relatório laboral por turno, em que consolida todas as análises realizadas de todos os produtos por turno de trabalho; e 1 Relatório de Não Conformidade, criando uma lista estruturada que evidencia e detalha todos os lotes de produtos reprovados (Não Conformes);

> Geração de Gráficos: Cria automaticamente 6 gráficos essenciais para melhorar a visualização dos dados, analisar tendências e auxiliar em tomadas de decisões: 3 Gráficos de Boxplot, sendo um para cada tipo de análise físico-química, permitindo visualizar a média e o desvio padrão dos lotes de cada tipo de produto, facilitando a identificação de variabilidade no processo para cada análise específica; e 3 Gráficos de Dispersão, sendo um para cada tipo de produto, permitindo analisar as tendências dos resultados das análises conforme o tipo de produto ao longo dos 3 lotes fabricados, ajudando a identificar padrões ou desvios ao longo do tempo;

> Criação de Logging: Implementa um sistema de logging completo para auditoria e rastreabilidade de todas as análises processadas e decisões de conformidade.

_____________________________

OBSERVAÇÃO 1: Para o desenvolvimento deste repositório, foi utilizado o VSCode como editor de código prinicpal. 

OBSERVAÇÃO 2: Em qualquer um dos diretórios contendo os scripts descritos acima, caso haja necessidade de modificar nomes dos arquivos de origem e variáveis dentro dos arquivos, é necessário atualizar todos os arquivos relacionados e seus scripts dentro dos diretórios para que não apresentem problemas de encontrar arquivos, caminhos e dados. Para mais informações, entre em contato comigo.

