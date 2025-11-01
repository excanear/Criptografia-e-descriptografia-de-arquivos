#!/usr/bin/env python3
"""
Exemplos de uso e testes básicos para o sistema de criptografia
"""
import os
import tempfile
from file_crypto import FileCrypto, generate_random_password


def exemplo_criptografia_arquivo():
    """
    Exemplo básico de criptografia e descriptografia de arquivo
    """
    print("=" * 50)
    print("EXEMPLO 1: Criptografia de Arquivo")
    print("=" * 50)
    
    # Cria um arquivo de exemplo
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("Este é um conteúdo secreto que será criptografado!\n")
        f.write("Linha 2 do arquivo.\n")
        f.write("Linha 3 com dados importantes.")
        arquivo_original = f.name
    
    print(f"📁 Arquivo criado: {arquivo_original}")
    
    # Criptografia
    crypto = FileCrypto()
    senha = "MinhaS3nhaS3gura!"
    
    try:
        arquivo_criptografado = crypto.encrypt_file(arquivo_original, senha)
        print(f"🔒 Arquivo criptografado: {arquivo_criptografado}")
        
        # Mostra o tamanho dos arquivos
        tamanho_original = os.path.getsize(arquivo_original)
        tamanho_criptografado = os.path.getsize(arquivo_criptografado)
        print(f"📊 Tamanho original: {tamanho_original} bytes")
        print(f"📊 Tamanho criptografado: {tamanho_criptografado} bytes")
        
        # Descriptografia
        arquivo_descriptografado = crypto.decrypt_file(arquivo_criptografado, senha)
        print(f"🔓 Arquivo descriptografado: {arquivo_descriptografado}")
        
        # Verifica se o conteúdo é o mesmo
        with open(arquivo_original, 'r') as f1, open(arquivo_descriptografado, 'r') as f2:
            conteudo_original = f1.read()
            conteudo_descriptografado = f2.read()
            
        if conteudo_original == conteudo_descriptografado:
            print("✅ Sucesso! Conteúdo original e descriptografado são idênticos")
        else:
            print("❌ Erro! Conteúdos são diferentes")
            
        # Limpeza
        os.unlink(arquivo_original)
        os.unlink(arquivo_criptografado)
        os.unlink(arquivo_descriptografado)
        print("🧹 Arquivos temporários removidos")
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")


def exemplo_criptografia_texto():
    """
    Exemplo de criptografia e descriptografia de texto
    """
    print("\n" + "=" * 50)
    print("EXEMPLO 2: Criptografia de Texto")
    print("=" * 50)
    
    crypto = FileCrypto()
    texto_original = "Esta é uma mensagem secreta que será criptografada!"
    senha = "OutraS3nhaS3gura123"
    
    try:
        # Criptografia
        texto_criptografado = crypto.encrypt_text(texto_original, senha)
        print(f"📝 Texto original: {texto_original}")
        print(f"🔒 Texto criptografado (base64): {texto_criptografado}")
        
        # Descriptografia
        texto_descriptografado = crypto.decrypt_text(texto_criptografado, senha)
        print(f"🔓 Texto descriptografado: {texto_descriptografado}")
        
        if texto_original == texto_descriptografado:
            print("✅ Sucesso! Textos original e descriptografado são idênticos")
        else:
            print("❌ Erro! Textos são diferentes")
            
    except Exception as e:
        print(f"❌ Erro: {str(e)}")


def exemplo_senha_aleatoria():
    """
    Exemplo de geração de senha aleatória
    """
    print("\n" + "=" * 50)
    print("EXEMPLO 3: Geração de Senha Aleatória")
    print("=" * 50)
    
    # Gera senhas de diferentes tamanhos
    for tamanho in [16, 32, 64]:
        senha = generate_random_password(tamanho)
        print(f"🔑 Senha de {tamanho} bytes: {senha}")


def teste_senha_incorreta():
    """
    Teste de comportamento com senha incorreta
    """
    print("\n" + "=" * 50)
    print("EXEMPLO 4: Teste com Senha Incorreta")
    print("=" * 50)
    
    crypto = FileCrypto()
    texto_original = "Texto para teste de senha incorreta"
    senha_correta = "SenhaCorreta123"
    senha_incorreta = "SenhaErrada456"
    
    try:
        # Criptografia com senha correta
        texto_criptografado = crypto.encrypt_text(texto_original, senha_correta)
        print(f"📝 Texto criptografado com sucesso")
        
        # Tentativa de descriptografia com senha incorreta
        try:
            crypto.decrypt_text(texto_criptografado, senha_incorreta)
            print("❌ ERRO: Descriptografia deveria ter falhado!")
        except Exception as e:
            print(f"✅ Sucesso! Descriptografia falhou como esperado: {type(e).__name__}")
            
        # Descriptografia com senha correta
        texto_descriptografado = crypto.decrypt_text(texto_criptografado, senha_correta)
        if texto_original == texto_descriptografado:
            print("✅ Sucesso! Descriptografia com senha correta funcionou")
            
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")


def teste_arquivo_grande():
    """
    Teste com arquivo maior para verificar performance
    """
    print("\n" + "=" * 50)
    print("EXEMPLO 5: Teste com Arquivo Maior")
    print("=" * 50)
    
    # Cria um arquivo maior (cerca de 100KB)
    conteudo_grande = "Este é um teste com arquivo maior.\n" * 3000
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write(conteudo_grande)
        arquivo_grande = f.name
    
    crypto = FileCrypto()
    senha = "SenhaParaArquivoGrande"
    
    try:
        import time
        
        # Mede tempo de criptografia
        inicio = time.time()
        arquivo_criptografado = crypto.encrypt_file(arquivo_grande, senha)
        tempo_criptografia = time.time() - inicio
        
        # Mede tempo de descriptografia
        inicio = time.time()
        arquivo_descriptografado = crypto.decrypt_file(arquivo_criptografado, senha)
        tempo_descriptografia = time.time() - inicio
        
        # Verifica integridade
        with open(arquivo_grande, 'r') as f1, open(arquivo_descriptografado, 'r') as f2:
            if f1.read() == f2.read():
                print("✅ Integridade verificada!")
            else:
                print("❌ Erro de integridade!")
        
        # Mostra estatísticas
        tamanho_original = os.path.getsize(arquivo_grande)
        tamanho_criptografado = os.path.getsize(arquivo_criptografado)
        
        print(f"📊 Tamanho original: {tamanho_original:,} bytes")
        print(f"📊 Tamanho criptografado: {tamanho_criptografado:,} bytes")
        print(f"⏱️  Tempo de criptografia: {tempo_criptografia:.3f}s")
        print(f"⏱️  Tempo de descriptografia: {tempo_descriptografia:.3f}s")
        
        # Limpeza
        os.unlink(arquivo_grande)
        os.unlink(arquivo_criptografado)
        os.unlink(arquivo_descriptografado)
        print("🧹 Arquivos temporários removidos")
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")


def main():
    """
    Executa todos os exemplos
    """
    print("🔐 EXEMPLOS DE CRIPTOGRAFIA E DESCRIPTOGRAFIA")
    print("Executando testes básicos...\n")
    
    exemplo_criptografia_arquivo()
    exemplo_criptografia_texto()
    exemplo_senha_aleatoria()
    teste_senha_incorreta()
    teste_arquivo_grande()
    
    print("\n" + "=" * 50)
    print("✅ Todos os exemplos foram executados!")
    print("=" * 50)


if __name__ == "__main__":
    main()