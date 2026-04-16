# 🐍 COMO ATIVAR O AMBIENTE VIRTUAL

## ✅ Forma MAIS CURTA (Recomendada)

```bash
source activate
```

Ou ainda mais curto:

```bash
. activate
```

## ❌ NÃO funciona:

```bash
./activate          # ❌ Não funciona (roda em subshell)
chmod +x activate   # ❌ Não resolve o problema
```

## 💡 Por quê?

O `source` executa o script no shell ATUAL, mantendo as variáveis de ambiente.
O `./` executa em um subshell separado que fecha depois.

## 🚀 Criar Alias Permanente (Opcional)

Adicione ao seu `~/.bashrc`:

```bash
echo "alias venv='source venv/bin/activate'" >> ~/.bashrc
source ~/.bashrc
```

Depois use apenas:

```bash
venv
```

## 📋 Resumo dos Comandos

| Comando                    | Descrição                         |
| -------------------------- | --------------------------------- |
| `source activate`          | Ativa venv (8 caracteres)         |
| `. activate`               | Ativa venv (9 caracteres)         |
| `source venv/bin/activate` | Forma tradicional (25 caracteres) |
| `deactivate`               | Desativa venv                     |

## ✅ Verificar se Ativou

Após ativar, você verá `(venv)` no início do prompt:

```bash
(venv) user@host:~/projeto$
```

Ou verifique:

```bash
which python3
# Deve mostrar: /caminho/do/projeto/venv/bin/python3
```
