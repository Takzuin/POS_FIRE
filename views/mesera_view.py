import flet as ft
import database as db

class MeseraView(ft.Column):
    def __init__(self):
        super().__init__(expand=True, spacing=20)
        self.selected_table_container = None
        self.selected_table_data = None
        self.tables_data = []
        self.menu_data = {}

        # Inicializa los controles
        self.tables_grid = ft.GridView(
            max_extent=150,
            child_aspect_ratio=1.0,
            spacing=10,
            run_spacing=10,
            expand=True,
        )

        self.order_title = ft.Text("Seleccione una mesa para gestionar", size=20, weight=ft.FontWeight.BOLD)
        
        # Controles para asignar cliente
        self.client_name_input = ft.TextField(label="Nombre del Cliente", width=200)
        self.group_size_dropdown = ft.Dropdown(label="Tamaño del Grupo", options=[], width=150)
        self.assign_client_button = ft.ElevatedButton(
            "Asignar Cliente", 
            icon=ft.Icons.PERSON_ADD, 
            on_click=self.assign_client,
            style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_400, color=ft.Colors.WHITE)
        )
        self.free_table_button = ft.ElevatedButton(
            "Liberar Mesa", 
            icon=ft.Icons.CLEAR, 
            on_click=self.free_table,
            style=ft.ButtonStyle(bgcolor=ft.Colors.RED_400, color=ft.Colors.WHITE)
        )
        
        # Controles para pedido
        self.category_dropdown = ft.Dropdown(label="Categoría", options=[], on_change=self.update_item_dropdown, width=200)
        self.item_dropdown = ft.Dropdown(label="Item", options=[], width=250)
        self.order_list = ft.Column(spacing=5, scroll=ft.ScrollMode.AUTO)
        self.order_total = ft.Text("Total: $0.00", weight=ft.FontWeight.BOLD, size=16)

        self.order_panel = ft.Column(
            disabled=True,
            spacing=15,
            controls=[
                self.order_title,
                
                # Sección de asignación de cliente - COLORES ADAPTATIVOS
                ft.Container(
                    content=ft.Column([
                        ft.Text("Asignación de Cliente:", weight=ft.FontWeight.BOLD, size=16),
                        ft.Row([
                            self.client_name_input,
                            self.group_size_dropdown,
                        ]),
                        ft.Row([
                            self.assign_client_button,
                            self.free_table_button
                        ])
                    ], spacing=10),
                    padding=15,
                    border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
                    border_radius=8,
                    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST
                ),
                
                ft.Divider(),
                
                # Sección de pedido - COLORES ADAPTATIVOS
                ft.Container(
                    content=ft.Column([
                        ft.Text("Gestión de Pedido:", weight=ft.FontWeight.BOLD, size=16),
                        ft.Row([self.category_dropdown, self.item_dropdown]),
                        ft.FilledButton("Agregar Item al Pedido", icon=ft.Icons.ADD, on_click=self.add_item_to_order),
                        ft.Text("Resumen del Pedido:", weight=ft.FontWeight.BOLD),
                        ft.Container(
                            content=self.order_list, 
                            border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT), 
                            border_radius=8, 
                            padding=10, 
                            height=150,  # Altura aumentada
                            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST
                        ),
                        self.order_total
                    ], spacing=10),
                    padding=15,
                    border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
                    border_radius=8,
                    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST
                )
            ]
        )

        # Crear los controles de estadísticas como atributos para poder actualizarlos
        self.stats_total = ft.Text(f"Total de mesas: {len(self.tables_data)}", size=16)
        self.stats_occupied = ft.Text(f"Mesas ocupadas: {len([t for t in self.tables_data if t.get('status') == 'occupied'])}", size=16)

        # Estructura mejorada con mejor distribución del espacio
        self.controls.extend([
            ft.Container(
                content=ft.Row([
                    # Columna izquierda - Mesas
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Mesas", size=24, weight=ft.FontWeight.BOLD),
                            ft.Container(
                                content=self.tables_grid,
                                expand=True,
                                border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
                                border_radius=8,
                                padding=10
                            )
                        ], spacing=10),
                        expand=2  # Más espacio para las mesas
                    ),

                    ft.VerticalDivider(),

                    # Columna derecha - Acciones
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Acciones", size=24, weight=ft.FontWeight.BOLD),
                            ft.ElevatedButton(
                                "Agregar Mesa", 
                                icon=ft.Icons.ADD, 
                                on_click=self.add_table,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.GREEN_400,
                                    color=ft.Colors.WHITE
                                )
                            ),
                            ft.ElevatedButton(
                                "Eliminar Última Mesa", 
                                icon=ft.Icons.DELETE, 
                                on_click=self.remove_last_table,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.RED_400,
                                    color=ft.Colors.WHITE
                                )
                            ),
                            ft.Divider(),
                            self.stats_total,
                            self.stats_occupied,
                        ], 
                        expand=1, 
                        spacing=15, 
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    )
                ], expand=True, spacing=20),
                expand=True
            ),
            
            ft.Divider(height=10, color=ft.Colors.GREY_300),
            
            # Panel de pedidos con altura AUMENTADA y colores adaptativos
            ft.Container(
                content=self.order_panel,
                height=400,  # Altura aumentada de 300 a 400
                padding=15,
                border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
                border_radius=8,
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST  # Color adaptativo
            )
        ])

        self.did_mount = self.on_did_mount

    def on_did_mount(self):
        if db.IS_FIREBASE_INITIALIZED:
            self.load_data_from_db()
        else:
            self.tables_grid.controls.append(ft.Text("Error: No se pudo conectar a Firebase.", color=ft.Colors.RED))
            self.update()

    def load_data_from_db(self):
        self.tables_data = db.get_all_tables()
        self.menu_data = db.get_menu()

        self.update_tables_grid()
        self.category_dropdown.options = [ft.dropdown.Option(cat) for cat in self.menu_data.keys()]
        
        # Actualizar las opciones del dropdown de tamaño de grupo basado en la capacidad máxima
        max_capacity = max([t.get('capacity', 4) for t in self.tables_data]) if self.tables_data else 4
        self.group_size_dropdown.options = [ft.dropdown.Option(str(i)) for i in range(1, max_capacity + 1)]
        
        self.update_stats()
        self.update()

    def update_tables_grid(self):
        self.tables_grid.controls.clear()
        for table_data in self.tables_data:
            is_occupied = table_data["status"] == "occupied"
            client_name = table_data.get("client_name", "")
            people_count = table_data.get("people", 0)
            
            # Colores según el estado
            if is_occupied:
                bgcolor = ft.Colors.RED_300
                icon_color = ft.Colors.RED_900
                status_text = "Ocupada"
            else:
                bgcolor = ft.Colors.GREEN_300
                icon_color = ft.Colors.GREEN_900
                status_text = "Libre"
            
            # Información a mostrar
            info_text = f"Cliente: {client_name}" if client_name else "Sin cliente"
            people_text = f"Personas: {people_count}" if people_count > 0 else f"Cap: {table_data['capacity']}"
            
            card = ft.Container(
                data=table_data,
                width=140,
                height=140,
                bgcolor=bgcolor,
                border_radius=10,
                ink=True,
                on_click=self.table_clicked,
                padding=10,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row([
                            ft.Icon(ft.Icons.TABLE_RESTAURANT, color=icon_color),
                            ft.Text(f"Mesa {table_data['id']}", weight=ft.FontWeight.BOLD),
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Text(people_text, size=12),
                        ft.Text(info_text, size=10, text_align=ft.TextAlign.CENTER),
                        ft.Text(status_text, weight=ft.FontWeight.W_500, size=12),
                    ]
                )
            )
            self.tables_grid.controls.append(card)
        self.update()

    def update_stats(self):
        """Actualiza las estadísticas mostradas en el panel de acciones"""
        total_mesas = len(self.tables_data)
        mesas_ocupadas = len([t for t in self.tables_data if t.get('status') == 'occupied'])
        
        # Actualizar los controles de estadísticas
        self.stats_total.value = f"Total de mesas: {total_mesas}"
        self.stats_occupied.value = f"Mesas ocupadas: {mesas_ocupadas}"

    def table_clicked(self, e: ft.ContainerTapEvent):
        self.selected_table_data = e.control.data
        if self.selected_table_container:
            self.selected_table_container.border = None
        self.selected_table_container = e.control
        self.selected_table_container.border = ft.border.all(3, ft.Colors.BLUE_500)
        self.order_panel.disabled = False
        self.update_order_panel()
        self.update()

    def update_order_panel(self):
        if not self.selected_table_data:
            return
            
        table_id = self.selected_table_data['id']
        is_occupied = self.selected_table_data['status'] == 'occupied'
        client_name = self.selected_table_data.get('client_name', '')
        people_count = self.selected_table_data.get('people', 0)
        capacity = self.selected_table_data.get('capacity', 4)
        
        # Actualizar título
        self.order_title.value = f"Mesa {table_id} - Capacidad: {capacity} personas"
        
        # Actualizar campos de cliente
        self.client_name_input.value = client_name
        self.group_size_dropdown.value = str(people_count) if people_count > 0 else ""
        
        # Habilitar/deshabilitar botones según el estado
        self.assign_client_button.disabled = is_occupied
        self.free_table_button.disabled = not is_occupied
        
        # Actualizar la lista de pedidos
        self.order_list.controls.clear()
        total = 0
        for item in self.selected_table_data.get("order", []):
            item_row = ft.Row([
                ft.Text(f"- {item['name']}", expand=True),
                ft.Text(f"${item['price']:.2f}", weight=ft.FontWeight.BOLD),
                ft.IconButton(
                    ft.Icons.DELETE,
                    icon_size=16,
                    on_click=lambda e, item_to_remove=item: self.remove_item_from_order(item_to_remove),
                    tooltip="Eliminar item"
                )
            ])
            self.order_list.controls.append(item_row)
            total += item['price']
        
        self.order_total.value = f"Total: ${total:.2f}"
        
        # Habilitar/deshabilitar sección de pedidos
        self.category_dropdown.disabled = not is_occupied
        self.item_dropdown.disabled = not is_occupied
        
        self.update()

    def remove_item_from_order(self, item_to_remove):
        """Elimina un item del pedido"""
        if not self.selected_table_data:
            return
        
        order = self.selected_table_data.get("order", [])
        if item_to_remove in order:
            order.remove(item_to_remove)
            db.update_table(self.selected_table_data)
            self.update_order_panel()

    def assign_client(self, e):
        """Asigna un cliente a la mesa seleccionada"""
        if not self.selected_table_data or not self.client_name_input.value or not self.group_size_dropdown.value:
            return
        
        # Verificar que el grupo no exceda la capacidad
        group_size = int(self.group_size_dropdown.value)
        capacity = self.selected_table_data.get('capacity', 4)
        
        if group_size > capacity:
            # Aquí podrías mostrar un mensaje de error si tuvieras un sistema de diálogos
            return
        
        # Actualizar datos de la mesa
        self.selected_table_data['status'] = 'occupied'
        self.selected_table_data['client_name'] = self.client_name_input.value
        self.selected_table_data['people'] = group_size
        
        # Guardar en la base de datos
        db.update_table(self.selected_table_data)
        
        # Actualizar vistas
        self.update_order_panel()
        self.update_tables_grid()
        self.update_stats()

    def free_table(self, e):
        """Libera la mesa seleccionada"""
        if not self.selected_table_data:
            return
        
        # Limpiar datos de la mesa
        self.selected_table_data['status'] = 'free'
        self.selected_table_data['client_name'] = ''
        self.selected_table_data['people'] = 0
        self.selected_table_data['order'] = []
        
        # Guardar en la base de datos
        db.update_table(self.selected_table_data)
        
        # Actualizar vistas
        self.update_order_panel()
        self.update_tables_grid()
        self.update_stats()

    def update_item_dropdown(self, e):
        category = self.category_dropdown.value
        self.item_dropdown.options = [
            ft.dropdown.Option(item["name"]) for item in self.menu_data.get(category, [])
        ]
        self.item_dropdown.value = None
        self.update()

    def add_item_to_order(self, e):
        if not self.selected_table_data or not self.item_dropdown.value or self.selected_table_data['status'] != 'occupied':
            return
        
        category = self.category_dropdown.value
        item_name = self.item_dropdown.value
        item_info = next((item for item in self.menu_data[category] if item["name"] == item_name), None)
        
        if item_info:
            self.selected_table_data.setdefault("order", []).append(item_info)
            db.update_table(self.selected_table_data)
            self.update_order_panel()
            
            # Limpiar selección
            self.item_dropdown.value = None
            self.update()

    def add_table(self, e):
        new_id = max(t["id"] for t in self.tables_data) + 1 if self.tables_data else 1
        new_table_data = {"id": new_id, "capacity": 4, "status": "free", "order": [], "people": 0, "client_name": ""}
        db.update_table(new_table_data)
        self.tables_data.append(new_table_data)
        self.update_tables_grid()
        self.update_stats()

    def remove_last_table(self, e):
        if self.tables_data:
            last_table = self.tables_data.pop()
            db.delete_table(last_table["id"])
            self.update_tables_grid()
            self.update_stats()
            
            # Si la mesa eliminada era la seleccionada, limpiar selección
            if self.selected_table_data and self.selected_table_data["id"] == last_table["id"]:
                self.selected_table_data = None
                self.selected_table_container = None
                self.order_panel.disabled = True
                self.order_title.value = "Seleccione una mesa para gestionar"
                self.client_name_input.value = ""
                self.group_size_dropdown.value = ""
                self.order_list.controls.clear()
                self.order_total.value = "Total: $0.00"
                self.update()