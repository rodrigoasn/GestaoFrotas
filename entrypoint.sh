#!/bin/sh

# Sair imediatamente se um comando sair com um status não-zero.
set -e

# Aplicar migrations
echo "Aplicando migrations..."
python manage.py makemigrations accounts
python manage.py makemigrations
python manage.py migrate

# Criar superuser se não existir
echo "Criando superuser..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='admin@example.com').exists():
    User.objects.create_superuser('admin@example.com', 'admin123')
    print('Superuser criado: admin@example.com / admin123')
else:
    print('Superuser já existe.')
END

# Executar o comando passado para docker run (CMD)
exec "$@"
