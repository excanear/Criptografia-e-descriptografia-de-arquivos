# 🚀 GUIA RÁPIDO DE USO

## Como usar o sistema de criptografia:

### 1. CRIPTOGRAFAR UM ARQUIVO
```bash
python main.py encrypt arquivo_teste.txt
```
- O sistema pedirá uma senha
- Criará um arquivo `arquivo_teste.txt.encrypted`

### 2. DESCRIPTOGRAFAR UM ARQUIVO
```bash
python main.py decrypt arquivo_teste.txt.encrypted
```
- Digite a mesma senha usada na criptografia
- Recuperará o arquivo original

### 3. CRIPTOGRAFAR TEXTO
```bash
python main.py encrypt-text "Minha mensagem secreta"
```
- Retornará o texto criptografado em base64

### 4. GERAR SENHA SEGURA
```bash
python main.py generate-password
```
- Gerará uma senha aleatória de 32 bytes

### 5. VER TODAS AS OPÇÕES
```bash
python main.py --help
```

## Exemplos prontos:
- Execute `python example.py` para ver demonstrações
- Use `arquivo_teste.txt` para testar

## Dicas importantes:
- ✅ Use senhas fortes (mínimo 12 caracteres)
- ✅ Guarde suas senhas em local seguro
- ✅ Teste a descriptografia antes de remover originais
- ⚠️ Sem a senha, NÃO é possível recuperar os dados!

## Tecnologia:
- AES-256-GCM (criptografia militar)
- PBKDF2 com 100.000 iterações
- Verificação de integridade automática