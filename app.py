import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

# Arquivo onde os dados serão salvos
ARQUIVO_CLIENTES = "clientes.json"

# ---------------- FUNÇÕES ---------------- #

def carregar_clientes():
    if os.path.exists(ARQUIVO_CLIENTES):
        with open(ARQUIVO_CLIENTES, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_clientes(clientes):
    with open(ARQUIVO_CLIENTES, "w", encoding="utf-8") as f:
        json.dump(clientes, f, indent=4, ensure_ascii=False)

def atualizar_lista():
    listbox_clientes.delete(0, tk.END)
    for cliente in clientes.keys():
        listbox_clientes.insert(tk.END, cliente)

def adicionar_cliente():
    nome = entry_nome.get().strip()
    telefone = entry_telefone.get().strip()
    obs = entry_obs.get("1.0", tk.END).strip()
    if not nome:
        messagebox.showwarning("Erro", "O nome do cliente é obrigatório!")
        return
    if nome in clientes:
        messagebox.showwarning("Erro", "Cliente já existe!")
        return
    clientes[nome] = {"telefone": telefone, "obs": obs, "servicos": [], "pagamentos": []}
    salvar_clientes(clientes)
    atualizar_lista()
    entry_nome.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)
    entry_obs.delete("1.0", tk.END)

def mostrar_detalhes(event=None):
    selection = listbox_clientes.curselection()
    if not selection:
        return
    nome = listbox_clientes.get(selection[0])
    cliente = clientes[nome]

    label_nome.config(text=f"Nome: {nome}")
    label_telefone.config(text=f"📞 Telefone: {cliente['telefone']}")
    label_obs.config(text=f"📝 Observações: {cliente.get('obs', '')}")


    for i in tree_servicos.get_children():
        tree_servicos.delete(i)
    for servico in cliente["servicos"]:
        tree_servicos.insert("", tk.END, values=(servico["data"], servico["descricao"]))

    for i in tree_pagamentos.get_children():
        tree_pagamentos.delete(i)
    for pagamento in cliente["pagamentos"]:
        tree_pagamentos.insert("", tk.END, values=(pagamento["data"], pagamento["valor"]))

def adicionar_servico():
    selection = listbox_clientes.curselection()
    if not selection:
        messagebox.showwarning("Erro", "Selecione um cliente primeiro!")
        return
    nome = listbox_clientes.get(selection[0])
    data = entry_data_servico.get().strip()
    descricao = entry_servico.get().strip()
    if not data or not descricao:
        messagebox.showwarning("Erro", "Preencha todos os campos do serviço!")
        return
    clientes[nome]["servicos"].append({"data": data, "descricao": descricao})
    salvar_clientes(clientes)
    mostrar_detalhes()
    entry_data_servico.delete(0, tk.END)
    entry_servico.delete(0, tk.END)

def adicionar_pagamento():
    selection = listbox_clientes.curselection()
    if not selection:
        messagebox.showwarning("Erro", "Selecione um cliente primeiro!")
        return
    nome = listbox_clientes.get(selection[0])
    data = entry_data_pagamento.get().strip()
    valor = entry_pagamento.get().strip()
    if not data or not valor:
        messagebox.showwarning("Erro", "Preencha todos os campos do pagamento!")
        return
    clientes[nome]["pagamentos"].append({"data": data, "valor": valor})
    salvar_clientes(clientes)
    mostrar_detalhes()
    entry_data_pagamento.delete(0, tk.END)
    entry_pagamento.delete(0, tk.END)

def editar_cliente_gui():
    selection = listbox_clientes.curselection()
    if not selection:
        messagebox.showwarning("Erro", "Selecione um cliente para editar!")
        return
    nome = listbox_clientes.get(selection[0])
    cliente = clientes[nome]

    edit_window = tk.Toplevel(root)
    edit_window.title("Editar Cliente")

    tk.Label(edit_window, text="Nome:").grid(row=0, column=0)
    entry_nome_edit = tk.Entry(edit_window)
    entry_nome_edit.insert(0, nome)
    entry_nome_edit.grid(row=0, column=1)

    tk.Label(edit_window, text="Telefone:").grid(row=1, column=0)
    entry_telefone_edit = tk.Entry(edit_window)
    entry_telefone_edit.insert(0, cliente["telefone"])
    entry_telefone_edit.grid(row=1, column=1)

    tk.Label(edit_window, text="Observações:").grid(row=2, column=0)
    entry_obs_edit = tk.Text(edit_window, height=4, width=30)
    entry_obs_edit.insert("1.0", cliente["obs"])
    entry_obs_edit.grid(row=2, column=1)

    def salvar_edicao():
        novo_nome = entry_nome_edit.get().strip()
        telefone = entry_telefone_edit.get().strip()
        obs = entry_obs_edit.get("1.0", tk.END).strip()
        if not novo_nome:
            messagebox.showwarning("Erro", "O nome do cliente é obrigatório!")
            return
        if novo_nome != nome and novo_nome in clientes:
            messagebox.showwarning("Erro", "Já existe um cliente com esse nome!")
            return

        clientes.pop(nome)
        clientes[novo_nome] = {"telefone": telefone, "obs": obs,
                               "servicos": cliente["servicos"],
                               "pagamentos": cliente["pagamentos"]}
        salvar_clientes(clientes)
        atualizar_lista()
        mostrar_detalhes()
        edit_window.destroy()

    tk.Button(edit_window, text="Salvar", command=salvar_edicao).grid(row=3, column=0, columnspan=2)

def excluir_cliente():
    selection = listbox_clientes.curselection()
    if not selection:
        messagebox.showwarning("Erro", "Selecione um cliente para excluir!")
        return

    nome = listbox_clientes.get(selection[0])
    resposta = messagebox.askyesno("Excluir Cliente",
                                   f"Tem certeza que deseja excluir o cliente '{nome}'?\nIsso apagará todos os serviços e pagamentos dele.")
    if resposta:
        if nome in clientes:
            del clientes[nome]
            salvar_clientes(clientes)
            atualizar_lista()
            label_nome.config(text="Nome:")
            label_telefone.config(text="📞 Telefone:")
            label_obs.config(text="📝 Observações:")
            for i in tree_servicos.get_children(): tree_servicos.delete(i)
            for i in tree_pagamentos.get_children(): tree_pagamentos.delete(i)
            messagebox.showinfo("✅ Sucesso", f"Cliente '{nome}' excluído!")

def editar_servico():
    selection_cliente = listbox_clientes.curselection()
    if not selection_cliente:
        messagebox.showwarning("Erro", "Selecione um cliente primeiro!")
        return
    nome = listbox_clientes.get(selection_cliente[0])

    selection_servico = tree_servicos.selection()
    if not selection_servico:
        messagebox.showwarning("Erro", "Selecione um serviço para editar!")
        return

    item = tree_servicos.item(selection_servico[0])
    data_antiga, desc_antiga = item["values"]

    edit_window = tk.Toplevel(root)
    edit_window.title("Editar Serviço")

    tk.Label(edit_window, text="Data:").grid(row=0, column=0)
    entry_data_edit = tk.Entry(edit_window)
    entry_data_edit.insert(0, data_antiga)
    entry_data_edit.grid(row=0, column=1)

    tk.Label(edit_window, text="Descrição:").grid(row=1, column=0)
    entry_desc_edit = tk.Entry(edit_window, width=30)
    entry_desc_edit.insert(0, desc_antiga)
    entry_desc_edit.grid(row=1, column=1)

    def salvar_edicao():
        nova_data = entry_data_edit.get().strip()
        nova_desc = entry_desc_edit.get().strip()
        if not nova_data or not nova_desc:
            messagebox.showwarning("Erro", "Preencha todos os campos!")
            return

        for servico in clientes[nome]["servicos"]:
            if servico["data"] == data_antiga and servico["descricao"] == desc_antiga:
                servico["data"] = nova_data
                servico["descricao"] = nova_desc
                break

        salvar_clientes(clientes)
        mostrar_detalhes()
        edit_window.destroy()

    tk.Button(edit_window, text="Salvar", command=salvar_edicao).grid(row=2, column=0, columnspan=2)

def excluir_servico():
    selection_cliente = listbox_clientes.curselection()
    if not selection_cliente:
        messagebox.showwarning("Erro", "Selecione um cliente primeiro!")
        return
    nome = listbox_clientes.get(selection_cliente[0])

    selection_servico = tree_servicos.selection()
    if not selection_servico:
        messagebox.showwarning("Erro", "Selecione um serviço para excluir!")
        return

    item = tree_servicos.item(selection_servico[0])
    data, desc = item["values"]

    resposta = messagebox.askyesno("Excluir Serviço", f"Tem certeza que deseja excluir o serviço '{desc}' do cliente {nome}?")
    if resposta:
        clientes[nome]["servicos"] = [s for s in clientes[nome]["servicos"] if not (s["data"] == data and s["descricao"] == desc)]
        salvar_clientes(clientes)
        mostrar_detalhes()
        messagebox.showinfo("✅ Sucesso", f"Serviço '{desc}' excluído!")

# --- Função para editar pagamento ---
# ...existing code...

def editar_pagamento():
    selection_cliente = listbox_clientes.curselection()
    if not selection_cliente:
        messagebox.showwarning("Atenção", "Selecione um cliente primeiro!")
        return
    nome = listbox_clientes.get(selection_cliente[0])

    selecionado = tree_pagamentos.selection()
    if not selecionado:
        messagebox.showwarning("Atenção", "Selecione um pagamento para editar.")
        return

    item = tree_pagamentos.item(selecionado[0])
    data_antiga, valor_antigo = item["values"]

    janela_editar = tk.Toplevel(root)
    janela_editar.title("Editar Pagamento")

    tk.Label(janela_editar, text="Data:").grid(row=0, column=0, padx=5, pady=5)
    entry_data_edit = tk.Entry(janela_editar)
    entry_data_edit.insert(0, data_antiga)
    entry_data_edit.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(janela_editar, text="Valor:").grid(row=1, column=0, padx=5, pady=5)
    entry_valor_edit = tk.Entry(janela_editar)
    entry_valor_edit.insert(0, valor_antigo)
    entry_valor_edit.grid(row=1, column=1, padx=5, pady=5)

    def salvar_alteracao():
        nova_data = entry_data_edit.get().strip()
        novo_valor = entry_valor_edit.get().strip()
        if not nova_data or not novo_valor:
            messagebox.showwarning("Erro", "Preencha todos os campos!")
            return
        for pagamento in clientes[nome]["pagamentos"]:
            if pagamento["data"] == data_antiga and pagamento["valor"] == valor_antigo:
                pagamento["data"] = nova_data
                pagamento["valor"] = novo_valor
                break
        salvar_clientes(clientes)
        mostrar_detalhes()
        janela_editar.destroy()
        messagebox.showinfo("Sucesso", "Pagamento atualizado com sucesso!")

    tk.Button(janela_editar, text="Salvar", command=salvar_alteracao).grid(row=2, column=0, columnspan=2, pady=10)

def excluir_pagamento():
    selection_cliente = listbox_clientes.curselection()
    if not selection_cliente:
        messagebox.showwarning("Atenção", "Selecione um cliente primeiro!")
        return
    nome = listbox_clientes.get(selection_cliente[0])

    selecionado = tree_pagamentos.selection()
    if not selecionado:
        messagebox.showwarning("Atenção", "Selecione um pagamento para excluir.")
        return

    item = tree_pagamentos.item(selecionado[0])
    data, valor = item["values"]

    resposta = messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este pagamento?")
    if resposta:
        clientes[nome]["pagamentos"] = [
            p for p in clientes[nome]["pagamentos"]
            if not (p["data"] == data and p["valor"] == valor)
        ]
        salvar_clientes(clientes)
        mostrar_detalhes()
        messagebox.showinfo("Sucesso", "Pagamento excluído com sucesso!")
# ...existing code...


# ---------------- INTERFACE ---------------- #

root = tk.Tk()
root.title("Gerenciador de Clientes")

clientes = carregar_clientes()

frame_esq = tk.Frame(root)
frame_esq.pack(side=tk.LEFT, padx=10, pady=10)

listbox_clientes = tk.Listbox(frame_esq, width=30, height=15)
listbox_clientes.pack()
listbox_clientes.bind("<<ListboxSelect>>", mostrar_detalhes)

tk.Label(frame_esq, text="Nome:").pack()
entry_nome = tk.Entry(frame_esq, width=30)
entry_nome.pack()
tk.Label(frame_esq, text="Telefone:").pack()
entry_telefone = tk.Entry(frame_esq, width=30)
entry_telefone.pack()
tk.Label(frame_esq, text="Observações:").pack()
entry_obs = tk.Text(frame_esq, width=25, height=3)
entry_obs.pack()

tk.Button(frame_esq, text="➕ Adicionar Cliente", width=25, command=adicionar_cliente).pack(pady=3)
tk.Button(frame_esq, text="✏️ Editar Cliente", width=25, command=editar_cliente_gui).pack(pady=3)
tk.Button(frame_esq, text="🗑️ Excluir Cliente", width=25, command=excluir_cliente).pack(pady=3)
tk.Button(frame_esq, text="✏️ Editar Serviço", command=editar_servico).pack(pady=3)
tk.Button(frame_esq, text="🗑️ Excluir Serviço", command=excluir_servico).pack(pady=3)
tk.Button(frame_esq, text="✏️ Editar Pagamento", command=editar_pagamento).pack(pady=3)
tk.Button(frame_esq, text="🗑️ Excluir Pagamento", command=excluir_pagamento).pack(pady=3)


frame_dir = tk.Frame(root)
frame_dir.pack(side=tk.LEFT, padx=10, pady=10)

label_nome = tk.Label(frame_dir, text="Nome:", font=("Arial", 12, "bold"))
label_nome.pack()
label_telefone = tk.Label(frame_dir, text="📞 Telefone:", font=("Arial", 12))
label_telefone.pack()
label_obs = tk.Label(frame_dir, text="📝 Observações:", font=("Arial", 12))
label_obs.pack()

tk.Label(frame_dir, text="Serviços:").pack()
tree_servicos = ttk.Treeview(frame_dir, columns=("Data", "Descrição"), show="headings", height=5)
tree_servicos.heading("Data", text="Data")
tree_servicos.heading("Descrição", text="Descrição")
tree_servicos.pack()

tk.Label(frame_dir, text="Adicionar Serviço:").pack()
entry_data_servico = tk.Entry(frame_dir, width=15)
entry_data_servico.pack()
entry_servico = tk.Entry(frame_dir, width=40)
entry_servico.pack()
tk.Button(frame_dir, text="Adicionar Serviço", command=adicionar_servico).pack(pady=3)

tk.Label(frame_dir, text="Pagamentos:").pack()
tree_pagamentos = ttk.Treeview(frame_dir, columns=("Data", "Valor"), show="headings", height=5)
tree_pagamentos.heading("Data", text="Data")
tree_pagamentos.heading("Valor", text="Valor")
tree_pagamentos.pack()

tk.Label(frame_dir, text="Adicionar Pagamento:").pack()
entry_data_pagamento = tk.Entry(frame_dir, width=15)
entry_data_pagamento.pack()
entry_pagamento = tk.Entry(frame_dir, width=40)
entry_pagamento.pack()
tk.Button(frame_dir, text="Adicionar Pagamento", command=adicionar_pagamento).pack(pady=3)

atualizar_lista()
root.mainloop()
