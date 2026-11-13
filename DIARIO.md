# Diário

Uma entrada por dia, com as suas palavras: o que você tentou, o que decidiu e por quê, o que deu errado
e o que aprendeu. Errar faz parte; o que conta é o que você fez com o erro.

## AAAA-MM-DD

- **Tentei:**
- **Decidi, e por quê:**
- **Deu errado:**
- **Aprendi:**

## 2026-11-07
- **Aprendi:** Sobre o projeto e iniciei lendo sobre os dados. Criei o repositório e marquei para conversar com alguém do varejo. Percebi que Diego é gerente há 6 meses e tem problemas de liderança, apesar de ter sido o melhor vendedor da loja. Bianca é uma vendedora com ótimo atendimento, porém seus clientes geralmente compram apenas 1 peça.
Também existe um problema de feedback vago, pois um texto frio ou injusto pode desmotivar a pessoa ou causar um problema trabalhista. Números são importantes mas é preciso analisar se o vendedor estava de férias ou se teve algum problema pessoal, se a loja estava em reforma.
- **Decidi, e por quê:** Fiquei com dúvidas na criação de pastas, de como ficaria a organização. Pedi ajuda ao Gemnini mas não gostei da estrutura que me enviou, gostei mais da estrutura de pastas que o GPT me sugeriu. Acabei excluindo as pastas contexto.py e roteiro.py porque vi que talvez não seria necessário no momento.
- **Aprendi:** Consegui abrir a aplicação com o Streamlit que mostra os indicadores de desempenho.

## 2026-11-08
- **Aprendi:** Criação do contexto. Essa etapa é importante porque mostra situações em que o vendedor vendeu menos, como: férias, problemas pessoais, trabalhar na escala 5x2, ser funcionário novo. A anotação sensível do Marcelo não deve ser repassada à IA, pois foi um problema pessoal. As demais anotações podem ser incluídas sem alterações.
Criação da função gerar_ficha() que recebe o identificador do vendedor e o mês. Essa função compara o desempenho do vendedor com o mês anterior e com os resultados da loja, sem criar competições entre os colegas.
- **Deu errado:** Na questão da API key. Eu já usei o Openrouter e dava certo, mas agora aparece que estou sem créditos e a aplicação não está funcionando.
Houve um problema na interpretação dos números brasileiros, o validador estava removendo pontos e vírgulas de maneira inadequada em alguns casos.
- **Decidi, e por quê:** Usei a API key gratuita do Gemini e deu certo, fiz apenas algumas modificações no .env. Também tive que fazer várias alterações nas validações de números.

## 2026-11-09
- **Decidi, e por quê:** Criação de três camadas de proteção: validar números, validar associações, e validar referências completas. Fiz várias implementações no código para captar erros de validação. Se na hora da edição eu trocar o valor das vendas pelo ticket, ou colocar um número falso, dá erro e o relatório não é aprovado. Criação da função para salvar relatório, inclusive os editados (que foram aprovados). Testei um relatório colocando 3 pontos de exclamação (!!!) e foi aprovado. Os relatórios aprovados ficam salvos em saidas/feedbacks_aprovados.csv. Criação do botão aprovar e salvar feedback.

## 2026-11-10
- **Decidi, e por quê:** Decidi criar uma nova função em validação para verificar aspectos básicos de organização e apresentação do texto. Essa função vai verificar se a IA entregou todos os campos obrigatórios: cuidados, abertuda, ponto forte, ponto a melhorar, etc.
- **Deu errado:** O feedback da Bianca está usando números com ponto como separador decimal, mas a função validar_referencias_completas foi criada para reconhecer apenas números com vírgula decimal.
- **Decidi, e por quê:** Fiz a mudança no padrão que identifica as referências: agora ele aceita tanto vírgula quanto ponto como separador decimal.
- **Tentei:** Fiz vários criando vários feedbacks de diferentes funcionários em meses diferentes. No mesmo mês e no mesmo funcionário a IA gera um feedback diferente. Percebi que dá erro de aprovação no feedback quando a IA gera um número que não foi identificado pelas fichas, como por exemplo “8”. Mas se eu editar e trocar por “oito”, o feedback é aprovado. A IA pode produzir resultados diferentes em execuções consecutivas, mesmo recebendo os mesmos dados.
- **Decidi, e por quê:** Fiz mais uma melhoria em validações e preservei o código. Finalmente os feedbacks estão dando sem erro. Somente o da Vanessa que dá erro por causa do 5x2, mas decidi tratar isso na edição do feedback para não fazer alterações no código que prejudique os feedbacks dos outros vendedores.
- **Decidi, e por quê:** Mudei a cor dos botões para verde, porque estavam em vermelho. A cor vermelha sempre está associada às opções "cancelar" e "excluir". Já a cor verde combina mais com os botões "Gerar feedback com IA" e "Aprovar e salvar feedback".
- **Decidi, e por quê:** Coloquei alguns emojis para ficar mais visualmente atrativo.

## 2026-11-11
- **Decidi, e por quê:** Dia de gravar o vídeo da demonstração do sistema, preparar o README e os slides.

## 2026-11-13
- **Decidi, e por quê:** Fiz alterações nos slides para deixar mais objetivo e deixei o vídeo mais acelerado. Fiz isso para otimizar a apresentação, que são 5 minutos. Também corrigi uns erros de digitação aqui no diário.