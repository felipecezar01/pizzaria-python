# Pizzaria Utilizando Python

![TELA 01](https://www.dropbox.com/scl/fi/5rtqbur2y8cyb0655fm9d/tela1.png?rlkey=7ajg4wgx47m1z1qeybs0a7yhm&raw=1)
![TELA 02](https://www.dropbox.com/scl/fi/qzit00iyn4f66gmy43ct0/tela2.png?rlkey=9tn9bekk47r8impka0pabipd1&raw=1)


## O que faz este projeto?

Ele tem uma tela de login e cadastro conectadas a um banco de dados. Existem 2 tipos de usuários: admin e comum. Se for um usuário comum, você terá acesso à tabela de produtos do banco de dados. Se for o admin, você, além de ver a tabela, poderá adicionar e remover produtos.

## O que eu aprendi com este projeto?

É meu primeiro projeto Python e quero destacar alguns aprendizados que adquiri:

1. **Tkinter**: é uma biblioteca para construção de interfaces gráficas;
2. **PyMySQL**: é uma biblioteca para que o python interaja com o banco de dados MySQL;
3. **Importar somente os componentes necessários** é importante pois melhora a legibilidade, otimiza a memória e melhora o desempenho de inicialização;
4. **Ter uma classe somente para a conexão do banco de dados** é mais prático;
5. **O uso de "_" no começo das variáveis em python** indicam que é um membro "privado" da classe, sugerindo que deve ser acessado apenas dentro da classe;
6. **Em python, quando uma classe é definida sem especificar uma superclasse**, ela implicitamente herda de 'object';
7. **Métodos mágicos**: em Python, também conhecidos como métodos especiais ou “dunder methods”, são funções que começam e terminam com dois sublinhados (underscores) e permitem que você personalize o comportamento de classes e objetos;
   - `__new__` é o método que efetivamente cria o objeto;
   - A **diferença de 'self' e 'cls'**: 'self' refere-se a instância específica da classe que está sendo usada, já 'cls' refere-se a própria classe, e não a uma instância dela. Na prática, se vc colocar 'self' no lugar de 'cls', irá tudo funcionar normalmente, porém é uma má prática. Isso é apenas uma convenção;
   - O Python vai seguir a regra de "mais específico para menos específico" na hierarquia de classes. Isso significa que ele vai procurar o método na classe mais específica primeiro;
   - `__new__` é o verdadeiro construtor em Python, responsável por criar a instância de uma classe;
   - `__init__` é um método de inicialização que configura um objeto após ele ter sido criado, sendo frequentemente referido como construtor devido ao seu papel na inicialização do objeto, embora tecnicamente seja um método de inicialização;
8. **cursorclass=pymysql.cursors.DictCursor**: Especifica que os dados retornados das consultas serão objetos DictCursor, que retornam os dados em um dicionário Python, com as colunas do banco de dados como chaves;
9. **if `__name__ == "__main__":`**
    É colocado no código de execução principal e não nos códigos módulos, pois irá ajudar a definir os fluxos de execução dos arquivos;
10. **`self.root = Tk()`**: cria uma janela;
11. **Entry**: é como se fosse o input no módulo tkinter;
12. **`%s`**: indica onde os valores de usuario e senha devem ser inseridos na consulta. O `%s` é usado como um placeholder (espaço reservado) na string da consulta SQL para indicar onde os valores dos parâmetros devem ser inseridos. Isso faz parte de uma prática chamada de parametrização de consultas, que é uma técnica importante para prevenir injeções SQL;
13. **`cursor.execute()` e `fetchone()`**: `cursor.execute()` executa uma consulta que busca por um usuário com um nome e senha específicos. O método `fetchone()` é então usado para recuperar o resultado dessa consulta. Se um registro correspondente é encontrado, `fetchone()` retorna uma tupla representando a linha encontrada (ou um dicionário, dependendo da configuração do cursor), permitindo-nos acessar informações como o nível de acesso do usuário. Se nenhum registro correspondente é encontrado, `fetchone()` retorna None, e o código pode tratar essa situação, por exemplo, exibindo uma mensagem de erro.

## Entendendo o Interpretador do Python

Observe o seguinte código:

```python
class Animal:
    def __init__(self, nome):
        print("Animal __init__")
        self.nome = nome

    def identificar(self):
        print(f"Eu sou um Animal chamado {self.nome}")

class Cachorro(Animal):  # Cachorro herda de Animal
    def __init__(self, nome, raca):
        super().__init__(nome)  # Chama o __init__ da superclasse Animal
        print("Cachorro __init__")
        self.raca = raca

    def identificar(self):
        super().identificar()  # Chama o método identificar() da superclasse Animal
        print(f"Eu sou um Cachorro da raça {self.raca}")

# Criando uma instância de Cachorro
rex = Cachorro("Rex", "Labrador")

# Chamando o método identificar
rex.identificar()
```

## **Você consegue fazer a sequência correta de prints?** Vamos detalhar!

1. **Definição da classe Animal**: A classe `Animal` é definida com um método construtor `__init__`, que é chamado automaticamente quando uma nova instância da classe é criada. Este método inicializa o objeto com o **nome do animal**. Há também um método `identificar` que, quando chamado, imprime uma mensagem indicando que o objeto é um animal e mostra seu nome.

2. **Definição da classe Cachorro**: A classe `Cachorro` é definida como subclasse da classe `Animal`, herdando suas propriedades e métodos. Ela tem seu próprio método construtor `__init__`, que chama o construtor da classe `Animal` usando `super().__init__(nome)` para inicializar o **nome do animal**. Após isso, inicializa um novo atributo, **raça**, e imprime uma mensagem. A classe `Cachorro` também tem um método `identificar` que sobrescreve o método da classe `Animal`, chamando primeiro a implementação da classe pai e, em seguida, imprimindo uma mensagem adicional que inclui a **raça do cachorro**.

3. **Criação de uma instância de Cachorro**: Quando a instância `rex` da classe `Cachorro` é criada com os argumentos "Rex" e "Labrador", o Python executa o seguinte:

   - **Chama o método `__init__` da classe `Cachorro`.**

   - **Dentro do método `__init__` da classe `Cachorro`, `super().__init__(nome)` é chamado**, o que por sua vez chama o método `__init__` da classe `Animal`. Isso resulta na execução do print "**Animal __init__**" e inicializa o atributo **nome** com o valor "Rex".

   - **Depois disso, a execução volta para o método `__init__` da classe `Cachorro`**, imprime "**Cachorro __init__**", e inicializa o atributo **raça** com o valor "Labrador".
   
4. **Chamada do método identificar**: Quando o método `identificar` é chamado no objeto `rex`, o seguinte ocorre:

   - **Primeiro, o método `identificar` da classe `Cachorro` é executado.** Dentro desse método, `super().identificar()` chama o método `identificar` da classe `Animal`, que imprime "**Eu sou um Animal chamado Rex**".
   
   - **Após a chamada do método da superclasse**, o método `identificar` da classe `Cachorro` continua sua execução, imprimindo "**Eu sou um Cachorro da raça Labrador**".


### Portando a saída é:

```python
Animal __init__
Cachorro __init__
Eu sou um Animal chamado Rex
Eu sou um Cachorro da raça Labrador"
```
