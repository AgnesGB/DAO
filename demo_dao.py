"""
Demonstração prática do uso do Padrão DAO implementado
Este arquivo mostra como utilizar as funcionalidades implementadas
"""

from app.dao import DAOFactory
from app.services import CategoriaService, ProdutoService
from app.dominio import Categoria, Produto


def demonstrar_uso_dao():
    """Demonstra o uso direto dos DAOs"""
    print("=== DEMONSTRAÇÃO: Uso Direto dos DAOs ===\n")
    
    # 1. Usando Factory para obter DAOs
    categoria_dao = DAOFactory.get_categoria_dao()
    produto_dao = DAOFactory.get_produto_dao()
    
    # 2. Operações com Categoria
    print("📂 Trabalhando com Categorias:")
    
    # Criar categoria
    categoria = Categoria(id=None, descricao="Exemplo DAO")
    categoria_dao.incluir(categoria)
    print("   ✅ Categoria criada")
    
    # Listar categorias
    categorias = categoria_dao.selecionar_todos()
    categoria_criada = None
    for cat in categorias:
        if cat.descricao == "Exemplo DAO":
            categoria_criada = cat
            print(f"   📋 Categoria encontrada: ID {cat.id} - {cat.descricao}")
            break
    
    # 3. Operações com Produto
    if categoria_criada:
        print("\n📦 Trabalhando com Produtos:")
        
        # Criar produto
        produto = Produto(
            id=None,
            descricao="Produto Exemplo",
            preco_unitario=25.50,
            quantidade_estoque=15,
            categoria=categoria_criada
        )
        produto_dao.incluir(produto)
        print("   ✅ Produto criado")
        
        # Buscar produtos da categoria
        produtos_categoria = produto_dao.selecionar_por_categoria(categoria_criada.id)
        print(f"   📋 {len(produtos_categoria)} produtos na categoria")
        
        # Buscar por descrição
        produtos_encontrados = produto_dao.buscar_por_descricao("Exemplo")
        print(f"   🔍 {len(produtos_encontrados)} produtos encontrados na busca")
        
        # Limpeza
        for prod in produtos_categoria:
            produto_dao.excluir(prod)
        print("   🗑️ Produtos removidos")
    
    # Limpeza final
    if categoria_criada:
        categoria_dao.excluir(categoria_criada)
        print("   🗑️ Categoria removida")


def demonstrar_uso_services():
    """Demonstra o uso dos Services (camada recomendada)"""
    print("\n=== DEMONSTRAÇÃO: Uso dos Services (Recomendado) ===\n")
    
    # 1. Instanciar Services
    categoria_service = CategoriaService()
    produto_service = ProdutoService()
    
    # 2. Operações com validações
    print("📂 Categorias com Validações:")
    
    try:
        # Criar categoria válida
        categoria_service.criar_categoria("Tecnologia")
        print("   ✅ Categoria 'Tecnologia' criada")
        
        # Tentar criar categoria duplicada (validação deve impedir)
        try:
            categoria_service.criar_categoria("Tecnologia")
        except ValueError as e:
            print(f"   ⚠️ Validação funcionando: {e}")
        
        # Tentar criar categoria vazia (validação deve impedir)
        try:
            categoria_service.criar_categoria("")
        except ValueError as e:
            print(f"   ⚠️ Validação funcionando: {e}")
        
        # Buscar categoria criada
        categorias = categoria_service.listar_todas()
        categoria_tecnologia = None
        for cat in categorias:
            if cat.descricao == "Tecnologia":
                categoria_tecnologia = cat
                break
        
        if categoria_tecnologia:
            print("\n📦 Produtos com Validações:")
            
            # Criar produto válido
            produto_service.criar_produto(
                descricao="Smartphone Android",
                preco_unitario=899.99,
                quantidade_estoque=5,
                categoria_id=categoria_tecnologia.id
            )
            print("   ✅ Produto 'Smartphone Android' criado")
            
            # Tentar criar produto com preço inválido
            try:
                produto_service.criar_produto(
                    descricao="Produto Inválido",
                    preco_unitario=-50.0,  # Preço negativo
                    quantidade_estoque=1,
                    categoria_id=categoria_tecnologia.id
                )
            except ValueError as e:
                print(f"   ⚠️ Validação funcionando: {e}")
            
            # Tentar criar produto com estoque negativo
            try:
                produto_service.criar_produto(
                    descricao="Produto Inválido 2",
                    preco_unitario=100.0,
                    quantidade_estoque=-5,  # Estoque negativo
                    categoria_id=categoria_tecnologia.id
                )
            except ValueError as e:
                print(f"   ⚠️ Validação funcionando: {e}")
            
            # 3. Funcionalidades especiais
            print("\n📊 Funcionalidades Especiais:")
            
            # Buscar produtos por descrição
            produtos_android = produto_service.buscar_por_descricao("Android")
            print(f"   🔍 {len(produtos_android)} produtos com 'Android' encontrados")
            
            # Verificar estoque baixo
            produtos_estoque_baixo = produto_service.verificar_estoque_baixo(10)
            print(f"   📉 {len(produtos_estoque_baixo)} produtos com estoque baixo")
            
            # Calcular valor total do estoque
            valor_total = produto_service.calcular_valor_total_estoque()
            print(f"   💰 Valor total do estoque: R$ {valor_total:.2f}")
            
            # Limpeza
            produtos = produto_service.listar_todos()
            for produto in produtos:
                if produto.categoria.id == categoria_tecnologia.id:
                    produto_service.excluir_produto(produto.id)
            print("   🗑️ Produtos da demonstração removidos")
            
            # Excluir categoria
            categoria_service.excluir_categoria(categoria_tecnologia.id)
            print("   🗑️ Categoria removida")


def demonstrar_seguranca():
    """Demonstra as funcionalidades de segurança implementadas"""
    print("\n=== DEMONSTRAÇÃO: Segurança e Robustez ===\n")
    
    print("🔒 Segurança Implementada:")
    print("   ✅ Prepared Statements (previne SQL Injection)")
    print("   ✅ Validação de tipos de dados")
    print("   ✅ Validação de regras de negócio")
    print("   ✅ Tratamento de exceções com logging")
    print("   ✅ Transações com rollback automático")
    print("   ✅ Conexões thread-safe (Singleton)")
    
    # Demonstrar prepared statements
    print("\n🛡️ Prepared Statements em Ação:")
    categoria_service = CategoriaService()
    
    # Tentar inserir dados que poderiam ser maliciosos em SQL injection
    descricao_maliciosa = "'; DROP TABLE Categoria; --"
    
    try:
        categoria_service.criar_categoria(descricao_maliciosa)
        print("   ✅ Dados 'maliciosos' inseridos com segurança")
        
        # Verificar se os dados foram inseridos corretamente
        categorias = categoria_service.listar_todas()
        categoria_encontrada = None
        for cat in categorias:
            if cat.descricao == descricao_maliciosa:
                categoria_encontrada = cat
                break
        
        if categoria_encontrada:
            print(f"   ✅ Dados preservados integralmente: '{categoria_encontrada.descricao}'")
            categoria_service.excluir_categoria(categoria_encontrada.id)
            print("   🗑️ Dados de teste removidos")
        
    except Exception as e:
        print(f"   ❌ Erro inesperado: {e}")


def main():
    """Executa todas as demonstrações"""
    print("🎯 DEMONSTRAÇÃO COMPLETA DO PADRÃO DAO")
    print("=" * 60)
    
    # Executar demonstrações
    demonstrar_uso_dao()
    demonstrar_uso_services()
    demonstrar_seguranca()
    
    print("\n" + "=" * 60)
    print("🎉 DEMONSTRAÇÃO CONCLUÍDA!")
    print("\n📚 Resumo do que foi implementado:")
    print("• Padrão DAO com interface abstrata e implementações concretas")
    print("• Factory para criação de objetos DAO")
    print("• Singleton para gerenciamento de conexões")
    print("• Service Layer com lógica de negócio e validações")
    print("• Prepared Statements para segurança contra SQL Injection")
    print("• Tratamento robusto de exceções")
    print("• Validações de dados e regras de negócio")
    print("• Funcionalidades avançadas de consulta e relatórios")
    
    print("\n✨ O projeto agora segue as melhores práticas de desenvolvimento!")


if __name__ == "__main__":
    main()
