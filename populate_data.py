# Archivo: populate_data.py

import database as db
from datetime import datetime

def populate_firestore_data():
    print("Iniciando el proceso de población con la estructura CORRECTA...")

    if not db.IS_FIREBASE_INITIALIZED:
        print("❌ ERROR: Firestore no está inicializado.")
        return

    # --- Poblar Meseros ---
    print("\nPoblando colección 'meseros'...")
    meseros_data = [
        {"name": "Ana García", "telefono": "3101234567"},
        {"name": "Carlos Ruíz", "telefono": "3009876543"}
    ]
    for data in meseros_data:
        db.add_mesero(data)
    print("✅ Meseros añadidos.")

    # --- Poblar Items ---
    print("\nPoblando colección 'items'...")
    items_data = [
        {"nombre": "Hamburguesa", "precio": 12500, "categoria": "Comidas", "descripcion": "Carne, lechuga, tomate y queso."},
        {"nombre": "Pizza", "precio": 18000, "categoria": "Comidas", "descripcion": "Salsa, mozzarella y pepperoni."},
        {"nombre": "Coca Cola", "precio": 3000, "categoria": "Bebidas", "descripcion": "Gaseosa 350ml."}
    ]
    for data in items_data:
        db.add_item(data) # <- CORREGIDO
    print("✅ Items añadidos.")
    
    # --- Poblar Mesas ---
    print("\nPoblando colección 'mesas'...")
    mesas_data = [
        {"numeromesa": 1, "meseroasig": "", "comensales": 0, "listaitems": []},
        {"numeromesa": 2, "meseroasig": "", "comensales": 0, "listaitems": []},
        {"numeromesa": 3, "meseroasig": "", "comensales": 0, "listaitems": []},
        {"numeromesa": 4, "meseroasig": "", "comensales": 0, "listaitems": []}
    ]
    for data in mesas_data:
        db.update_mesa(data) # <- CORREGIDO
    print("✅ Mesas añadidas.")

    # --- Poblar Clientes ---
    print("\nPoblando colección 'clientes'...")
    clientes_data = [
        {"nombre": "Juan Pérez", "telefono": "3115554433", "correo": "juan.p@example.com", "documento": "1030000001"},
        {"nombre": "María López", "telefono": "3107771122", "correo": "maria.l@example.com", "documento": "1030000002"},
    ]
    for data in clientes_data:
        db.add_cliente(data) # <- CORREGIDO
    print("✅ Clientes añadidos.")

    # --- Poblar Ventas (Ejemplo) ---
    print("\nPoblando colección 'ventas'...")
    ventas_data = [
        {
            "numeroventa": 1001,
            "cliente": {"nombre": "Juan Pérez", "documento": "1030000001"},
            "listaitems": [{"nombre": "Hamburguesa", "precio": 12500, "cantidad": 2}],
            "fecha": datetime.now(),
            "valor_venta": 25000  # Nota: "valor venta" se guarda como "valor_venta"
        }
    ]
    for data in ventas_data:
        db.add_venta(data) # <- CORREGIDO
    print("✅ Ventas de ejemplo añadidas.")

    print("\n🚀 ¡Población de datos finalizada!")

if __name__ == "__main__":
    populate_firestore_data()