import firebase_admin
from firebase_admin import credentials, firestore
import os

# Debug: Confirm database.py is loaded
print("Loading database.py from:", __file__)

db_client = None
IS_FIREBASE_INITIALIZED = False

def initialize_firestore():
    """Inicializa la conexión con Firestore si no se ha hecho antes."""
    global db_client, IS_FIREBASE_INITIALIZED
    if IS_FIREBASE_INITIALIZED:
        return

    cred_path = 'serviceAccountKey.json'
    if not os.path.exists(cred_path):
        print(f"Error: El archivo '{cred_path}' no se encontró.")
        return

    try:
        cred = credentials.Certificate(cred_path)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        
        db_client = firestore.client()
        IS_FIREBASE_INITIALIZED = True
        print("Módulo de base de datos inicializado.")
    except Exception as e:
        print(f"Error al inicializar Firestore: {e}")

# --- INICIALIZACIÓN AUTOMÁTICA ---
initialize_firestore()

# --- FUNCIONES PARA MESAS ---

def add_mesa(data):
    """Añade una nueva mesa y guarda su ID de documento en un campo."""
    if not db_client:
        print("Error: Firestore no está inicializado.")
        return None
    try:
        _, doc_ref = db_client.collection('mesas').add(data)
        doc_ref.update({'doc_id': doc_ref.id})
        return doc_ref.id
    except Exception as e:
        print(f"Error al añadir mesa: {e}")
        return None

def get_all_mesas():
    """Obtiene todas las mesas, ordenadas por su ID."""
    if not db_client:
        print("Error: Firestore no está inicializado.")
        return []
    try:
        docs = db_client.collection('mesas').stream()
        mesas = [doc.to_dict() for doc in docs]
        return sorted(mesas, key=lambda x: x.get('id', ''))
    except Exception as e:
        print(f"Error al obtener mesas: {e}")
        return []

def delete_mesa(doc_id):
    """Elimina una mesa usando su ID de documento."""
    if not db_client:
        print("Error: Firestore no está inicializado.")
        return
    try:
        db_client.collection('mesas').document(doc_id).delete()
    except Exception as e:
        print(f"Error al eliminar mesa: {e}")

# --- FUNCIONES PARA ITEMS ---

def add_item(data):
    """Añade un nuevo ítem a la colección."""
    if not db_client:
        print("Error: Firestore no está inicializado.")
        return None
    try:
        _, doc_ref = db_client.collection('items').add(data)
        doc_ref.update({'doc_id': doc_ref.id})
        return doc_ref.id
    except Exception as e:
        print(f"Error al añadir ítem: {e}")
        return None

def get_all_items():
    """Obtiene todos los ítems de la colección."""
    if not db_client:
        print("Error: Firestore no está inicializado.")
        return []
    try:
        docs = db_client.collection('items').stream()
        return [doc.to_dict() for doc in docs]
    except Exception as e:
        print(f"Error al obtener ítems: {e}")
        return []

# --- FUNCIONES PARA CLIENTES ---

def add_client(data):
    """Añade un nuevo cliente y guarda su ID de documento en un campo."""
    if not db_client:
        print("Error: Firestore no está inicializado.")
        return None
    try:
        _, doc_ref = db_client.collection('clientes').add(data)
        doc_ref.update({'doc_id': doc_ref.id})
        return doc_ref.id
    except Exception as e:
        print(f"Error al añadir cliente: {e}")
        return None

def get_all_clients():
    """Obtiene todos los clientes, ordenados por nombre."""
    if not db_client:
        print("Error: Firestore no está inicializado.")
        return []
    try:
        docs = db_client.collection('clientes').stream()
        clientes = [doc.to_dict() for doc in docs]
        return sorted(clientes, key=lambda x: x.get('nombre', ''))
    except Exception as e:
        print(f"Error al obtener clientes: {e}")
        return []

def delete_client(doc_id):
    """Elimina un cliente usando su ID de documento."""
    if not db_client:
        print("Error: Firestore no está inicializado.")
        return
    try:
        db_client.collection('clientes').document(doc_id).delete()
    except Exception as e:
        print(f"Error al eliminar cliente: {e}")