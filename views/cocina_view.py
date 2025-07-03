import flet as ft

class CocinaView(ft.Container):
    def __init__(self):
        super().__init__(padding=20, expand=True)
        self.content = ft.Column(
            controls=[
                ft.Text("Módulo Cocina", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Aquí irán las funciones de cocina: pedidos pendientes, preparación, etc.")
            ]
        )