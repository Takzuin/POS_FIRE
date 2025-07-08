import flet as ft
import databasefire as db

def CajaView(page):
    """
    Vista de Caja (POS) que muestra una capa de confirmación superpuesta
    en lugar de un diálogo, para máxima compatibilidad.
    """
    
    # --- CONTROLES DE LA UI PRINCIPAL ---
    mesas_dropdown = ft.Dropdown(label="Seleccionar Mesa Ocupada", hint_text="Elige una mesa", options=[], expand=True, on_change=lambda e: seleccionar_mesa(e))
    items_dropdown = ft.Dropdown(label="Buscar Producto", hint_text="Añade un producto", options=[], expand=True)
    items_venta_list = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)
    total_text = ft.Text("TOTAL: $0.00", size=20, weight=ft.FontWeight.BOLD)
    
    # --- CONTROLES PARA LA CAPA DE FACTURACIÓN (NUESTRO "DIÁLOGO") ---
    factura_items_col = ft.Column() # Columna para la lista de productos en la tirilla
    factura_total_text = ft.Text(weight=ft.FontWeight.BOLD, size=18)
    factura_mesa_text = ft.Text(weight=ft.FontWeight.BOLD)

    # El contenedor principal de la factura, inicialmente invisible
    factura_container = ft.Container(
        visible=False, # Empieza oculto
        bgcolor=ft.Colors.with_opacity(0.85, ft.Colors.BLACK),
        border_radius=10,
        padding=20,
        expand=True,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=400,
                    padding=20,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=10,
                    content=ft.Column([
                        ft.Text("Confirmar Cobro", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                        factura_mesa_text,
                        ft.Divider(),
                        factura_items_col,
                        ft.Divider(),
                        ft.Row([
                            ft.Text("TOTAL", weight=ft.FontWeight.BOLD, size=18, color=ft.Colors.BLACK),
                            factura_total_text,
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.END,
                            controls=[
                                ft.TextButton("Cancelar", on_click=lambda e: ocultar_factura()),
                                ft.ElevatedButton("Cobrar", on_click=lambda e: confirmar_cobro(), bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE)
                            ]
                        )
                    ])
                )
            ]
        )
    )

    # --- LÓGICA DE LA VISTA ---
    
    # La lógica para cargar datos, añadir/eliminar items y actualizar la venta no cambia.
    # ... (copiamos las funciones de la versión anterior que ya funcionaban bien)
    venta_actual = {"mesa_doc_id": None, "mesa_id": None, "items": [], "total": 0.0}
    datos_cargados = {"items_catalogo": []}

    def cargar_datos_maestros(e=None):
        try:
            page.splash = ft.ProgressBar(); page.update()
            todas_las_mesas = db.get_all_mesas()
            mesas_ocupadas = [m for m in todas_las_mesas if m.get('status') == 'Ocupada']
            mesas_dropdown.options.clear()
            if not mesas_ocupadas:
                mesas_dropdown.options.append(ft.dropdown.Option(key=None, text="No hay mesas ocupadas"))
            else:
                for mesa in mesas_ocupadas:
                    mesas_dropdown.options.append(ft.dropdown.Option(key=mesa.get('doc_id'), text=f"Mesa {mesa.get('id')}"))
            datos_cargados["items_catalogo"] = db.get_all_items()
            items_dropdown.options.clear()
            for item in datos_cargados["items_catalogo"]:
                items_dropdown.options.append(ft.dropdown.Option(key=item.get('doc_id'), text=f"{item.get('nombre')} - ${item.get('precio', 0):,.2f}"))
        finally:
            page.splash = None; page.update()

    def seleccionar_mesa(e):
        mesa_doc_id = mesas_dropdown.value
        limpiar_vista_pedido()
        if not mesa_doc_id: page.update(); return
        mesa_obj = next((m for m in db.get_all_mesas() if m.get('doc_id') == mesa_doc_id), None)
        if mesa_obj:
            venta_actual.update({"mesa_doc_id": mesa_doc_id, "mesa_id": mesa_obj.get('id'), "items": db.get_orden_actual(mesa_doc_id)})
            actualizar_display_venta()

    def anadir_item(e):
        item_doc_id = items_dropdown.value
        mesa_doc_id = venta_actual["mesa_doc_id"]
        if not mesa_doc_id or not item_doc_id: return
        item_seleccionado = next((i for i in datos_cargados["items_catalogo"] if i.get('doc_id') == item_doc_id), None)
        if item_seleccionado and db.add_item_a_orden(mesa_doc_id, item_seleccionado):
            venta_actual["items"] = db.get_orden_actual(mesa_doc_id)
            actualizar_display_venta()

    def eliminar_item(item_doc_id):
        mesa_doc_id = venta_actual["mesa_doc_id"]
        if not mesa_doc_id: return
        if db.remove_item_de_orden(mesa_doc_id, item_doc_id):
            venta_actual["items"] = db.get_orden_actual(mesa_doc_id)
            actualizar_display_venta()

    def actualizar_display_venta():
        items_venta_list.controls.clear()
        venta_actual["total"] = sum(float(item.get('precio', 0)) * int(item.get('cantidad', 0)) for item in venta_actual["items"])
        if not venta_actual["items"]:
            items_venta_list.controls.append(ft.Text("Pedido vacío.", text_align=ft.TextAlign.CENTER))
        else:
            for item in venta_actual["items"]:
                items_venta_list.controls.append(ft.Container(content=ft.Row([ft.Text(f"{item.get('cantidad')}x {item.get('nombre')}", expand=True), ft.Text(f"${float(item.get('precio',0)) * int(item.get('cantidad',0)):,.2f}"), ft.IconButton(icon=ft.Icons.DELETE_OUTLINE, icon_color=ft.Colors.RED_400, on_click=lambda e, i=item.get('doc_id'): eliminar_item(i))])))
        total_text.value = f"TOTAL: ${venta_actual['total']:,.2f}"
        page.update()

    def limpiar_vista_pedido():
        venta_actual.update({"mesa_doc_id": None, "mesa_id": None, "items": [], "total": 0.0})
        mesas_dropdown.value = None
        actualizar_display_venta()

    # --- NUEVA LÓGICA PARA MOSTRAR/OCULTAR Y PROCESAR LA FACTURA ---
    def mostrar_factura():
        if not venta_actual["mesa_doc_id"] or not venta_actual["items"]:
            # Usamos un snackbar en lugar de un print
            page.snack_bar = ft.SnackBar(ft.Text("El pedido está vacío o no hay mesa seleccionada."), open=True)
            page.update()
            return
        
        # 1. Llenar la tirilla con los datos actuales
        factura_mesa_text.value = f"Mesa: {venta_actual['mesa_id']}"
        factura_items_col.controls.clear()
        for item in venta_actual['items']:
            factura_items_col.controls.append(ft.Row([ft.Text(f"{item.get('cantidad')}x {item.get('nombre')}", color=ft.Colors.BLACK, expand=True), ft.Text(f"${float(item.get('precio', 0)) * int(item.get('cantidad', 0)):,.2f}", color=ft.Colors.BLACK)]))
        factura_total_text.value = f"${venta_actual['total']:,.2f}"
        factura_total_text.color = ft.Colors.BLACK

        # 2. Hacer visible el contenedor de la factura
        factura_container.visible = True
        page.update()

    def ocultar_factura():
        factura_container.visible = False
        page.update()

    def confirmar_cobro():
        ocultar_factura()
        page.splash = ft.ProgressBar()
        datos_factura = {"mesa_id": venta_actual["mesa_id"], "total_cobrado": venta_actual["total"], "items_vendidos": venta_actual["items"], "estado": "Facturado"}
        id_factura = db.add_factura(datos_factura)
        if id_factura:
            db.limpiar_orden_actual(venta_actual["mesa_doc_id"])
            db.update_mesa(venta_actual["mesa_doc_id"], {"status": "Libre"})
            limpiar_vista_pedido()
            cargar_datos_maestros()
        page.splash = None
        page.update()

    # --- INICIALIZACIÓN ---
    cargar_datos_maestros()
    
    # El layout principal ahora es un STACK para poder superponer la factura
    return ft.Stack(
        expand=True,
        controls=[
            # Capa 1: El contenido principal de la vista
            ft.Column(
                expand=True,
                controls=[
                    ft.Row([ft.Text("Caja - Punto de Venta", size=24, weight=ft.FontWeight.BOLD), ft.IconButton(icon=ft.Icons.REFRESH, on_click=cargar_datos_maestros)]),
                    ft.Divider(),
                    ft.Row([mesas_dropdown]),
                    ft.Row([items_dropdown, ft.IconButton(icon=ft.Icons.ADD_SHOPPING_CART, on_click=anadir_item)]),
                    ft.Divider(height=10),
                    ft.Text("Pedido Actual", weight=ft.FontWeight.BOLD),
                    items_venta_list,
                    ft.Divider(height=10),
                    ft.Row([total_text], alignment=ft.MainAxisAlignment.END),
                    ft.Row(alignment=ft.MainAxisAlignment.END, controls=[ft.ElevatedButton(text="Facturar", icon=ft.Icons.POINT_OF_SALE, on_click=lambda e: mostrar_factura(), bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE)])
                ]
            ),
            # Capa 2: La capa de facturación, superpuesta y oculta
            factura_container
        ]
    )