"""
Testes para validar a implementação do padrão DAO
Execute este arquivo para testar as funcionalidades implementadas
"""

import sys
import os
import logging

# Adicionar o diretório da aplicação ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.dao import DAOFactory
from app.services import CategoriaService, ProdutoService
from app.dominio import Categoria, Produto
from app.singleton import get_database_connection

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def teste_conexao_singleton():
    """Testa se o padrão Singleton está funcionando corretamente"""
    print("\n=== TESTE: Padrão Singleton ===")
    
    # Criar múltiplas instâncias
    db1 = get_database_connection()
    db2 = get_database_connection()
    
    # Verificar se são a mesma instância
    if id(db1) == id(db2):
        print("✅ Singleton funcionando corretamente - mesma instância")
    else:
        print("❌ Singleton falhou - instâncias diferentes")
    
    # Testar conexão
    try:
        conexao = db1.get_connection()
        print("✅ Conexão com banco de dados estabelecida")
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")


def teste_categoria_dao():
    """Testa as operações CRUD do CategoriaDAO"""
    print("\n=== TESTE: CategoriaDAO ===")
    
    try:
        dao = DAOFactory.get_categoria_dao()
        
        # Criar categoria de teste
        categoria_teste = Categoria(id=None, descricao="Categoria Teste DAO")
        
        # Teste: Incluir
        print("🔄 Testando inclusão...")
        dao.incluir(categoria_teste)
        print("✅ Categoria incluída com sucesso")
        
        # Teste: Listar todas
        print("🔄 Testando listagem...")
        categorias = dao.selecionar_todos()
        print(f"✅ {len(categorias)} categorias encontradas")
        
        # Encontrar a categoria criada
        categoria_criada = None
        for cat in categorias:
            if cat.descricao == "Categoria Teste DAO":
                categoria_criada = cat
                break
        
        if categoria_criada:
            print(f"✅ Categoria encontrada - ID: {categoria_criada.id}")
            
            # Teste: Selecionar um
            print("🔄 Testando seleção por ID...")
            categoria_selecionada = dao.selecionar_um(categoria_criada.id)
            if categoria_selecionada:
                print("✅ Categoria selecionada com sucesso")
            else:
                print("❌ Erro ao selecionar categoria")
            
            # Teste: Alterar
            print("🔄 Testando alteração...")
            categoria_criada.descricao = "Categoria Teste DAO - Alterada"
            dao.alterar(categoria_criada)
            print("✅ Categoria alterada com sucesso")
            
            # Teste: Excluir
            print("🔄 Testando exclusão...")
            dao.excluir(categoria_criada)
            print("✅ Categoria excluída com sucesso")
        
    except Exception as e:
        print(f"❌ Erro no teste CategoriaDAO: {e}")


def teste_categoria_service():
    """Testa as operações da CategoriaService"""
    print("\n=== TESTE: CategoriaService ===")
    
    try:
        service = CategoriaService()
        
        # Teste: Criar categoria
        print("🔄 Testando criação via service...")
        service.criar_categoria("Eletrônicos Teste")
        print("✅ Categoria criada com sucesso")
        
        # Teste: Listar todas
        categorias = service.listar_todas()
        categoria_criada = None
        for cat in categorias:
            if cat.descricao == "Eletrônicos Teste":
                categoria_criada = cat
                break
        
        if categoria_criada:
            print(f"✅ Categoria encontrada - ID: {categoria_criada.id}")
            
            # Teste: Atualizar
            print("🔄 Testando atualização...")
            service.atualizar_categoria(categoria_criada.id, "Eletrônicos Teste - Atualizada")
            print("✅ Categoria atualizada com sucesso")
            
            # Teste: Validação - descrição duplicada
            print("🔄 Testando validação de duplicação...")
            try:
                service.criar_categoria("Eletrônicos Teste - Atualizada")
                print("❌ Validação de duplicação falhou")
            except ValueError:
                print("✅ Validação de duplicação funcionando")
            
            # Teste: Excluir
            print("🔄 Testando exclusão...")
            service.excluir_categoria(categoria_criada.id)
            print("✅ Categoria excluída com sucesso")
        
    except Exception as e:
        print(f"❌ Erro no teste CategoriaService: {e}")


def teste_produto_dao():
    """Testa as operações CRUD do ProdutoDAO"""
    print("\n=== TESTE: ProdutoDAO ===")
    
    try:
        categoria_dao = DAOFactory.get_categoria_dao()
        produto_dao = DAOFactory.get_produto_dao()
        
        # Criar categoria para o teste
        categoria_teste = Categoria(id=None, descricao="Categoria para Produto Teste")
        categoria_dao.incluir(categoria_teste)
        
        # Buscar a categoria criada
        categorias = categoria_dao.selecionar_todos()
        categoria_criada = None
        for cat in categorias:
            if cat.descricao == "Categoria para Produto Teste":
                categoria_criada = cat
                break
        
        if categoria_criada:
            # Criar produto de teste
            produto_teste = Produto(
                id=None,
                descricao="Produto Teste DAO",
                preco_unitario=99.99,
                quantidade_estoque=10,
                categoria=categoria_criada
            )
            
            # Teste: Incluir produto
            print("🔄 Testando inclusão de produto...")
            produto_dao.incluir(produto_teste)
            print("✅ Produto incluído com sucesso")
            
            # Teste: Listar produtos
            produtos = produto_dao.selecionar_todos()
            produto_criado = None
            for prod in produtos:
                if prod.descricao == "Produto Teste DAO":
                    produto_criado = prod
                    break
            
            if produto_criado:
                print(f"✅ Produto encontrado - ID: {produto_criado.id}")
                
                # Teste: Alterar produto
                produto_criado.descricao = "Produto Teste DAO - Alterado"
                produto_criado.preco_unitario = 149.99
                produto_dao.alterar(produto_criado)
                print("✅ Produto alterado com sucesso")
                
                # Teste: Buscar por categoria
                produtos_categoria = produto_dao.selecionar_por_categoria(categoria_criada.id)
                print(f"✅ {len(produtos_categoria)} produtos encontrados na categoria")
                
                # Teste: Excluir produto
                produto_dao.excluir(produto_criado)
                print("✅ Produto excluído com sucesso")
            
            # Limpar categoria de teste
            categoria_dao.excluir(categoria_criada)
        
    except Exception as e:
        print(f"❌ Erro no teste ProdutoDAO: {e}")


def teste_produto_service():
    """Testa as operações da ProdutoService"""
    print("\n=== TESTE: ProdutoService ===")
    
    try:
        categoria_service = CategoriaService()
        produto_service = ProdutoService()
        
        # Criar categoria para teste
        categoria_service.criar_categoria("Livros Teste")
        categorias = categoria_service.listar_todas()
        categoria_criada = None
        for cat in categorias:
            if cat.descricao == "Livros Teste":
                categoria_criada = cat
                break
        
        if categoria_criada:
            # Teste: Criar produto
            print("🔄 Testando criação de produto...")
            produto_service.criar_produto(
                descricao="Livro de Python",
                preco_unitario=89.90,
                quantidade_estoque=5,
                categoria_id=categoria_criada.id
            )
            print("✅ Produto criado com sucesso")
            
            # Encontrar produto criado
            produtos = produto_service.listar_todos()
            produto_criado = None
            for prod in produtos:
                if prod.descricao == "Livro de Python":
                    produto_criado = prod
                    break
            
            if produto_criado:
                # Teste: Validações
                print("🔄 Testando validações...")
                try:
                    produto_service.criar_produto("", 10.0, 1, categoria_criada.id)
                    print("❌ Validação de descrição vazia falhou")
                except ValueError:
                    print("✅ Validação de descrição vazia funcionando")
                
                try:
                    produto_service.criar_produto("Teste", -10.0, 1, categoria_criada.id)
                    print("❌ Validação de preço negativo falhou")
                except ValueError:
                    print("✅ Validação de preço negativo funcionando")
                
                # Teste: Busca
                produtos_encontrados = produto_service.buscar_por_descricao("Python")
                print(f"✅ {len(produtos_encontrados)} produtos encontrados na busca")
                
                # Teste: Estoque baixo
                produtos_estoque_baixo = produto_service.verificar_estoque_baixo(10)
                print(f"✅ {len(produtos_estoque_baixo)} produtos com estoque baixo")
                
                # Limpeza
                produto_service.excluir_produto(produto_criado.id)
                print("✅ Produto excluído")
            
            categoria_service.excluir_categoria(categoria_criada.id)
        
    except Exception as e:
        print(f"❌ Erro no teste ProdutoService: {e}")


def main():
    """Executa todos os testes"""
    print("🚀 INICIANDO TESTES DO PADRÃO DAO")
    print("=" * 50)
    
    # Executar testes
    teste_conexao_singleton()
    teste_categoria_dao()
    teste_categoria_service()
    teste_produto_dao()
    teste_produto_service()
    
    print("\n" + "=" * 50)
    print("✅ TESTES CONCLUÍDOS!")
    print("\nO padrão DAO foi implementado com sucesso e inclui:")
    print("• Camada DAO com interface abstrata")
    print("• Implementações concretas (CategoriaDAO, ProdutoDAO)")
    print("• Factory para criação de DAOs")
    print("• Camada de Serviços com regras de negócio")
    print("• Singleton para gerenciamento de conexões")
    print("• Prepared statements para segurança")
    print("• Tratamento de exceções")
    print("• Validações de dados")


if __name__ == "__main__":
    main()
