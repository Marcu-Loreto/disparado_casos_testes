#!/usr/bin/env python3
"""
Análise do workflow para identificar problemas na execução.
"""

from app.workflow import WorkflowExecutor
from config.settings import Settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_workflow():
    """Analisa o workflow para identificar problemas."""
    
    settings = Settings()
    executor = WorkflowExecutor(settings)
    
    print("=== ANÁLISE DO WORKFLOW ===\n")
    
    # 1. Lista todos os nós
    print("1. NÓDULOS DEFINIDOS:")
    for node_name in executor.nodes.keys():
        print(f"   - {node_name}")
    
    print(f"\nTotal de nós: {len(executor.nodes)}")
    
    # 2. Verifica conexões
    print("\n2. CONEXÕES DEFINIDAS:")
    for source, connections in executor.connections.items():
        if connections.get("main"):
            for connection_group in connections["main"]:
                for connection in connection_group:
                    target = connection["node"]
                    print(f"   {source} -> {target}")
    
    # 3. Verifica ordem topológica
    print("\n3. ORDEM DE EXECUÇÃO:")
    execution_order = executor._topological_sort()
    for i, node in enumerate(execution_order):
        print(f"   {i+1}. {node}")
    
    # 4. Verifica se HTTP Request1 está na ordem
    print(f"\n4. HTTP REQUEST1 NA EXECUÇÃO:")
    if "HTTP Request1" in execution_order:
        position = execution_order.index("HTTP Request1") + 1
        print(f"   ✅ SIM - Posição {position}")
    else:
        print("   ❌ NÃO - Não está na ordem de execução")
    
    # 5. Verifica dependências do HTTP Request1
    print(f"\n5. DEPENDÊNCIAS DO HTTP REQUEST1:")
    inputs = executor._gather_inputs("HTTP Request1")
    print(f"   Inputs esperados: {list(inputs.keys()) if inputs else 'Nenhum'}")
    
    # 6. Verifica o caminho até HTTP Request1
    print(f"\n6. CAMINHO PARA HTTP REQUEST1:")
    
    # Encontra nós que conectam ao HTTP Request1
    sources_to_http = []
    for source, connections in executor.connections.items():
        if connections.get("main"):
            for connection_group in connections["main"]:
                for connection in connection_group:
                    if connection["node"] == "HTTP Request1":
                        sources_to_http.append(source)
    
    print(f"   Nós que conectam ao HTTP Request1: {sources_to_http}")
    
    # 7. Verifica se esses nós estão sendo executados
    print(f"\n7. STATUS DOS NÓS PREDECESSORES:")
    for source in sources_to_http:
        if source in execution_order:
            pos = execution_order.index(source) + 1
            print(f"   ✅ {source} - Posição {pos}")
        else:
            print(f"   ❌ {source} - NÃO está na execução")

if __name__ == "__main__":
    analyze_workflow()