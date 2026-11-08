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
**Aprendi:** Consegui abrir a aplicação com o Streamlit que mostra os indicadores de desempenho.

## 2026-11-08
- **Aprendi:** Criação de do contexto. Essa etapa é importante porque mostra situações em que o vendedor vendeu menos, como: férias, problemas pessoais, trabalhar na escala 5x2, ser funcionário novo. A anotação sensível do Marcelo não deve ser repassada à IA, pois foi um problema pessoal. As demais anotações podem ser incluídas sem alterações.
Criação da função gerar_ficha() que recebe o identificador do vendedor e o mês. Essa função compara o desempenho do vendedor com o mês anterior e com os resultados da loja, sem criar competições entre os colegas.