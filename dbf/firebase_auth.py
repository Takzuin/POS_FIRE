from firebase_admin import auth
import hashlib
import firebase_admin
from dbf.databasefire import db_client
from firebase_admin import firestore

def create_user_with_email_password(email, password, display_name=None):
    """Crea un usuario en Firebase Auth"""
    try:
        user = auth.create_user(
            email=email,
            password=password,
            display_name=display_name
        )
        return user.uid
    except Exception as e:
        print(f"Error creating user: {e}")
        return None

def verify_user_credentials(email, password):
    """
    Verifica las credenciales del usuario
    Nota: Firebase Admin SDK no tiene verificación directa de contraseñas
    Esta función es un ejemplo de cómo podrías implementarla
    """
    try:
        user = auth.get_user_by_email(email)
        # Aquí tendrías que implementar tu propia lógica de verificación
        # o usar el Firebase Auth REST API
        return user.uid
    except Exception as e:
        print(f"Error verifying user: {e}")
        return None

def get_user_info(uid):
    """Obtiene información del usuario por UID"""
    try:
        user = auth.get_user(uid)
        return {
            'uid': user.uid,
            'email': user.email,
            'display_name': user.display_name,
            'email_verified': user.email_verified
        }
    except Exception as e:
        print(f"Error getting user info: {e}")
        return None

# Funciones adicionales para tu database.py
def add_user_session(user_email, session_data):
    """Guarda información de sesión del usuario"""
    if not db_client: return None
    try:
        session_data['email'] = user_email
        session_data['login_time'] = firestore.SERVER_TIMESTAMP
        _, doc_ref = db_client.collection('user_sessions').add(session_data)
        return doc_ref.id
    except Exception as e:
        print(f"Error saving user session: {e}")
        return None

def get_user_permissions(user_email):
    """Obtiene permisos del usuario"""
    if not db_client: return {}
    try:
        doc = db_client.collection('user_permissions').document(user_email).get()
        if doc.exists:
            return doc.to_dict()
        else:
            # Permisos por defecto
            return {
                'can_add_items': False,
                'can_delete_items': False,
                'can_view_reports': False,
                'can_manage_users': False
            }
    except Exception as e:
        print(f"Error getting user permissions: {e}")
        return {}