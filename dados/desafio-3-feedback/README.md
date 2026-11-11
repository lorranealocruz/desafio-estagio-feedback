# 📊 Feedback Aurora — Desafio 3

**Feedback para vendedores e gerentes usando IA.**

> Como ajudar gerentes a dar feedback frequente, justo e útil para os vendedores, e a receber feedback também?

## Sobre o projeto

O **Feedback Aurora** é uma aplicação desenvolvida em Python e Streamlit que utiliza Inteligência Artificial para auxiliar gerentes na elaboração de feedbacks individuais para vendedores.

A proposta é transformar dados de vendas, metas e informações contextuais em feedbacks mais objetivos, personalizados e construtivos, contribuindo para o desenvolvimento dos colaboradores e para uma gestão mais justa.

A aplicação utiliza a API do Gemini para gerar sugestões de feedback com base em informações reais dos arquivos de dados, evitando avaliações genéricas ou fundamentadas em informações inventadas.

O projeto também considera situações que exigem cuidados na avaliação, como férias, tempo de empresa, escala de trabalho, frequência de vendas e anotações gerenciais sensíveis.

**Foco da solução:** apoiar o gerente na elaboração de feedbacks para os vendedores, com validações que aumentam a confiabilidade das informações antes da aprovação.

## Funcionalidades

- **Cálculo de indicadores:** processamento dos dados de vendas, atendimentos, peças vendidas, metas e resultados individuais e da loja.
- **Comparação de desempenho:** comparação dos indicadores do vendedor com o mês anterior e com os resultados gerais da loja.
- **Análise de contexto:** identificação de situações que devem ser consideradas durante a elaboração do feedback.
- **Proteção de informações sensíveis:** identificação de anotações gerenciais sensíveis, impedindo que seu conteúdo seja exposto no feedback gerado.
- **Geração de feedback com IA:** utilização do Gemini para elaborar sugestões estruturadas e personalizadas.
- **Validação de confiabilidade:** verificação dos números, referências, estrutura e qualidade do feedback.
- **Aprovação do feedback:** apresentação dos resultados das validações antes de permitir a aprovação.
- **Armazenamento:** registro dos feedbacks aprovados em arquivo CSV.

## Validações do sistema

Um dos principais diferenciais do Feedback Aurora é a etapa de validação das respostas geradas pela Inteligência Artificial.

Antes que um feedback possa ser aprovado, o sistema realiza verificações para reduzir inconsistências e informações incorretas.

### 1. Validação numérica

Verifica se os números apresentados no feedback correspondem aos valores disponíveis na ficha de contexto, identificando números que não foram encontrados nos dados.

### 2. Validação de associações

Confere se cada valor está associado ao indicador correto.

Por exemplo, impede que o valor vendido seja apresentado incorretamente como ticket médio.

### 3. Validação de referências

Verifica se os números apresentados estão acompanhados de referências que identificam sua origem na ficha de contexto.

### 4. Validação de estrutura

Verifica a presença e o preenchimento dos campos obrigatórios do feedback:

- Cuidados;
- Abertura;
- Ponto forte;
- Ponto a melhorar;
- Pergunta aberta;
- Combinado para a semana;
- Acompanhamento;
- Fontes.

### 5. Validação de qualidade

Verifica aspectos básicos de organização e apresentação do texto, como seções obrigatórias, conteúdo vazio, excesso de pontuação e extensão das seções.

**Importante:** a IA gera uma sugestão, mas o feedback só pode ser aprovado quando todas as validações implementadas pelo sistema forem atendidas.

## Tecnologias utilizadas

| Tecnologia | Aplicação no projeto |
|---|---|
| Python | Linguagem principal |
| Streamlit | Interface da aplicação |
| Gemini API | Geração dos feedbacks com IA |
| Pandas | Manipulação e análise de dados |
| CSV | Armazenamento dos dados e feedbacks aprovados |
| Requests | Comunicação com a API |
| Python-dotenv | Gerenciamento de variáveis de ambiente |
| Git e GitHub | Controle de versão e hospedagem do código |

## Estrutura do projeto

```text
desafio-3-feedback/
│
├── .streamlit/
│ └── config.toml
│
├── apresentacao/
│   ├── VIDEO.md
│   └── slides-feedback.pdf
│
├── prompts/
│   └── PROMPTS.md
│
├── src/
│   ├── __init__.py
│   ├── indicadores.py
│   ├── contexto.py
│   ├── ficha.py
│   ├── validacao.py
│   ├── ia.py
│   └── registro.py
│
├── saidas/
│   ├── sensiveis.csv
│   ├── feedbacks_aprovados.csv
│   └── teste_feedbacks.csv
│
├── vendedores.csv
├── indicadores_diarios_vendedor.csv
├── metas_vendedor.csv
├── metas_loja.csv
├── anotacoes_gerente.csv
│
├── exemplos_feedbacks_ruins.md
├── app.py
└── README.md
├── requirements.txt
├── .env.example
├── .gitignore
└── LEIAME.md
```

### Organização dos módulos

**Pasta `streamlit/`**

Contém a configuração da cor do tema (cor dos botões).

- `config.toml`: cor primária.

**Pasta `apresentacao/`**

Contém as mídias da apresentação.

- `VIDEO.md`: url do vídeo da apresentação.
- `slides-feedback.pdf`: os slides da apresentação.

**Pasta `prompts/`**

Contém o histórico de IA

- `PROMPTS.md`: histórico das conversas com Gemini e GPT.

**Pasta `src/`**

Contém os módulos responsáveis pela lógica da aplicação:

- `indicadores.py`: calcula os indicadores individuais e gerais da loja.
- `contexto.py`: identifica alertas e situações que exigem cuidados na elaboração do feedback.
- `ficha.py`: reúne os indicadores e informações contextuais em uma ficha individual.
- `validacao.py`: executa as validações numéricas, de associações, referências, estrutura e qualidade.
- `ia.py`: realiza a integração com a API do Gemini e gera os feedbacks.
- `registro.py`: salva os feedbacks aprovados.

**Pasta `saidas/`**

Armazena arquivos relacionados à proteção de informações e aos resultados da aplicação:

- `sensiveis.csv`: identifica anotações gerenciais que devem ser tratadas como sensíveis.
- `feedbacks_aprovados.csv`: armazena os feedbacks aprovados.
- `teste_feedbacks.csv`: arquivo utilizado para testes de armazenamento.

**Arquivos de dados**

- `vendedores.csv`: informações dos vendedores.
- `indicadores_diarios_vendedor.csv`: registros diários de desempenho.
- `metas_vendedor.csv`: metas individuais.
- `metas_loja.csv`: metas gerais da loja.
- `anotacoes_gerente.csv`: anotações realizadas pela gestão.
- `exemplos_feedbacks_ruins.md`: exemplos de feedbacks inadequados utilizados como referência para orientar a geração.

## Como executar o projeto

### 1. Pré-requisitos

- Python instalado (preferencialmente Python 3.11 ou superior).
- Git instalado.
- Chave de API do Google Gemini.

### 2. Clonar o repositório

No terminal, execute:

```bash
git clone https://github.com/lorranealocruz/desafio-estagio-feedback.git
```

### 3. Acessar a pasta do projeto

Primeiro, entre na pasta `dados`:

```bash
cd dados
```

Depois, entre na pasta do Desafio 3:

```bash
cd desafio-3-feedback
```

### 4. Criar um ambiente virtual (recomendado)

```bash
python -m venv venv
```

Ative o ambiente virtual no Windows:

```powershell
venv\Scripts\Activate.ps1
```

### 5. Instalar as dependências

Com o ambiente virtual ativado, execute:

```bash
pip install -r requirements.txt
```

### 6. Configurar a chave da API Gemini

Crie um arquivo chamado `.env` na raiz da pasta `desafio-3-feedback`, utilizando o `.env.example` como modelo.

Configure as variáveis:

```env
GEMINI_API_KEY=sua_chave_de_api
GEMINI_MODEL=gemini-3.5-flash-lite
```

Substitua `sua_chave_de_api` pela sua chave pessoal do Gemini.

A chave pode ser obtida no [Google AI Studio](https://aistudio.google.com/).

**Atenção:** nunca compartilhe sua chave de API nem envie o arquivo `.env` para o GitHub.

### 7. Executar a aplicação

Com as dependências instaladas e as variáveis de ambiente configuradas, execute:

```bash
streamlit run app.py
```

A aplicação será aberta no navegador, permitindo utilizar o Feedback Aurora.

## Fluxo de funcionamento

1. O gerente acessa a aplicação.
2. Seleciona o vendedor e o mês de referência.
3. O sistema processa os dados e calcula os indicadores.
4. São identificados os alertas e as informações contextuais relevantes.
5. A ficha individual é enviada à IA para elaboração do feedback.
6. O sistema recebe a sugestão gerada pelo Gemini.
7. As validações de confiabilidade são executadas.
8. Se todas as validações forem aprovadas, o gerente pode aprovar e salvar o feedback.
9. O feedback aprovado é registrado em `saidas/feedbacks_aprovados.csv`.

## Segurança e cuidados com os dados

- Os dados utilizados no desafio são fictícios.
- Anotações classificadas como sensíveis não são expostas no conteúdo enviado para geração do feedback.
- A aplicação utiliza variáveis de ambiente para armazenar a chave da API.
- O arquivo `.env` deve permanecer fora do controle de versão.
- A aprovação depende do resultado das validações implementadas.

## Objetivo de aprendizado

Este projeto foi desenvolvido como parte do **Desafio 3 — O feedback que ninguém dá**, com o objetivo de aplicar conhecimentos de programação, manipulação de dados, integração com serviços de Inteligência Artificial, desenvolvimento de interfaces e validação de informações.

Além da implementação técnica, o desenvolvimento envolveu a preocupação com a qualidade dos feedbacks, a proteção de informações sensíveis e a redução de possíveis erros produzidos pela IA.

---

**Desenvolvido por:** Lorrane Aló Cruz

**Repositório:** [desafio-estagio-feedback](https://github.com/lorranealocruz/desafio-estagio-feedback)