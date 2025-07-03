import flet as ft

class AdministracionView(ft.Container):
    def __init__(self):
        super().__init__(padding=20, expand=True)
        self.content = ft.Column(
            controls=[
                ft.Text("Módulo Administración", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Aquí irán las funciones administrativas: inventario, usuarios, configuración, etc.")
            ]
        )