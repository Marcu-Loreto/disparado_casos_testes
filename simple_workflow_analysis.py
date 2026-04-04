#!/usr/bin/env python3
"""
Análise simples do workflow para identificar o problema.
"""

from app.workflow import WorkflowExecutor
from config.settings import Settings

def analyze_http_request_path():
    """Analisa por que HTTP Request1 não está sendo executado."""
    
    settings = Settings()
    executor = WorkflowExecutor(settings)
    
    print("=== ANÁLISE SIMPLES DO WORKFLOW ===\n")
    
    # Verifica a cadeia de dependências para HTTP Request1
    print("1. CADEIA DE DEPENDÊNCIAS PARA HTTP REQUEST1:")
    
    # HTTP Request1 depende de Edit Fields1
    print("   HTTP Request1 <- Edit Fields1")
    
    # Edit Fields1 depende de Edit Fields
    print("   Edit Fields1 <- Edit Fields")
    
    # Edit Fields depende de Loop Over Items
    print("   Edit Fields <- Loop Over Items")
    
    # Loop Over Items depende de Get row(s) ou Wait
    print("   Loop Over Items <- Get row(s) OU Wait")
    
    # Verifica se esses nós estão definidos
    required_nodes = ["HTTP Request1", "Edit Fields1", "Edit Fields", "Loop Over Items", "Get row(s)", "Wait"]
    
    print(f"\n2. VERIFICAÇÃO DE NÓDULOS NECESSÁRIOS:")
    for node in required_nodes:
        if node in executor.nodes:
            print(f"   ✅ {node} - Definido")
        else:
            print(f"   ❌ {node} - NÃO definido")
    
    # Verifica as conexões específicas
    print(f"\n3. VERIFICAÇÃO DE CONEXÕES:")
    
    connections_to_check = [
        ("Edit Fields1", "HTTP Request1"),
        ("Edit Fields", "Edit Fields1"), 
        ("Loop Over Items", "Edit Fields"),
        ("Get row(s)", "Loop Over Items"),
        ("Wait", "Loop Over Items")
    ]
    
    for source, target in connections_to_check:
        found = False
        if source in executor.connections:
            connections = executor.connections[source]
            if "main" in connections:
                for connection_group in connections["main"]:
                    for connection in connection_group:
                        if connection["node"] == target:
                            found = True
                            break
        
        if found:
            print(f"   ✅ {source} -> {target}")
        else:
            print(f"   ❌ {source} -> {target} - CONEXÃO FALTANDO")

if __name__ == "__main__":
    analyze_http_request_path()