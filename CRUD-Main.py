import customtkinter as ctk
import csv
#importando TKINTER
from tkinter import*
import tkinter as tk
from tkinter import Tk, StringVar, ttk, Button
from tkinter import messagebox
# imagem
from PIL import Image, ImageTk

# FUNÇÃO PARA CRIAR O ARQUIVO --------------------------------------------------------------------------------------------------------------------------------------------
def criar_arquivo():
    with open("dados.txt", "w") as arquivo:
        arquivo.write("")

    with open('numero.csv', 'w', encoding='cp1252', newline='\r\n') as arquivo:
        writer = csv.writer(arquivo)

# FUNÇÃO PARA LER O ARQUIVO ----------------------------------------------------------------------------------------------------------------------------------------------
def ler_arquivo():
    try:
        with open('numero.csv', 'r', encoding='cp1252', newline='\r\n') as arquivo_csv:
            leitor_csv = csv.reader(arquivo_csv)
            dados = list(map(str.strip, row) for row in leitor_csv)
            dados = [linha for linha in dados if any(c.strip() for c in linha)]
        return dados
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        return []
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return []
    

# FUNÇÃO COLETAR DADOS ---------------------------------------------------------------------------------------------------------------------------------------------------
def inserir_registro():
    nome = entrada_nome.get()
    idade = entrada_idade.get()
    sexo = entrada_sexo.get()
    matricula = entrada_matricula.get()
    nota1 = entrada_nota1.get()
    nota2 = entrada_nota2.get()
    nota3 = entrada_nota3.get()

    if not nome or not idade or not sexo or not matricula or not nota1 or not nota2 or not nota3:
        messagebox.showerror("Erro", "Preencha todos os campos antes de inserir um registro.")
        return
    try:
        nota1 = float(nota1.replace(',', '.'))
        nota2 = float(nota2.replace(',', '.'))
        nota3 = float(nota3.replace(',', '.'))
    except ValueError:
        messagebox.showerror("Erro", "As notas devem ser números válidos.")
        return
    
    media = (nota1 + nota2 + nota3) / 3
    media = round(media, 1)

    dados = [nome, idade, sexo, matricula, nota1, nota2, nota3, media]

    registros = ler_arquivo()

    registros.append(dados)

    registros_ordenados = sorted(registros, key=lambda x: x[0].lower())

    with open("numero.csv", "w", newline='') as arquivo:
        writer = csv.writer(arquivo)
        writer.writerows(registros_ordenados)
    
    mostrar_tabela()
    exibir()
    apagar()



# Função para limpar os campos -------------------------------------------------------------------------------------------------------------------------------------------
def apagar():
    entrada_nome.delete(0, tk.END)
    entrada_idade.delete(0, tk.END)
    entrada_sexo.delete(0, tk.END)
    entrada_matricula.delete(0, tk.END)
    entrada_nota1.delete(0, tk.END)
    entrada_nota2.delete(0, tk.END)
    entrada_nota3.delete(0, tk.END)




# FUNÇÃO PARA EXIBIR DADOS -----------------------------------------------------------------------------------------------------------------------------------------------
def exibir():
    var_nome_exibir = entrada_nome.get()
    var_matricula_exibir = entrada_matricula.get()

    if not var_matricula_exibir and not var_nome_exibir:
        messagebox.showerror("Erro", "Por favor, informe a matrícula ou o nome a serem exibidos.")
        return

    dados = ler_arquivo()

    for widget in frameMeioD.winfo_children():
        widget.destroy()

    for i, linha in enumerate(dados):
        matricula_atual = linha[3].strip()
        nome_atual = linha[0]

        if (var_matricula_exibir and matricula_atual == var_matricula_exibir) or \
           (var_nome_exibir and nome_atual == var_nome_exibir):
            
            for j, (rotulo, elemento) in enumerate(zip(["Nome", "Idade", "Sexo", "Matrícula", "Nota", "Nota", "Nota", "Média"], linha)):
                label_item = Label(frameMeioD, text=f"{rotulo}: {elemento}", font=('ivy 10 bold'), bg='gray')
                label_item.place(x=10, y=i * 5 + j * 20)
        
    if not frameMeioD.winfo_children():
        label_aviso = Label(frameMeioD, text="Matrícula ou nome não encontrados.")
        label_aviso.place(x=10, y=10)
    apagar()


# FUNÇÃO PARA ATUALIZAR REGISTRO------------------------------------------------------------------------------------------------------------------------------------------

def atualizar_registro():
    nome = entrada_nome.get()
    idade = entrada_idade.get()
    sexo = entrada_sexo.get()
    matricula = entrada_matricula.get()
    nota1 = entrada_nota1.get()
    nota2 = entrada_nota2.get()
    nota3 = entrada_nota3.get()

    if not nota1 or not nota2 or not nota3:
        messagebox.showerror("Erro", "As notas devem ser inseridas.")
        return

    try:
        nota1 = float(nota1.replace(',', '.'))
        nota2 = float(nota2.replace(',', '.'))
        nota3 = float(nota3.replace(',', '.'))
    except ValueError:
        messagebox.showerror("Erro", "As notas devem ser números válidos.")
        return

    media = (nota1 + nota2 + nota3) / 3
    media = round(media, 1)

    dados = ler_arquivo()
    dados_atualizados = []

    for i, linha in enumerate(dados):
        try:
            # Verifica se o elemento em dados[i] é uma string
            if isinstance(linha, list):
                if len(linha) >= 4:
                    nome_atual = linha[0].strip()
                    matricula_atual = linha[3].strip()

                    if matricula_atual == matricula or nome_atual == nome:
                        linha[0] = nome
                        linha[1] = str(idade)
                        linha[2] = sexo
                        linha[3] = matricula
                        linha[4] = str(nota1)
                        linha[5] = str(nota2)
                        linha[6] = str(nota3)
                        linha[7] = str(media)

                dados_atualizados.append(",".join(linha))

        except IndexError:
            messagebox.showerror("Erro", f"A linha {i + 1} não possui o número esperado de elementos.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar a linha {i + 1}: {e}")

    with open("numero.csv", "r+", encoding='cp1252', newline='\r\n') as arquivo:
        arquivo.writelines('\n'.join(dado.strip() for dado in dados_atualizados if isinstance(dado, str) and dado.strip()))

    mostrar_tabela()
    exibir()
    apagar()




# FUNÇÃO PARA EXCLUIR DADOS ----------------------------------------------------------------------------------------------------------------------------------------------
def excluir():
    var_matricula_excluir = entrada_matricula.get()
    var_nome_excluir = entrada_nome.get()

    if not var_matricula_excluir and not var_nome_excluir:
        messagebox.showerror("Erro", "Por favor, informe a matrícula ou nome a ser excluído.")
        return

    dados = ler_arquivo()

    dados_atualizados = []

    for linha in dados:
        if len(linha) >= 4:
            matricula = linha[3].strip()
            nome = linha[0].strip()
            if matricula != var_matricula_excluir and nome != var_nome_excluir:
                dados_atualizados.append(",".join(map(str, linha)))

    with open("numero.csv", "w", encoding='cp1252', newline='\r\n') as arquivo:
        arquivo.writelines('\n'.join(dados_atualizados))

    messagebox.showinfo("Sucesso", "Registro excluído com sucesso!")

    mostrar_tabela()
    apagar()

# CRIAR INTERFACE (Janela)------------------------------------------------------------------------------------------------------------------------------------------------
janela = tk.Tk()
janela.title ("Cadastro de Alunos")
janela.geometry('900x600')
janela.resizable(width=FALSE, height= FALSE)

# Divisão de frame -------------------------------------------------------------------------------------------------------------------------------------------------------
frameCima = Frame(janela, width=1043, height=50, bg='gray', relief=FLAT)
frameCima.place(x=0, y=1)

frameMeioD = Frame(janela, width=200, height=290, bg='gray', pady=20, relief=FLAT)
frameMeioD.place(x=698, y=52)

frameMeioE = Frame(janela, width=695, height=290, bg='gray', pady=20, relief=FLAT)
frameMeioE.place(x=0, y=52)

frameBaixo = Frame(janela, width=1043, height=450, bg='gray', relief=FLAT)
frameBaixo.place(x=0, y=343)


# Trabalhando no frame Cima ----------------------------------------------------------------------------------------------------------------------------------------------

# Abrindo imagem 
app_img = Image.open('imagem1.png')
app_img = app_img.resize((45,45))
app_img = ImageTk.PhotoImage(app_img)


app_logo = Label(frameCima, 
                 image=app_img, 
                 text='     Cadastro de Aluno', 
                 width=900, 
                 compound=LEFT,
                 relief=RAISED, 
                 anchor=NW, 
                 #OR CENTER
                 font=('verdana 20 bold'), 
                 bg='gray', 
                 foreground="black",
                 justify=CENTER 
                 )
app_logo.place(x=0, y=0)

#Frame Meio---------------------------------------------------------------------------------------------------------------------------------------------------------------
# CAIXAS DE ENTRADA

l_nome = Label(frameMeioE, text='Nome', height=1, anchor=NW, font=('ivy 10 bold'), bg='gray', fg='black')
l_nome.place(x=100, y=20)
entrada_nome = Entry(frameMeioE, width=30, justify='left', relief='solid')
entrada_nome.place(x=180, y=21)

l_idade = Label(frameMeioE, text='Idade', height=1, anchor=NW, font=('ivy 10 bold'), bg='gray', fg='black')
l_idade.place(x=100, y=50)
entrada_idade = Entry(frameMeioE, width=30, justify='left', relief='solid')
entrada_idade.place(x=180, y=51)

l_sexo = Label(frameMeioE, text='Sexo', height=1, anchor=NW, font=('ivy 10 bold'), bg='gray', fg='black')
l_sexo.place(x=100, y=80)
entrada_sexo = Entry(frameMeioE, width=30, justify='left', relief='solid')
entrada_sexo.place(x=180, y=81)

l_matricula = Label(frameMeioE, text='matricula', height=1, anchor=NW, font=('ivy 10 bold'), bg='gray', fg='black')
l_matricula.place(x=100, y=110)
entrada_matricula = Entry(frameMeioE, width=30, justify='left', relief='solid')
entrada_matricula.place(x=180, y=111)

l_nota1 = Label(frameMeioE, text='Nota', height=1, anchor=NW, font=('ivy 10 bold'), bg='gray', fg='black')
l_nota1.place(x=100, y=140)
entrada_nota1 = Entry(frameMeioE, width=30, justify='left', relief='solid')
entrada_nota1.place(x=180, y=141)


l_nota2 = Label(frameMeioE, text='Nota', height=1, anchor=NW, font=('ivy 10 bold'), bg='gray', fg='black')
l_nota2.place(x=100, y=170)
entrada_nota2 = Entry(frameMeioE, width=30, justify='left', relief='solid')
entrada_nota2.place(x=180, y=171)


l_nota3 = Label(frameMeioE, text='Nota', height=1, anchor=NW, font=('ivy 10 bold'), bg='gray', fg='black')
l_nota3.place(x=100, y=200)
entrada_nota3 = Entry(frameMeioE, width=30, justify='left', relief='solid')
entrada_nota3.place(x=180, y=201)



# BOTÕES -----------------------------------------------------------------------------------------------------------------------------------------------------------------

b_inserir = Button(frameMeioE, command=inserir_registro , width=30, text= "    Inserir".upper(), compound=CENTER,anchor=NW, overrelief=RIDGE, relief='solid', font=('ivy 8 bold'), bg='black', fg='gray')
b_inserir.place(x=430, y=20)

b_exibir = Button(frameMeioE, width=30, command= exibir ,text= "    Exibir".upper(), compound=CENTER,anchor=NW, overrelief=RIDGE, relief='solid', font=('ivy 8 bold'), bg='black', fg='gray')
b_exibir.place(x=430, y=50)

b_atualizar = Button(frameMeioE, command=atualizar_registro , width=30, text= "    Atualizar".upper(), compound=CENTER,anchor=NW, overrelief=RIDGE, relief='solid', font=('ivy 8 bold'), bg='black', fg='gray')
b_atualizar.place(x=430, y=80)

b_excluir = Button(frameMeioE, command=excluir , width=30, text= "    Excluir".upper(), compound=CENTER,anchor=NW, overrelief=RIDGE, relief='solid', font=('ivy 8 bold'), bg='black', fg='gray')
b_excluir.place(x=430, y=110)



# TABELA------------------------------------------------------------------------------------------------------------------------------------------------------------------
global tree

def ler_arquivo():
    try:
        with open("numero.csv", "r") as arquivo:
            leitor_csv = csv.reader(arquivo)
            dados = list(leitor_csv)
        return dados
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        return []
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return []
    

def exibir_info_selecionada(tree, event):
    item = tree.selection()
    if item:
        values = tree.item(item, 'values')

        entrada_matricula.delete(0, tk.END)  
        entrada_matricula.insert(0, values[3])  

        exibir()


def exibir_info(values):
    var_matricula_exibir = values[3].strip()

    if not var_matricula_exibir:
        messagebox.showerror("Erro", "Por favor, informe a matrícula a ser exibida.")
        return

    dados = ler_arquivo()

    for widget in frameMeioD.winfo_children():
        widget.destroy()


    for i, linha in enumerate(dados):
        matricula_atual = linha[3].strip()

        if matricula_atual == var_matricula_exibir:
            for j, (rotulo, elemento) in enumerate(zip(["Nome", "Idade", "Sexo", "Matrícula", "Nota", "Nota", "Nota", "Média"], linha)):
                label_item = Label(frameMeioD, text=f"{rotulo}: {elemento}", font=('ivy 10 bold'), bg='gray')
                label_item.place(x=10, y=i * 5 + j * 20)
            break  

    if not frameMeioD.winfo_children():
        label_aviso = Label(frameMeioD, text="Matrícula não encontrada.")
        label_aviso.place(x=10, y=10)


def mostrar_tabela():

    tabela_head = ['Nome', 'Idade', 'Sexo', 'Matricula', 'Nota1', 'Nota2', 'Nota3', 'Media']

    lista_itens = ler_arquivo()

    tree = ttk.Treeview(frameBaixo, columns=tabela_head, show="headings")

    vsb = ttk.Scrollbar(frameBaixo, orient="vertical", command=tree.yview)

    hsb = ttk.Scrollbar(frameBaixo, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    tree.configure(xscrollcommand=hsb.set)
    tree.grid(column=0, row=0, sticky='nsew')
    hsb.grid(column=0, row=1, sticky='ew')
    frameBaixo.grid_rowconfigure(0, weight=12)

    hd = ["center", "center", "center", "center", "center", "center", "center", 'center']
    h = [250, 90, 90, 90, 90, 90, 90, 90]
    n = 0

    for col in tabela_head:
        tree.heading(col, text=col.title(), anchor=CENTER)
        tree.column(col, width=h[n], anchor=hd[n])
        n += 1

    for item in lista_itens:
        tree.insert('', 'end', values=item)

    tree.bind('<ButtonRelease-1>', lambda event: exibir_info_selecionada(tree, event))

mostrar_tabela()



janela.mainloop()