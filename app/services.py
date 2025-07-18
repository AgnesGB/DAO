"""
Camada de Serviços - Contém a lógica de negócio da aplicação
Esta camada fica entre as Views e os DAOs, implementando as regras de negócio
"""

from typing import Optional, List
from .dominio import Categoria, Produto
from .dao import DAOFactory
import logging


class CategoriaService:
    """Serviço para gerenciar a lógica de negócio relacionada a categorias"""
    
    def __init__(self):
        self.dao = DAOFactory.get_categoria_dao()
    
    def listar_todas(self) -> List[Categoria]:
        """Lista todas as categorias ordenadas por descrição"""
        return self.dao.selecionar_todos()
    
    def obter_por_id(self, id: int) -> Optional[Categoria]:
        """Obtém uma categoria pelo ID"""
        return self.dao.selecionar_um(id)
    
    def criar_categoria(self, descricao: str) -> bool:
        """
        Cria uma nova categoria, validando regras de negócio
        
        Regras:
        - Descrição não pode estar vazia
        - Descrição deve ser única
        """
        try:
            # Validação: descrição não pode estar vazia
            if not descricao or not descricao.strip():
                raise ValueError("A descrição da categoria não pode estar vazia")
            
            descricao = descricao.strip()
            
            # Validação: descrição deve ser única
            if self.dao.existe_categoria(descricao):
                raise ValueError("Já existe uma categoria com esta descrição")
            
            # Criar categoria
            categoria = Categoria(id=None, descricao=descricao)
            self.dao.incluir(categoria)
            return True
            
        except Exception as e:
            logging.error(f"Erro ao criar categoria: {e}")
            raise
    
    def atualizar_categoria(self, id: int, descricao: str) -> bool:
        """
        Atualiza uma categoria existente, validando regras de negócio
        """
        try:
            # Validação: categoria deve existir
            categoria_existente = self.dao.selecionar_um(id)
            if not categoria_existente:
                raise ValueError("Categoria não encontrada")
            
            # Validação: descrição não pode estar vazia
            if not descricao or not descricao.strip():
                raise ValueError("A descrição da categoria não pode estar vazia")
            
            descricao = descricao.strip()
            
            # Validação: descrição deve ser única (exceto para o próprio registro)
            if self.dao.existe_categoria(descricao, id):
                raise ValueError("Já existe uma categoria com esta descrição")
            
            # Atualizar categoria
            categoria = Categoria(id=id, descricao=descricao)
            self.dao.alterar(categoria)
            return True
            
        except Exception as e:
            logging.error(f"Erro ao atualizar categoria: {e}")
            raise
    
    def excluir_categoria(self, id: int) -> bool:
        """
        Exclui uma categoria, validando regras de negócio
        
        Regras:
        - Categoria deve existir
        - Não pode ter produtos vinculados
        """
        try:
            # Validação: categoria deve existir
            categoria = self.dao.selecionar_um(id)
            if not categoria:
                raise ValueError("Categoria não encontrada")
            
            # Validação: não pode ter produtos vinculados
            produto_service = ProdutoService()
            produtos = produto_service.listar_por_categoria(id)
            if produtos:
                raise ValueError(f"Não é possível excluir a categoria. Existe(m) {len(produtos)} produto(s) vinculado(s)")
            
            # Excluir categoria
            self.dao.excluir(categoria)
            return True
            
        except Exception as e:
            logging.error(f"Erro ao excluir categoria: {e}")
            raise


class ProdutoService:
    """Serviço para gerenciar a lógica de negócio relacionada a produtos"""
    
    def __init__(self):
        self.dao = DAOFactory.get_produto_dao()
        self.categoria_service = CategoriaService()
    
    def listar_todos(self) -> List[Produto]:
        """Lista todos os produtos ordenados por descrição"""
        return self.dao.selecionar_todos()
    
    def obter_por_id(self, id: int) -> Optional[Produto]:
        """Obtém um produto pelo ID"""
        return self.dao.selecionar_um(id)
    
    def listar_por_categoria(self, categoria_id: int) -> List[Produto]:
        """Lista produtos de uma categoria específica"""
        return self.dao.selecionar_por_categoria(categoria_id)
    
    def buscar_por_descricao(self, termo: str) -> List[Produto]:
        """Busca produtos pela descrição"""
        if not termo or not termo.strip():
            return []
        return self.dao.buscar_por_descricao(termo.strip())
    
    def criar_produto(self, descricao: str, preco_unitario: float, 
                     quantidade_estoque: int, categoria_id: int) -> bool:
        """
        Cria um novo produto, validando regras de negócio
        
        Regras:
        - Descrição não pode estar vazia
        - Preço deve ser positivo
        - Quantidade de estoque não pode ser negativa
        - Categoria deve existir
        """
        try:
            # Validação: descrição não pode estar vazia
            if not descricao or not descricao.strip():
                raise ValueError("A descrição do produto não pode estar vazia")
            
            # Validação: preço deve ser positivo
            if preco_unitario <= 0:
                raise ValueError("O preço unitário deve ser maior que zero")
            
            # Validação: quantidade de estoque não pode ser negativa
            if quantidade_estoque < 0:
                raise ValueError("A quantidade em estoque não pode ser negativa")
            
            # Validação: categoria deve existir
            categoria = self.categoria_service.obter_por_id(categoria_id)
            if not categoria:
                raise ValueError("Categoria não encontrada")
            
            # Criar produto
            produto = Produto(
                id=None,
                descricao=descricao.strip(),
                preco_unitario=preco_unitario,
                quantidade_estoque=quantidade_estoque,
                categoria=categoria
            )
            self.dao.incluir(produto)
            return True
            
        except Exception as e:
            logging.error(f"Erro ao criar produto: {e}")
            raise
    
    def atualizar_produto(self, id: int, descricao: str, preco_unitario: float,
                         quantidade_estoque: int, categoria_id: int) -> bool:
        """
        Atualiza um produto existente, validando regras de negócio
        """
        try:
            # Validação: produto deve existir
            produto_existente = self.dao.selecionar_um(id)
            if not produto_existente:
                raise ValueError("Produto não encontrado")
            
            # Validação: descrição não pode estar vazia
            if not descricao or not descricao.strip():
                raise ValueError("A descrição do produto não pode estar vazia")
            
            # Validação: preço deve ser positivo
            if preco_unitario <= 0:
                raise ValueError("O preço unitário deve ser maior que zero")
            
            # Validação: quantidade de estoque não pode ser negativa
            if quantidade_estoque < 0:
                raise ValueError("A quantidade em estoque não pode ser negativa")
            
            # Validação: categoria deve existir
            categoria = self.categoria_service.obter_por_id(categoria_id)
            if not categoria:
                raise ValueError("Categoria não encontrada")
            
            # Atualizar produto
            produto = Produto(
                id=id,
                descricao=descricao.strip(),
                preco_unitario=preco_unitario,
                quantidade_estoque=quantidade_estoque,
                categoria=categoria
            )
            self.dao.alterar(produto)
            return True
            
        except Exception as e:
            logging.error(f"Erro ao atualizar produto: {e}")
            raise
    
    def excluir_produto(self, id: int) -> bool:
        """
        Exclui um produto, validando regras de negócio
        
        Regras:
        - Produto deve existir
        """
        try:
            # Validação: produto deve existir
            produto = self.dao.selecionar_um(id)
            if not produto:
                raise ValueError("Produto não encontrado")
            
            # Excluir produto
            self.dao.excluir(produto)
            return True
            
        except Exception as e:
            logging.error(f"Erro ao excluir produto: {e}")
            raise
    
    def verificar_estoque_baixo(self, limite: int = 10) -> List[Produto]:
        """
        Retorna produtos com estoque baixo (abaixo do limite especificado)
        """
        todos_produtos = self.dao.selecionar_todos()
        return [p for p in todos_produtos if p.quantidade_estoque is not None and p.quantidade_estoque < limite]
    
    def calcular_valor_total_estoque(self) -> float:
        """
        Calcula o valor total do estoque (soma de preço * quantidade de todos os produtos)
        """
        produtos = self.dao.selecionar_todos()
        return sum(p.preco_unitario * (p.quantidade_estoque or 0) for p in produtos)
