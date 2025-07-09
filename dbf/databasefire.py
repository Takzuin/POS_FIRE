import firebase_admin
from firebase_admin import credentials, firestore, auth
import os
from firebase_admin import auth
import datetime

# --- INICIALIZACIÓN DE FIRESTORE ---
db_client = None
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate('serviceAccountKey.json')
        firebase_admin.initialize_app(cred)
        db_client = firestore.client()
        print("Módulo de base de datos inicializado correctamente.")
    except Exception as e:
        print(f"Error al inicializar Firestore: {e}")

# --- FUNCIONES PARA MESAS ---

def add_mesa(data):
    """Añade una nueva mesa y guarda su ID de documento en un campo."""
    if not db_client: return None
    try:
        _, doc_ref = db_client.collection('mesas').add(data)
        doc_ref.update({'doc_id': doc_ref.id})
        return doc_ref.id
    except Exception as e:
        print(f"Error al añadir mesa: {e}")
        return None

def get_all_mesas():
    """Obtiene todas las mesas."""
    if not db_client: return []
    try:
        docs = db_client.collection('mesas').stream()
        return [doc.to_dict() for doc in docs]
    except Exception as e:
        print(f"Error al obtener mesas: {e}")
        return []

def get_mesa_by_id(mesa_id):
    """Obtiene una mesa específica por su ID de forma eficiente."""
    if not db_client: return None
    try:
        docs = db_client.collection('mesas').where('id', '==', mesa_id).limit(1).stream()
        for doc in docs:
            return doc.to_dict()
        return None
    except Exception as e:
        print(f"Error al obtener mesa: {e}")
        return None

def update_mesa(doc_id, data):
    """Actualiza una mesa existente usando su ID de documento."""
    if not db_client: return False
    try:
        db_client.collection('mesas').document(doc_id).update(data)
        return True
    except Exception as e:
        print(f"Error al actualizar mesa: {e}")
        return False

def delete_mesa(doc_id):
    """Elimina una mesa usando su ID de documento."""
    if not db_client: return
    try:
        db_client.collection('mesas').document(doc_id).delete()
    except Exception as e:
        print(f"Error al eliminar mesa: {e}")

# --- FUNCIONES PARA MESEROS ---

def add_mesero(data):
    """Añade un nuevo mesero y guarda su ID de documento."""
    if not db_client: return None
    try:
        _, doc_ref = db_client.collection('meseros').add(data)
        doc_ref.update({'doc_id': doc_ref.id})
        return doc_ref.id
    except Exception as e:
        print(f"Error al añadir mesero: {e}")
        return None

def get_all_meseros():
    """Obtiene todos los meseros."""
    if not db_client: return []
    try:
        docs = db_client.collection('meseros').stream()
        return [doc.to_dict() for doc in docs]
    except Exception as e:
        print(f"Error al obtener meseros: {e}")
        return []

def delete_mesero(doc_id):
    """Elimina un mesero usando su ID de documento."""
    if not db_client: return
    try:
        db_client.collection('meseros').document(doc_id).delete()
    except Exception as e:
        print(f"Error al eliminar mesero: {e}")

# --- FUNCIONES PARA PRODUCTOS (ITEMS) ---

def add_item(data):
    """Añade un nuevo ítem a la colección."""
    if not db_client: return None
    try:
        _, doc_ref = db_client.collection('items').add(data)
        doc_ref.update({'doc_id': doc_ref.id})
        return doc_ref.id
    except Exception as e:
        print(f"Error al añadir ítem: {e}")
        return None

def get_all_items():
    """Obtiene todos los ítems de la colección."""
    if not db_client: return []
    try:
        docs = db_client.collection('items').stream()
        return [doc.to_dict() for doc in docs]
    except Exception as e:
        print(f"Error al obtener ítems: {e}")
        return []

def delete_item(doc_id):
    """Elimina un ítem usando su ID de documento."""
    print(f"--- INTENTANDO BORRAR ÍTEM CON DOC_ID: '{doc_id}' ---")
    if not db_client:
        print("Error: Firestore no está inicializado.")
        return
    if not doc_id:
        print("ERROR: El ID del documento está vacío. No se puede borrar.")
        return
    try:
        db_client.collection('items').document(doc_id).delete()
        print(">>> Borrado en Firestore ejecutado con éxito.")
    except Exception as e:
        print(f"!!! Error de Firestore al intentar borrar: {e}")


# --- FUNCIONES PARA VENTAS ---

def add_venta(data):
    """Añade una nueva venta a la colección 'ventas'."""
    if not db_client: return None
    try:
        # Añadimos una marca de tiempo automática al crear la venta
        data['timestamp'] = firestore.SERVER_TIMESTAMP
        _, doc_ref = db_client.collection('ventas').add(data)
        doc_ref.update({'doc_id': doc_ref.id})
        return doc_ref.id
    except Exception as e:
        print(f"Error al añadir venta: {e}")
        return None
    


# --- FUNCIONES PARA LA ORDEN EN TIEMPO REAL DE UNA MESA ---

def get_orden_actual(mesa_doc_id):
    """Obtiene los ítems del pedido actual de una mesa desde su subcolección 'orden_actual'."""
    if not db_client or not mesa_doc_id: return []
    try:
        items_ref = db_client.collection('mesas').document(mesa_doc_id).collection('orden_actual').stream()
        return [item.to_dict() for item in items_ref]
    except Exception as e:
        print(f"Error al obtener la orden actual: {e}")
        return []

def add_item_a_orden(mesa_doc_id, item_data):
    """Añade o actualiza la cantidad de un ítem en la orden actual de una mesa."""
    if not db_client or not mesa_doc_id: return None
    try:
        # Usamos el doc_id del producto como ID del documento en la subcolección para evitar duplicados
        item_doc_ref = db_client.collection('mesas').document(mesa_doc_id).collection('orden_actual').document(item_data['doc_id'])
        
        # Verificamos si el ítem ya existe para solo actualizar la cantidad
        if item_doc_ref.get().exists:
            # Si existe, incrementamos la cantidad en 1
            item_doc_ref.update({'cantidad': firestore.Increment(1)})
        else:
            # Si no existe, lo creamos con cantidad 1
            item_data['cantidad'] = 1
            item_doc_ref.set(item_data)
        return True
    except Exception as e:
        print(f"Error al añadir ítem a la orden: {e}")
        return False

def remove_item_de_orden(mesa_doc_id, item_doc_id):
    """Elimina un ítem de la orden actual de una mesa."""
    if not db_client or not mesa_doc_id or not item_doc_id: return False
    try:
        db_client.collection('mesas').document(mesa_doc_id).collection('orden_actual').document(item_doc_id).delete()
        return True
    except Exception as e:
        print(f"Error al eliminar ítem de la orden: {e}")
        return False

def limpiar_orden_actual(mesa_doc_id):
    """Elimina todos los ítems de la orden de una mesa (usado después de facturar)."""
    if not db_client or not mesa_doc_id: return False
    try:
        docs = db_client.collection('mesas').document(mesa_doc_id).collection('orden_actual').stream()
        for doc in docs:
            doc.reference.delete()
        return True
    except Exception as e:
        print(f"Error al limpiar la orden: {e}")
        return False
    
# --- FUNCION PARA FACTURACION FINAL ---

def add_factura(data):
    """Añade una factura final a la colección 'facturado'."""
    if not db_client: return None
    try:
        data['fecha_facturacion'] = firestore.SERVER_TIMESTAMP
        _, doc_ref = db_client.collection('facturado').add(data)
        doc_ref.update({'doc_id': doc_ref.id})
        return doc_ref.id
    except Exception as e:
        print(f"Error al añadir factura: {e}")
        return None
    
# --- FUNCION PARA OBTENER VENTAS FILTRADAS ---

def get_facturas_por_fecha(fecha_seleccionada):
    """
    Obtiene todas las facturas de un día específico.
    'fecha_seleccionada' debe ser un objeto datetime.date.
    """
    if not db_client: return []
    try:
        # El inicio del día (00:00:00)
        start_of_day = datetime.combine(fecha_seleccionada, datetime.min.time())
        # El final del día (23:59:59)
        end_of_day = datetime.combine(fecha_seleccionada, datetime.max.time())

        docs = db_client.collection('facturado') \
            .where('fecha_facturacion', '>=', start_of_day) \
            .where('fecha_facturacion', '<=', end_of_day) \
            .order_by('fecha_facturacion', direction=firestore.Query.DESCENDING) \
            .stream()
        
        return [doc.to_dict() for doc in docs]
    except Exception as e:
        print(f"Error al obtener facturas por fecha: {e}")
        return []

def get_all_facturas():
    """Obtiene todas las facturas ordenadas por fecha descendente."""
    if not db_client: return []
    try:
        docs = db_client.collection('facturado') \
            .order_by('fecha_facturacion', direction=firestore.Query.DESCENDING) \
            .stream()
        return [doc.to_dict() for doc in docs]
    except Exception as e:
        print(f"Error al obtener todas las facturas: {e}")
        return []

def verify_user_credentials(email, password):
    try:
        user = auth.get_user_by_email(email)
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