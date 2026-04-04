#!/usr/bin/env python3
"""
Identifica e corrige os ciclos no workflow.
"""

from app.workflow import WorkflowExecutor
from config.settings import Settings
from collections import defaultdict, deque
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def find_cycles():
    """Encontra ciclos no workflow."""
    
    settings = Settings()
    executor = WorkflowExecutor(settings)
    
    # Constrói o grafo
    graph = defaultdict(list)
    for source, connections in executor.connections.items():
        if connections.get("main"):
            for connection_group in connections["main"]:
                for connection in connection_group:
                    target = connection["node"]
                    graph[source].append(target)
    
    print("=== ANÁLISE DE CICLOS NO WORKFLOW ===\n")
    
    # Detecta ciclos usando DFS
    visited = set()
    rec_stack = set()
    cycles_found = []
    
    def dfs(node, path):
        if node in rec_stack:
            # Encontrou um ciclo
            cycle_start = path.index(node)
            cycle = path[cycle_start:] + [node]
            cycles_found.append(cycle)
            return True
        
        if node in visited:
            return False
        
        visited.add(node)
        rec_stack.add(node)
        path.append(node)
        
        for neighbor in graph[node]:
            if dfs(neighbor, path):
                return True
        
        rec_stack.remove(node)
        path.pop()
        return False
    
    # Verifica todos os nós
    for node in executor.nodes:
        if node not in visited:
            dfs(node, [])
    
    if cycles_found:
        print("🔄 CICLOS ENCONTRADOS:")
        for i, cycle in enumerate(cycles_found):
            print(f"   Ciclo {i+1}: {' -> '.join(cycle)}")
    else:
        print("✅ Nenhum ciclo encontrado")
    
    # Analisa o caminho específico para HTTP Request1
    print(f"\n📍 ANÁLISE DO CAMINHO PARA HTTP REQUEST1:")
    
    def find_path_to_node(target_node):
        """Encontra todos os caminhos que levam a um nó específico."""
        paths = []
        
        def dfs_path(current, path, visited_in_path):
            if current == target_node and len(path) > 1:
                paths.append(path.copy())
                return
            
            if current in visited_in_path:
                return  # Evita ciclos infinitos
            
            visited_in_path.add(current)
            
            for neighbor in graph[current]:
                path.append(neighbor)
                dfs_path(neighbor, path, visited_in_path.copy())
                path.pop()
        
        # Inicia a busca de todos os nós
        for start_node in executor.nodes:
            if start_node != target_node:
                dfs_path(start_node, [start_node], set())
        
        return paths
    
    paths_to_http = find_path_to_node("HTTP Request1")
    
    if paths_to_http:
        print("   Caminhos encontrados para HTTP Request1:")
        for i, path in enumerate(paths_to_http):
            print(f"     {i+1}. {' -> '.join(path)}")
    else:
        print("   ❌ Nenhum caminho encontrado para HTTP Request1")
    
    # Verifica se há nós órfãos
    print(f"\n🔍 ANÁLISE DE NÓS ÓRFÃOS:")
    
    all_targets = set()
    for source, connections in executor.connections.items():
        if connections.get("main"):
            for connection_group in connections["main"]:
                for connection in connection_group:
                    all_targets.add(connection["node"])
    
    orphan_nodes = []
    for node in executor.nodes:
        if node not in all_targets and node != "Webhook":  # Webhook é o ponto de entrada
            orphan_nodes.append(node)
    
    if orphan_nodes:
        print("   Nós órfãos (sem conexões de entrada):")
        for node in orphan_nodes:
            print(f"     - {node}")
    else:
        print("   ✅ Todos os nós têm conexões de entrada")

if __name__ == "__main__":
    find_cycles()