#!/bin/sh

echo "⚙️ Применяю миграции..."
python manage.py migrate --noinput

echo "👤 Создаю суперпользователя (если не существует)..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@example.com", "admin")
EOF

echo "🚀 Запускаю сервер Django..."
exec python manage.py runserver 0.0.0.0:8000