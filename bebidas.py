import subprocess

moedas =              [] # Moedas validas
moedas_quantidade   = [] # quantidade de moedas
produtos =            [] # produtos
precos =              [] # preços dos produtos
produtos_quantidade = [] # quantidade dos produtos 
historico =           [] # Lista para guardar o historico de compras

site = "relatorio_maquina.html"
arq_moedas = "moedas.txt"
arq_produtos = "produtos.txt"
arq_historico = "historico.txt"

# CARREGAR DADOS DOS FICHEIROS

with open(arq_moedas,"r", encoding="utf-8") as f:
    for linha in f:
        colunas = [coluna.strip() for coluna in linha.split(";")]
        try: 
            moedas.append(int(colunas[0]))
            moedas_quantidade.append(int(colunas[1]))
        except: ""

with open(arq_produtos,"r", encoding="utf-8") as f:
    for linha in f:
        colunas = [coluna.strip() for coluna in linha.split(";")]
        try: 
            produtos.append(colunas[0])
            precos.append(int(colunas[1]))
            produtos_quantidade.append(int(colunas[2]))
        except: ""

# Carregar o histórico de compras, se o ficheiro existir
try:
    with open(arq_historico, "r", encoding="utf-8") as f:
        for linha in f:
            if linha.strip() != "":
                historico.append(linha.strip())
except: ""

msg = ""

while True:
    preco = troco = 0
    subprocess.run('cls', shell=True)

    # 1. MENU DE BEBIDAS
    
    while True:
        print('\n MENU')
        
        for i in range(len(produtos)):
            print('\t', (i + 1), '.', produtos[i])
            
        print("\n\t", msg)

        try: opcao = int(input('\n Escolha a sua bebida: '))
        except: opcao = -1

        if (opcao > 0 and opcao <= len(produtos)) or opcao == 123: break

    print()

    # MENU ADMINISTRATIVO
    
    if opcao == 123: 
        subprocess.run('cls', shell=True)

        inicio = """<!DOCTYPE html>
<html lang="pt-pt">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Relatório - Máquina de Bebidas</title>
<style>
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: #f4f7f6;
        color: #333;
        margin: 0;
        padding: 30px;
    }
    .container {
        max-width: 800px;
        margin: 0 auto;
        background: #ffffff;
        padding: 30px 40px;
        border-radius: 8px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    h1 {
        color: #2c3e50;
        text-align: center;
        border-bottom: 2px solid #3498db;
        padding-bottom: 10px;
        margin-bottom: 30px;
    }
    h2, h3 {
        color: #2c3e50;
        margin-top: 30px;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 15px;
    }
    th, td {
        padding: 12px 15px;
        text-align: left;
        border-bottom: 1px solid #ddd;
    }
    th {
        background-color: #3498db;
        color: white;
        font-weight: bold;
    }
    tr:nth-child(even) {
        background-color: #f9f9f9;
    }
    tr:hover {
        background-color: #f1f1f1;
    }
    .historico-item {
        background-color: #f8f9fa;
        border-left: 4px solid #3498db;
        padding: 12px 15px;
        margin-bottom: 10px;
        font-size: 0.95em;
        border-radius: 0 4px 4px 0;
    }
    .total-caixa {
        font-size: 1.2em;
        background-color: #e8f4f8;
        padding: 15px;
        border-radius: 6px;
        font-weight: bold;
    }
</style>
</head>
<body>
<div class="container">
    <h1>Relatório de Gestão</h1>
"""
        fim = """</div>
</body>
</html>
"""
        while True:
            subprocess.run('cls', shell=True)
            print('\n MENU ADMINISTRATIVO')
            print("\t 1. Ver Faturamento")
            print("\t 2. Ver Dinheiro no Moedeiro")
            print("\t 3. Ver Stock de Produtos")
            print("\t 4. Gerar Relatório HTML")
            print("\t 5. Adicionar Moedas ao Moedeiro")
            print("\t 6. Ver Estatísticas de Vendas")
            print("\t 10. Guardar e Desligar Máquina")
            print("\t 0. Voltar ao Menu Principal")

            try: admin = int(input('\n Escolha uma opção: '))
            except: admin = -1

            if admin == 1:
                total_caixa = 0
                for i in range(len(moedas)):
                    valor_moeda = int(moedas[i])
                    quantidade = int(moedas_quantidade[i])
                    total_caixa += valor_moeda * quantidade
                
                euros = total_caixa // 100
                centimos = total_caixa % 100
                
                print("\n\t Dinheiro total em caixa:", euros, "euros e", centimos, "cêntimos (", total_caixa, "cêntimos)")
                input("\n \n Pressione enter para continuar ...")
            
            if admin == 2:
                print("\n\t Moedas existentes no moedeiro: ")
                for i in range(len(moedas)):
                    print("\n\t " , moedas[i], "cêntimos:", moedas_quantidade[i])
                
                input("\n \n Pressione enter para continuar ...")

            if admin == 3:
                print("\n\t Produtos disponiveis")
                for i in range(len(produtos)):
                    print("\n\t", produtos[i], ":", produtos_quantidade[i], "Unidades.")
                input("\n \n Pressione enter para continuar ...")

            if admin == 4: 
                total_caixa = 0
                for i in range(len(moedas)):
                    valor_moeda = int(moedas[i])
                    quantidade = int(moedas_quantidade[i])
                    total_caixa += valor_moeda * quantidade
                                
                euros = total_caixa // 100
                centimos = total_caixa % 100
                
                # Calcular estatísticas para o HTML
                vendas_por_produto = []
                for i in range(len(produtos)):
                    vendas_por_produto.append(0)
                    
                for registo in historico:
                    for i in range(len(produtos)):
                        if "Produto: " + str(produtos[i]) + " |" in registo:
                            vendas_por_produto[i] += 1

                with open(site, "w", encoding="utf-8") as f:
                    f.write(inicio)

                    f.write('<h2>Faturamento Total</h2>\n')
                    f.write('<div class="total-caixa">\n')
                    f.write('Dinheiro total em caixa: ' + str(euros) + ' euros e ' + str(centimos) + ' cêntimos (' + str(total_caixa) + ' cêntimos)\n')
                    f.write('</div>\n')
                    
                    f.write('<h3>Dinheiro no Moedeiro</h3>\n')
                    f.write('<table>\n')
                    f.write('<tr><th>Valor da Moeda</th><th>Quantidade Disponível</th></tr>\n')
                    for i in range(len(moedas)): 
                        f.write('<tr><td>' + str(moedas[i]) + ' cêntimos</td><td>' + str(moedas_quantidade[i]) + ' moedas</td></tr>\n')
                    f.write('</table>\n')
                    
                    f.write('<h3>Stock de Produtos</h3>\n')
                    f.write('<table>\n')
                    f.write('<tr><th>Produto</th><th>Quantidade</th></tr>\n')
                    for i in range(len(produtos)): 
                        f.write('<tr><td>' + str(produtos[i]) + '</td><td>' + str(produtos_quantidade[i]) + ' Unidades</td></tr>\n')
                    f.write('</table>\n')
                    
                    f.write('<h3>Estatísticas de Vendas</h3>\n')
                    f.write('<table>\n')
                    f.write('<tr><th>Produto</th><th>Vezes Vendidas</th></tr>\n')
                    for i in range(len(produtos)): 
                        f.write('<tr><td>' + str(produtos[i]) + '</td><td>' + str(vendas_por_produto[i]) + ' vendas</td></tr>\n')
                    f.write('</table>\n')

                    f.write('<h3>Histórico de Operações</h3>\n')
                    if len(historico) == 0:
                        f.write('<p>Nenhuma operação registada ainda.</p>\n')
                    else:
                        for i in range(len(historico)):
                            f.write('<div class="historico-item">' + str(historico[i]) + '</div>\n')

                    f.write(fim)
                
                print("\n\t Relatório HTML gerado com sucesso!")
                input("\n \n Pressione enter para continuar ...")
                
            if admin == 5:
                print("\n\t --- REABASTECER MOEDEIRO ---")
                try: 
                    moeda_add = int(input('\t Qual o valor da moeda que quer adicionar (5, 10, 20, 50, 100, 200)? '))
                except: 
                    moeda_add = 0
                
                if moeda_add in moedas:
                    try:
                        qtd_add = int(input('\t Quantas moedas de ' + str(moeda_add) + ' cêntimos vai colocar? '))
                    except:
                        qtd_add = 0
                    
                    if qtd_add > 0:
                        posicao = moedas.index(moeda_add)
                        moedas_quantidade[posicao] += qtd_add
                        
                        print('\n\t Sucesso! Foram adicionadas ' + str(qtd_add) + ' moedas de ' + str(moeda_add) + ' cêntimos.')
                        
                        with open(arq_moedas, "w", encoding="utf-8") as f:
                            for i in range(len(moedas)):
                                f.write(str(moedas[i]) + ";" + str(moedas_quantidade[i]) + "\n")
                    else:
                        print('\n\t Erro: Quantidade inválida. Operação cancelada.')
                else:
                    print('\n\t Erro: Moeda não reconhecida pelo sistema.')
                    
                input("\n \n Pressione enter para continuar ...")
                
            if admin == 6:
                print("\n\t --- ESTATÍSTICAS DE VENDAS ---")
                
                vendas_por_produto = []
                for i in range(len(produtos)):
                    vendas_por_produto.append(0)
                    
                for registo in historico:
                    for i in range(len(produtos)):
                        if "Produto: " + str(produtos[i]) + " |" in registo:
                            vendas_por_produto[i] += 1
                            
                for i in range(len(produtos)):
                    print("\n\t " + str(produtos[i]) + " -> " + str(vendas_por_produto[i]) + " vezes vendidas")
                    
                input("\n \n Pressione enter para continuar ...")
            
            if admin == 10: break
            if admin == 0: break
        
        if admin == 10: break
        continue 

    # 2. ESCOLHER O PREÇO E VERIFICAR O STOCK DO PRODUTO
    
    indice_produto = opcao - 1

    if produtos_quantidade[indice_produto] <= 0:
        msg = "Desculpe, o produto " + str(produtos[indice_produto]) + " está esgotado!"
        continue

    preco = precos[indice_produto]
    print("\n Preço do produto: ", produtos[indice_produto], "-", preco, "cêntimos \n")

    # 3. RECEBER MOEDAS VÁLIDAS

    dinheiro_inserido = 0
    moedas_inseridas_registo = "" 

    while dinheiro_inserido < preco:
        try: 
            moeda_inserida = int(input(' Introduza uma moeda válida (5, 10, 20, 50, 100, 200): '))
        except: 
            moeda_inserida = 0

        if moeda_inserida in moedas:
            dinheiro_inserido += moeda_inserida
            moedas_inseridas_registo += str(moeda_inserida) + " "
            
            posicao = moedas.index(moeda_inserida)
            moedas_quantidade[posicao] += 1
            
            falta = preco - dinheiro_inserido
            if falta > 0:
                print(' Em falta:', falta, 'cêntimos \n')
        else:
            print(' Moeda inválida. Tente novamente.\n')

    # 4. DEVOLUÇÃO DO TROCO E ATUALIZAR FICHEIROS

    troco = dinheiro_inserido - preco
    print('\n Troco:', troco, 'cêntimos \n')

    troco_restante = troco
    
    moedas_devolvidas = []
    for i in range(len(moedas)):
        moedas_devolvidas.append(0)

    while troco_restante > 0:
        melhor_indice = -1
        maior_valor = -1
        
        for i in range(len(moedas)):
            if moedas[i] <= troco_restante and moedas_quantidade[i] > 0:
                if moedas[i] > maior_valor:
                    maior_valor = moedas[i]
                    melhor_indice = i
                    
        if melhor_indice == -1:
            break
            
        troco_restante -= moedas[melhor_indice]
        moedas_quantidade[melhor_indice] -= 1
        moedas_devolvidas[melhor_indice] += 1

    if troco_restante > 0:
        msg = "Aviso: Máquina sem moedas para o troco! Contacte a administração."
    else:
        msg = "Compra efetuada com sucesso! Retire a sua bebida."
        produtos_quantidade[indice_produto] -= 1

        if troco > 0:
            print(" Moedas devolvidas:")
            for i in range(len(moedas)):
                if moedas_devolvidas[i] > 0:
                    print("\t", moedas[i], "cêntimos:", moedas_devolvidas[i], "moeda(s)")

        # SALVAR AUTOMATICAMENTE APÓS A COMPRA
        
        with open(arq_moedas, "w", encoding="utf-8") as f:
            for i in range(len(moedas)):
                f.write(str(moedas[i]) + ";" + str(moedas_quantidade[i]) + "\n")
        
        with open(arq_produtos, "w", encoding="utf-8") as f:
            for i in range(len(produtos)):
                f.write(str(produtos[i]) + ";" + str(precos[i]) + ";" + str(produtos_quantidade[i]) + "\n")
                
        # Guardar o registo desta compra no histórico
        novo_registo = "Produto: " + str(produtos[indice_produto]) + " | Moedas inseridas: " + moedas_inseridas_registo + "| Troco: " + str(troco) + " cênt."
        historico.append(novo_registo)
        
        with open(arq_historico, "a", encoding="utf-8") as f:
            f.write(novo_registo + "\n")

    input("\n Pressione enter para continuar ...")