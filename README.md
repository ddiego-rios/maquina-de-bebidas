# Máquina de Bebidas

Aplicação de consola, escrita em Python, que simula uma máquina de venda de
bebidas. O programa apresenta os produtos disponíveis, recebe moedas,
calcula e devolve o troco, atualiza o stock e mantém o estado da máquina em
ficheiros de texto. Também disponibiliza um menu administrativo para consultar
o estado da máquina e gerar um relatório HTML.

## Objetivo

O programa permite:

- consultar e comprar as bebidas configuradas;
- aceitar apenas os valores de moeda reconhecidos pela máquina;
- verificar se existe stock do produto escolhido;
- calcular o troco com as moedas disponíveis no moedeiro;
- persistir quantidades de moedas, stock e histórico de compras;
- consultar faturamento, moedeiro, stock e estatísticas de vendas;
- gerar o ficheiro `relatorio_maquina.html`.

Todos os valores monetários são tratados em **cêntimos**. Por exemplo, `35`
corresponde a 35 cêntimos e equivale a 0,35 €.

## Requisitos

- Windows;
- Python 3 instalado e disponível no `PATH`;
- permissões de leitura e escrita na pasta do projeto;
- os ficheiros `bebidas.py`, `moedas.txt` e `produtos.txt` na mesma pasta.

Não são necessárias bibliotecas externas. O módulo `subprocess`, usado para
limpar a consola com o comando `cls`, faz parte da biblioteca padrão do
Python.

## Como executar no Windows

1. Abra o **PowerShell** ou o **Prompt de Comando**.
2. Entre na pasta do projeto:

   ```powershell
   cd C:\python\bebidas
   ```

3. Execute o programa:

   ```powershell
   python bebidas.py
   ```

   Se o comando `python` não estiver associado ao Python instalado, também
   pode ser utilizado:

   ```powershell
   py bebidas.py
   ```

É importante executar o programa a partir da pasta que contém os ficheiros de
dados, porque os nomes dos ficheiros são relativos à pasta atual.

## Menu do utilizador

Ao iniciar, o programa mostra a lista de produtos numerada. O utilizador deve:

1. introduzir o número da bebida;
2. inserir moedas até atingir ou ultrapassar o preço;
3. retirar a bebida e o troco, quando a compra for concluída.

O programa repete a pergunta quando a opção não é um número válido ou não
corresponde a um produto. Se a bebida estiver sem stock, a compra não começa e
é apresentada uma mensagem de indisponibilidade.

Durante o pagamento, são aceites apenas os valores existentes em `moedas.txt`
(na configuração inicial: 5, 10, 20, 50, 100 e 200 cêntimos). O programa
mostra o valor que ainda falta quando o total inserido não é suficiente.

### Acesso administrativo

No menu principal, a opção especial `123` abre o menu administrativo. Esta
opção não é apresentada como produto, mas é tratada pelo programa como uma
entrada reservada para administração.

## Menu administrativo

O menu administrativo disponibiliza:

| Opção | Função |
|---|---|
| 1 | **Ver Faturamento**: soma o valor de todas as moedas atualmente no moedeiro. |
| 2 | **Ver Dinheiro no Moedeiro**: mostra a quantidade de cada denominação. |
| 3 | **Ver Stock de Produtos**: mostra as unidades disponíveis de cada bebida. |
| 4 | **Gerar Relatório HTML**: cria ou substitui `relatorio_maquina.html`. |
| 5 | **Adicionar Moedas ao Moedeiro**: acrescenta uma quantidade positiva de uma denominação já configurada e grava `moedas.txt`. |
| 6 | **Ver Estatísticas de Vendas**: conta as compras do histórico por produto. |
| 10 | **Guardar e Desligar Máquina**: sai do menu administrativo e termina o programa. |
| 0 | **Voltar ao Menu Principal**: regressa à seleção de bebidas. |

A opção 5 só aceita denominações que já estejam carregadas e uma quantidade
maior que zero. As alterações ao moedeiro são gravadas imediatamente.

## Ficheiros de dados

Os ficheiros usam texto simples, codificação UTF-8, uma linha por registo e
ponto e vírgula (`;`) como separador. Não possuem linha de cabeçalho.

### `moedas.txt`

Cada linha tem o formato:

```text
valor_em_centimos;quantidade
```

Exemplo:

```text
5;50
10;50
20;50
50;50
100;50
200;50
```

O primeiro campo identifica a denominação da moeda e o segundo indica quantas
moedas estão disponíveis. Estes valores são usados para validar as moedas
inseridas, calcular o total em caixa e formar o troco.

### `produtos.txt`

Cada linha tem o formato:

```text
nome;preco_em_centimos;quantidade
```

Exemplo:

```text
Café;35;35
Galão;35;35
Capuccino;50;35
Chá;40;35
Chocolate-Quente;35;35
```

O nome é mostrado nos menus, o preço é usado no pagamento e a quantidade
controla a disponibilidade. A ordem das linhas define a ordem numérica das
bebidas no menu.

### `historico.txt`

Este ficheiro é criado automaticamente quando ocorre uma compra concluída. Tem
uma linha por operação, no formato:

```text
Produto: NOME | Moedas inseridas: VALOR1 VALOR2 ... | Troco: VALOR cênt.
```

O histórico existente é carregado ao iniciar. Linhas vazias são ignoradas. O
conteúdo também é usado para calcular as vendas por produto e para preencher o
relatório HTML. Se o ficheiro ainda não existir, o programa começa com um
histórico vazio.

## Geração de `relatorio_maquina.html`

No menu administrativo, escolha a opção `4`. O programa calcula o estado atual
e grava `relatorio_maquina.html` na pasta de execução, substituindo o ficheiro
anterior caso exista.

O relatório é um documento HTML autónomo, com estilos incorporados, e inclui:

- faturamento total em euros e cêntimos;
- moedas existentes e respetivas quantidades;
- stock atual de cada produto;
- número de vendas por produto, obtido a partir do histórico;
- histórico completo de operações.

Depois de gerado, o ficheiro pode ser aberto num navegador, por exemplo:

```powershell
start .\relatorio_maquina.html
```

## Funcionamento interno importante

### Carregamento persistente

No arranque, `bebidas.py` lê `moedas.txt` e `produtos.txt`, separa cada linha
por `;` e converte os campos numéricos para inteiros. O histórico é carregado
se `historico.txt` existir. Os dados ficam em listas paralelas: denominações e
quantidades de moedas, e nomes, preços e quantidades de produtos.

Após uma compra bem-sucedida:

- `moedas.txt` é reescrito com as quantidades atualizadas;
- `produtos.txt` é reescrito com o stock reduzido em uma unidade;
- a nova operação é acrescentada ao fim de `historico.txt`.

O reabastecimento administrativo do moedeiro também reescreve
imediatamente `moedas.txt`.

### Validação

As entradas numéricas são convertidas com `int`. Entradas que não podem ser
convertidas são tratadas como opções ou moedas inválidas e o programa volta a
pedir a informação. A opção do produto deve estar entre 1 e o número de
produtos, exceto a opção reservada `123`. A compra só avança se o produto
tiver stock e se cada moeda inserida existir na lista carregada.

Ao carregar os ficheiros, linhas com campos que não possam ser convertidos
para os tipos esperados são ignoradas pelo programa.

### Cálculo do troco

Depois de receber dinheiro suficiente, o troco é calculado como:

```text
troco = dinheiro_inserido - preco
```

Para o devolver, o programa escolhe repetidamente a maior moeda disponível que
não ultrapasse o valor ainda em falta. Cada moeda devolvida é retirada da
quantidade do moedeiro. Se não for possível formar o troco completo com as
moedas existentes, é apresentada uma mensagem para contactar a administração
e a compra não é finalizada como bem-sucedida.

Quando o troco é formado integralmente, a bebida é retirada do stock, os
ficheiros são atualizados e a operação é registada.

### Atualização do stock e do histórico

O stock só é reduzido depois de a máquina conseguir completar o troco. Nesse
momento, o registo guardado contém o produto, as moedas inseridas e o troco em
cêntimos. As estatísticas do menu administrativo e do relatório contam os
registos que correspondem a cada produto.

## Observações

- Os nomes e os preços devem permanecer consistentes entre as listas e os
  ficheiros de dados.
- Não devem ser adicionados cabeçalhos aos ficheiros `.txt`.
- Faça cópias de segurança dos ficheiros de dados antes de alterações manuais.
- O programa foi implementado para uma execução local em Windows e limpa a
  consola usando `cls`.
