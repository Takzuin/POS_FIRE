import flet as ft
from views.mesera_view import MeseraView
from views.ventas_view import VentasView
from views.caja_view import CajaView
from views.clientes_view import ClientesView
from views.administracion_view import AdministracionView

class AppLayout(ft.Column):
    def __init__(self):
        super().__init__(expand=True, spacing=0)
        self.did_mount = self.on_did_mount

    def on_did_mount(self):
        self.page.on_resize = self.page_resize
        self.build_layout()

    def toggle_theme(self, e):
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            self.page.theme_mode = ft.ThemeMode.DARK
            self.theme_button.icon = ft.Icons.LIGHT_MODE_OUTLINED
            self.theme_button.tooltip = "Cambiar a tema claro"
            # Actualizar colores del header para tema oscuro
            self.header_container.gradient = ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[
                    ft.Colors.BLUE_GREY_900,
                    ft.Colors.BLUE_GREY_800,
                    ft.Colors.INDIGO_900
                ]
            )
            # Actualizar color del contenedor de tabs para tema oscuro
            self.tabs_container.bgcolor = ft.Colors.GREY_900
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.theme_button.icon = ft.Icons.DARK_MODE_OUTLINED
            self.theme_button.tooltip = "Cambiar a tema oscuro"
            # Actualizar colores del header para tema claro
            self.header_container.gradient = ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[
                    ft.Colors.BLUE_600,
                    ft.Colors.INDIGO_600,
                    ft.Colors.PURPLE_600
                ]
            )
            # Actualizar color del contenedor de tabs para tema claro
            self.tabs_container.bgcolor = ft.Colors.WHITE
        self.page.update()

    def page_resize(self, e):
        pass

    def build_layout(self):
        # Botón de tema con efecto hover
        self.theme_button = ft.IconButton(
            icon=ft.Icons.DARK_MODE_OUTLINED,
            tooltip="Cambiar a tema oscuro",
            on_click=self.toggle_theme,
            icon_color=ft.Colors.WHITE,
            hover_color=ft.Colors.WHITE24,
            icon_size=24,
            style=ft.ButtonStyle(
                animation_duration=200,
                overlay_color=ft.Colors.WHITE12
            )
        )

        # Logo/Icono del sistema
        logo_container = ft.Container(
            content=ft.Icon(
                ft.Icons.STORE_OUTLINED,
                size=32,
                color=ft.Colors.WHITE
            ),
            width=45,
            height=45,
            bgcolor=ft.Colors.WHITE24,
            border_radius=12,
            alignment=ft.alignment.center
        )

        # Título principal con mejor tipografía
        title_text = ft.Text(
            "Sistema POS",
            size=32,
            weight=ft.FontWeight.W_700,
            color=ft.Colors.WHITE,
            font_family="Segoe UI"
        )

        # Subtítulo
        subtitle_text = ft.Text(
            "Punto de Venta Profesional",
            size=14,
            weight=ft.FontWeight.W_400,
            color=ft.Colors.WHITE70,
            font_family="Segoe UI"
        )

        # Contenedor del header con gradiente
        self.header_container = ft.Container(
            content=ft.Row([
                ft.Row([
                    logo_container,
                    ft.Column([
                        title_text,
                        subtitle_text
                    ], spacing=0, tight=True)
                ], spacing=15, alignment=ft.MainAxisAlignment.START),
                ft.Row([
                    self.theme_button
                ], alignment=ft.MainAxisAlignment.END)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.only(left=30, right=30, top=20, bottom=20),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[
                    ft.Colors.BLUE_600,
                    ft.Colors.INDIGO_600,
                    ft.Colors.PURPLE_600
                ]
            ),
            border_radius=ft.border_radius.only(bottom_left=20, bottom_right=20),
            shadow=ft.BoxShadow(
                spread_radius=2,
                blur_radius=10,
                color=ft.Colors.BLACK26,
                offset=ft.Offset(0, 3)
            )
        )

        # Tabs con diseño mejorado
        tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            indicator_color=ft.Colors.INDIGO_600,
            label_color=ft.Colors.INDIGO_600,
            unselected_label_color=ft.Colors.GREY_600,
            indicator_tab_size=True,
            divider_color=ft.Colors.TRANSPARENT,
            tabs=[
                ft.Tab(
                    text="Mesera",
                    icon=ft.Icons.RESTAURANT_MENU_OUTLINED,
                    content=ft.Container(
                        content=MeseraView(self.page),
                        padding=ft.padding.all(20)
                    )
                ),
                ft.Tab(
                    text="Caja",
                    icon=ft.Icons.POINT_OF_SALE_OUTLINED,
                    content=ft.Container(
                        content=CajaView(self.page),
                        padding=ft.padding.all(20)
                    )
                ),
                ft.Tab(
                    text="Ventas",
                    icon=ft.Icons.TRENDING_UP_OUTLINED,
                    content=ft.Container(
                        content=VentasView(self.page),
                        padding=ft.padding.all(20)
                    )
                ),
                ft.Tab(
                    text="Administración",
                    icon=ft.Icons.ADMIN_PANEL_SETTINGS_OUTLINED,
                    content=ft.Container(
                        content=AdministracionView(self.page),
                        padding=ft.padding.all(20)
                    )
                ),
            ],
            expand=1,
        )

        # Contenedor principal de tabs con sombra sutil
        self.tabs_container = ft.Container(
            content=tabs,
            expand=True,
            margin=ft.margin.only(top=5),
            bgcolor=ft.Colors.WHITE if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.Colors.GREY_900,
            border_radius=ft.border_radius.only(top_left=15, top_right=15),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=5,
                color=ft.Colors.BLACK12,
                offset=ft.Offset(0, -2)
            )
        )

        # Construir layout final
        self.controls.extend([
            self.header_container,
            self.tabs_container
        ])
        self.update()