import flet as ft
from app_layout import AppLayout

def main(page: ft.Page):
    page.title = "Sistema POS"
    page.window_width = 1200
    page.window_height = 800
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # Creamos una instancia de nuestro layout principal
    app = AppLayout()
    
    # Agregamos el layout a la página
    page.add(app)
    page.update()

# Ejecutar la aplicación
if __name__ == "__main__":
    ft.app(target=main)