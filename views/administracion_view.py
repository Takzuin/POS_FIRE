import flet as ft
import database as db
from datetime import datetime

class AdministracionView(ft.Column):
    def __init__(self):
        super().__init__(expand=True, spacing=20)
        self.menu_data = {}
        self.tables_data = []
        self.selected_menu_item = None
        self.selected_category = None
        # Crear las pestañas principales
        self.admin_tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            expand=True,
            tabs=[
                ft.Tab(
                    text="Gestión de Menú",
                    icon=ft.Icons.RESTAURANT_MENU,
                    content=self.create_menu_management_tab()
                ),
                ft.Tab(
                    text="Configuración de Mesas",
                    icon=ft.Icons.TABLE_RESTAURANT,
                    content=self.create_table_management_tab()
                ),
                ft.Tab(
                    text="Reportes",
                    icon=ft.Icons.ANALYTICS,
                    content=self.create_reports_tab()
                ),
                ft.Tab(
                    text="Configuración",
                    icon=ft.Icons.SETTINGS,
                    content=self.create_settings_tab()
                )
            ]
        )
        # Estructura principal
        self.controls.extend([
            ft.Container(
                content=ft.Column([
                    ft.Text("Panel de Administración", size=28, weight=ft.FontWeight.BOLD),
                    ft.Text("Gestione el menú, mesas, reportes y configuración del sistema", size=16),
                    ft.Divider(),
                    self.admin_tabs
                ], spacing=15),
                padding=20,
                expand=True
            )
        ])
        self.did_mount = self.on_did_mount

    def on_did_mount(self):
        if db.IS_FIREBASE_INITIALIZED:
            self.load_data_from_db()
        else:
            self.admin_tabs.tabs[0].content = ft.Text("Error: No se pudo conectar a Firebase.", color=ft.Colors.RED)
            self.update()

    def load_data_from_db(self):
        """Carga todos los datos necesarios desde la base de datos"""
        self.menu_data = db.get_menu()
        self.tables_data = db.get_all_tables()
        # Actualizar todas las vistas
        self.update_menu_categories()
        self.update_table_list()
        self.update_reports()
        self.update()

    def create_menu_management_tab(self):
        """Crea la pestaña de gestión de menú"""
        # Controles para categorías
        self.category_list = ft.ListView(expand=True, spacing=5)
        self.new_category_input = ft.TextField(label="Nueva Categoría", width=200)
        self.add_category_button = ft.ElevatedButton(
            "Agregar Categoría",
            icon=ft.Icons.ADD,
            on_click=self.add_category,
            style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE)
        )
        # Controles para items del menú
        self.menu_items_list = ft.ListView(expand=True, spacing=5)
        self.item_name_input = ft.TextField(label="Nombre del Item", width=200)
        self.item_price_input = ft.TextField(label="Precio", width=100, keyboard_type=ft.KeyboardType.NUMBER)
        self.item_description_input = ft.TextField(label="Descripción", width=300, multiline=True, max_lines=3)
        self.category_for_item_dropdown = ft.Dropdown(label="Categoría", width=200, options=[])
        self.add_item_button = ft.ElevatedButton(
            "Agregar Item",
            icon=ft.Icons.ADD,
            on_click=self.add_menu_item,
            style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_400, color=ft.Colors.WHITE)
        )
        # Controles para edición
        self.edit_item_name = ft.TextField(label="Nombre", width=200)
        self.edit_item_price = ft.TextField(label="Precio", width=100, keyboard_type=ft.KeyboardType.NUMBER)
        self.edit_item_description = ft.TextField(label="Descripción", width=300, multiline=True, max_lines=3)
        self.update_item_button = ft.ElevatedButton(
            "Actualizar Item",
            icon=ft.Icons.UPDATE,
            on_click=self.update_menu_item,
            style=ft.ButtonStyle(bgcolor=ft.Colors.ORANGE_400, color=ft.Colors.WHITE),
            disabled=True
        )
        self.delete_item_button = ft.ElevatedButton(
            "Eliminar Item",
            icon=ft.Icons.DELETE,
            on_click=self.delete_menu_item,
            style=ft.ButtonStyle(bgcolor=ft.Colors.RED_400, color=ft.Colors.WHITE),
            disabled=True
        )
        return ft.Container(
            content=ft.Row([
                # Columna izquierda - Categorías
                ft.Container(
                    content=ft.Column([
                        ft.Text("Categorías", size=20, weight=ft.FontWeight.BOLD),
                        ft.Container(
                            content=self.category_list,
                            height=300,
                            border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
                            border_radius=8,
                            padding=10,
                            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST
                        ),
                        ft.Row([
                            self.new_category_input,
                            self.add_category_button
                        ])
                    ], spacing=10),
                    expand=1
                ),
                ft.VerticalDivider(),
                # Columna central - Items del menú
                ft.Container(
                    content=ft.Column([
                        ft.Text("Items del Menú", size=20, weight=ft.FontWeight.BOLD),
                        ft.Container(
                            content=self.menu_items_list,
                            height=300,
                            border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
                            border_radius=8,
                            padding=10,
                            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST
                        ),
                        ft.Text("Agregar Nuevo Item:", weight=ft.FontWeight.BOLD),
                        ft.Row([
                            self.item_name_input,
                            self.item_price_input,
                            self.category_for_item_dropdown
                        ]),
                        self.item_description_input,
                        self.add_item_button
                    ], spacing=10),
                    expand=2
                ),
                ft.VerticalDivider(),
                # Columna derecha - Edición
                ft.Container(
                    content=ft.Column([
                        ft.Text("Editar Item Seleccionado", size=20, weight=ft.FontWeight.BOLD),
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Seleccione un item para editar", size=14),
                                ft.Divider(),
                                self.edit_item_name,
                                self.edit_item_price,
                                self.edit_item_description,
                                ft.Row([
                                    self.update_item_button,
                                    self.delete_item_button
                                ])
                            ], spacing=10),
                            padding=15,
                            border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
                            border_radius=8,
                            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST
                        )
                    ], spacing=10),
                    expand=1
                )
            ], spacing=20),
            padding=20,
            expand=True
        )

    def create_table_management_tab(self):
        """Crea la pestaña de configuración de mesas"""
        self.table_config_list = ft.ListView(expand=True, spacing=5)
        self.new_table_capacity = ft.TextField(label="Capacidad", width=100, keyboard_type=ft.KeyboardType.NUMBER, value="4")
        self.add_table_config_button = ft.ElevatedButton(
            "Agregar Mesa",
            icon=ft.Icons.ADD,
            on_click=self.add_table_from_config,
            style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_400, color=ft.Colors.WHITE)
        )
        # Controles para configuración masiva
        self.bulk_tables_count = ft.TextField(label="Cantidad de Mesas", width=150, keyboard_type=ft.KeyboardType.NUMBER)
        self.bulk_tables_capacity = ft.TextField(label="Capacidad por Mesa", width=150, keyboard_type=ft.KeyboardType.NUMBER, value="4")
        self.add_bulk_tables_button = ft.ElevatedButton(
            "Agregar Mesas en Lote",
            icon=ft.Icons.ADD_BUSINESS,
            on_click=self.add_bulk_tables,
            style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE)
        )
        return ft.Container(
            content=ft.Column([
                ft.Text("Configuración de Mesas", size=24, weight=ft.FontWeight.BOLD),
                ft.Row([
                    # Columna izquierda - Lista de mesas
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Mesas Actuales", size=18, weight=ft.FontWeight.BOLD),
                            ft.Container(
                                content=self.table_config_list,
                                height=400,
                                border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
                                border_radius=8,
                                padding=10,
                                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST
                            )
                        ], spacing=10),
                        expand=2
                    ),
                    ft.VerticalDivider(),
                    # Columna derecha - Configuración
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Gestión de Mesas", size=18, weight=ft.FontWeight.BOLD),
                            # Agregar mesa individual
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Agregar Mesa Individual:", weight=ft.FontWeight.BOLD),
                                    ft.Row([
                                        self.new_table_capacity,
                                        self.add_table_config_button
                                    ])
                                ], spacing=10),
                                padding=15,
                                border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
                                border_radius=8,
                                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST
                            ),
                            # Agregar mesas en lote
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Agregar Mesas en Lote:", weight=ft.FontWeight.BOLD),
                                    self.bulk_tables_count,
                                    self.bulk_tables_capacity,
                                    self.add_bulk_tables_button
                                ], spacing=10),
                                padding=15,
                                border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
                                border_radius=8,
                                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST
                            ),
                            # Acciones generales
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Acciones Generales:", weight=ft.FontWeight.BOLD),
                                    ft.ElevatedButton(
                                        "Liberar Todas las Mesas",
                                        icon=ft.Icons.CLEAR_ALL,
                                        on_click=self.free_all_tables,
                                        style=ft.ButtonStyle(bgcolor=ft.Colors.ORANGE_400, color=ft.Colors.WHITE)
                                    ),
                                    ft.ElevatedButton(
                                        "Eliminar Todas las Mesas Libres",
                                        icon=ft.Icons.DELETE_SWEEP,
                                        on_click=self.delete_all_free_tables,
                                        style=ft.ButtonStyle(bgcolor=ft.Colors.RED_400, color=ft.Colors.WHITE)
                                    )
                                ], spacing=10),
                                padding=15,
                                border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
                                border_radius=8,
                                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST
                            )
                        ], spacing=15),
                        expand=1
                    )
                ], spacing=20)
            ], spacing=15),
            padding=20,
            expand=True
        )

    def create_reports_tab(self):
        """Crea la pestaña de reportes"""
        self.sales_summary = ft.Text("Resumen de Ventas: Cargando...", size=16)
        self.popular_items = ft.Text("Items Más Populares: Cargando...", size=16)
        self.table_usage = ft.Text("Uso de Mesas: Cargando...", size=16)
        return ft.Container(
            content=ft.Column([
                ft.Text("Reportes y Estadísticas", size=24, weight=ft.FontWeight.BOLD),
                # Resumen general
                ft.Container(
                    content=ft.Column([
                        ft.Text("Resumen General", size=20, weight=ft.FontWeight.BOLD),
                        self.sales_summary,
                        self.popular_items,
                        self.table_usage,
                        ft.ElevatedButton(
                            "Actualizar Reportes",
                            icon=ft.Icons.REFRESH,
                            on_click=self.update_reports,
                            style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE)
                        )
                    ], spacing=10),
                    padding=20,
                    border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
                    border_radius=8,
                    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST
                ),
                # Estadísticas en tiempo real
                ft.Container(
                    content=ft.Column([
                        ft.Text("Estado Actual del Sistema", size=20, weight=ft.FontWeight.BOLD),
                        ft.Row([
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Mesas", weight=ft.FontWeight.BOLD),
                                    ft.Text("Total: 0", size=14),
                                    ft.Text("Ocupadas: 0", size=14),
                                    ft.Text("Libres: 0", size=14)
                                ], spacing=5),
                                padding=15,
                                border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
                                border_radius=8,
                                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                                expand=1
                            ),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Pedidos", weight=ft.FontWeight.BOLD),
                                    ft.Text("Pendientes: 0", size=14),
                                    ft.Text("En Preparación: 0", size=14),
                                    ft.Text("Listos: 0", size=14)
                                ], spacing=5),
                                padding=15,
                                border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
                                border_radius=8,
                                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                                expand=1
                            ),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Menú", weight=ft.FontWeight.BOLD),
                                    ft.Text("Categorías: 0", size=14),
                                    ft.Text("Items: 0", size=14),
                                    ft.Text("Activos: 0", size=14)
                                ], spacing=5),
                                padding=15,
                                border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
                                border_radius=8,
                                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                                expand=1
                            )
                        ], spacing=15)
                    ], spacing=10),
                    padding=20,
                    border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
                    border_radius=8,
                    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST
                )
            ], spacing=20),
            padding=20,
            expand=True
        )

    def create_settings_tab(self):
        """Crea la pestaña de configuración"""
        return ft.Container(
            content=ft.Column([
                ft.Text("Configuración del Sistema", size=24, weight=ft.FontWeight.BOLD),
                # Configuración general
                ft.Container(
                    content=ft.Column([
                        ft.Text("Configuración General", size=20, weight=ft.FontWeight.BOLD),
                        ft.Row([
                            ft.TextField(label="Nombre del Restaurante", width=300, value="Sistema POS"),
                            ft.TextField(label="Moneda", width=100, value="$")
                        ]),
                        ft.Row([
                            ft.TextField(label="Dirección", width=400),
                            ft.TextField(label="Teléfono", width=200)
                        ]),
                        ft.ElevatedButton(
                            "Guardar Configuración",
                            icon=ft.Icons.SAVE,
                            on_click=self.save_settings,
                            style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_400, color=ft.Colors.WHITE)
                        )
                    ], spacing=10),
                    padding=20,
                    border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
                    border_radius=8,
                    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST
                ),
                # Configuración de la base de datos
                ft.Container(
                    content=ft.Column([
                        ft.Text("Gestión de Datos", size=20, weight=ft.FontWeight.BOLD),
                        ft.Text("Estas acciones afectan toda la información del sistema.", size=12, color=ft.Colors.ORANGE_700),
                        ft.Row([
                            ft.ElevatedButton(
                                "Respaldar Datos",
                                icon=ft.Icons.BACKUP,
                                on_click=self.backup_data,
                                style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE)
                            ),
                            ft.ElevatedButton(
                                "Limpiar Todos los Pedidos",
                                icon=ft.Icons.CLEANING_SERVICES,
                                on_click=self.clear_all_orders,
                                style=ft.ButtonStyle(bgcolor=ft.Colors.ORANGE_400, color=ft.Colors.WHITE)
                            ),
                            ft.ElevatedButton(
                                "Restablecer Sistema",
                                icon=ft.Icons.RESTART_ALT,
                                on_click=self.reset_system,
                                style=ft.ButtonStyle(bgcolor=ft.Colors.RED_400, color=ft.Colors.WHITE)
                            )
                        ])
                    ], spacing=10),
                    padding=20,
                    border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
                    border_radius=8,
                    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST
                ),
                # Información del sistema
                ft.Container(
                    content=ft.Column([
                        ft.Text("Información del Sistema", size=20, weight=ft.FontWeight.BOLD),
                        ft.Text(f"Versión: 1.0.0", size=14),
                        ft.Text(f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", size=14),
                        ft.Text("Estado de la conexión: Conectado", size=14, color=ft.Colors.GREEN_700),
                        ft.Text("Framework: Flet + Firebase", size=14)
                    ], spacing=5),
                    padding=20,
                    border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
                    border_radius=8,
                    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST
                )
            ], spacing=20),
            padding=20,
            expand=True
        )

    # Métodos para gestión de menú
    def update_menu_categories(self):
        """Actualiza la lista de categorías del menú"""
        self.category_list.controls.clear()
        self.category_for_item_dropdown.options.clear()
        for category in self.menu_data.keys():
            # Agregar a la lista visual
            category_item = ft.ListTile(
                title=ft.Text(category, weight=ft.FontWeight.BOLD),
                subtitle=ft.Text(f"{len(self.menu_data[category])} items"),
                leading=ft.Icon(ft.Icons.CATEGORY),
                on_click=lambda e, cat=category: self.select_category(cat),
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST
            )
            self.category_list.controls.append(category_item)
            # Agregar al dropdown
            self.category_for_item_dropdown.options.append(ft.dropdown.Option(category))
        self.update()

    def select_category(self, category):
        """Selecciona una categoría y muestra sus items"""
        self.selected_category = category
        self.update_menu_items_for_category()

    def update_menu_items_for_category(self):
        """Actualiza la lista de items para la categoría seleccionada"""
        if not self.selected_category:
            return
        self.menu_items_list.controls.clear()
        for item in self.menu_data.get(self.selected_category, []):
            item_tile = ft.ListTile(
                title=ft.Text(item["name"], weight=ft.FontWeight.BOLD),
                subtitle=ft.Text(f"${item['price']:.2f} - {item.get('description', 'Sin descripción')}"),
                leading=ft.Icon(ft.Icons.RESTAURANT),
                on_click=lambda e, item_data=item: self.select_menu_item(item_data),
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST
            )
            self.menu_items_list.controls.append(item_tile)
        self.update()

    def select_menu_item(self, item_data):
        """Selecciona un item del menú para editar"""
        self.selected_menu_item = item_data
        # Cargar datos en los campos de edición
        self.edit_item_name.value = item_data["name"]
        self.edit_item_price.value = str(item_data["price"])
        self.edit_item_description.value = item_data.get("description", "")
        # Habilitar botones
        self.update_item_button.disabled = False
        self.delete_item_button.disabled = False
        self.update()

    def add_category(self, e):
        """Agrega una nueva categoría"""
        if not self.new_category_input.value:
            return
        category_name = self.new_category_input.value.strip()
        if category_name not in self.menu_data:
            self.menu_data[category_name] = []
            # Aquí deberías actualizar la base de datos
            # db.update_menu_category(category_name, [])
            self.new_category_input.value = ""
            self.update_menu_categories()

    def add_menu_item(self, e):
        """Agrega un nuevo item al menú"""
        if not all([self.item_name_input.value, self.item_price_input.value, self.category_for_item_dropdown.value]):
            return
        try:
            new_item = {
                "name": self.item_name_input.value.strip(),
                "price": float(self.item_price_input.value),
                "description": self.item_description_input.value.strip() or "Sin descripción"
            }
            category = self.category_for_item_dropdown.value
            if category not in self.menu_data:
                self.menu_data[category] = []
            self.menu_data[category].append(new_item)
            # Limpiar campos
            self.item_name_input.value = ""
            self.item_price_input.value = ""
            self.item_description_input.value = ""
            # Actualizar vista si es la categoría seleccionada
            if self.selected_category == category:
                self.update_menu_items_for_category()
            self.update()
        except ValueError:
            # Manejar error de precio inválido
            pass

    def update_menu_item(self, e):
        """Actualiza el item seleccionado"""
        if not self.selected_menu_item:
            return
        try:
            # Actualizar datos
            self.selected_menu_item["name"] = self.edit_item_name.value.strip()
            self.selected_menu_item["price"] = float(self.edit_item_price.value)
            self.selected_menu_item["description"] = self.edit_item_description.value.strip()
            # Actualizar vista
            self.update_menu_items_for_category()
        except ValueError:
            # Manejar error de precio inválido
            pass

    def delete_menu_item(self, e):
        """Elimina el item seleccionado"""
        if not self.selected_menu_item or not self.selected_category:
            return
        category_items = self.menu_data.get(self.selected_category, [])
        if self.selected_menu_item in category_items:
            category_items.remove(self.selected_menu_item)
            # Limpiar selección
            self.selected_menu_item = None
            self.edit_item_name.value = ""
            self.edit_item_price.value = ""
            self.edit_item_description.value = ""
            self.update_item_button.disabled = True
            self.delete_item_button.disabled = True
            # Actualizar vista
            self.update_menu_items_for_category()

    # Métodos para gestión de mesas
    def update_table_list(self):
        """Actualiza la lista de mesas en configuración"""
        self.table_config_list.controls.clear()
        for table in self.tables_data:
            status_color = ft.Colors.GREEN_700 if table["status"] == "free" else ft.Colors.RED_700
            status_text = "Libre" if table["status"] == "free" else "Ocupada"
            table_tile = ft.ListTile(
                title=ft.Text(f"Mesa {table['id']}", weight=ft.FontWeight.BOLD),
                subtitle=ft.Text(f"Capacidad: {table['capacity']} personas - Estado: {status_text}"),
                leading=ft.Icon(ft.Icons.TABLE_RESTAURANT, color=status_color),
                trailing=ft.IconButton(
                    ft.Icons.DELETE,
                    on_click=lambda e, table_id=table['id']: self.delete_table_config(e, table_id),
                    icon_color=ft.Colors.RED_400
                ),
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST
            )
            self.table_config_list.controls.append(table_tile)
        self.update()

    def add_table_from_config(self, e):
        """Agrega una mesa desde la configuración"""
        if not self.new_table_capacity.value:
            return
        try:
            capacity = int(self.new_table_capacity.value)
            if capacity <= 0:
                return
            new_id = max(t["id"] for t in self.tables_data) + 1 if self.tables_data else 1
            new_table = {
                "id": new_id,
                "capacity": capacity,
                "status": "free",
                "order": [],
                "people": 0,
                "client_name": ""
            }
            db.update_table(new_table)
            self.tables_data.append(new_table)
            self.update_table_list()
        except ValueError:
            pass

    def add_bulk_tables(self, e):
        """Agrega múltiples mesas de una vez"""
        if not self.bulk_tables_count.value or not self.bulk_tables_capacity.value:
            return
        try:
            count = int(self.bulk_tables_count.value)
            capacity = int(self.bulk_tables_capacity.value)
            if count <= 0 or capacity <= 0:
                return
            start_id = max(t["id"] for t in self.tables_data) + 1 if self.tables_data else 1
            for i in range(count):
                new_table = {
                    "id": start_id + i,
                    "capacity": capacity,
                    "status": "free",
                    "order": [],
                    "people": 0,
                    "client_name": ""
                }
                db.update_table(new_table)
                self.tables_data.append(new_table)
            self.bulk_tables_count.value = ""
            self.bulk_tables_capacity.value = "4"
            self.update_table_list()
        except ValueError:
            pass

    def delete_table_config(self, e, table_id):
        """Elimina una mesa desde la configuración"""
        if not table_id:
            return
        # Eliminar de la base de datos
        db.delete_table(table_id)
        # Actualizar la lista local de mesas
        self.tables_data = [table for table in self.tables_data if table['id'] != table_id]
        # Actualizar la vista
        self.update_table_list()

    def free_all_tables(self, e):
        """Libera todas las mesas"""
        for table in self.tables_data:
            if table["status"] == "occupied":
                table["status"] = "free"
                table["order"] = []
                table["people"] = 0
                table["client_name"] = ""
                db.update_table(table)
        self.update_table_list()

    def delete_all_free_tables(self, e):
        """Elimina todas las mesas libres"""
        tables_to_delete = [table for table in self.tables_data if table["status"] == "free"]
        for table in tables_to_delete:
            db.delete_table(table["id"])
        self.tables_data = [table for table in self.tables_data if table["status"] == "occupied"]
        self.update_table_list()

    def update_reports(self, e=None):
        """Actualiza los reportes"""
        # Aquí deberías obtener los datos reales desde la base de datos
        sales_summary = "Ventas totales: $1000.00\nVentas hoy: $500.00"
        popular_items = "Item 1: 50 ventas\nItem 2: 30 ventas"
        table_usage = "Mesas ocupadas: 5/10\nPorcentaje de uso: 50%"
        self.sales_summary.value = f"Resumen de Ventas:\n{sales_summary}"
        self.popular_items.value = f"Items Más Populares:\n{popular_items}"
        self.table_usage.value = f"Uso de Mesas:\n{table_usage}"
        self.update()

    def save_settings(self, e):
        """Guarda la configuración del sistema"""
        # Aquí deberías guardar los datos en la base de datos o en un archivo de configuración
        pass

    def backup_data(self, e):
        """Realiza un respaldo de los datos"""
        # Aquí deberías implementar la lógica de respaldo
        pass

    def clear_all_orders(self, e):
        """Limpia todos los pedidos"""
        for table in self.tables_data:
            table["order"] = []
            db.update_table(table)
        self.update_table_list()

    def reset_system(self, e):
        """Restablece el sistema a su estado inicial"""
        # Aquí deberías implementar la lógica de restablecimiento
        pass