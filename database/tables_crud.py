from firebase_admin import db, exceptions

def get_all_tables():
    """Obtiene todas las mesas de la base de datos."""
    ref = db.reference('/tables')
    try:
        tables = ref.get()
    except (exceptions.NotFoundError, ValueError):
        # The path likely doesn't exist yet. Return an empty list.
        return []

    if not tables:
        return []
    # Firebase puede devolver un diccionario con IDs como claves. Lo convertimos a una lista.
    list_of_tables = [value for key, value in tables.items()] if isinstance(tables, dict) else tables
    # Filtramos posibles valores nulos que Firebase a veces deja (ej. en el índice 0)
    list_of_tables = [t for t in list_of_tables if t is not None]
    return sorted(list_of_tables, key=lambda x: x['id'])

def update_table(table_data):
    """Actualiza o crea los datos de una mesa específica por su ID."""
    table_id = table_data.get('id')
    if not table_id:
        print("Error: El diccionario de la mesa no tiene 'id'.")
        return
    # Usamos el ID de la mesa como clave en el nodo 'tables'.
    ref = db.reference(f'/tables/{table_id}')
    ref.set(table_data)

def delete_table(table_id):
    """Elimina una mesa por su ID."""
    ref = db.reference(f'/tables/{table_id}')
    ref.delete()