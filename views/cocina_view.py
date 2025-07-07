import flet as ft
import database as db

class CocinaView(ft.Column):
    def __init__(self):
        super().__init__(expand=True, spacing=20)
        self.tables_data = []
        self.selected_order = None
        self.selected_order_container = None

        # Controles principales
        self.orders_grid = ft.GridView(
            max_extent=200,
            child_aspect_ratio=0.8,
            spacing=10,
            run_spacing=10,
            expand=True,
        )

        self.order_detail_title = ft.Text("Seleccione un pedido para ver detalles", size=20, weight=ft.FontWeight.BOLD)
        self.order_items_list = ft.Column(spacing=5, scroll=ft.ScrollMode.AUTO)
        self.order_total = ft.Text("Total: $0.00", weight=ft.FontWeight.BOLD, size=16)
        
        # Botones de acción
        self.mark_ready_button = ft.ElevatedButton(
            "Marcar como Listo",
            icon=ft.Icons.DONE_ALL,
            on_click=self.mark_order_ready,
            style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_400, color=ft.Colors.WHITE),
            disabled=True
        )
        
        self.mark_preparing_button = ft.ElevatedButton(
            "Marcar En Preparación",
            icon=ft.Icons.RESTAURANT,
            on_click=self.mark_order_preparing,
            style=ft.ButtonStyle(bgcolor=ft.Colors.ORANGE_400, color=ft.Colors.WHITE),
            disabled=True
        )

        # Panel de detalles del pedido
        self.order_detail_panel = ft.Container(
            content=ft.Column([
                self.order_detail_title,
                ft.Divider(),
                ft.Text("Items del Pedido:", weight=ft.FontWeight.BOLD, size=16),
                ft.Container(
                    content=self.order_items_list,
                    border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
                    border_radius=8,
                    padding=10,
                    height=200,
                    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST
                ),
                self.order_total,
                ft.Divider(),
                ft.Row([
                    self.mark_preparing_button,
                    self.mark_ready_button
                ], alignment=ft.MainAxisAlignment.SPACE_AROUND)
            ], spacing=15),
            padding=15,
            border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
            border_radius=8,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST
        )

        # Controles de estadísticas
        self.stats_pending = ft.Text("Pedidos pendientes: 0", size=16, weight=ft.FontWeight.BOLD)
        self.stats_preparing = ft.Text("En preparación: 0", size=16, weight=ft.FontWeight.BOLD)
        self.stats_ready = ft.Text("Listos: 0", size=16, weight=ft.FontWeight.BOLD)

        # Estructura principal
        self.controls.extend([
            ft.Container(
                content=ft.Row([
                    # Columna izquierda - Pedidos
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Pedidos Activos", size=24, weight=ft.FontWeight.BOLD),
                            ft.Container(
                                content=self.orders_grid,
                                expand=True,
                                border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
                                border_radius=8,
                                padding=10
                            )
                        ], spacing=10),
                        expand=2
                    ),

                    ft.VerticalDivider(),

                    # Columna derecha - Estadísticas
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Estadísticas", size=24, weight=ft.FontWeight.BOLD),
                            ft.Container(
                                content=ft.Column([
                                    self.stats_pending,
                                    self.stats_preparing,
                                    self.stats_ready,
                                    ft.Divider(),
                                    ft.ElevatedButton(
                                        "Actualizar Pedidos",
                                        icon=ft.Icons.REFRESH,
                                        on_click=self.refresh_orders,
                                        style=ft.ButtonStyle(
                                            bgcolor=ft.Colors.BLUE_400,
                                            color=ft.Colors.WHITE
                                        )
                                    )
                                ], spacing=15),
                                padding=15,
                                border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
                                border_radius=8,
                                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST
                            )
                        ], spacing=15),
                        expand=1
                    )
                ], expand=True, spacing=20),
                expand=True
            ),

            ft.Divider(height=10, color=ft.Colors.GREY_300),

            # Panel de detalles del pedido
            ft.Container(
                content=self.order_detail_panel,
                height=350,
                padding=15,
                border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
                border_radius=8,
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST
            )
        ])

        self.did_mount = self.on_did_mount

    def on_did_mount(self):
        if db.IS_FIREBASE_INITIALIZED:
            self.load_orders_from_db()
        else:
            self.orders_grid.controls.append(
                ft.Text("Error: No se pudo conectar a Firebase.", color=ft.Colors.RED)
            )
            self.update()

    def load_orders_from_db(self):
        """Carga los pedidos desde la base de datos"""
        self.tables_data = db.get_all_tables()
        self.update_orders_grid()
        self.update_stats()
        self.update()

    def update_orders_grid(self):
        """Actualiza la grilla de pedidos"""
        self.orders_grid.controls.clear()
        
        for table_data in self.tables_data:
            order = table_data.get("order", [])
            if not order:  # Solo mostrar mesas con pedidos
                continue
            
            # Determinar estado del pedido
            cooking_status = table_data.get("cooking_status", "pending")
            client_name = table_data.get("client_name", "Sin nombre")
            people_count = table_data.get("people", 0)
            
            # Colores según el estado de cocina
            if cooking_status == "ready":
                bgcolor = ft.Colors.GREEN_300
                icon_color = ft.Colors.GREEN_900
                status_text = "LISTO"
            elif cooking_status == "preparing":
                bgcolor = ft.Colors.ORANGE_300
                icon_color = ft.Colors.ORANGE_900
                status_text = "PREPARANDO"
            else:  # pending
                bgcolor = ft.Colors.RED_300
                icon_color = ft.Colors.RED_900
                status_text = "PENDIENTE"
            
            # Calcular total y cantidad de items
            total = sum(item["price"] for item in order)
            item_count = len(order)
            
            # Crear tarjeta del pedido
            card = ft.Container(
                data=table_data,
                width=190,
                height=240,
                bgcolor=bgcolor,
                border_radius=10,
                ink=True,
                on_click=self.order_clicked,
                padding=10,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row([
                            ft.Icon(ft.Icons.RESTAURANT_MENU, color=icon_color),
                            ft.Text(f"Mesa {table_data['id']}", weight=ft.FontWeight.BOLD),
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Text(f"Cliente: {client_name}", size=12, text_align=ft.TextAlign.CENTER),
                        ft.Text(f"Personas: {people_count}", size=12),
                        ft.Text(f"Items: {item_count}", size=12),
                        ft.Text(f"Total: ${total:.2f}", size=14, weight=ft.FontWeight.BOLD),
                        ft.Container(
                            content=ft.Text(status_text, weight=ft.FontWeight.BOLD, size=12),
                            padding=5,
                            bgcolor=ft.Colors.WHITE,
                            border_radius=5
                        )
                    ]
                )
            )
            self.orders_grid.controls.append(card)
        
        self.update()

    def update_stats(self):
        """Actualiza las estadísticas de pedidos"""
        pending = 0
        preparing = 0
        ready = 0
        
        for table_data in self.tables_data:
            order = table_data.get("order", [])
            if not order:
                continue
            
            cooking_status = table_data.get("cooking_status", "pending")
            if cooking_status == "ready":
                ready += 1
            elif cooking_status == "preparing":
                preparing += 1
            else:
                pending += 1
        
        self.stats_pending.value = f"Pedidos pendientes: {pending}"
        self.stats_preparing.value = f"En preparación: {preparing}"
        self.stats_ready.value = f"Listos: {ready}"

    def order_clicked(self, e: ft.ContainerTapEvent):
        """Maneja el clic en un pedido"""
        self.selected_order = e.control.data
        
        # Actualizar borde visual
        if self.selected_order_container:
            self.selected_order_container.border = None
        self.selected_order_container = e.control
        self.selected_order_container.border = ft.border.all(3, ft.Colors.BLUE_500)
        
        # Actualizar panel de detalles
        self.update_order_detail_panel()
        self.update()

    def update_order_detail_panel(self):
        """Actualiza el panel de detalles del pedido seleccionado"""
        if not self.selected_order:
            return
        
        table_id = self.selected_order['id']
        client_name = self.selected_order.get('client_name', 'Sin nombre')
        people_count = self.selected_order.get('people', 0)
        cooking_status = self.selected_order.get('cooking_status', 'pending')
        
        # Actualizar título
        self.order_detail_title.value = f"Mesa {table_id} - {client_name} ({people_count} personas)"
        
        # Actualizar lista de items
        self.order_items_list.controls.clear()
        total = 0
        
        for item in self.selected_order.get("order", []):
            item_row = ft.Row([
                ft.Text(f"• {item['name']}", expand=True),
                ft.Text(f"${item['price']:.2f}", weight=ft.FontWeight.BOLD),
            ])
            self.order_items_list.controls.append(item_row)
            total += item['price']
        
        self.order_total.value = f"Total: ${total:.2f}"
        
        # Habilitar/deshabilitar botones según el estado
        if cooking_status == "ready":
            self.mark_preparing_button.disabled = False
            self.mark_ready_button.disabled = True
        elif cooking_status == "preparing":
            self.mark_preparing_button.disabled = True
            self.mark_ready_button.disabled = False
        else:  # pending
            self.mark_preparing_button.disabled = False
            self.mark_ready_button.disabled = False
        
        self.update()

    def mark_order_preparing(self, e):
        """Marca el pedido como en preparación"""
        if not self.selected_order:
            return
        
        self.selected_order['cooking_status'] = 'preparing'
        db.update_table(self.selected_order)
        self.load_orders_from_db()
        self.update_order_detail_panel()

    def mark_order_ready(self, e):
        """Marca el pedido como listo"""
        if not self.selected_order:
            return
        
        self.selected_order['cooking_status'] = 'ready'
        db.update_table(self.selected_order)
        self.load_orders_from_db()
        self.update_order_detail_panel()

    def refresh_orders(self, e):
        """Actualiza manualmente los pedidos"""
        self.load_orders_from_db()