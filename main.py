import json
import os
from tabulate import tabulate

ARQUIVO_CLIENTES = "clientes.json"

# Funções para salvar e carregar dados
def salvar_dados(clientes):
    with open(ARQUIVO_CLIENTES, "w", encoding="utf-8") as f:
        json.dump(clientes, f, indent=4, ensure_ascii=False)

def carregar_dados():
    if os.path.exists(ARQUIVO_CLIENTES):
        with open(ARQUIVO_CLIENTES, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

clientes = carregar_dados()

# ---------------- Funções principais ----------------
def adicionar_cliente():
    nome = input("Digite o nome do cliente: ").strip()
    if nome in clientes:
        print("⚠️ Cliente já cadastrado!")
    else:
        telefone = input("Digite o telefone do cliente: ").strip()
        clientes[nome] = {"telefone": telefone, "pagamentos": []}
        salvar_dados(clientes)
        print(f"✅ Cliente {nome} adicionado com sucesso!")

def registrar_pagamento():
    nome = input("Digite o nome do cliente: ").strip()
    if nome not in clientes:
        print("⚠️ Cliente não encontrado!")
        return

    if "pagamentos" not in clientes[nome]:
        clientes[nome]["pagamentos"] = []

    servico = input("Digite o tipo de serviço (Limpeza/Manutenção): ").capitalize()
    valor = float(input("Digite o valor do serviço: R$ "))
    pago = input("O cliente pagou? (s/n): ").lower() == "s"
    data = input("Digite a data do pagamento (ex: 20/08/2025): ")

    clientes[nome]["pagamentos"].append({
        "servico": servico,
        "valor": valor,
        "pago": pago,
        "data": data
    })
    salvar_dados(clientes)
    print("💰 Pagamento registrado com sucesso!")

def ver_pagamentos():
    nome = input("Digite o nome do cliente: ").strip()
    if nome not in clientes:
        print("⚠️ Cliente não encontrado!")
        return

    pagamentos = clientes[nome].get("pagamentos", [])
    if not pagamentos:
        print("⚠️ Nenhum pagamento registrado para este cliente.")
        return

    print(f"\n--- Pagamentos de {nome} ---")
    for i, p in enumerate(pagamentos, 1):
        status = "Pago" if p.get("pago", False) else "Em aberto"
        data = p.get("data", "-")
        servico = p.get("servico", "-")
        valor = p.get("valor", 0.0)
        print(f"\nPagamento {i}:")
        print(f"Serviço realizado: {servico}")
        print(f"Valor do serviço: R$ {valor}")
        print(f"Status do pagamento: {status}")
        print(f"Data do pagamento: {data}")

def editar_pagamento():
    nome = input("Digite o nome do cliente: ").strip()
    if nome not in clientes:
        print("⚠️ Cliente não encontrado!")
        return

    pagamentos = clientes[nome].get("pagamentos", [])
    if not pagamentos:
        print("⚠️ Nenhum pagamento registrado para este cliente.")
        return

    print(f"\n--- Pagamentos de {nome} ---")
    for i, p in enumerate(pagamentos, 1):
        status = "Pago" if p.get("pago", False) else "Em aberto"
        data = p.get("data", "-")
        servico = p.get("servico", "-")
        valor = p.get("valor", 0.0)
        print(f"{i}. {servico} - R$ {valor} - {status} - Data: {data}")

    try:
        escolha = int(input("Digite o número do pagamento que deseja editar: "))
        if 1 <= escolha <= len(pagamentos):
            pagamento = pagamentos[escolha - 1]
            print("Deixe em branco se não quiser alterar.")

            servico = input(f"Serviço atual ({pagamento.get('servico', '-')}) : ").capitalize() or pagamento.get('servico', '-')
            valor_input = input(f"Valor atual (R$ {pagamento.get('valor', 0.0)}): ")
            valor = float(valor_input) if valor_input else pagamento.get('valor', 0.0)
            pago_input = input(f"Status atual ({'Pago' if pagamento.get('pago', False) else 'Em aberto'}) (s/n): ")
            if pago_input.lower() == "s":
                pago = True
            elif pago_input.lower() == "n":
                pago = False
            else:
                pago = pagamento.get('pago', False)
            data = input(f"Data atual ({pagamento.get('data', '-')}) : ") or pagamento.get('data', '-')

            pagamento.update({
                "servico": servico,
                "valor": valor,
                "pago": pago,
                "data": data
            })
            salvar_dados(clientes)
            print("✏️ Pagamento atualizado com sucesso!")
        else:
            print("⚠️ Opção inválida.")
    except ValueError:
        print("⚠️ Entrada inválida. Digite um número.")

def remover_pagamento():
    nome = input("Digite o nome do cliente: ").strip()
    if nome not in clientes:
        print("⚠️ Cliente não encontrado!")
        return

    pagamentos = clientes[nome].get("pagamentos", [])
    if not pagamentos:
        print("⚠️ Nenhum pagamento registrado para este cliente.")
        return

    print(f"\n--- Pagamentos de {nome} ---")
    for i, p in enumerate(pagamentos, 1):
        status = "Pago" if p.get("pago", False) else "Em aberto"
        data = p.get("data", "-")
        servico = p.get("servico", "-")
        valor = p.get("valor", 0.0)
        print(f"{i}. {servico} - R$ {valor} - {status} - Data: {data}")

    try:
        escolha = int(input("Digite o número do pagamento que deseja remover: "))
        if 1 <= escolha <= len(pagamentos):
            removido = pagamentos.pop(escolha - 1)
            salvar_dados(clientes)
            print(f"🗑️ Pagamento de {removido.get('servico', '-')} no valor R$ {removido.get('valor', 0.0)} removido com sucesso!")
        else:
            print("⚠️ Opção inválida.")
    except ValueError:
        print("⚠️ Entrada inválida. Digite um número.")

def ver_ficha_cliente():
    nome = input("Digite o nome do cliente: ").strip()
    if nome not in clientes:
        print("⚠️ Cliente não encontrado!")
        return

    cliente = clientes[nome]
    print(f"\n--- Ficha do Cliente: {nome} ---")
    print(f"Telefone: {cliente.get('telefone', '-')}")
    print("\nPagamentos:")

    pagamentos = cliente.get("pagamentos", [])
    if not pagamentos:
        print("Nenhum pagamento registrado.")
    else:
        for i, p in enumerate(pagamentos, 1):
            status = "Pago" if p.get("pago", False) else "Em aberto"
            data = p.get("data", "-")
            servico = p.get("servico", "-")
            valor = p.get("valor", 0.0)
            print(f"\nPagamento {i}:")
            print(f"Serviço realizado: {servico}")
            print(f"Valor do serviço: R$ {valor}")
            print(f"Status do pagamento: {status}")
            print(f"Data do pagamento: {data}")

def editar_contato():
    nome = input("Digite o nome do cliente: ").strip()
    if nome not in clientes:
        print("⚠️ Cliente não encontrado!")
        return

    cliente = clientes[nome]
    print(f"\n--- Editar contato de {nome} ---")
    print(f"Telefone atual: {cliente.get('telefone', '-')}")
    
    novo_telefone = input("Digite o novo telefone (deixe em branco para manter o atual): ").strip()
    if novo_telefone:
        cliente['telefone'] = novo_telefone
        salvar_dados(clientes)
        print("✅ Telefone atualizado com sucesso!")
    else:
        print("ℹ️ Nenhuma alteração feita.")

def ver_tabela_clientes():
    tabela = []
    for nome, dados in clientes.items():
        telefone = dados.get("telefone", "-")
        pagamentos = dados.get("pagamentos", [])
        if pagamentos:
            for p in pagamentos:
                servico = p.get("servico", "-")
                valor = p.get("valor", 0.0)
                pago = "Pago" if p.get("pago", False) else "Em aberto"
                data = p.get("data", "-")
                tabela.append([nome, telefone, servico, valor, pago, data])
        else:
            tabela.append([nome, telefone, "-", "-", "-", "-"])

    headers = ["Cliente", "Telefone", "Serviço", "Valor", "Status", "Data"]
    print("\n" + tabulate(tabela, headers=headers, tablefmt="fancy_grid"))

# ---------------- Menu principal ----------------
def menu():
    while True:
        print("\n--- Sistema de Clientes ---")
        print("1. Adicionar cliente")
        print("2. Registrar pagamento")
        print("3. Ver clientes")
        print("4. Ver pagamentos de um cliente")
        print("5. Editar pagamento")
        print("6. Remover pagamento")
        print("7. Sair")
        print("8. Ver ficha de um cliente")
        print("9. Editar contato de um cliente")
        print("10. Ver todos os clientes em tabela")

        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            adicionar_cliente()
        elif opcao == "2":
            registrar_pagamento()
        elif opcao == "3":
            print("\n--- Clientes ---")
            for c in clientes:
                print(c)
        elif opcao == "4":
            ver_pagamentos()
        elif opcao == "5":
            editar_pagamento()
        elif opcao == "6":
            remover_pagamento()
        elif opcao == "7":
            print("👋 Saindo... Até mais!")
            break
        elif opcao == "8":
            ver_ficha_cliente()
        elif opcao == "9":
            editar_contato()
        elif opcao == "10":
            ver_tabela_clientes()
        else:
            print("⚠️ Opção inválida.")

menu()
