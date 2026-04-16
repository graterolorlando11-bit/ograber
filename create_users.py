#!/usr/bin/env python3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoapi.settings')
django.setup()

from django.contrib.auth.models import User

# Crear usuario normal
if not User.objects.filter(username='usuario_normal').exists():
    user = User.objects.create_user(
        username='usuario_normal',
        email='usuario@example.com',
        password='usuario123',
        first_name='Usuario',
        last_name='Normal'
    )
    user.save()
    print("✅ Usuario 'usuario_normal' creado con contraseña 'usuario123'")
else:
    print("ℹ️ Usuario 'usuario_normal' ya existe")

# Crear usuario admin (si no existe)
if not User.objects.filter(username='admin_normal').exists():
    admin = User.objects.create_user(
        username='admin_normal',
        email='admin@example.com',
        password='admin123',
        first_name='Admin',
        last_name='Normal',
        is_staff=True
    )
    admin.save()
    print("✅ Usuario admin 'admin_normal' creado con contraseña 'admin123'")
else:
    print("ℹ️ Usuario admin 'admin_normal' ya existe")

print("\n📋 Usuarios disponibles:")
for user in User.objects.all():
    role = "ADMIN" if user.is_staff or user.is_superuser else "USER"
    print(f"  • {user.username} ({role}) - {user.email}")