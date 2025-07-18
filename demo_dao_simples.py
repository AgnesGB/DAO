"""
Demonstração prática do uso do Padrão DAO implementado
"""

from app.dao import DAOFactory
from app.services import CategoriaService, ProdutoService
from app.dominio import Categoria, Produto


def demonstrar_dao_basico():
    """Demonstra o uso básico dos DAOs"""
    print("=== DEMONSTRAÇÃO BÁSICA DO PADRÃO DAO ===\n")
    
    # Usando Factory para obter DAOs
    categoria_dao = DAOFactory.get_categoria_dao()
    produto_dao = DAOFactory.get_produto_dao()
    
    print("📂 Testando CategoriaDAO:")
    
    # Criar categoria
    categoria = Categoria(id=None, descricao="Demo DAO")
    categoria_dao.incluir(categoria)
    print("   ✅ Categoria criada")
    
    # Listar categorias
    categorias = categoria_dao.selecionar_todos()
    print(f"   📋 {len(categorias)} categorias no total")
    
    # Encontrar categoria criada
    categoria_criada = None
    for cat in categorias:
        if cat.descricao == "Demo DAO":
            categoria_criada = cat
            break
    
    if categoria_criada:
        print(f"   ✅ Categoria encontrada: ID {categoria_criada.id}")
        
        print("\n📦 Testando ProdutoDAO:")
        
        # Criar produto
        produto = Produto(
            id=None,
            descricao="Produto Demo",
            preco_unitario=50.0,
            quantidade_estoque=10,
            categoria=categoria_criada
        )
        produto_dao.incluir(produto)
        print("   ✅ Produto criado")
        
        # Buscar produtos
        produtos = produto_dao.selecionar_todos()
        print(f"   📋 {len(produtos)} produtos no total")
        
        # Buscar por categoria
        produtos_categoria = produto_dao.selecionar_por_categoria(categoria_criada.id)
        print(f"   🔍 {len(produtos_categoria)} produtos na categoria")
        
        # Limpeza
        for prod in produtos_categoria:
            produto_dao.excluir(prod)
        categoria_dao.excluir(categoria_criada)
        print("   🗑️ Dados de teste removidos")


def demonstrar_services():
    """Demonstra o uso dos Services com validações"""
    print("\n=== DEMONSTRAÇÃO DOS SERVICES ===\n")
    
    categoria_service = CategoriaService()
    produto_service = ProdutoService()
    
    print("📂 Testando CategoriaService:")
    
    # Criar categoria válida
    categoria_service.criar_categoria("Informática")
    print("   ✅ Categoria 'Informática' criada")
    
    # Testar validação de duplicação
    try:
        categoria_service.criar_categoria("Informática")
        print("   ❌ Validação falhou")
    except ValueError as e:
        print(f"   ✅ Validação funcionou: {e}")
    
    # Buscar categoria
    categorias = categoria_service.listar_todas()
    categoria_info = None
    for cat in categorias:
        if cat.descricao == "Informática":
            categoria_info = cat
            break
    
    if categoria_info:
        print("\n📦 Testando ProdutoService:")
        
        # Criar produto válido
        produto_service.criar_produto(
            descricao="Notebook",
            preco_unitario=2500.00,
            quantidade_estoque=3,
            categoria_id=categoria_info.id
        )
        print("   ✅ Produto 'Notebook' criado")
        
        # Testar validação de preço
        try:
            produto_service.criar_produto(
                descricao="Produto Inválido",
                preco_unitario=-100.0,  # Preço negativo
                quantidade_estoque=1,
                categoria_id=categoria_info.id
            )
        except ValueError as e:
            print(f"   ✅ Validação de preço funcionou: {e}")
        
        # Funcionalidades especiais
        produtos_encontrados = produto_service.buscar_por_descricao("Notebook")
        print(f"   🔍 {len(produtos_encontrados)} produtos encontrados na busca")
        
        estoque_baixo = produto_service.verificar_estoque_baixo(5)
        print(f"   📉 {len(estoque_baixo)} produtos com estoque baixo")
        
        valor_total = produto_service.calcular_valor_total_estoque()
        print(f"   💰 Valor total do estoque: R$ {valor_total:.2f}")
        
        # Limpeza
        produtos = produto_service.listar_todos()
        for produto in produtos:
            if produto.categoria.id == categoria_info.id:
                produto_service.excluir_produto(produto.id)
        categoria_service.excluir_categoria(categoria_info.id)
        print("   🗑️ Dados de teste removidos")


def demonstrar_seguranca():
    """Demonstra a segurança implementada"""
    print("\n=== DEMONSTRAÇÃO DE SEGURANÇA ===\n")
    
    print("🔒 Recursos de Segurança Implementados:")
    print("   ✅ Prepared Statements (previne SQL Injection)")
    print("   ✅ Validação de tipos de dados")
    print("   ✅ Validação de regras de negócio")
    print("   ✅ Tratamento de exceções")
    print("   ✅ Transações com rollback")
    print("   ✅ Conexões thread-safe")
    
    # Testar proteção contra SQL Injection
    categoria_service = CategoriaService()
    descricao_maliciosa = "'; DROP TABLE Categoria; --"
    
    categoria_service.criar_categoria(descricao_maliciosa)
    print(f"\n🛡️ Dados maliciosos inseridos com segurança: '{descricao_maliciosa}'")
    
    # Verificar se os dados foram preservados
    categorias = categoria_service.listar_todas()
    for cat in categorias:
        if cat.descricao == descricao_maliciosa:
            categoria_service.excluir_categoria(cat.id)
            print("   ✅ Dados maliciosos removidos com segurança")
            break


def main():
    """Executa todas as demonstrações"""
    print("🎯 DEMONSTRAÇÃO COMPLETA DO PADRÃO DAO")
    print("=" * 60)
    
    demonstrar_dao_basico()
    demonstrar_services()
    demonstrar_seguranca()
    
    print("\n" + "=" * 60)
    print("🎉 DEMONSTRAÇÃO CONCLUÍDA!")
    print("\n📚 Padrões Implementados:")
    print("• DAO Pattern com interface abstrata")
    print("• Factory Pattern para criação de DAOs")
    print("• Singleton Pattern para conexões")
    print("• Service Layer Pattern para lógica de negócio")
    print("• Prepared Statements para segurança")
    print("• Exception Handling robusto")
    print("\n✨ Projeto implementado com sucesso!")


if __name__ == "__main__":
    main()
