import flet as ft
from app_layout import AppLayout
from views.login_view import LoginView

def main(page: ft.Page):
    page.title = "Sistema POS"
    page.window_width = 1200
    page.window_height = 800
    page.theme_mode = ft.ThemeMode.LIGHT

    # Función que cambia a AppLayout
    def mostrar_app_layout():
        page.controls.clear()
        page.add(AppLayout())  # Aquí va tu vista principal
        page.update()

    # Cargar el login, pasando la función de cambio como callback
    login_view = LoginView(page, on_login_success=mostrar_app_layout)
    page.add(login_view)
    page.update()

# Ejecutar la aplicación
if __name__ == "__main__":
    ft.app(target=main)
