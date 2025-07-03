import firebase_admin
from firebase_admin import credentials

def initialize_firebase():
    """
    Inicializa la conexión con Firebase.
    Esta función es segura de llamar múltiples veces.
    """
    # --- CONFIGURACIÓN ---
    cred_path = 'serviceAccountKey.json'
    database_url = 'https://pos-flet-default-rtdb.firebaseio.com/'
    # --- FIN DE CONFIGURACIÓN ---

    try:
        # Revisa si la app ya está inicializada para evitar errores en hot reload
        if not firebase_admin._apps:
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