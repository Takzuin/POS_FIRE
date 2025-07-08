from .connection import initialize_firebase
from .tables_crud import get_all_tables, update_table, delete_table
from .menu_crud import get_menu

# Inicializa Firebase al importar el paquete y expone el estado de la conexión.
IS_FIREBASE_INITIALIZED = initialize_firebase()