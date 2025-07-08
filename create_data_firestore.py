import sys
import os
from datetime import datetime

# Importa tu módulo 'database.py'
# Al importarlo, se ejecutará la función initialize_firestore() que está dentro.
import database as db

def populate_firestore_data():
    """
    Puebla Firestore con datos de ejemplo utilizando las funciones del módulo 'database'.
    """
    print("Iniciando el proceso de población de datos de prueba...")

    # 1. Verificamos que la inicialización desde el otro archivo fue exitosa.
    if not db.IS_FIREBASE_INITIALIZED:
        print("❌ ERROR: No se pudo inicializar Firestore desde el módulo 'database'.")
        return

    # --- 2. Poblar Meseros ---
    print("\n POBlando colección 'meseros'...")
    meseros_data = [
        {"name": "Ana Garcia", "telefono": "3101234567"},
        {"name": "Carlos Ruiz", "telefono": "3009876543"},
        {"name": "Luisa Diaz", "telefono": "3015558877"}
    ]
    for mesero in meseros_data:
        new_id = db.add_mesero(mesero)
        if new_id:
            print(f"  -> Mesero '{mesero['name']}' añadido.")
    print("✅ Meseros de ejemplo añadidos.")

    # --- 3. Poblar Items (Menú) ---
    print("\n POBlando colección 'menu'...")
    menu_items_data = [
        {"nombre": "Hamburguesa Sencilla", "precio": 12500, "categoria": "Comidas", "descripcion": "Carne de res, lechuga, tomate y queso."},
        {"nombre": "Pizza Pepperoni", "precio": 18000, "categoria": "Comidas", "descripcion": "Pizza con salsa de tomate, mozzarella y pepperoni."},
        {"nombre": "Ensalada César", "precio": 9500, "categoria": "Comidas", "descripcion": "Lechuga romana, crutones, queso parmesano y aderezo César."},
        {"nombre": "Coca Cola", "precio": 3000, "categoria": "Bebidas", "descripcion": "Bebida gaseosa 350ml."},
        {"nombre": "Jugo Natural Naranja", "precio": 4500, "categoria": "Bebidas", "descripcion": "Jugo de naranja recién exprimido."},
        {"nombre": "Postre Tres Leches", "precio": 6000, "categoria": "Postres", "descripcion": "Bizcocho empapado en tres tipos de leche."}
    ]
    for item in menu_items_data:
        new_id = db.add_menu_item(item)
        if new_id:
            print(f"  -> Item '{item['nombre']}' añadido.")
    print("✅ Items de menú de ejemplo añadidos.")
    
    # --- 4. Poblar Mesas ---
    print("\n POBlando colección 'tables'...")
    tables_data = [
        {"numeromesa": 1, "capacity": 4, "status": "free", "meseroAsignado": "", "client_name": "", "people": 0, "order": []},
        {"numeromesa": 2, "capacity": 6, "status": "free", "meseroAsignado": "", "client_name": "", "people": 0, "order": []},
        {"numeromesa": 3, "capacity": 4, "status": "free", "meseroAsignado": "", "client_name": "", "people": 0, "order": []},
        {"numeromesa": 4, "capacity": 2, "status": "free", "meseroAsignado": "", "client_name": "", "people": 0, "order": []},
        {"numeromesa": 5, "capacity": 8, "status": "free", "meseroAsignado": "", "client_name": "", "people": 0, "order": []}
    ]
    for table in tables_data:
        db.update_table(table)
        print(f"  -> Mesa {table['numeromesa']} añadida.")
    print("✅ Mesas de ejemplo añadidas.")

    # --- 5. Poblar Clientes ---
    print("\n POBlando colección 'clients'...")
    clients_data = [
        {"name": "Juan Pérez", "telefono": "3115554433", "correo": "juan.p@example.com", "documento": "1030000001"},
        {"name": "María López", "telefono": "3107771122", "correo": "maria.l@example.com", "documento": "1030000002"},
        {"name": "Consumidor Final", "telefono": "0000000000", "correo": "final@example.com", "documento": "0000000000"}
    ]
    for client in clients_data:
        new_id = db.add_client(client)
        if new_id:
            print(f"  -> Cliente '{client['name']}' añadido.")
    print("✅ Clientes de ejemplo añadidos.")

    print("\n🚀 ¡Población de datos finalizada exitosamente!")

if __name__ == "__main__":
    populate_firestore_data()