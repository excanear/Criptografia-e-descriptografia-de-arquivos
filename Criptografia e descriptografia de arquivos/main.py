#!/usr/bin/env python3
"""
Interface de linha de comando para criptografia e descriptografia de arquivos
"""
import argparse
import getpass
import os
import sys
from file_crypto import FileCrypto, generate_random_password


def print_banner():
    """Exibe o banner do programa"""
    print("=" * 60)
    print("     CRIPTOGRAFIA E DESCRIPTOGRAFIA DE ARQUIVOS")
    print("                    AES-256-GCM")
    print("=" * 60)
    print()


def get_password(prompt: str = "Digite a senha: ") -> str:
    """
    Obtém senha do usuário de forma segura
    """
    password = getpass.getpass(prompt)
    if not password:
        print("❌ Senha não pode estar vazia!")
        sys.exit(1)
    return password


def confirm_password() -> str:
    """
    Solicita confirmação de senha
    """
    password = get_password("Digite a senha: ")
    confirm = get_password("Confirme a senha: ")
    
    if password != confirm:
        print("❌ Senhas não conferem!")
        sys.exit(1)
    
    return password


def encrypt_command(args):
    """Comando para criptografar arquivo"""
    crypto = FileCrypto()
    
    if not os.path.exists(args.file):
        print(f"❌ Arquivo não encontrado: {args.file}")
        sys.exit(1)
    
    print(f"📁 Arquivo a ser criptografado: {args.file}")
    
    if args.password:
        password = args.password
    elif args.generate_password:
        password = generate_random_password()
        print(f"🔑 Senha gerada automaticamente: {password}")
        print("⚠️  IMPORTANTE: Guarde esta senha em local seguro!")
    else:
        password = confirm_password()
    
    try:
        output_file = crypto.encrypt_file(args.file, password, args.output)
        print(f"✅ Arquivo criptografado com sucesso!")
        print(f"📄 Arquivo de saída: {output_file}")
        
        if args.delete_original:
            os.remove(args.file)
            print(f"🗑️  Arquivo original removido: {args.file}")
            
    except Exception as e:
        print(f"❌ Erro durante a criptografia: {str(e)}")
        sys.exit(1)


def decrypt_command(args):
    """Comando para descriptografar arquivo"""
    crypto = FileCrypto()
    
    if not os.path.exists(args.file):
        print(f"❌ Arquivo não encontrado: {args.file}")
        sys.exit(1)
    
    print(f"🔒 Arquivo a ser descriptografado: {args.file}")
    
    if args.password:
        password = args.password
    else:
        password = get_password()
    
    try:
        output_file = crypto.decrypt_file(args.file, password, args.output)
        print(f"✅ Arquivo descriptografado com sucesso!")
        print(f"📄 Arquivo de saída: {output_file}")
        
        if args.delete_encrypted:
            os.remove(args.file)
            print(f"🗑️  Arquivo criptografado removido: {args.file}")
            
    except Exception as e:
        print(f"❌ Erro durante a descriptografia: {str(e)}")
        print("💡 Verifique se a senha está correta e o arquivo não está corrompido.")
        sys.exit(1)


def encrypt_text_command(args):
    """Comando para criptografar texto"""
    crypto = FileCrypto()
    
    if args.text:
        text = args.text
    else:
        print("Digite o texto a ser criptografado (pressione Ctrl+D para finalizar):")
        text = sys.stdin.read().strip()
    
    if not text:
        print("❌ Texto não pode estar vazio!")
        sys.exit(1)
    
    if args.password:
        password = args.password
    elif args.generate_password:
        password = generate_random_password()
        print(f"🔑 Senha gerada automaticamente: {password}")
        print("⚠️  IMPORTANTE: Guarde esta senha em local seguro!")
    else:
        password = confirm_password()
    
    try:
        encrypted_text = crypto.encrypt_text(text, password)
        print(f"✅ Texto criptografado com sucesso!")
        print(f"🔒 Texto criptografado:")
        print(encrypted_text)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(encrypted_text)
            print(f"📄 Texto salvo em: {args.output}")
            
    except Exception as e:
        print(f"❌ Erro durante a criptografia: {str(e)}")
        sys.exit(1)


def decrypt_text_command(args):
    """Comando para descriptografar texto"""
    crypto = FileCrypto()
    
    if args.text:
        encrypted_text = args.text
    elif args.file:
        try:
            with open(args.file, 'r') as f:
                encrypted_text = f.read().strip()
        except Exception as e:
            print(f"❌ Erro ao ler arquivo: {str(e)}")
            sys.exit(1)
    else:
        print("Digite o texto criptografado:")
        encrypted_text = input().strip()
    
    if not encrypted_text:
        print("❌ Texto criptografado não pode estar vazio!")
        sys.exit(1)
    
    if args.password:
        password = args.password
    else:
        password = get_password()
    
    try:
        decrypted_text = crypto.decrypt_text(encrypted_text, password)
        print(f"✅ Texto descriptografado com sucesso!")
        print(f"📝 Texto original:")
        print(decrypted_text)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(decrypted_text)
            print(f"📄 Texto salvo em: {args.output}")
            
    except Exception as e:
        print(f"❌ Erro durante a descriptografia: {str(e)}")
        print("💡 Verifique se a senha está correta e o texto não está corrompido.")
        sys.exit(1)


def generate_password_command(args):
    """Comando para gerar senha aleatória"""
    password = generate_random_password(args.length)
    print(f"🔑 Senha gerada: {password}")
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(password)
        print(f"📄 Senha salva em: {args.output}")


def main():
    """Função principal"""
    print_banner()
    
    parser = argparse.ArgumentParser(
        description="Criptografia e descriptografia de arquivos usando AES-256-GCM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:

  Criptografar arquivo:
    python main.py encrypt arquivo.txt
    python main.py encrypt arquivo.txt -o arquivo_criptografado.bin
    python main.py encrypt arquivo.txt --generate-password
    
  Descriptografar arquivo:
    python main.py decrypt arquivo.txt.encrypted
    python main.py decrypt arquivo_criptografado.bin -o arquivo_recuperado.txt
    
  Criptografar texto:
    python main.py encrypt-text "Meu texto secreto"
    python main.py encrypt-text --generate-password -o texto_criptografado.txt
    
  Descriptografar texto:
    python main.py decrypt-text "base64_string_aqui"
    python main.py decrypt-text -f texto_criptografado.txt
    
  Gerar senha:
    python main.py generate-password
    python main.py generate-password --length 64
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponíveis')
    
    # Comando encrypt
    encrypt_parser = subparsers.add_parser('encrypt', help='Criptografar arquivo')
    encrypt_parser.add_argument('file', help='Arquivo a ser criptografado')
    encrypt_parser.add_argument('-o', '--output', help='Arquivo de saída (padrão: arquivo.encrypted)')
    encrypt_parser.add_argument('-p', '--password', help='Senha para criptografia (não recomendado)')
    encrypt_parser.add_argument('-g', '--generate-password', action='store_true', 
                               help='Gerar senha aleatória automaticamente')
    encrypt_parser.add_argument('--delete-original', action='store_true',
                               help='Remover arquivo original após criptografia')
    encrypt_parser.set_defaults(func=encrypt_command)
    
    # Comando decrypt
    decrypt_parser = subparsers.add_parser('decrypt', help='Descriptografar arquivo')
    decrypt_parser.add_argument('file', help='Arquivo a ser descriptografado')
    decrypt_parser.add_argument('-o', '--output', help='Arquivo de saída')
    decrypt_parser.add_argument('-p', '--password', help='Senha para descriptografia (não recomendado)')
    decrypt_parser.add_argument('--delete-encrypted', action='store_true',
                               help='Remover arquivo criptografado após descriptografia')
    decrypt_parser.set_defaults(func=decrypt_command)
    
    # Comando encrypt-text
    encrypt_text_parser = subparsers.add_parser('encrypt-text', help='Criptografar texto')
    encrypt_text_parser.add_argument('text', nargs='?', help='Texto a ser criptografado')
    encrypt_text_parser.add_argument('-o', '--output', help='Arquivo para salvar o texto criptografado')
    encrypt_text_parser.add_argument('-p', '--password', help='Senha para criptografia (não recomendado)')
    encrypt_text_parser.add_argument('-g', '--generate-password', action='store_true',
                                   help='Gerar senha aleatória automaticamente')
    encrypt_text_parser.set_defaults(func=encrypt_text_command)
    
    # Comando decrypt-text
    decrypt_text_parser = subparsers.add_parser('decrypt-text', help='Descriptografar texto')
    decrypt_text_parser.add_argument('text', nargs='?', help='Texto criptografado')
    decrypt_text_parser.add_argument('-f', '--file', help='Arquivo contendo texto criptografado')
    decrypt_text_parser.add_argument('-o', '--output', help='Arquivo para salvar o texto descriptografado')
    decrypt_text_parser.add_argument('-p', '--password', help='Senha para descriptografia (não recomendado)')
    decrypt_text_parser.set_defaults(func=decrypt_text_command)
    
    # Comando generate-password
    gen_pass_parser = subparsers.add_parser('generate-password', help='Gerar senha aleatória')
    gen_pass_parser.add_argument('-l', '--length', type=int, default=32,
                                help='Comprimento da senha (padrão: 32)')
    gen_pass_parser.add_argument('-o', '--output', help='Arquivo para salvar a senha')
    gen_pass_parser.set_defaults(func=generate_password_command)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == "__main__":
    main()