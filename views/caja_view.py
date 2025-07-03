import flet as ft

class CajaView(ft.Container):
    def __init__(self):
        super().__init__(padding=20, expand=True)
        self.content = ft.Column(
            controls=[
                ft.Text("Módulo Caja", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Aquí irán las funciones de caja: facturación, pagos, reportes de venta, etc.")
            ]
        )