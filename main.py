import flet as ft


def main(page: ft.Page):
    page.title = "Sistema POS"
    page.window_width = 1200
    page.window_height = 800
    page.theme_mode = ft.ThemeMode.LIGHT

    # Función para cambiar tema
    def toggle_theme(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            theme_button.icon = ft.Icons.LIGHT_MODE
            theme_button.tooltip = "Cambiar a tema claro"
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_button.icon = ft.Icons.DARK_MODE
            theme_button.tooltip = "Cambiar a tema oscuro"
        page.update()

    # Botón para cambiar tema
    theme_button = ft.IconButton(
        icon=ft.Icons.DARK_MODE,
        tooltip="Cambiar a tema oscuro",
        on_click=toggle_theme
    )

    # Contenido para cada tab
    def mesera_content():
        return ft.Container(
            content=ft.Column([
                ft.Text("Módulo Mesera", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Aquí irán las funciones de mesera: tomar pedidos, mesas, etc.")
            ]),
            padding=20
        )

    def cocina_content():
        return ft.Container(
            content=ft.Column([
                ft.Text("Módulo Cocina", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Aquí irán las funciones de cocina: pedidos pendientes, preparación, etc.")
            ]),
            padding=20
        )

    def caja_content():
        return ft.Container(
            content=ft.Column([
                ft.Text("Módulo Caja", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Aquí irán las funciones de caja: facturación, pagos, reportes de venta, etc.")
            ]),
            padding=20
        )

    def administracion_content():
        return ft.Container(
            content=ft.Column([
                ft.Text("Módulo Administración", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Aquí irán las funciones administrativas: inventario, usuarios, configuración, etc.")]),
            padding=20
        )

    # Crear los tabs
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Mesera",
                icon=ft.Icons.RESTAURANT_MENU,
                content=mesera_content()
            ),
            ft.Tab(
                text="Cocina",
                icon=ft.Icons.KITCHEN,
                content=cocina_content()
            ),
            ft.Tab(
                text="Caja",
                icon=ft.Icons.ATTACH_MONEY_ROUNDED,
                content=caja_content()
            ),
            ft.Tab(
                text="Administración",
                icon=ft.Icons.ADMIN_PANEL_SETTINGS,
                content=administracion_content()
            ),
        ],
        expand=1,
    )

    # Header con título y botón de tema
    header = ft.Container(
        content=ft.Row([
            ft.Text("Sistema POS", size=28, weight=ft.FontWeight.BOLD),
            theme_button
        ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.padding.only(left=20, right=20, top=10, bottom=10),
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        border_radius=ft.border_radius.only(bottom_left=10, bottom_right=10)
    )

    # Agregar header y tabs a la página
    page.add(
        ft.Column([
            header,
            ft.Container(tabs, expand=True)
        ], expand=True)
    )


# Ejecutar la aplicación
if __name__ == "__main__":
    ft.app(target=main)