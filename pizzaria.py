from tkinter import Tk, Label, Entry, Button, messagebox, Toplevel, font
import tkinter.ttk as ttk
import pymysql.cursors

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.connection = None
        return cls._instance

    def connect(self):
        if not self.connection:
            try:
                self.connection = pymysql.connect(
                    host='localhost',
                    user='root',
                    password='',
                    db='erp',
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor
                )
            except Exception as e:
                print(f'Erro ao conectar ao banco de dados: {e}')
                return None
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

class JanelaLogin:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.root = Tk()
        self.root.title('Login')
        self.root.configure(bg='#f0f0f0')
        fontStyle = font.Font(family="Arial", size=12)

        Label(self.root, text='Usuário', bg='#f0f0f0', font=fontStyle).grid(row=0, column=0, pady=10, padx=10)
        self.usuario = Entry(self.root, font=fontStyle)
        self.usuario.grid(row=0, column=1, pady=10, padx=10)

        Label(self.root, text='Senha', bg='#f0f0f0', font=fontStyle).grid(row=1, column=0, pady=10, padx=10)
        self.senha = Entry(self.root, show='*', font=fontStyle)
        self.senha.grid(row=1, column=1, pady=10, padx=10)

        Button(self.root, text='Login', command=self.verifica_login, bg='#0078D7', fg='white', font=fontStyle).grid(row=2, column=0, columnspan=2, pady=10)
        Button(self.root, text='Cadastrar', command=self.cadastrar_usuario_ui, bg='#f0f0f0', fg='black', font=fontStyle).grid(row=3, column=0, columnspan=2, pady=10)

        self.root.mainloop()

    def verifica_login(self):
        usuario = self.usuario.get()
        senha = self.senha.get()
        connection = self.db_connection.connect()
        if connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM cadastros WHERE nome = %s AND senha = %s', (usuario, senha))
                resultado = cursor.fetchone()
                if resultado:
                    messagebox.showinfo("Login", "Login bem-sucedido!")
                    self.root.destroy()
                    nivel_acesso = resultado['nivel']
                    AdminJanela(self.db_connection, nivel_acesso)
                else:
                    messagebox.showerror("Login", "Usuário ou senha inválidos.")
            self.db_connection.close()

    def cadastrar_usuario_ui(self):
        self.cadastro_window = Toplevel(self.root)
        self.cadastro_window.title('Cadastro de Usuário')
        fontStyle = font.Font(family="Arial", size=12)

        Label(self.cadastro_window, text='Usuário', font=fontStyle).grid(row=0, column=0, pady=10, padx=10)
        self.novo_usuario = Entry(self.cadastro_window, font=fontStyle)
        self.novo_usuario.grid(row=0, column=1, pady=10, padx=10)

        Label(self.cadastro_window, text='Senha', font=fontStyle).grid(row=1, column=0, pady=10, padx=10)
        self.nova_senha = Entry(self.cadastro_window, show='*', font=fontStyle)
        self.nova_senha.grid(row=1, column=1, pady=10, padx=10)

        Button(self.cadastro_window, text='Cadastrar', command=self.efetivar_cadastro_usuario, bg='#0078D7', fg='white', font=fontStyle).grid(row=2, column=0, columnspan=2, pady=10)

    def efetivar_cadastro_usuario(self):
        usuario = self.novo_usuario.get()
        senha = self.nova_senha.get()
        nivel_acesso = 1  # Por padrão, todos os novos usuários terão nível de acesso 1.
        connection = self.db_connection.connect()
        if connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute('INSERT INTO cadastros (nome, senha, nivel) VALUES (%s, %s, %s)', (usuario, senha, nivel_acesso))
                    connection.commit()
                    messagebox.showinfo("Cadastro", "Cadastro realizado com sucesso.")
                    self.cadastro_window.destroy()
                except Exception as e:
                    messagebox.showerror("Erro", f"Falha ao cadastrar usuário: {e}")
            self.db_connection.close()

class AdminJanela:
    def __init__(self, db_connection, nivel_acesso):
        self.db_connection = db_connection
        self.nivel_acesso = nivel_acesso
        self.root = Tk()
        self.root.title('Administração')
        self.root.configure(bg='#f0f0f0')
        self.setup_ui()

    def setup_ui(self):
        fontStyle = font.Font(family="Arial", size=12)
        buttonStyle = {'bg': '#0078D7', 'fg': 'white', 'font': fontStyle}

        if self.nivel_acesso == 1:
            self.visualizar_produtos()
        elif self.nivel_acesso == 2:
            Button(self.root, text='Cadastrar Produto', command=self.cadastrar_produto, **buttonStyle).grid(row=0, column=0, padx=10, pady=10)
            Button(self.root, text='Remover Produto', command=self.remover_produto_ui, **buttonStyle).grid(row=1, column=0, padx=10, pady=10)
            self.visualizar_produtos()

    def visualizar_produtos(self):
        self.tree = ttk.Treeview(self.root, columns=('Nome', 'Ingredientes', 'Grupo', 'Preço'), show='headings')
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
        self.tree.grid(row=2, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)
        self.atualizar_lista_produtos()

    # Os métodos cadastrar_produto, efetivar_cadastro, remover_produto_ui, remover_produto e atualizar_lista_produtos permanecem os mesmos.


    def cadastrar_produto(self):
        cadastro_window = Toplevel(self.root)
        cadastro_window.title('Cadastro de Produto')

        campos = ['Nome', 'Ingredientes', 'Grupo', 'Preço']
        self.entries = {}
        for i, campo in enumerate(campos):
            Label(cadastro_window, text=campo).grid(row=i, column=0)
            entry = Entry(cadastro_window)
            entry.grid(row=i, column=1)
            self.entries[campo] = entry

        Button(cadastro_window, text='Cadastrar', command=self.efetivar_cadastro).grid(row=len(campos), column=0,
                                                                                       columnspan=2)

    def efetivar_cadastro(self):
        dados = {campo: entry.get() for campo, entry in self.entries.items()}
        connection = self.db_connection.connect()
        if connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute('INSERT INTO produtos(nome, ingredientes, grupo, preco) VALUES(%s, %s, %s, %s)',
                                   (dados['Nome'], dados['Ingredientes'], dados['Grupo'], dados['Preço']))
                    connection.commit()
                    messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso.")
                except Exception as e:
                    messagebox.showerror("Erro", f"Falha ao cadastrar produto: {e}")
            self.db_connection.close()
        self.atualizar_lista_produtos()

    def remover_produto_ui(self):
        selecionado = self.tree.focus()
        if not selecionado:
            messagebox.showerror("Erro", "Selecione um produto para remover.")
            return

        dados = self.tree.item(selecionado, 'values')
        nome_produto = dados[0]

        resposta = messagebox.askyesno("Confirmação", f"Tem certeza que deseja remover o produto {nome_produto}?")
        if resposta:
            self.remover_produto(nome_produto)

    def remover_produto(self, nome_produto):
        connection = self.db_connection.connect()
        if connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute('DELETE FROM produtos WHERE nome = %s', (nome_produto,))
                    connection.commit()
                    messagebox.showinfo("Sucesso", "Produto removido com sucesso.")
                except Exception as e:
                    messagebox.showerror("Erro", f"Falha ao remover produto: {e}")
            self.db_connection.close()
        self.atualizar_lista_produtos()

    def atualizar_lista_produtos(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        connection = self.db_connection.connect()
        if connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT nome, ingredientes, grupo, preco FROM produtos')
                for produto in cursor.fetchall():
                    self.tree.insert('', 'end', values=(
                    produto['nome'], produto['ingredientes'], produto['grupo'], produto['preco']))
            self.db_connection.close()

def main():
    db_connection = DatabaseConnection()
    JanelaLogin(db_connection)

if __name__ == "__main__":
    main()
