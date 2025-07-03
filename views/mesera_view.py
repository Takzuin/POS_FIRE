import flet as ft
import database as db  # Importamos nuestro paquete de base de datos

class MeseraView(ft.Column):
    def __init__(self):
        super().__init__(expand=True, spacing=20)
        self.selected_table_container = None
        self.selected_table_data = None
        
        # --- DATOS (Ahora desde Firebase) ---
        self.tables_data = []
        self.menu_data = {}
        # --- FIN DE DATOS ---

        # El método 'did_mount' se llama cuando el control se agrega a la página
        self.did_mount = self.on_did_mount
        # Construimos la interfaz
        self.controls = self.build()

    def on_did_mount(self):
        """Se llama después de que el control se agrega a la página. Ideal para cargar datos iniciales."""
        if db.IS_FIREBASE_INITIALIZED:
            self.load_data_from_db()
        else:
            # Muestra un error si Firebase no se pudo inicializar
            self.tables_grid.controls.append(ft.Text("Error: No se pudo conectar a Firebase.", color=ft.colors.RED))
            self.update()

    def load_data_from_db(self):
        """Carga los datos de mesas y menú desde Firebase y actualiza la UI."""
        self.tables_data = db.get_all_tables()
        self.menu_data = db.get_menu()
        
        self.update_tables_grid()
        self.category_dropdown.options = [ft.dropdown.Option(cat) for cat in self.menu_data.keys()]
        self.update()

    def update_tables_grid(self):
        """Recarga la cuadrícula de mesas a partir de self.tables_data."""
        self.tables_grid.controls.clear()
        for table_data in self.tables_data:
            is_occupied = table_data["status"] == "occupied"
            table_card = ft.Container(
                data=table_data,
                width=140,
                height=140,
                bgcolor=ft.Colors.RED_200 if is_occupied else ft.Colors.GREEN_200,
                border_radius=10,
                ink=True,
                on_click=self.table_clicked,
                padding=10,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row([
                            ft.Icon(ft.Icons.TABLE_RESTAURANT),
                            ft.Text(f"Mesa {table_data['id']}", weight=ft.FontWeight.BOLD),
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Text(f"Capacidad: {table_data['capacity']}"),
                        ft.Text(f"Estado: {table_data['status'].capitalize()}", weight=ft.FontWeight.W_500),
                    ]
                )
            )
            self.tables_grid.controls.append(table_card)
        self.update()

    def table_clicked(self, e: ft.ContainerTapEvent):
        """Maneja el clic en una mesa."""
        self.selected_table_data = e.control.data

        # Resetea el borde de la mesa anteriormente seleccionada
        if self.selected_table_container:
            self.selected_table_container.border = None

        # Pone un borde a la mesa seleccionada actualmente
        self.selected_table_container = e.control
        self.selected_table_container.border = ft.border.all(3, ft.colors.BLUE_500)

        # Habilita y actualiza el panel de pedidos
        self.order_panel.disabled = False
        self.update_order_panel()
        self.update()

    def update_order_panel(self):
        """Actualiza el panel inferior con los datos de la mesa seleccionada."""
        if not self.selected_table_data:
            return

        table_id = self.selected_table_data['id']
        self.order_title.value = f"Pedido - Mesa {table_id}"
        self.people_input.value = str(self.selected_table_data.get("people", 0))
        
        self.order_list.controls.clear()
        total = 0
        # Usamos .get("order", []) para manejar casos donde una mesa aún no tiene pedidos.
        for item in self.selected_table_data.get("order", []):
            self.order_list.controls.append(ft.Text(f"- {item['name']} (${item['price']:.2f})"))
            total += item['price']
        
        self.order_total.value = f"Total: ${total:.2f}"
        self.update()

    def update_item_dropdown(self, e):
        """Actualiza las opciones del dropdown de items según la categoría."""
        category = self.category_dropdown.value
        self.item_dropdown.options = [
            ft.dropdown.Option(item["name"]) for item in self.menu_data.get(category, [])
        ]
        self.item_dropdown.value = None
        self.update()

    def add_item_to_order(self, e):
        """Agrega un item al pedido de la mesa seleccionada y lo guarda en la DB."""
        if not self.selected_table_data or not self.item_dropdown.value:
            return

        category = self.category_dropdown.value
        item_name = self.item_dropdown.value
        
        # Encontrar el item en los datos del menú para obtener el precio
        item_info = next((item for item in self.menu_data[category] if item["name"] == item_name), None)
        
        if item_info:
            # Usamos setdefault para crear la lista 'order' si no existe
            self.selected_table_data.setdefault("order", []).append(item_info)
            self.selected_table_data["status"] = "occupied"
            self.selected_table_data["people"] = int(self.people_input.value) if self.people_input.value.isdigit() else 0
            
            # Actualiza la base de datos
            db.update_table(self.selected_table_data)

            # Actualiza la UI localmente para reflejar el cambio al instante
            self.update_order_panel()
            self.update_tables_grid() # Para que cambie el color si estaba libre

    def add_table(self, e):
        """Agrega una nueva mesa a la DB."""
        new_id = max(t["id"] for t in self.tables_data) + 1 if self.tables_data else 1
        new_table_data = {"id": new_id, "capacity": 4, "status": "free", "order": [], "people": 0}
        
        # Guarda la nueva mesa en Firebase
        db.update_table(new_table_data)
        
        # Actualiza la UI local
        self.tables_data.append(new_table_data)
        self.update_tables_grid()

    def remove_last_table(self, e):
        """Elimina la última mesa de la DB."""
        if self.tables_data:
            last_table = self.tables_data.pop()
            db.delete_table(last_table['id'])
            
            # Actualiza la UI local
            self.update_tables_grid()

    def build(self):
        # --- Controles de la Interfaz ---
        self.tables_grid = ft.GridView(
            expand=True,
            max_extent=150,
            child_aspect_ratio=1.0,
            spacing=10,
            run_spacing=10,
        )

        # Panel de Pedidos (inicialmente deshabilitado)
        self.order_title = ft.Text("Seleccione una mesa para ver el pedido", size=20, weight=ft.FontWeight.BOLD)
        self.people_input = ft.TextField(label="Personas en la mesa", width=180, keyboard_type=ft.KeyboardType.NUMBER)
        self.category_dropdown = ft.Dropdown(
            label="Categoría",
            # Las opciones se cargarán desde la DB en on_did_mount
            options=[],
            on_change=self.update_item_dropdown,
            width=200
        )
        self.item_dropdown = ft.Dropdown(label="Item", options=[], width=250)
        self.order_list = ft.Column(spacing=5)
        self.order_total = ft.Text("Total: $0.00", weight=ft.FontWeight.BOLD, size=16)

        self.order_panel = ft.Column(
            disabled=True,
            spacing=15,
            controls=[
                self.order_title,
                ft.Row([self.people_input, self.category_dropdown, self.item_dropdown]),
                ft.FilledButton("Agregar Item al Pedido", icon=ft.Icons.ADD, on_click=self.add_item_to_order),
                ft.Text("Pedido Actual:", weight=ft.FontWeight.BOLD),
                ft.Container(content=self.order_list, border=ft.border.all(1, ft.Colors.OUTLINE), border_radius=5, padding=10, height=150),
                self.order_total
            ]
        )

        # --- Estructura Principal de la Vista ---
        return [
            ft.Row(
                [
                    # Columna de Mesas
                    ft.Column([
                        ft.Text("Mesas", size=24, weight=ft.FontWeight.BOLD),
                        self.tables_grid
                    ], expand=4),
                    
                    ft.VerticalDivider(),

                    # Columna de Acciones
                    ft.Column([
                        ft.Text("Acciones", size=24, weight=ft.FontWeight.BOLD),
                        ft.ElevatedButton("Agregar Mesa", icon=ft.Icons.ADD, on_click=self.add_table),
                        ft.ElevatedButton("Eliminar Última Mesa", icon=ft.Icons.DELETE, on_click=self.remove_last_table, color=ft.Colors.RED),
                    ], expand=1, spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                ],
                expand=True,
                spacing=20
            ),
            ft.Divider(height=10, color=ft.Colors.GREY_300),
            self.order_panel
        ]