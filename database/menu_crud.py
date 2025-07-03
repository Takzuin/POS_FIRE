from firebase_admin import db, exceptions

def get_menu():
    """Obtiene la estructura del menú de la base de datos."""
    ref = db.reference('/menu')
    try:
        menu = ref.get()
    except (exceptions.NotFoundError, ValueError):
        # The path likely doesn't exist yet. Return an empty dict.
        return {}
    return menu if menu else {}