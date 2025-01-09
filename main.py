import json

class Produto:
    def __init__(self, id, nome, categoria, quantidade, preco):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.quantidade = quantidade
        self.preco = preco

    def __str__(self):
        return f"ID: {self.id}, Nome: {self.nome}, Categoria: {self.categoria}, Quantidade: {self.quantidade}, Preço: {self.preco}"

class Estoque:
    def __init__(self, arquivo):
        self.arquivo = arquivo
        self.produtos = self.carregar_produtos()

    def carregar_produtos(self):
        try:
            with open(self.arquivo, "r") as file:
                produtos_data = json.load(file)
                return [Produto(**produto) for produto in produtos_data]
        except FileNotFoundError:
            return []

    def salvar_produtos(self):
        with open(self.arquivo, "w") as file:
            json.dump([produto.__dict__ for produto in self.produtos], file, indent=4)

    def adicionar_produto(self, nome, categoria, quantidade, preco):
        novo_id = len(self.produtos) + 1
        novo_produto = Produto(novo_id, nome, categoria, quantidade, preco)
        self.produtos.append(novo_produto)
        self.salvar_produtos()

    def listar_produtos(self):
        if self.produtos:
            for produto in self.produtos:
                print(produto)
        else:
            print("Nenhum produto encontrado.")

    def buscar_produto(self, termo):
        encontrados = [produto for produto in self.produtos if termo.lower() in produto.nome.lower()]
        if encontrados:
            for produto in encontrados:
                print(produto)
        else:
            print("Produto não encontrado.")

    def atualizar_produto(self, id_produto, nome=None, categoria=None, quantidade=None, preco=None):
        produto = next((p for p in self.produtos if p.id == id_produto), None)
        if produto:
            if nome:
                produto.nome = nome
            if categoria:
                produto.categoria = categoria
            if quantidade:
                produto.quantidade = quantidade
            if preco:
                produto.preco = preco
            self.salvar_produtos()
            print(f"Produto ID {id_produto} atualizado com sucesso.")
        else:
            print(f"Produto ID {id_produto} não encontrado.")

    def excluir_produto(self, id_produto):
        produto = next((p for p in self.produtos if p.id == id_produto), None)
        if produto:
            self.produtos.remove(produto)
            self.salvar_produtos()
            print(f"Produto ID {id_produto} excluído com sucesso.")
        else:
            print(f"Produto ID {id_produto} não encontrado.")

def menu():
    estoque = Estoque("estoque.json")

    while True:
        print("\n1. Adicionar Produto")
        print("2. Listar Produtos")
        print("3. Buscar Produto")
        print("4. Atualizar Produto")
        print("5. Excluir Produto")
        print("6. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome do Produto: ")
            categoria = input("Categoria: ")
            quantidade = int(input("Quantidade: "))
            preco = float(input("Preço: "))
            estoque.adicionar_produto(nome, categoria, quantidade, preco)

        elif opcao == "2":
            estoque.listar_produtos()

        elif opcao == "3":
            termo = input("Digite o nome ou parte do nome do produto: ")
            estoque.buscar_produto(termo)

        elif opcao == "4":
            id_produto = int(input("Digite o ID do produto a ser atualizado: "))
            nome = input("Novo Nome (deixe em branco para não alterar): ")
            categoria = input("Nova Categoria (deixe em branco para não alterar): ")
            quantidade = input("Nova Quantidade (deixe em branco para não alterar): ")
            preco = input("Novo Preço (deixe em branco para não alterar): ")

            estoque.atualizar_produto(
                id_produto,
                nome if nome else None,
                categoria if categoria else None,
                int(quantidade) if quantidade else None,
                float(preco) if preco else None
            )

        elif opcao == "5":
            id_produto = int(input("Digite o ID do produto a ser excluído: "))
            estoque.excluir_produto(id_produto)

        elif opcao == "6":
            print("Saindo...")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()

