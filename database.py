import firebase_admin
from firebase_admin import credentials, db

def initialize_firebase():
    """
    Inicializa la conexión con Firebase.
    Asegúrate de tener tu archivo de credenciales y la URL de tu base de datos.
    """
    # --- CONFIGURACIÓN ---
    # 1. Coloca tu archivo de credenciales 'serviceAccountKey.json' en la raíz del proyecto.
    cred_path = 'serviceAccountKey.json'

    # 2. Reemplaza la URL de abajo con la URL de tu Realtime Database.
    database_url = 'https://pos-flet-default-rtdb.firebaseio.com/'
    # --- FIN DE CONFIGURACIÓN ---

    try:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred, {
            'databaseURL': database_url
        })
        print("Firebase inicializado correctamente.")
        return True
    except Exception as e:
        print(f"Error al inicializar Firebase: {e}")
        print("Asegúrate de que tu archivo 'serviceAccountKey.json' y la URL de la base de datos son correctos.")
        return False

# --- Funciones para Mesas (Tables) ---

def get_tables():
    """Obtiene todas las mesas de la base de datos."""
    ref = db.reference('/tables')
    tables = ref.get()
    if not tables:
        return []
    # Firebase puede devolver un diccionario con IDs como claves. Lo convertimos a una lista.
    # Usamos `items()` para asegurar que obtenemos los datos correctos si la estructura es un diccionario.
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

# --- Funciones para Menú (Menu) ---

def get_menu():
    """Obtiene la estructura del menú de la base de datos."""
    ref = db.reference('/menu')
    menu = ref.get()
    return menu if menu else {}

# --- Inicialización ---
IS_FIREBASE_INITIALIZED = initialize_firebase()