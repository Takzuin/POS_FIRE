import flet as ft
import database as db

class CajaView(ft.Container):
    def __init__(self):
        super().__init__(padding=20, expand=True)
        self.tables_data = []
        self.did_mount = self.on_did_mount
        self.order_list_column = ft.Column(spacing=15, scroll=ft.ScrollMode.AUTO)
        self.content = ft.Column(
            controls=[
                ft.Text("Módulo Caja", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Lista de pedidos por mesa para facturar y finalizar."),
                ft.Divider(),
                self.order_list_column
            ],
            spacing=15,
            expand=True
        )

    def on_did_mount(self):
        if db.IS_FIREBASE_INITIALIZED:
            self.load_tables()
        else:
            self.content.controls.append(
                ft.Text("No se pudo conectar a Firebase.", color=ft.colors.RED)
            )
            self.update()

    def load_tables(self):
        self.tables_data = db.get_all_tables()
        self.render_orders()

    def render_orders(self):
        self.order_list_column.controls.clear()
        for table in self.tables_data:
            order = table.get("order", [])
            if not order:
                continue  # Solo mostrar mesas con pedidos

            total = sum(item["price"] for item in order)
            order_items = "\n".join(f"- {item['name']} (${item['price']:.2f})" for item in order)

            card = ft.Card(
                content=ft.Container(
                    padding=15,
                    content=ft.Column([
                        ft.Text(f"Mesa {table['id']} - Total: ${total:.2f}", weight=ft.FontWeight.BOLD, size=18),
                        ft.Text(order_items),
                        ft.Row([
                            ft.ElevatedButton(
                                text="Finalizar Pedido",
                                icon=ft.Icons.CHECK,
                                on_click=lambda e, t=table: self.finalizar_pedido(t),
                                bgcolor=ft.Colors.GREEN_400,
                                color=ft.Colors.WHITE
                            )
                        ], alignment=ft.MainAxisAlignment.END)
                    ])
                )
            )
            self.order_list_column.controls.append(card)
        self.update()

    def finalizar_pedido(self, table_data):
        """Marca la mesa como libre y limpia su pedido."""
        table_data["order"] = []
        table_data["status"] = "free"
        table_data["people"] = 0
        db.update_table(table_data)
        self.load_tables()  # Recarga la vista
