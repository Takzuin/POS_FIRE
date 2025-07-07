import os

def extract_python_files(directory):
    """
    Recorre un directorio y extrae el texto plano de todos los archivos .py,
    ignorando la carpeta '.venv'.
    """
    # Lista para almacenar el contenido de los archivos
    file_contents = {}

    # Recorrer el árbol de directorios
    for root, dirs, files in os.walk(directory):
        # Ignorar la carpeta '.venv'
        if '.venv' in dirs:
            dirs.remove('.venv')  # No explorar esta carpeta

        # Procesar cada archivo en el directorio actual
        for file in files:
            if file.endswith('.py'):  # Solo procesar archivos con extensión .py
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        file_contents[file_path] = content
                except Exception as e:
                    print(f"Error al leer el archivo {file_path}: {e}")

    return file_contents

# Directorio raíz donde buscar los archivos .py
root_directory = r"C:\Users\Jose\Desktop\POS_FIRE"

# Obtener el texto plano de los archivos .py
python_files_content = extract_python_files(root_directory)

# Ruta del archivo de salida
output_file_path = "output.txt"

# Escribir el contenido de cada archivo en output.txt
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for file_path, content in python_files_content.items():
        output_file.write(f"Archivo: {file_path}\n")
        output_file.write(content)
        output_file.write("\n" + "="*80 + "\n")  # Separador entre archivos

print(f"El contenido de los archivos .py se ha guardado en {output_file_path}")