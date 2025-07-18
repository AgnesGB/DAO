

from typing import Any, Optional
from .dominio import *
from abc import ABC, abstractmethod
import sqlite3
import logging


class DAO(ABC):

    _conexao: sqlite3.Connection

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

    def obter_conexao(self) -> sqlite3.Connection:
        """Obtém uma conexão com o banco de dados SQLite"""
        try:
            self._conexao = sqlite3.connect('arq_soft.sqlite3')
            # Habilita verificação de chaves estrangeiras
            self._conexao.execute("PRAGMA foreign_keys = ON")
            return self._conexao
        except sqlite3.Error as e:
            logging.error(f"Erro ao conectar com o banco de dados: {e}")
            raise

    def fechar_conexao(self):
        """Fecha a conexão com o banco de dados"""
        try:
            if hasattr(self, '_conexao') and self._conexao is not None:
                self._conexao.close()
        except sqlite3.Error as e:
            logging.error(f"Erro ao fechar conexão: {e}")

    def executar_sql(self, sql: str, parametros: tuple = (), commit: bool = True) -> Any:
        """Executa um comando SQL no BD (geralmente um INSERT, UPDATE ou DELETE)"""
        conexao = None
        try:
            # obtém conexão
            conexao = self.obter_conexao()
            # cria um cursor() e executa o SQL informado
            cursor = conexao.cursor()
            ret = cursor.execute(sql, parametros)
            # verifica se é para efetivar as modificações no BD
            if commit:
                conexao.commit()
            # retorna o resultado do método execute()
            return ret 
        except sqlite3.Error as e:
            if conexao and commit:
                conexao.rollback()
            logging.error(f"Erro ao executar SQL: {sql} - Erro: {e}")
            raise
        finally:
            if conexao:
                conexao.close()

    def executar_select(self, sql: str, parametros: tuple = ()) -> list[Any]:
        """Executa um comando SELECT no BD e retorna os registros"""
        conexao = None
        try:
            # obtém conexão
            conexao = self.obter_conexao()
            # cria um cursor(), executa o SELECT informado e traz todos os registros
            cursor = conexao.cursor()
            ret = cursor.execute(sql, parametros).fetchall()
            # retorna os registros do BD
            return ret 
        except sqlite3.Error as e:
            logging.error(f"Erro ao executar SELECT: {sql} - Erro: {e}")
            raise
        finally:
            if conexao:
                conexao.close()
    

class CategoriaDAO(DAO):
    """DAO para operações com a entidade Categoria"""
    
    def incluir(self, obj: Categoria) -> None:
        """Inclui uma nova categoria no banco de dados"""
        sql = "INSERT INTO Categoria(descricao) VALUES(?)"
        self.executar_sql(sql, (obj.descricao,))

    def alterar(self, obj: Categoria) -> None:
        """Altera uma categoria existente no banco de dados"""
        sql = "UPDATE Categoria SET descricao = ? WHERE id = ?"
        self.executar_sql(sql, (obj.descricao, obj.id))

    def excluir(self, obj: Categoria) -> None:
        """Exclui uma categoria do banco de dados"""
        sql = "DELETE FROM Categoria WHERE id = ?"
        self.executar_sql(sql, (obj.id,))

    def selecionar_todos(self) -> list[Categoria]: 
        """Seleciona todas as categorias do banco de dados"""
        sql = "SELECT id, descricao FROM Categoria ORDER BY descricao"
        registros = self.executar_select(sql)
        # converte os registros para objetos e adiciona na lista
        dados = []
        for reg in registros:
            dados.append(Categoria(id=reg[0], descricao=reg[1]))
        return dados

    def selecionar_um(self, id: int) -> Optional[Categoria]: 
        """Seleciona uma categoria específica pelo ID"""
        sql = "SELECT id, descricao FROM Categoria WHERE id = ?"
        registros = self.executar_select(sql, (id,))
        if registros:
            reg = registros[0]
            return Categoria(id=reg[0], descricao=reg[1])
        return None

    def existe_categoria(self, descricao: str, id_excluir: int = None) -> bool:
        """Verifica se já existe uma categoria com a mesma descrição"""
        if id_excluir:
            sql = "SELECT COUNT(*) FROM Categoria WHERE descricao = ? AND id != ?"
            registros = self.executar_select(sql, (descricao, id_excluir))
        else:
            sql = "SELECT COUNT(*) FROM Categoria WHERE descricao = ?"
            registros = self.executar_select(sql, (descricao,))
        return registros[0][0] > 0


class ProdutoDAO(DAO):
    """DAO para operações com a entidade Produto"""
    
    def incluir(self, obj: Produto) -> None:
        """Inclui um novo produto no banco de dados"""
        sql = """INSERT INTO Produto (descricao, preco_unitario, quantidade_estoque, categoria_id) 
                 VALUES (?, ?, ?, ?)"""
        self.executar_sql(sql, (obj.descricao, obj.preco_unitario, 
                               obj.quantidade_estoque, obj.categoria.id))

    def alterar(self, obj: Produto) -> None:
        """Altera um produto existente no banco de dados"""
        sql = """UPDATE Produto 
                 SET descricao = ?, preco_unitario = ?, quantidade_estoque = ?, categoria_id = ? 
                 WHERE id = ?"""
        self.executar_sql(sql, (obj.descricao, obj.preco_unitario, 
                               obj.quantidade_estoque, obj.categoria.id, obj.id))

    def excluir(self, obj: Produto) -> None:
        """Exclui um produto do banco de dados"""
        sql = "DELETE FROM Produto WHERE id = ?"
        self.executar_sql(sql, (obj.id,))

    def selecionar_todos(self) -> list[Produto]:
        """Seleciona todos os produtos do banco de dados com suas categorias"""
        sql = """SELECT p.id, p.descricao, p.preco_unitario, p.quantidade_estoque,
                        p.categoria_id, c.descricao as categoria_descricao
                 FROM Produto p
                 INNER JOIN Categoria c ON c.id = p.categoria_id
                 ORDER BY p.descricao"""
        registros = self.executar_select(sql)
        produtos = []
        for reg in registros:
            categoria = Categoria(id=reg[4], descricao=reg[5])
            produto = Produto(
                id=reg[0],
                descricao=reg[1], 
                preco_unitario=reg[2],
                quantidade_estoque=reg[3],
                categoria=categoria
            )
            produtos.append(produto)
        return produtos

    def selecionar_um(self, id: int) -> Optional[Produto]:
        """Seleciona um produto específico pelo ID"""
        sql = """SELECT p.id, p.descricao, p.preco_unitario, p.quantidade_estoque,
                        p.categoria_id, c.descricao as categoria_descricao
                 FROM Produto p
                 INNER JOIN Categoria c ON c.id = p.categoria_id
                 WHERE p.id = ?"""
        registros = self.executar_select(sql, (id,))
        if registros:
            reg = registros[0]
            categoria = Categoria(id=reg[4], descricao=reg[5])
            return Produto(
                id=reg[0],
                descricao=reg[1],
                preco_unitario=reg[2],
                quantidade_estoque=reg[3],
                categoria=categoria
            )
        return None

    def selecionar_por_categoria(self, categoria_id: int) -> list[Produto]:
        """Seleciona todos os produtos de uma categoria específica"""
        sql = """SELECT p.id, p.descricao, p.preco_unitario, p.quantidade_estoque,
                        p.categoria_id, c.descricao as categoria_descricao
                 FROM Produto p
                 INNER JOIN Categoria c ON c.id = p.categoria_id
                 WHERE p.categoria_id = ?
                 ORDER BY p.descricao"""
        registros = self.executar_select(sql, (categoria_id,))
        produtos = []
        for reg in registros:
            categoria = Categoria(id=reg[4], descricao=reg[5])
            produto = Produto(
                id=reg[0],
                descricao=reg[1],
                preco_unitario=reg[2],
                quantidade_estoque=reg[3],
                categoria=categoria
            )
            produtos.append(produto)
        return produtos

    def buscar_por_descricao(self, termo: str) -> list[Produto]:
        """Busca produtos pela descrição (busca parcial)"""
        sql = """SELECT p.id, p.descricao, p.preco_unitario, p.quantidade_estoque,
                        p.categoria_id, c.descricao as categoria_descricao
                 FROM Produto p
                 INNER JOIN Categoria c ON c.id = p.categoria_id
                 WHERE p.descricao LIKE ?
                 ORDER BY p.descricao"""
        registros = self.executar_select(sql, (f"%{termo}%",))
        produtos = []
        for reg in registros:
            categoria = Categoria(id=reg[4], descricao=reg[5])
            produto = Produto(
                id=reg[0],
                descricao=reg[1],
                preco_unitario=reg[2],
                quantidade_estoque=reg[3],
                categoria=categoria
            )
            produtos.append(produto)
        return produtos


class DAOFactory:
    """Factory para criar instâncias dos DAOs"""
    
    @staticmethod
    def get_categoria_dao() -> CategoriaDAO:
        """Retorna uma instância do CategoriaDAO"""
        return CategoriaDAO()
    
    @staticmethod
    def get_produto_dao() -> ProdutoDAO:
        """Retorna uma instância do ProdutoDAO"""
        return ProdutoDAO()
