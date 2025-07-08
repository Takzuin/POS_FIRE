import firebase_admin
from firebase_admin import credentials, firestore
import os

print("Iniciando prueba de conexión a Firestore...")

# 1. Define la ruta a tu clave de servicio
cred_path = 'serviceAccountKey.json'

# 2. Verifica que el archivo de la clave exista
if not os.path.exists(cred_path):
    print(f"❌ ERROR: No se encontró el archivo '{cred_path}'.")
    print("Asegúrate de que el nombre es correcto y está en la misma carpeta que este script.")
else:
    try:
        # 3. Inicializa la conexión con Firebase
        cred = credentials.Certificate(cred_path)
        
        # Evita el error de "re-inicialización" si ya lo has corrido antes
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        
        # 4. Obtén el cliente de Firestore
        db = firestore.client()

        # 5. Intenta escribir un documento como prueba
        # Esto confirma que tienes permisos de escritura y la conexión funciona.
        test_collection_ref = db.collection('pruebas_conexion')
        test_doc_ref = test_collection_ref.document('test_documento')
        test_doc_ref.set({
            'mensaje': 'Conexión exitosa desde Python',
            'timestamp': firestore.SERVER_TIMESTAMP # Usa la hora del servidor
        })

        print("\n✅ ¡Conexión y escritura en Firestore exitosas!")
        print("👉 Revisa tu consola de Firebase: Deberías ver una colección 'pruebas_conexion'.")

    except Exception as e:
        print(f"\n❌ Ocurrió un error al intentar conectar o escribir en Firestore:")
        print(f"   Error: {e}")