#!/usr/bin/env python3
"""
Git Automator - Commit, Push e Criação de Repo automático
Garante que TODAS as alterações sejam commitadas
Suporta criação automática de repositório no GitHub
"""

import subprocess
import sys
import os
import urllib.request
import urllib.error
import json
from pathlib import Path

# Carregar variáveis do .env
from dotenv import load_dotenv

load_dotenv()


def run(cmd, capture=True):
    """Executa comando shell"""
    result = subprocess.run(cmd, shell=True, capture_output=capture, text=True)
    return result.returncode, result.stdout, result.stderr


def get_github_token():
    """Busca token do GitHub nas variáveis de ambiente"""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("   ⚠️ GITHUB_TOKEN não configurado!")
        print("   Configure com: export GITHUB_TOKEN=seu_token_aqui")
        print("   或 use .env file")
    return token


def get_current_repo_name():
    """Obtém nome do repositório based no diretório atual"""
    cwd = os.getcwd()
    return Path(cwd).name


def check_github_repo_exists(token, repo_name, username="Marcu-Loreto"):
    """Verifica se repo já existe no GitHub"""
    if not token:
        return None  # Não consegue verificar

    url = f"https://api.github.com/repos/{username}/{repo_name}"

    req = urllib.request.Request(url)
    req.add_header("Authorization", f"token {token}")
    req.add_header("Accept", "application/vnd.github.v3+json")

    try:
        with urllib.request.urlopen(req) as response:
            return response.status == 200
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False
        print(f"   ⚠️ Erro ao verificar repo: {e.code}")
        return None


def create_github_repo(token, repo_name, username="Marcu-Loreto"):
    """Cria novo repositório no GitHub"""
    if not token:
        print("   ❌ Token não disponível para criar repositório")
        return False

    url = f"https://api.github.com/user/repos"

    data = json.dumps(
        {
            "name": repo_name,
            "description": f"Repositório {repo_name} criado automaticamente",
            "private": False,
            "auto_init": True,
        }
    ).encode("utf-8")

    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", f"token {token}")
    req.add_header("Accept", "application/vnd.github.v3+json")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            print(f"   ✅ Repositório criado: {result.get('html_url')}")
            return True
    except urllib.error.HTTPError as e:
        error_body = json.loads(e.read().decode())
        print(f"   ❌ Erro ao criar repo: {error_body.get('message', e.code)}")
        return False


def setup_git_remote(token, repo_name, username="Marcu-Loreto"):
    """Configura remote se necessário"""
    # Verificar se remote existe
    code, out, err = run("git remote geturl origin")

    if code == 0 and out.strip():
        print(f"   📌 Remote já existe: {out.strip()}")
        return True

    # Criar remote
    remote_url = f"https://github.com/{username}/{repo_name}.git"
    code, out, err = run(f"git remote add origin {remote_url}")

    if code == 0:
        print(f"   ✅ Remote configurado: {remote_url}")
        return True
    else:
        # Tentar setar URL se remote já existe
        code2, out2, err2 = run(f"git remote set-url origin {remote_url}")
        if code2 == 0:
            print(f"   ✅ Remote atualizado: {remote_url}")
            return True
        print(f"   ❌ Erro ao configurar remote: {err}")
        return False


def main():
    print("=" * 60)
    print("GIT AUTOMATOR - Commit, Push & Create Repo")
    print("=" * 60)
    print()

    # Obter configurações
    repo_name = get_current_repo_name()
    username = os.getenv("GITHUB_USER", "Marcu-Loreto")
    token = get_github_token()

    print(f"📁 Projeto: {repo_name}")
    print(f"👤 Usuário GitHub: {username}")
    print()

    # 1. Verificar status atual
    print("1️⃣ Verificando status...")
    code, out, err = run("git status --porcelain")
    if out.strip():
        print("   Alterações encontradas:")
        for line in out.strip().split("\n")[:10]:  # Limitar a 10 linhas
            print(f"   {line}")
    else:
        print("   Nenhuma alteração encontrada")
        print("\n✅ Tudo já está commitado!")
        return

    print()

    # 2. Verificar/criar repositório no GitHub
    print("2️⃣ Verificando repositório no GitHub...")

    if token:
        exists = check_github_repo_exists(token, repo_name, username)

        if exists is True:
            print("   ✅ Repositório já existe")
            setup_git_remote(token, repo_name, username)
        elif exists is False:
            print("   📦 Repositório não existe, criando...")
            if create_github_repo(token, repo_name, username):
                setup_git_remote(token, repo_name, username)
                # Primeiro push precisa configurar upstream
                run("git push -u origin master")
        else:
            print("   ⚠️ Pulando criação de repo (token não disponível)")
    else:
        print("   ⚠️ Pulando criação de repo (GITHUB_TOKEN não configurado)")
        print("   Para criar repos automaticamente, configure GITHUB_TOKEN")

    print()

    # 3. Stage TODOS os arquivos
    print("3️⃣ Fazendo git add -A (TODOS os arquivos)...")
    code, out, err = run("git add -A")
    if code != 0:
        print(f"   ❌ Erro: {err}")
        return
    print("   ✅ Arquivos adicionados")

    print()

    # 4. Mostrar o que será commitado
    print("4️⃣ Alterações a serem commitadas:")
    code, out, err = run("git diff --staged --stat")
    print(out if out else "   Nenhuma")

    print()

    # 5. Criar commit
    msg = (
        " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "chore: atualizações diversas"
    )
    print(f"📝 Criando commit: {msg}")
    code, out, err = run(f'git commit -m "{msg}"')
    if code != 0:
        print(f"   ❌ Erro: {err}")
        return
    print("   ✅ Commit criado")

    print()

    # 6. Push
    print("5️⃣ Fazendo push...")
    code, out, err = run("git push origin master")
    if code != 0:
        print(f"   ⚠️ Tentando com -u (primeiro push)...")
        code, out, err = run("git push -u origin master")

    if code == 0:
        print("   ✅ Push realizado!")
    else:
        print(f"   ❌ Erro no push: {err}")

    print()

    # 7. Status final
    print("6️⃣ Status final:")
    run("git status")

    print()
    print("=" * 60)
    print("✅ OPERAÇÃO CONCLUÍDA!")
    print("=" * 60)


if __name__ == "__main__":
    main()
