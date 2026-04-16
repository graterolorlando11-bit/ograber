#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoapi.settings')
django.setup()

from django.db import connection

cursor = connection.cursor()

print("\n" + "="*70)
print("TABLAS EN LA BASE DE DATOS 'exam'")
print("="*70)

# Obtener tablas
cursor.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
    ORDER BY table_name
""")

tables = cursor.fetchall()

if not tables:
    print("❌ No hay tablas en la base de datos")
else:
    for table in tables:
        table_name = table[0]
        
        # Saltar tablas del sistema Django
        if table_name.startswith('django_'):
            continue
            
        print(f"\n📋 Tabla: {table_name}")
        print("─" * 70)
        
        # Obtener columnas
        cursor.execute(f"""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = '{table_name}'
            ORDER BY ordinal_position
        """)
        
        columns = cursor.fetchall()
        for col in columns:
            nullable = "✓ NULL" if col[2] == "YES" else "✗ NOT NULL"
            print(f"  • {col[0]:30} {col[1]:25} {nullable}")
        
        # Contar filas
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"  ➜ Total filas: {count}")

print("\n" + "="*70)
print("✅ Escaneo completado")
print("="*70 + "\n")
