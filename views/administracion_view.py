import flet as ft
import databasefire as db

def AdministracionView(page):
    # --- CONTROLES PARA EL FORMULARIO ---
    new_item_name = ft.TextField(label="Nombre del Producto", expand=True)
    new_item_price = ft.TextField(label="Precio", width=150, keyboard_type=ft.KeyboardType.NUMBER, prefix_text="$")
    new_item_category = ft.TextField(label="Categoría", expand=True)
    new_item_description = ft.TextField(label="Descripción (opcional)", multiline=True, min_lines=2)
    
    items_list = ft.Column(spacing=10)

    def cargar_items():
        """Carga todos los ítems desde Firestore y los muestra en la UI."""
        try:
            lista_de_items = db.get_all_items()
            items_list.controls.clear()
            if not lista_de_items:
                items_list.controls.append(ft.Text("No hay productos registrados.", size=16))
            else:
                for item in lista_de_items:
                    item_card = ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Text(item.get('nombre', 'N/A'), size=18, weight=ft.FontWeight.BOLD, expand=True),
                                ft.Container(
                                    content=ft.Text(item.get('categoria', 'Sin categoría'), size=12, weight=ft.FontWeight.W_500),
                                    bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.PRIMARY),
                                    padding=ft.padding.symmetric(vertical=2, horizontal=8),
                                    border_radius=10
                                )
                            ]),
                            ft.Text(f"${item.get('precio', 0):,.2f}", size=16, color=ft.Colors.GREEN),
                            ft.Text(item.get('descripcion', ''), size=14, italic=True),
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.DELETE_OUTLINE,
                                    tooltip="Eliminar Producto",
                                    on_click=lambda e, i_id=item.get('doc_id'), i_name=item.get('nombre'): confirmar_eliminar(i_id, i_name)
                                )
                            ], alignment=ft.MainAxisAlignment.END)
                        ]),
                        padding=15,
                        border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
                        border_radius=10
                    )
                    items_list.controls.append(item_card)
            
            page.update()
        except Exception as e:
            items_list.controls.clear()
            items_list.controls.append(ft.Text(f"Error al cargar productos: {e}", color=ft.Colors.RED))
            page.update()

    def agregar_item():
        """Agrega un nuevo ítem a Firestore de forma eficiente."""
        try:
            nombre = new_item_name.value.strip()
            precio_str = new_item_price.value.strip()
            categoria = new_item_category.value.strip()

            if not all([nombre, precio_str, categoria]):
                page.snack_bar = ft.SnackBar(ft.Text("Nombre, precio y categoría son obligatorios."), open=True)
                page.update()
                return

            nuevo_item = {
                "nombre": nombre, "precio": float(precio_str),
                "categoria": categoria, "descripcion": new_item_description.value.strip()
            }
            
            doc_id = db.add_item(nuevo_item)
            if doc_id:
                new_item_name.value, new_item_price.value, new_item_category.value, new_item_description.value = "", "", "", ""
                page.snack_bar = ft.SnackBar(ft.Text("Producto agregado exitosamente"), open=True)
                cargar_items()
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Error al guardar el producto."), open=True)
            page.update()
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("El precio debe ser un número válido."), open=True)
            page.update()
        except Exception as e:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error inesperado: {e}"), open=True)
            page.update()

    def confirmar_eliminar(doc_id, item_nombre):
        """Muestra un diálogo de confirmación antes de eliminar."""
        
        def eliminar_action(e):
            # Cerramos el diálogo y limpiamos el overlay
            confirm_dialog.open = False
            page.update()
            
            # Pequeña pausa para asegurar que el diálogo se cierre completamente
            import time
            time.sleep(0.1)
            
            # Eliminamos el diálogo del overlay
            if confirm_dialog in page.overlay:
                page.overlay.remove(confirm_dialog)
            
            # Realizamos la eliminación
            try:
                db.delete_item(doc_id)
                page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"'{item_nombre}' eliminado."),
                    open=True,
                    duration=3000
                )
                cargar_items()
            except Exception as ex:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Error al eliminar: {ex}"),
                    open=True,
                    duration=3000
                )
            
            # Actualizamos la página
            page.update()

        def cancelar_action(e):
            confirm_dialog.open = False
            page.update()
            
            # Pequeña pausa para asegurar que el diálogo se cierre completamente
            import time
            time.sleep(0.1)
            
            # Eliminamos el diálogo del overlay
            if confirm_dialog in page.overlay:
                page.overlay.remove(confirm_dialog)
            
            page.update()

        confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Eliminación"),
            content=ft.Text(f"¿Estás seguro de que quieres eliminar el producto '{item_nombre}'?"),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar_action),
                ft.FilledButton("Eliminar", on_click=eliminar_action, bgcolor=ft.Colors.RED_700, color=ft.Colors.WHITE),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(confirm_dialog)
        confirm_dialog.open = True
        page.update()

    # --- Estructura de la página ---
    add_item_form = ft.Container(
        content=ft.Column([
            ft.Row([new_item_name, new_item_price]),
            ft.Row([new_item_category]),
            ft.Row([new_item_description]),
            ft.Row(
                [ft.FilledButton(text="Agregar Producto", icon=ft.Icons.ADD, on_click=lambda _: agregar_item())],
                alignment=ft.MainAxisAlignment.END
            )
        ]),
        padding=20,
        border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
        border_radius=10,
        margin=ft.margin.only(bottom=20)
    )

    # Cargar los ítems iniciales
    cargar_items()

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Gestión de Productos", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                add_item_form,
                ft.Text("Lista de Productos", size=20),
                items_list,
            ],
            scroll=ft.ScrollMode.ADAPTIVE,
            spacing=20
        ),
        padding=20,
        expand=True
    )