"""HoloOS Database Manager - SQL, NoSQL, KV"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import time
import json

@dataclass
class Record:
    id: str
    data: Dict
    table: str
    timestamp: float

class SQLStore:
    """Armazenamento SQL-like"""
    def __init__(self):
        self.tables: Dict[str, List[Record]] = {}
    
    def create_table(self, name: str) -> None:
        if name not in self.tables:
            self.tables[name] = []
    
    def insert(self, table: str, data: Dict) -> str:
        if table not in self.tables:
            self.create_table(table)
        record_id = f"rec_{len(self.tables[table])}"
        record = Record(id=record_id, data=data, table=table, timestamp=time.time())
        self.tables[table].append(record)
        return record_id
    
    def query(self, table: str, filter_fn=None) -> List[Dict]:
        if table not in self.tables:
            return []
        if filter_fn:
            return [r.data for r in self.tables[table] if filter_fn(r.data)]
        return [r.data for r in self.tables[table]]

class NoSQLStore:
    """Armazenamento NoSQL-like"""
    def __init__(self):
        self.collections: Dict[str, Dict] = {}
    
    def set(self, collection: str, key: str, value: Any) -> None:
        if collection not in self.collections:
            self.collections[collection] = {}
        self.collections[collection][key] = value
    
    def get(self, collection: str, key: str) -> Optional[Any]:
        return self.collections.get(collection, {}).get(key)
    
    def delete(self, collection: str, key: str) -> bool:
        if collection in self.collections and key in self.collections[collection]:
            del self.collections[collection][key]
            return True
        return False

class KVStore:
    """Key-Value store"""
    def __init__(self):
        self.store: Dict[str, str] = {}
    
    def set(self, key: str, value: str) -> None:
        self.store[key] = value
    
    def get(self, key: str) -> Optional[str]:
        return self.store.get(key)
    
    def delete(self, key: str) -> bool:
        if key in self.store:
            del self.store[key]
            return True
        return False
    
    def keys(self) -> List[str]:
        return list(self.store.keys())

class DatabaseManager:
    """Gerenciador de banco de dados unificado"""
    
    def __init__(self):
        self.sql = SQLStore()
        self.nosql = NoSQLStore()
        self.kv = KVStore()
    
    def query_sql(self, table: str, filter_fn=None) -> List[Dict]:
        return self.sql.query(table, filter_fn)
    
    def insert_sql(self, table: str, data: Dict) -> str:
        return self.sql.insert(table, data)
    
    def set_nosql(self, collection: str, key: str, value: Any) -> None:
        self.nosql.set(collection, key, value)
    
    def get_nosql(self, collection: str, key: str) -> Optional[Any]:
        return self.nosql.get(collection, key)
    
    def set_kv(self, key: str, value: str) -> None:
        self.kv.set(key, value)
    
    def get_kv(self, key: str) -> Optional[str]:
        return self.kv.get(key)
    
    def get_status(self) -> Dict:
        return {
            "sql_tables": len(self.sql.tables),
            "nosql_collections": len(self.nosql.collections),
            "kv_keys": len(self.kv.store),
        }

__all__ = ["DatabaseManager", "SQLStore", "NoSQLStore", "KVStore"]
