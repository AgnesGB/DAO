# Projeto Padrões de Design - Implementação do Padrão DAO

Este projeto demonstra a implementação completa do **Padrão DAO (Data Access Object)** em Python com Django, incluindo boas práticas de desenvolvimento e outros padrões de design complementares.

## 🎯 Objetivo

Implementar uma arquitetura robusta utilizando o padrão DAO para separar a lógica de acesso a dados da lógica de negócio, garantindo:

- **Separação de responsabilidades**
- **Facilidade de manutenção**
- **Testabilidade**
- **Segurança de dados**
- **Flexibilidade para mudanças**

## 🏗️ Arquitetura Implementada

### Camadas da Aplicação

```
┌─────────────────────────────────────┐
│              VIEWS                  │  ← Interface com usuário (Django Views)
├─────────────────────────────────────┤
│             SERVICES                │  ← Lógica de negócio e validações
├─────────────────────────────────────┤
│               DAO                   │  ← Acesso a dados (Data Access Objects)
├─────────────────────────────────────┤
│             DOMÍNIO                 │  ← Entidades de negócio
├─────────────────────────────────────┤
│           SINGLETON                 │  ← Gerenciamento de conexões
├─────────────────────────────────────┤
│         BANCO DE DADOS              │  ← SQLite
└─────────────────────────────────────┘
```

## 📁 Estrutura do Projeto

```
projeto/
├── app/
│   ├── dao.py          # Implementação do padrão DAO
│   ├── services.py     # Camada de serviços com lógica de negócio
│   ├── dominio.py      # Entidades de domínio
│   ├── singleton.py    # Padrão Singleton para conexões
│   └── views.py        # Views Django atualizadas
├── teste_dao.py        # Testes automatizados
└── README.md          # Esta documentação
```

## 🔧 Padrões Implementados

### 1. **Padrão DAO (Data Access Object)**

#### Interface Base (DAO Abstrato)
```python
class DAO(ABC):
    @abstractmethod
    def incluir(self, obj: Any): pass
    
    @abstractmethod
    def alterar(self, obj: Any): pass
    
    @abstractmethod
    def excluir(self, obj: Any): pass
    
    @abstractmethod
    def selecionar_todos(self) -> list[Any]: pass
    
    @abstractmethod
    def selecionar_um(self, id: int) -> Optional[Any]: pass
```

#### Implementações Concretas
- **CategoriaDAO**: Gerencia operações CRUD para categorias
- **ProdutoDAO**: Gerencia operações CRUD para produtos

#### Características Implementadas:
- ✅ **Prepared Statements** para evitar SQL Injection
- ✅ **Tratamento de exceções** com logging
- ✅ **Transações** com commit/rollback automático
- ✅ **Conexões thread-safe**

### 2. **Padrão Factory**

```python
class DAOFactory:
    @staticmethod
    def get_categoria_dao() -> CategoriaDAO:
        return CategoriaDAO()
    
    @staticmethod
    def get_produto_dao() -> ProdutoDAO:
        return ProdutoDAO()
```

### 3. **Padrão Singleton**

Gerenciamento centralizado de conexões de banco de dados:

```python
class DatabaseConnection:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        # Implementação thread-safe do Singleton
```

### 4. **Padrão Service Layer**

Camada intermediária com lógica de negócio:

- **CategoriaService**: Validações e regras para categorias
- **ProdutoService**: Validações e regras para produtos

## 🚀 Funcionalidades Implementadas

### CategoriaDAO/Service
- ✅ CRUD completo (Create, Read, Update, Delete)
- ✅ Validação de descrição única
- ✅ Verificação de dependências antes da exclusão
- ✅ Listagem ordenada

### ProdutoDAO/Service
- ✅ CRUD completo com relacionamento categoria
- ✅ Busca por descrição (LIKE)
- ✅ Filtro por categoria
- ✅ Validações de preço e estoque
- ✅ Relatórios de estoque baixo
- ✅ Cálculo de valor total do estoque

## 🔒 Segurança Implementada

### Prepared Statements
Todos os comandos SQL utilizam prepared statements para evitar SQL Injection:

```python
def incluir(self, obj: Categoria) -> None:
    sql = "INSERT INTO Categoria(descricao) VALUES(?)"
    self.executar_sql(sql, (obj.descricao,))
```

### Validações de Entrada
- Campos obrigatórios
- Tipos de dados
- Regras de negócio
- Integridade referencial

## 🧪 Testes

Execute o arquivo de testes para validar a implementação:

```bash
python teste_dao.py
```

### Testes Incluídos:
- ✅ Padrão Singleton
- ✅ Operações CRUD do CategoriaDAO
- ✅ Validações do CategoriaService
- ✅ Operações CRUD do ProdutoDAO
- ✅ Validações do ProdutoService
- ✅ Relacionamentos entre entidades

## 🎮 Como Usar

### 1. Usando os DAOs Diretamente

```python
from app.dao import DAOFactory
from app.dominio import Categoria

# Criar DAO
dao = DAOFactory.get_categoria_dao()

# Criar categoria
categoria = Categoria(id=None, descricao="Eletrônicos")
dao.incluir(categoria)

# Listar todas
categorias = dao.selecionar_todos()
```

### 2. Usando os Services (Recomendado)

```python
from app.services import CategoriaService

# Criar service
service = CategoriaService()

# Criar categoria com validações
service.criar_categoria("Eletrônicos")

# Listar todas
categorias = service.listar_todas()
```

### 3. Nas Views Django

```python
def categorias(request):
    service = CategoriaService()
    
    if request.method == 'POST':
        try:
            service.criar_categoria(request.POST['descricao'])
            messages.success(request, 'Categoria criada!')
        except ValueError as e:
            messages.error(request, str(e))
    
    categorias = service.listar_todas()
    return render(request, 'template.html', {'categorias': categorias})
```

## 🔄 Melhorias Implementadas

### Antes (Código Original)
- ❌ SQL concatenado (vulnerável a injection)
- ❌ Sem tratamento de exceções
- ❌ Sem validações de negócio
- ❌ Código duplicado
- ❌ Conexões mal gerenciadas

### Depois (Com Padrão DAO)
- ✅ Prepared statements
- ✅ Tratamento completo de exceções
- ✅ Validações de negócio na camada Service
- ✅ Código reutilizável e organizadão
- ✅ Singleton para gerenciar conexões
- ✅ Separação clara de responsabilidades

## 📊 Benefícios Alcançados

### 1. **Manutenibilidade**
- Código organizado em camadas
- Responsabilidades bem definidas
- Fácil localização de bugs

### 2. **Testabilidade**
- DAOs podem ser mockados
- Testes unitários independentes
- Validação automática de funcionalidades

### 3. **Segurança**
- Proteção contra SQL Injection
- Validação de entrada de dados
- Tratamento adequado de erros

### 4. **Performance**
- Reutilização de conexões
- Transações otimizadas
- Queries eficientes

### 5. **Flexibilidade**
- Fácil mudança de banco de dados
- Adição de novas entidades simplificada
- Modificação de regras de negócio centralizadas

## 🎯 Conclusão

A implementação do padrão DAO neste projeto demonstra como uma arquitetura bem estruturada pode:

- **Melhorar a qualidade do código**
- **Facilitar a manutenção**
- **Aumentar a segurança**
- **Promover a reutilização**
- **Simplificar os testes**

O projeto serve como exemplo prático de como aplicar padrões de design em aplicações reais, seguindo as melhores práticas de desenvolvimento de software.

## 📝 Próximos Passos

Sugestões para melhorias futuras:
- [ ] Implementar cache de consultas
- [ ] Adicionar pool de conexões
- [ ] Criar interceptadores para auditoria
- [ ] Implementar paginação
- [ ] Adicionar métricas de performance
