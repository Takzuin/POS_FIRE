import flet as ft

# Importamos las vistas individuales desde la carpeta 'views'
from views.mesera_view import MeseraView
from views.cocina_view import CocinaView
from views.caja_view import CajaView
from views.administracion_view import AdministracionView

class AppLayout(ft.Column):
    def __init__(self):
        super().__init__(expand=True)
        
        # El método 'did_mount' se llama cuando el control se agrega a la página
        self.did_mount = self.on_did_mount

    def on_did_mount(self):
        # self.page está disponible después de que el control se monta
        self.page.on_resize = self.page_resize
        self.build_layout()

    def toggle_theme(self, e):
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            self.page.theme_mode = ft.ThemeMode.DARK
            self.theme_button.icon = ft.Icons.LIGHT_MODE
            self.theme_button.tooltip = "Cambiar a tema claro"
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.theme_button.icon = ft.Icons.DARK_MODE
            self.theme_button.tooltip = "Cambiar a tema oscuro"
        self.page.update()

    def page_resize(self, e):
        # Lógica para adaptar la UI si es necesario en el futuro
        pass

    def build_layout(self):
        self.theme_button = ft.IconButton(
            icon=ft.Icons.DARK_MODE,
            tooltip="Cambiar a tema oscuro",
            on_click=self.toggle_theme
        )

        header = ft.Container(
            content=ft.Row([
                ft.Text("Sistema POS", size=28, weight=ft.FontWeight.BOLD),
                self.theme_button
            ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.only(left=20, right=20, top=10, bottom=10),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            border_radius=ft.border_radius.only(bottom_left=10, bottom_right=10)
        )

        tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Mesera",
                    icon=ft.Icons.RESTAURANT_MENU,
                    content=MeseraView() # Usamos la clase de la vista
                ),
                ft.Tab(
                    text="Cocina",
                    icon=ft.Icons.KITCHEN,
                    content=CocinaView()
                ),
                ft.Tab(
                    text="Caja",
                    icon=ft.Icons.ATTACH_MONEY_ROUNDED,
                    content=CajaView()
                ),
                ft.Tab(
                    text="Administración",
                    icon=ft.Icons.ADMIN_PANEL_SETTINGS,
                    content=AdministracionView()
                ),
            ],
            expand=1,
        )

        self.controls.extend([
            header,
            ft.Container(tabs, expand=True)
        ])
        self.update()