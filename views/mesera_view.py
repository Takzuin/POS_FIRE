import flet as ft
import databasefire as db

def MeseraView(page):
    mesas_list = ft.Column()

    def cargar_mesas():
        """Carga todas las mesas desde Firestore y las muestra en la UI."""
        try:
            lista_de_mesas = db.get_all_mesas()
            lista_de_meseros = db.get_all_meseros()
            
            mesas_list.controls.clear()
            if not lista_de_mesas:
                mesas_list.controls.append(ft.Text("No hay mesas disponibles.", size=16, text_align=ft.TextAlign.CENTER))
            else:
                for mesa in lista_de_mesas:
                    
                    """ print("─" * 40)
                    print(f"ANALIZANDO MESA: {mesa}")
                    print(f"VALOR DEL CAMPO 'mesero_id': {mesa.get('mesero_id')}")
                     """
                    mesa_id = mesa.get('id', 'N/A')
                    mesa_status = mesa.get('status', 'Desconocido')
                    mesero_id = mesa.get('mesero_id', None)
                    doc_id = mesa.get('doc_id', '')
                    meser = mesa.get('mesero_id', '')   
                    # Encontrar el nombre del mesero
                    #mesero_nombre = "Sin asignar"
                    mesero_nombre = meser


                    """ if mesero_id:
                        mesero = next((m for m in lista_de_meseros if m.get('id') == mesero_id), None)
                        if mesero:
                            mesero_nombre = mesero.get('name', 'Desconocido')
                    """ 
                    # Determinar colores según el estado
                    if mesa_status.lower() == "libre":
                        color_fondo = ft.Colors.GREEN_100
                        color_texto = ft.Colors.GREEN_800
                    elif mesa_status.lower() == "ocupada":
                        color_fondo = ft.Colors.RED_100
                        color_texto = ft.Colors.RED_800
                    elif mesa_status.lower() == "reservada":
                        color_fondo = ft.Colors.YELLOW_100
                        color_texto = ft.Colors.YELLOW_800
                    else:
                        color_fondo = ft.Colors.GREY_100
                        color_texto = ft.Colors.GREY_800
                    
                    mesa_card = ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Text(f"Mesa {mesa_id}", size=18, weight=ft.FontWeight.BOLD),
                                ft.Text(f" - {mesa_status}", size=16, color=color_texto)
                            ]),
                            ft.Row([
                                ft.Icon(ft.Icons.PERSON, size=16),
                                ft.Text(f"Mesero: {mesero_nombre}", size=14, color=ft.Colors.GREY_700)
                            ]),
                            ft.Row([
                                ft.ElevatedButton(
                                    text="Ocupar" if mesa_status.lower() == "libre" else "Liberar",
                                    on_click=lambda e, m_id=mesa_id, m_status=mesa_status: toggle_mesa_status(m_id, m_status),
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.BLUE_400 if mesa_status.lower() == "libre" else ft.Colors.ORANGE_400
                                ),
                                ft.ElevatedButton(
                                    text="Editar",
                                    icon=ft.Icons.EDIT,
                                    on_click=lambda e, m_id=mesa_id, d_id=doc_id: abrir_dialog_editar(m_id, d_id),
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.PURPLE_400
                                ),
                                ft.ElevatedButton(
                                    text="Asignar Mesero",
                                    icon=ft.Icons.PERSON_ADD,
                                    on_click=lambda e, m_id=mesa_id, d_id=doc_id: abrir_dialog_asignar_mesero(m_id, d_id),
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.CYAN_400
                                ),
                                ft.ElevatedButton(
                                    text="Eliminar",
                                    icon=ft.Icons.DELETE,
                                    on_click=lambda e, d_id=doc_id, m_id=mesa_id: confirmar_eliminar(d_id, m_id),
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.RED_400
                                )
                            ], alignment=ft.MainAxisAlignment.END, wrap=True)
                        ]),
                        padding=10,
                        bgcolor=color_fondo,
                        border_radius=10,
                        margin=5,
                        border=ft.border.all(1, color_texto)
                    )
                    mesas_list.controls.append(mesa_card)
            page.update()
        except Exception as e:
            mesas_list.controls.append(
                ft.Text(f"Error al cargar mesas: {e}", color=ft.Colors.RED, size=16, text_align=ft.TextAlign.CENTER)
            )
            page.update()

    def toggle_mesa_status(mesa_id, current_status):
        """Cambia el estado de la mesa entre 'Libre' y 'Ocupada'."""
        new_status = "Ocupada" if current_status.lower() == "libre" else "Libre"
        try:
            mesa = db.get_mesa_by_id(mesa_id)
            if mesa:
                doc_id = mesa.get('doc_id')
                success = db.update_mesa(doc_id, {"status": new_status})
                if success:
                    page.snack_bar = ft.SnackBar(ft.Text(f"Mesa {mesa_id} actualizada a {new_status}"), open=True)
                    cargar_mesas()
                else:
                    page.snack_bar = ft.SnackBar(ft.Text(f"Error al actualizar mesa {mesa_id}"), open=True)
            page.update()
        except Exception as e:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error al actualizar mesa: {e}"), open=True)
            page.update()

    def abrir_dialog_editar(mesa_id, doc_id):
        """Abre un diálogo para editar la mesa."""
        # Obtener datos actuales de la mesa
        mesa_actual = db.get_mesa_by_id(mesa_id)
        if not mesa_actual:
            page.snack_bar = ft.SnackBar(ft.Text("No se pudo encontrar la mesa"), open=True)
            page.update()
            return

        # Campos del formulario
        id_field = ft.TextField(
            label="ID de Mesa",
            value=mesa_actual.get('id', ''),
            width=300
        )
        
        status_dropdown = ft.Dropdown(
            label="Estado",
            value=mesa_actual.get('status', 'Libre'),
            options=[
                ft.dropdown.Option("Libre"),
                ft.dropdown.Option("Ocupada"),
                ft.dropdown.Option("Reservada"),
                ft.dropdown.Option("Fuera de servicio")
            ],
            width=300
        )

        def guardar_cambios(e):
            try:
                # Verificar si el nuevo ID ya existe (si se cambió)
                nuevo_id = id_field.value.strip()
                if nuevo_id != mesa_actual.get('id'):
                    mesas_existentes = db.get_all_mesas()
                    if any(m.get('id') == nuevo_id for m in mesas_existentes):
                        page.snack_bar = ft.SnackBar(ft.Text(f"El ID {nuevo_id} ya existe"), open=True)
                        page.update()
                        return

                # Actualizar mesa
                datos_actualizados = {
                    'id': nuevo_id,
                    'status': status_dropdown.value
                }
                
                success = db.update_mesa(doc_id, datos_actualizados)
                if success:
                    page.snack_bar = ft.SnackBar(ft.Text("Mesa actualizada exitosamente"), open=True)
                    cargar_mesas()
                    dialog_editar.open = False
                else:
                    page.snack_bar = ft.SnackBar(ft.Text("Error al actualizar la mesa"), open=True)
                
                page.update()
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"), open=True)
                page.update()

        def cancelar_edicion(e):
            dialog_editar.open = False
            page.update()

        dialog_editar = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Editar Mesa {mesa_id}"),
            content=ft.Column([
                id_field,
                status_dropdown
            ], tight=True),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar_edicion),
                ft.TextButton("Guardar", on_click=guardar_cambios)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        page.overlay.append(dialog_editar)
        dialog_editar.open = True
        page.update()

    def abrir_dialog_asignar_mesero(mesa_id, doc_id):
        """Abre un diálogo para asignar un mesero a la mesa."""
        # Obtener datos actuales de la mesa
        mesa_actual = db.get_mesa_by_id(mesa_id)
        if not mesa_actual:
            page.snack_bar = ft.SnackBar(ft.Text("No se pudo encontrar la mesa"), open=True)
            page.update()
            return

        # Obtener lista de meseros
        meseros = db.get_all_meseros()
        if not meseros:
            page.snack_bar = ft.SnackBar(ft.Text("No hay meseros disponibles. Agregue meseros primero."), open=True)
            page.update()
            return

        # Crear opciones para el dropdown
        mesero_options = [ft.dropdown.Option(key="", text="Sin asignar")]
        for mesero in meseros:
            mesero_options.append(
                ft.dropdown.Option(
                    key=mesero.get('id', ''),
                    text=f"{mesero.get('name', 'Sin nombre')} - {mesero.get('id', '')}"
                )
            )

        mesero_dropdown = ft.Dropdown(
            label="Seleccionar Mesero",
            value=str(mesa_actual.get('mesero_id', '')) if mesa_actual.get('mesero_id') is not None else "",
            options=mesero_options,
            width=400
        )

        def asignar_mesero(e):
            try:
                mesero_id = mesero_dropdown.value if mesero_dropdown.value else None
                
                # Actualizar mesa con el mesero asignado
                datos_actualizados = {
                    'mesero_id': mesero_id
                }
                
                success = db.update_mesa(doc_id, datos_actualizados)
                if success:
                    mesero_nombre = "Sin asignar"
                    if mesero_id:
                        mesero = next((m for m in meseros if m.get('id') == mesero_id), None)
                        if mesero:
                            mesero_nombre = mesero.get('name', 'Desconocido')
                    
                    page.snack_bar = ft.SnackBar(ft.Text(f"Mesa {mesa_id} asignada a {mesero_nombre}"), open=True)
                    cargar_mesas()
                    dialog_asignar.open = False
                else:
                    page.snack_bar = ft.SnackBar(ft.Text("Error al asignar mesero"), open=True)
                
                page.update()
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"), open=True)
                page.update()

        def cancelar_asignacion(e):
            dialog_asignar.open = False
            page.update()

        dialog_asignar = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Asignar Mesero a Mesa {mesa_id}"),
            content=ft.Column([
                ft.Text("Seleccione el mesero que atenderá esta mesa:"),
                mesero_dropdown
            ], tight=True),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar_asignacion),
                ft.TextButton("Asignar", on_click=asignar_mesero)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        page.overlay.append(dialog_asignar)
        dialog_asignar.open = True
        page.update()

    def confirmar_eliminar(doc_id, mesa_id):
        """Confirma la eliminación de una mesa."""
        def eliminar_mesa(e):
            try:
                db.delete_mesa(doc_id)
                page.snack_bar = ft.SnackBar(ft.Text(f"Mesa {mesa_id} eliminada exitosamente"), open=True)
                cargar_mesas()
                dialog_confirmar.open = False
                page.update()
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"Error al eliminar mesa: {ex}"), open=True)
                page.update()

        def cancelar_eliminacion(e):
            dialog_confirmar.open = False
            page.update()

        dialog_confirmar = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text(f"¿Está seguro de que desea eliminar la Mesa {mesa_id}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar_eliminacion),
                ft.TextButton("Eliminar", on_click=eliminar_mesa, style=ft.ButtonStyle(color=ft.Colors.RED))
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        page.overlay.append(dialog_confirmar)
        dialog_confirmar.open = True
        page.update()

    def abrir_dialog_nueva_mesa():
        """Abre un diálogo para agregar una nueva mesa."""
        # Obtener lista de meseros
        meseros = db.get_all_meseros()
        
        # Crear opciones para el dropdown de meseros
        mesero_options = [ft.dropdown.Option(key="", text="Sin asignar")]
        for mesero in meseros:
            mesero_options.append(
                ft.dropdown.Option(
                    key=mesero.get('id', ''),
                    text=f"{mesero.get('name', 'Sin nombre')} - {mesero.get('id', '')}"
                )
            )

        # Campos del formulario
        id_field = ft.TextField(
            label="ID de Mesa",
            hint_text="Ej: 5, A1, etc.",
            width=300
        )
        
        status_dropdown = ft.Dropdown(
            label="Estado",
            value="Libre",
            options=[
                ft.dropdown.Option("Libre"),
                ft.dropdown.Option("Ocupada"),
                ft.dropdown.Option("Reservada"),
                ft.dropdown.Option("Fuera de servicio")
            ],
            width=300
        )

        mesero_dropdown = ft.Dropdown(
            label="Mesero Asignado",
            value="",
            options=mesero_options,
            width=400
        )

        def agregar_mesa(e):
            try:
                nuevo_id = id_field.value.strip()
                if not nuevo_id:
                    page.snack_bar = ft.SnackBar(ft.Text("El ID de la mesa es requerido"), open=True)
                    page.update()
                    return

                # Verificar si el ID ya existe
                mesas_existentes = db.get_all_mesas()
                if any(m.get('id') == nuevo_id for m in mesas_existentes):
                    page.snack_bar = ft.SnackBar(ft.Text(f"El ID {nuevo_id} ya existe"), open=True)
                    page.update()
                    return

                # Agregar nueva mesa
                datos_mesa = {
                    'id': nuevo_id,
                    'status': status_dropdown.value,
                    'mesero_id': mesero_dropdown.value or None
                }
                
                doc_id = db.add_mesa(datos_mesa)
                if doc_id:
                    page.snack_bar = ft.SnackBar(ft.Text(f"Mesa {nuevo_id} agregada exitosamente"), open=True)
                    cargar_mesas()
                    dialog_nueva.open = False
                else:
                    page.snack_bar = ft.SnackBar(ft.Text("Error al agregar la mesa"), open=True)
                
                page.update()
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"), open=True)
                page.update()

        def cancelar_agregar(e):
            dialog_nueva.open = False
            page.update()

        dialog_nueva = ft.AlertDialog(
            modal=True,
            title=ft.Text("Agregar Nueva Mesa"),
            content=ft.Column([
                id_field,
                status_dropdown,
                mesero_dropdown
            ], tight=True),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar_agregar),
                ft.TextButton("Agregar", on_click=agregar_mesa)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        page.overlay.append(dialog_nueva)
        dialog_nueva.open = True
        page.update()

    def abrir_dialog_gestionar_meseros():
        """Abre un diálogo para gestionar meseros."""
        meseros_list = ft.Column(height=300, scroll=ft.ScrollMode.AUTO)
        
        def cargar_meseros():
            meseros = db.get_all_meseros()
            meseros_list.controls.clear()
            
            if not meseros:
                meseros_list.controls.append(ft.Text("No hay meseros registrados"))
            else:
                for mesero in meseros:
                    mesero_card = ft.Container(
                        content=ft.Row([
                            ft.Column([
                                ft.Text(f"ID: {mesero.get('id', 'N/A')}", weight=ft.FontWeight.BOLD),
                                ft.Text(f"Nombre: {mesero.get('name', 'N/A')}")
                            ], expand=True),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                on_click=lambda e, doc_id=mesero.get('doc_id'): eliminar_mesero(doc_id)
                            )
                        ]),
                        padding=10,
                        bgcolor=ft.Colors.SURFACE_VARIANT,
                        border_radius=5,
                        margin=2
                    )
                    meseros_list.controls.append(mesero_card)
            
            page.update()

        def eliminar_mesero(doc_id):
            try:
                db.delete_mesero(doc_id)
                page.snack_bar = ft.SnackBar(ft.Text("Mesero eliminado exitosamente"), open=True)
                cargar_meseros()
                page.update()
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"Error al eliminar mesero: {ex}"), open=True)
                page.update()

        # Campos para agregar nuevo mesero
        id_mesero_field = ft.TextField(label="ID del Mesero", width=200)
        nombre_mesero_field = ft.TextField(label="Nombre del Mesero", width=200)

        def agregar_mesero(e):
            try:
                id_mesero = id_mesero_field.value.strip()
                nombre_mesero = nombre_mesero_field.value.strip()
                
                if not id_mesero or not nombre_mesero:
                    page.snack_bar = ft.SnackBar(ft.Text("ID y nombre son requeridos"), open=True)
                    page.update()
                    return

                # Verificar si el ID ya existe
                meseros_existentes = db.get_all_meseros()
                if any(m.get('id') == id_mesero for m in meseros_existentes):
                    page.snack_bar = ft.SnackBar(ft.Text(f"El ID {id_mesero} ya existe"), open=True)
                    page.update()
                    return

                # Agregar nuevo mesero
                datos_mesero = {
                    'id': id_mesero,
                    'nombre': nombre_mesero
                }
                
                doc_id = db.add_mesero(datos_mesero)
                if doc_id:
                    page.snack_bar = ft.SnackBar(ft.Text(f"Mesero {nombre_mesero} agregado exitosamente"), open=True)
                    id_mesero_field.value = ""
                    nombre_mesero_field.value = ""
                    cargar_meseros()
                else:
                    page.snack_bar = ft.SnackBar(ft.Text("Error al agregar mesero"), open=True)
                
                page.update()
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"), open=True)
                page.update()

        def cerrar_dialog(e):
            dialog_meseros.open = False
            page.update()

        dialog_meseros = ft.AlertDialog(
            modal=True,
            title=ft.Text("Gestionar Meseros"),
            content=ft.Column([
                ft.Text("Meseros Registrados:", weight=ft.FontWeight.BOLD),
                meseros_list,
                ft.Divider(),
                ft.Text("Agregar Nuevo Mesero:", weight=ft.FontWeight.BOLD),
                ft.Row([id_mesero_field, nombre_mesero_field]),
                ft.ElevatedButton("Agregar Mesero", on_click=agregar_mesero)
            ], tight=True, width=500),
            actions=[
                ft.TextButton("Cerrar", on_click=cerrar_dialog)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        page.overlay.append(dialog_meseros)
        dialog_meseros.open = True
        cargar_meseros()
        page.update()

    # Cargar mesas al iniciar
    cargar_mesas()

    # Botones de acción
    botones_accion = ft.Row([
        ft.ElevatedButton(
            text="Agregar Mesa",
            icon=ft.Icons.ADD,
            on_click=lambda e: abrir_dialog_nueva_mesa(),
            bgcolor=ft.Colors.GREEN_400,
            color=ft.Colors.WHITE
        ),
        ft.ElevatedButton(
            text="Gestionar Meseros",
            icon=ft.Icons.PEOPLE,
            on_click=lambda e: abrir_dialog_gestionar_meseros(),
            bgcolor=ft.Colors.INDIGO_400,
            color=ft.Colors.WHITE
        ),
        ft.ElevatedButton(
            text="Recargar",
            icon=ft.Icons.REFRESH,
            on_click=lambda e: cargar_mesas(),
            bgcolor=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE
        )
    ], alignment=ft.MainAxisAlignment.CENTER, wrap=True)

    return ft.Container(
        content=ft.Column([
            ft.Text("Vista Mesera", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            ft.Divider(height=2, color=ft.Colors.GREY_300),
            botones_accion,
            ft.Divider(height=1, color=ft.Colors.GREY_200),
            mesas_list
        ], spacing=10, scroll=ft.ScrollMode.AUTO),
        padding=10,
        expand=True
    )