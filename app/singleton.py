"""
Implementação do padrão Singleton para gerenciar conexão com banco de dados
"""
import sqlite3
import threading
from typing import Optional, Dict


class DatabaseConnection:
    """
    Implementação do padrão Singleton para gerenciar a conexão com o banco de dados.
    Garante que apenas uma instância da classe exista e gerencia conexões por thread.
    """
    
    _instance: Optional['DatabaseConnection'] = None
    _lock: threading.Lock = threading.Lock()
    _connections: Dict[int, sqlite3.Connection] = {}
    
    def __new__(cls) -> 'DatabaseConnection':
        """
        Controla a criação de instâncias garantindo que apenas uma exista.
        Thread-safe implementation.
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def get_connection(self) -> sqlite3.Connection:
        """
        Retorna a conexão com o banco de dados para a thread atual.
        Cada thread terá sua própria conexão para evitar problemas de concorrência.
        """
        thread_id = threading.current_thread().ident
        
        if thread_id not in self._connections or self._connections[thread_id] is None:
            # Criar nova conexão para esta thread
            connection = sqlite3.connect(
                'arq_soft.sqlite3',
                check_same_thread=False,  # Permite uso em threads diferentes
                timeout=30.0  # Timeout para evitar locks indefinidos
            )
            # Habilita checagem de foreign keys
            connection.execute("PRAGMA foreign_keys = ON")
            # Configura para WAL mode (melhor para concorrência)
            connection.execute("PRAGMA journal_mode = WAL")
            
            self._connections[thread_id] = connection
        
        return self._connections[thread_id]
    
    def close_connection(self, thread_id: Optional[int] = None) -> None:
        """
        Fecha a conexão com o banco de dados para uma thread específica ou atual.
        """
        if thread_id is None:
            thread_id = threading.current_thread().ident
            
        if thread_id in self._connections and self._connections[thread_id] is not None:
            self._connections[thread_id].close()
            del self._connections[thread_id]
    
    def close_all_connections(self) -> None:
        """
        Fecha todas as conexões ativas.
        """
        for thread_id in list(self._connections.keys()):
            if self._connections[thread_id] is not None:
                self._connections[thread_id].close()
        self._connections.clear()
    
    def execute_sql(self, sql: str, parametros: tuple = (), commit: bool = True) -> sqlite3.Cursor:
        """
        Executa um comando SQL no banco de dados usando prepared statements.
        
        Args:
            sql: Comando SQL a ser executado
            parametros: Parâmetros para o prepared statement
            commit: Se deve confirmar a transação (padrão: True)
            
        Returns:
            Cursor com o resultado da execução
        """
        connection = self.get_connection()
        cursor = connection.cursor()
        
        try:
            result = cursor.execute(sql, parametros)
            
            if commit:
                connection.commit()
                
            return result
        except Exception as e:
            # Em caso de erro, fazer rollback
            if commit:
                connection.rollback()
            raise e
    
    def execute_select(self, sql: str, parametros: tuple = ()) -> list:
        """
        Executa um comando SELECT usando prepared statements e retorna todos os resultados.
        
        Args:
            sql: Comando SELECT a ser executado
            parametros: Parâmetros para o prepared statement
            
        Returns:
            Lista com todos os registros encontrados
        """
        connection = self.get_connection()
        cursor = connection.cursor()
        result = cursor.execute(sql, parametros).fetchall()
        return result


# Função de conveniência para obter a instância singleton
def get_database_connection() -> DatabaseConnection:
    """
    Função de conveniência para obter a instância singleton do DatabaseConnection.
    """
    return DatabaseConnection()
