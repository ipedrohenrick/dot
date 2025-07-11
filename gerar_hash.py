from os import getenv
import bcrypt

# Senha para o administrador
senha = getenv('ADMIN_PASSWORD')

# Gerar o hash
hashed = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

# Exibir o hash
print(hashed.decode('utf-8'))
