"""
Módulo para criptografia e descriptografia de arquivos usando AES
"""
import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from typing import Union


class FileCrypto:
    """
    Classe para criptografar e descriptografar arquivos usando AES-256 em modo GCM
    """
    
    def __init__(self):
        self.salt_size = 16  # 16 bytes para o salt
        self.nonce_size = 12  # 12 bytes para o nonce (GCM)
        self.tag_size = 16   # 16 bytes para o tag de autenticação
        self.key_length = 32  # 32 bytes para AES-256
        
    def _derive_key(self, password: str, salt: bytes) -> bytes:
        """
        Deriva uma chave a partir de uma senha usando PBKDF2
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=self.key_length,
            salt=salt,
            iterations=100000,  # Número alto de iterações para segurança
            backend=default_backend()
        )
        return kdf.derive(password.encode())
    
    def encrypt_file(self, file_path: str, password: str, output_path: str = None) -> str:
        """
        Criptografa um arquivo usando AES-256-GCM
        
        Args:
            file_path: Caminho para o arquivo a ser criptografado
            password: Senha para criptografia
            output_path: Caminho para o arquivo criptografado (opcional)
            
        Returns:
            Caminho do arquivo criptografado
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
            
        if output_path is None:
            output_path = file_path + ".encrypted"
            
        # Gera salt e nonce aleatórios
        salt = os.urandom(self.salt_size)
        nonce = os.urandom(self.nonce_size)
        
        # Deriva a chave da senha
        key = self._derive_key(password, salt)
        
        # Configura o cifrador AES-GCM
        cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
        encryptor = cipher.encryptor()
        
        try:
            with open(file_path, 'rb') as infile, open(output_path, 'wb') as outfile:
                # Escreve salt e nonce no início do arquivo
                outfile.write(salt)
                outfile.write(nonce)
                
                # Criptografa o arquivo em chunks
                while True:
                    chunk = infile.read(8192)  # Lê em chunks de 8KB
                    if not chunk:
                        break
                    encrypted_chunk = encryptor.update(chunk)
                    outfile.write(encrypted_chunk)
                
                # Finaliza a criptografia e escreve o tag de autenticação
                encryptor.finalize()
                outfile.write(encryptor.tag)
                
        except Exception as e:
            # Remove arquivo de saída em caso de erro
            if os.path.exists(output_path):
                os.remove(output_path)
            raise e
            
        return output_path
    
    def decrypt_file(self, encrypted_file_path: str, password: str, output_path: str = None) -> str:
        """
        Descriptografa um arquivo usando AES-256-GCM
        
        Args:
            encrypted_file_path: Caminho para o arquivo criptografado
            password: Senha para descriptografia
            output_path: Caminho para o arquivo descriptografado (opcional)
            
        Returns:
            Caminho do arquivo descriptografado
        """
        if not os.path.exists(encrypted_file_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {encrypted_file_path}")
            
        if output_path is None:
            if encrypted_file_path.endswith(".encrypted"):
                output_path = encrypted_file_path[:-10]  # Remove ".encrypted"
            else:
                output_path = encrypted_file_path + ".decrypted"
                
        try:
            with open(encrypted_file_path, 'rb') as infile:
                # Lê salt, nonce e tag
                salt = infile.read(self.salt_size)
                nonce = infile.read(self.nonce_size)
                
                if len(salt) != self.salt_size or len(nonce) != self.nonce_size:
                    raise ValueError("Arquivo criptografado inválido: cabeçalho corrompido")
                
                # Lê o conteúdo criptografado
                encrypted_data = infile.read()
                
                if len(encrypted_data) < self.tag_size:
                    raise ValueError("Arquivo criptografado inválido: muito pequeno")
                
                # Separa o tag do conteúdo
                tag = encrypted_data[-self.tag_size:]
                encrypted_content = encrypted_data[:-self.tag_size]
                
            # Deriva a chave da senha
            key = self._derive_key(password, salt)
            
            # Configura o decifrador AES-GCM
            cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
            decryptor = cipher.decryptor()
            
            with open(output_path, 'wb') as outfile:
                # Descriptografa em chunks
                chunk_size = 8192
                for i in range(0, len(encrypted_content), chunk_size):
                    chunk = encrypted_content[i:i + chunk_size]
                    decrypted_chunk = decryptor.update(chunk)
                    outfile.write(decrypted_chunk)
                
                # Finaliza a descriptografia (verifica o tag)
                decryptor.finalize()
                
        except Exception as e:
            # Remove arquivo de saída em caso de erro
            if os.path.exists(output_path):
                os.remove(output_path)
            raise e
            
        return output_path
    
    def encrypt_text(self, text: str, password: str) -> str:
        """
        Criptografa texto e retorna como string base64
        
        Args:
            text: Texto a ser criptografado
            password: Senha para criptografia
            
        Returns:
            Texto criptografado em base64
        """
        # Gera salt e nonce aleatórios
        salt = os.urandom(self.salt_size)
        nonce = os.urandom(self.nonce_size)
        
        # Deriva a chave da senha
        key = self._derive_key(password, salt)
        
        # Configura o cifrador AES-GCM
        cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
        encryptor = cipher.encryptor()
        
        # Criptografa o texto
        encrypted_text = encryptor.update(text.encode())
        encryptor.finalize()
        
        # Combina salt + nonce + texto criptografado + tag
        encrypted_data = salt + nonce + encrypted_text + encryptor.tag
        
        # Retorna como base64
        return base64.b64encode(encrypted_data).decode()
    
    def decrypt_text(self, encrypted_base64: str, password: str) -> str:
        """
        Descriptografa texto de string base64
        
        Args:
            encrypted_base64: Texto criptografado em base64
            password: Senha para descriptografia
            
        Returns:
            Texto descriptografado
        """
        try:
            # Decodifica de base64
            encrypted_data = base64.b64decode(encrypted_base64.encode())
            
            # Extrai componentes
            salt = encrypted_data[:self.salt_size]
            nonce = encrypted_data[self.salt_size:self.salt_size + self.nonce_size]
            tag = encrypted_data[-self.tag_size:]
            encrypted_text = encrypted_data[self.salt_size + self.nonce_size:-self.tag_size]
            
            # Deriva a chave da senha
            key = self._derive_key(password, salt)
            
            # Configura o decifrador AES-GCM
            cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
            decryptor = cipher.decryptor()
            
            # Descriptografa o texto
            decrypted_text = decryptor.update(encrypted_text)
            decryptor.finalize()
            
            return decrypted_text.decode()
            
        except Exception as e:
            raise ValueError(f"Erro na descriptografia: {str(e)}")


def generate_random_password(length: int = 32) -> str:
    """
    Gera uma senha aleatória segura
    
    Args:
        length: Comprimento da senha (padrão: 32)
        
    Returns:
        Senha aleatória em base64
    """
    random_bytes = os.urandom(length)
    return base64.b64encode(random_bytes).decode()