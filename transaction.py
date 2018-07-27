# Criado por: Alcides Dias

# Função que adiciona a transação ao arquivo transaction.txt
def nova_transacao(tipo, cod, quant, unidade, final):
    arq = open("transaction.txt", "r", encoding="ISO-8859-1")
    produtos = arq.read()

    if produtos == '':
        numero = 1
    else:
        produtos = produtos.replace('\n', '') # Retirando '\n' para não atrapalhar o len abaixo
        numero = int((len(produtos) / 30) + 1) # Cálculo para descobrir o número da transação

    arq.close()

    # Espaçamentos para padronizar a formatação
    espnum = espcod = espquant = espunid = espfinal = ''

    if len(str(numero)) < 4: espnum = (4 - len(str(numero))) * ' '
    if len(str(cod)) < 4: espcod = (4 - len(str(cod))) * ' '
    if len(str(quant)) < 4: espquant = (4 - len(str(quant))) * ' '
    if len(str(unidade)) < 8: espunid = (8 - len(str(unidade))) * ' '
    if len(str(final)) < 8: espfinal = (8 - len(str(final))) * ' '

    # Adicionando a nova transação ao final do arquivo
    arq = open("transaction.txt", "a", encoding="ISO-8859-1")
    arq.write(str(numero) + espnum + tipo + ' ' + str(cod) + espcod +
              str(quant) + espquant + str(unidade) + espunid + str(final) + espfinal + "\n")
    arq.close()
    return

# Função para atualizar produtos no arquivo produtos.txt
def alterar_produtos(tipo, index, quantidade):
    arq = open("produtos.txt", "r", encoding="ISO-8859-1")
    produtos = arq.readlines()
    arq.close()

    esp = ''

    if len(str(int(produtos[index][40:44]))) < 4:               # Se a quantidade não tiver 4 caracteres...
        esp = (4 - len(str(int(produtos[index][40:44])))) * ' ' # adiciona caracteres em branco

    # Condição para saber se é compra (adicionar) ou venda (subtrair) de produtos
    # linhaalt é a linha que substituirá a antiga, alterando apenas a quantidade
    if tipo == 'C':
        linhaalt = produtos[index][:40] + str(int(produtos[index][40:44]) + quantidade) + esp + produtos[index][44:]
    else:
        linhaalt = produtos[index][:40] + str(int(produtos[index][40:44]) - quantidade) + esp + produtos[index][44:]

    # Recriando o arquivo com a linha alterada
    arq = open("produtos.txt", "w", encoding="ISO-8859-1")
    for linha in produtos:
        if produtos.index(linha) == index:
            arq.write(linhaalt)
        else:
            arq.write(linha)
    arq.close()
    return

# Função para operação de compra
def comprar(codigo, quantidade):
    cont = 0 # Serve para descobrir o índice da linha a ser alterada
    arq = open("produtos.txt", "r", encoding="ISO-8859-1")
    produtos = arq.readlines()
    arq.close()

    for linha in produtos:
        if codigo == int(linha[:4]): # Se o código corresponder...
            valoru = float(linha[34:40])
            valorf = float(linha[34:40]) * quantidade

            alterar_produtos('C', cont, quantidade)
            nova_transacao('C', codigo, quantidade, valoru, valorf)

            print("Compra efetuada com sucesso!\n")
            return

        cont += 1
    print("Código inválido!\n")
    return


# Função para operação de venda
def vender(codigo, quantidade):
    cont = 0
    arq = open("produtos.txt", "r", encoding="ISO-8859-1")
    produtos = arq.readlines()
    arq.close()

    # A diferença da compra está no segundo if, pois é necessário
    # saber se há quantidade suficiente para vender
    for linha in produtos:
        if codigo == int(linha[:4]): # Se o código corresponder...
            if quantidade <= int(linha[40:44]):
                valoru = float(linha[34:40])
                valorf = float(linha[34:40]) * quantidade

                alterar_produtos('V', cont, quantidade)
                nova_transacao('V', codigo, quantidade, valoru, valorf)

                print("Venda efetuada com sucesso!\n")
                return
            else:
                print("Quantidade insuficiente!\n")
                return
        cont += 1
    print("Código inválido!\n")
    return

# Programa principal
while True:
    print("Gerenciamento de transações\n"
          "Menu:\n"
          "C - Comprar\n"
          "V - Vender\n"
          "X - Encerrar\n")

    tipotran = input("Digite o código desejado: ")

    if tipotran.upper() == 'X':
        print("Programa encerrado.")
        break
    elif tipotran.upper() == 'C' or tipotran.upper() == 'V':
        codprod = int(input("Digite o código do produto: "))
        qnt = int(input("Digite a quantidade desejada: "))
        print()

        # Chamar função correspondente da operação
        if tipotran.upper() == 'C':
            comprar(codprod, qnt)
        else:
            vender(codprod, qnt)
    else:
        print("Comando inválido! Tente novamente.\n")
