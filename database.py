import firebase_admin
from firebase_admin import credentials, firestore


def initialize_firestore():
    cred_path = 'serviceAccountKey.json'
    try:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        print("Firestore inicializado correctamente.")
        return firestore.client()
    except Exception as e:
        print(f"Error al inicializar Firestore: {e}")
        return None

db = initialize_firestore()

# Obtener colección de mesas
def get_all_tables():
    tables_ref = db.collection('tables')
    docs = tables_ref.stream()
    tables = [doc.to_dict() for doc in docs]
    return sorted(tables, key=lambda x: x['id'])

def update_table(table_data):
    table_id = str(table_data.get('id'))
    if not table_id:
        print("Error: falta el 'id' de la mesa.")
        return
    db.collection('tables').document(table_id).set(table_data)

def delete_table(table_id):
    db.collection('tables').document(str(table_id)).delete()

def get_menu():
    menu_ref = db.collection('menu')
    docs = menu_ref.stream()
    return {doc.id: doc.to_dict() for doc in docs}
