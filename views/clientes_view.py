import flet as ft
from dbf import databasefire as db

# Debug: Print Flet module path
print(f"Flet module path: {ft.__file__}")

def ClientesView(page):
    clientes_list = ft.Column()

    def cargar_clientes():
        """Carga todos los clientes desde Firestore y los muestra en la UI."""
        try:
            lista_de_clientes = db.get_all_clients()
            clientes_list.controls.clear()
            if not lista_de_clientes:
                clientes_list.controls.append(ft.Text("No hay clientes registrados."))
            else:
                for cliente in lista_de_clientes:
                    clientes_list.controls.append(
                        ft.Container(
                            content=ft.Text(
                                f"Cliente: {cliente.get('nombre', 'N/A')}",
                                size=16
                            ),
                            padding=10,
                            bgcolor=ft.Colors.ON_SURFACE_VARIANT,
                            border_radius=5,
                            margin=5
                        )
                    )
            page.update()  # Use passed page object
        except Exception as e:
            clientes_list.controls.append(
                ft.Text(f"Error al cargar clientes: {e}", color=ft.Colors.RED)
            )
            page.update()  # Use passed page object

    cargar_clientes()

    return ft.Column([
        ft.Text("Vista Clientes", size=20, weight=ft.FontWeight.BOLD),
        clientes_list
    ], expand=True)