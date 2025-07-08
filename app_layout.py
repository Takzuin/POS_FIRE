import flet as ft
from views.mesera_view import MeseraView
from views.ventas_view import VentasView
from views.caja_view import CajaView
from views.clientes_view import ClientesView
from views.administracion_view import AdministracionView

class AppLayout(ft.Column):
    def __init__(self):
        super().__init__(expand=True)
        self.did_mount = self.on_did_mount

    def on_did_mount(self):
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
            bgcolor=ft.Colors.ON_SURFACE_VARIANT,
            border_radius=ft.border_radius.only(bottom_left=10, bottom_right=10)
        )

        tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Mesera",
                    icon=ft.Icons.RESTAURANT_MENU,
                    content=MeseraView(self.page)  # Pass page to MeseraView
                ),
                ft.Tab(
                    text="Caja",
                    icon=ft.Icons.POINT_OF_SALE,
                    content=CajaView(self.page)  # Pass page to CajaView
                ),
                ft.Tab(
                    text="Ventas",
                    icon=ft.Icons.PEOPLE_OUTLINE,
                    content=VentasView(self.page)  # Pass page to ClientesView
                ),
                ft.Tab(
                    text="Administración",
                    icon=ft.Icons.ADMIN_PANEL_SETTINGS,
                    content=AdministracionView(self.page)  # Pass page to AdministracionView
                ),
            ],
            expand=1,
        )

        self.controls.extend([
            header,
            ft.Container(tabs, expand=True)
        ])
        self.update()