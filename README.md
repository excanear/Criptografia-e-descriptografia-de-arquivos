# 🔐 Sistema de Criptografia e Descriptografia de Arquivos

Um sistema completo e seguro para criptografar e descriptografar arquivos e textos usando **AES-256-GCM** em Python.

## ✨ Características

- **Criptografia AES-256-GCM**: Algoritmo de criptografia militar com autenticação
- **Derivação de chave segura**: PBKDF2 com SHA-256 e 100.000 iterações
- **Interface de linha de comando**: Fácil de usar via terminal
- **Suporte a arquivos e texto**: Criptografe arquivos ou strings de texto
- **Geração de senhas**: Gera senhas aleatórias seguras
- **Verificação de integridade**: Detecta modificações nos dados criptografados
- **Cross-platform**: Funciona em Windows, Linux e macOS

## 🛠️ Instalação

### Pré-requisitos
- Python 3.7 ou superior
- pip (gerenciador de pacotes do Python)

### Passos de instalação

1. **Clone ou baixe o projeto**:
   ```bash
   git clone <url-do-repositorio>
   cd "Criptografia e descriptografia de arquivos"
   ```

2. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

   Ou manualmente:
   ```bash
   pip install cryptography==41.0.7
   ```

## 🚀 Uso Rápido

### Interface de Linha de Comando

O sistema inclui uma interface completa de linha de comando:

```bash
python main.py --help
```

### Exemplos Básicos

#### 1. Criptografar um arquivo
```bash
# Criptografia básica (pedirá senha)
python main.py encrypt documento.txt

# Especificar arquivo de saída
python main.py encrypt documento.txt -o documento_seguro.bin

# Gerar senha automaticamente
python main.py encrypt documento.txt --generate-password

# Remover arquivo original após criptografia
python main.py encrypt documento.txt --delete-original
```

#### 2. Descriptografar um arquivo
```bash
# Descriptografia básica (pedirá senha)
python main.py decrypt documento.txt.encrypted

# Especificar arquivo de saída
python main.py decrypt documento_seguro.bin -o documento_recuperado.txt

# Remover arquivo criptografado após descriptografia
python main.py decrypt documento.txt.encrypted --delete-encrypted
```

#### 3. Criptografar texto
```bash
# Criptografar texto diretamente
python main.py encrypt-text "Minha mensagem secreta"

# Salvar resultado em arquivo
python main.py encrypt-text "Mensagem" -o mensagem_criptografada.txt

# Gerar senha automaticamente
python main.py encrypt-text "Mensagem" --generate-password
```

#### 4. Descriptografar texto
```bash
# Descriptografar texto
python main.py decrypt-text "dGVzdGUgZGUgdGV4dG8gY3JpcHRvZ3JhZmFkbw=="

# Descriptografar de arquivo
python main.py decrypt-text -f mensagem_criptografada.txt

# Salvar resultado em arquivo
python main.py decrypt-text "texto_base64" -o mensagem_original.txt
```

#### 5. Gerar senha aleatória
```bash
# Senha padrão (32 bytes)
python main.py generate-password

# Senha com tamanho específico
python main.py generate-password --length 64

# Salvar senha em arquivo
python main.py generate-password -o minha_senha.txt
```

## 🔧 Uso Programático

### Exemplo básico

```python
from file_crypto import FileCrypto, generate_random_password

# Criar instância do criptografador
crypto = FileCrypto()

# Criptografar arquivo
senha = "MinhaS3nhaS3gura!"
arquivo_criptografado = crypto.encrypt_file("documento.txt", senha)
print(f"Arquivo criptografado: {arquivo_criptografado}")

# Descriptografar arquivo
arquivo_descriptografado = crypto.decrypt_file(arquivo_criptografado, senha)
print(f"Arquivo descriptografado: {arquivo_descriptografado}")
```

### Criptografia de texto

```python
from file_crypto import FileCrypto

crypto = FileCrypto()
senha = "MinhaS3nha123"

# Criptografar texto
texto_original = "Esta é uma mensagem secreta"
texto_criptografado = crypto.encrypt_text(texto_original, senha)
print(f"Texto criptografado: {texto_criptografado}")

# Descriptografar texto
texto_recuperado = crypto.decrypt_text(texto_criptografado, senha)
print(f"Texto recuperado: {texto_recuperado}")
```

### Geração de senhas

```python
from file_crypto import generate_random_password

# Gerar senha de 32 bytes (padrão)
senha1 = generate_random_password()

# Gerar senha de 64 bytes
senha2 = generate_random_password(64)

print(f"Senha 32 bytes: {senha1}")
print(f"Senha 64 bytes: {senha2}")
```

## 🧪 Executar Testes e Exemplos

Execute os exemplos incluídos para ver o sistema em ação:

```bash
python example.py
```

Este comando executará:
- Teste de criptografia/descriptografia de arquivo
- Teste de criptografia/descriptografia de texto
- Demonstração de geração de senhas
- Teste de segurança com senha incorreta
- Teste de performance com arquivo maior

## 🔒 Segurança

### Algoritmos Utilizados
- **AES-256-GCM**: Criptografia simétrica com autenticação
- **PBKDF2**: Derivação de chave com SHA-256 e 100.000 iterações
- **Salt aleatório**: 16 bytes únicos por arquivo/texto
- **Nonce aleatório**: 12 bytes únicos para cada operação
- **Tag de autenticação**: 16 bytes para verificação de integridade

### Boas Práticas Implementadas
- ✅ Uso de bibliotecas criptográficas estabelecidas
- ✅ Salt único para cada operação
- ✅ Nonce único para cada criptografia
- ✅ Verificação de integridade automática
- ✅ Limpeza de arquivos temporários em caso de erro
- ✅ Senhas não são armazenadas em logs ou memória desnecessariamente

### Recomendações de Uso
- 🔑 Use senhas fortes (mínimo 12 caracteres, misture maiúsculas, minúsculas, números e símbolos)
- 💾 Faça backup seguro das suas senhas
- 🗑️ Use a opção `--delete-original` apenas se tiver certeza
- 🔄 Teste a descriptografia antes de remover arquivos originais

## 📁 Estrutura do Projeto

```
Criptografia e descriptografia de arquivos/
├── file_crypto.py      # Módulo principal de criptografia
├── main.py            # Interface de linha de comando
├── example.py         # Exemplos e testes
├── requirements.txt   # Dependências do projeto
└── README.md         # Este arquivo
```

### Descrição dos Arquivos

- **`file_crypto.py`**: Contém a classe `FileCrypto` com todos os métodos de criptografia e descriptografia
- **`main.py`**: Interface CLI completa com argumentos e comandos
- **`example.py`**: Exemplos práticos e testes de funcionamento
- **`requirements.txt`**: Lista das dependências Python necessárias

## 🔧 API Reference

### Classe FileCrypto

#### `encrypt_file(file_path, password, output_path=None)`
Criptografa um arquivo.

**Parâmetros:**
- `file_path` (str): Caminho do arquivo a ser criptografado
- `password` (str): Senha para criptografia
- `output_path` (str, opcional): Caminho do arquivo de saída

**Retorna:** String com o caminho do arquivo criptografado

#### `decrypt_file(encrypted_file_path, password, output_path=None)`
Descriptografa um arquivo.

**Parâmetros:**
- `encrypted_file_path` (str): Caminho do arquivo criptografado
- `password` (str): Senha para descriptografia
- `output_path` (str, opcional): Caminho do arquivo de saída

**Retorna:** String com o caminho do arquivo descriptografado

#### `encrypt_text(text, password)`
Criptografa texto.

**Parâmetros:**
- `text` (str): Texto a ser criptografado
- `password` (str): Senha para criptografia

**Retorna:** String em base64 com o texto criptografado

#### `decrypt_text(encrypted_base64, password)`
Descriptografa texto.

**Parâmetros:**
- `encrypted_base64` (str): Texto criptografado em base64
- `password` (str): Senha para descriptografia

**Retorna:** String com o texto original

### Função generate_random_password

#### `generate_random_password(length=32)`
Gera uma senha aleatória segura.

**Parâmetros:**
- `length` (int, opcional): Comprimento da senha em bytes (padrão: 32)

**Retorna:** String em base64 com a senha gerada

## ⚠️ Tratamento de Erros

O sistema trata diversos tipos de erro:

- **FileNotFoundError**: Arquivo não encontrado
- **ValueError**: Dados corrompidos ou senha incorreta
- **PermissionError**: Problemas de permissão de arquivo
- **CryptographyError**: Erros internos de criptografia

Exemplo de tratamento:

```python
try:
    crypto = FileCrypto()
    resultado = crypto.encrypt_file("arquivo.txt", "senha")
except FileNotFoundError:
    print("Arquivo não encontrado!")
except ValueError as e:
    print(f"Erro de validação: {e}")
except Exception as e:
    print(f"Erro inesperado: {e}")
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🆘 Suporte

Se você encontrar problemas ou tiver dúvidas:

1. Verifique se todas as dependências estão instaladas
2. Execute `python example.py` para testar o funcionamento básico
3. Consulte a seção de tratamento de erros
4. Abra uma issue no repositório do projeto

## 🔮 Roadmap

- [ ] Interface gráfica (GUI)
- [ ] Suporte a criptografia assimétrica (RSA)
- [ ] Compressão automática antes da criptografia
- [ ] Suporte a múltiplos arquivos simultâneos
- [ ] Integração com serviços de nuvem
- [ ] Modo de apagamento seguro

---

**⚠️ Aviso Legal**: Este software é fornecido "como está", sem garantias. Use por sua própria conta e risco. Sempre faça backup dos seus dados importantes antes de usar qualquer ferramenta de criptografia.
