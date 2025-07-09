import flet as ft
from dbf import databasefire as db
from datetime import datetime

def VentasView(page):
    """
    Vista para mostrar la lista de ventas facturadas,
    con la capacidad de filtrar por fecha.
    """

    # --- CONTROLES DE LA UI ---
    lista_ventas_col = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)
    total_ventas_text = ft.Text("Total en ventas: $0.00", size=18, weight=ft.FontWeight.BOLD)
    fecha_seleccionada_text = ft.Text("Mostrando todas las ventas", size=16, italic=True)

    def on_date_change(e):
        """Se ejecuta cuando el usuario selecciona una fecha en el DatePicker."""
        fecha_seleccionada = date_picker.value.date()
        cargar_ventas(fecha=fecha_seleccionada)
        date_picker_dialog.open = False
        page.update()

    date_picker = ft.DatePicker(
        on_change=on_date_change,
        first_date=datetime(2023, 1, 1),
        last_date=datetime.now(),
        help_text="Selecciona una fecha para filtrar"
    )
    
    date_picker_dialog = ft.AlertDialog(
        content=date_picker,
    )
    page.overlay.append(date_picker)


    # --- LÓGICA DE LA VISTA ---

    def cargar_ventas(e=None, fecha=None):
        """Carga las ventas desde Firestore, opcionalmente filtradas por fecha."""
        try:
            page.splash = ft.ProgressBar()
            page.update()

            if fecha:
                # Cargar ventas para una fecha específica
                lista_de_facturas = db.get_facturas_por_fecha(fecha)
                fecha_seleccionada_text.value = f"Mostrando ventas para: {fecha.strftime('%d/%m/%Y')}"
            else:
                # Cargar todas las ventas
                lista_de_facturas = db.get_all_facturas()
                fecha_seleccionada_text.value = "Mostrando todas las ventas"

            lista_ventas_col.controls.clear()
            total_del_periodo = 0

            if not lista_de_facturas:
                lista_ventas_col.controls.append(ft.Text("No se encontraron ventas para el período seleccionado.", text_align=ft.TextAlign.CENTER))
            else:
                for factura in lista_de_facturas:
                    total_del_periodo += factura.get('total_cobrado', 0)
                    
                    # Formatear la fecha para mostrarla
                    fecha_factura = factura.get('fecha_facturacion')
                    if isinstance(fecha_factura, datetime):
                        fecha_str = fecha_factura.strftime("%d/%m/%Y %I:%M %p")
                    else:
                        fecha_str = "Fecha no disponible"

                    # Crear una tarjeta para cada venta
                    tarjeta_venta = ft.Container(
                        padding=15,
                        border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
                        border_radius=10,
                        content=ft.Column([
                            ft.Row([
                                ft.Text(f"Factura #{factura.get('doc_id', 'N/A')[:6]}...", weight=ft.FontWeight.BOLD),
                                ft.Text(fecha_str, italic=True)
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Text(f"Mesa atendida: {factura.get('mesa_id', 'N/A')}"),
                            ft.Divider(),
                            ft.Text("Items Vendidos:"),
                            ft.Column([
                                ft.Row([
                                    ft.Text(f"  - {item.get('cantidad')}x {item.get('nombre')}"),
                                ]) for item in factura.get('items_vendidos', [])
                            ]),
                            ft.Row([
                                ft.Text("TOTAL:", weight=ft.FontWeight.BOLD, size=16),
                                ft.Text(f"${factura.get('total_cobrado', 0):,.2f}", size=16, color=ft.Colors.GREEN_700)
                            ], alignment=ft.MainAxisAlignment.END)
                        ])
                    )
                    lista_ventas_col.controls.append(tarjeta_venta)
            
            total_ventas_text.value = f"Total en ventas: ${total_del_periodo:,.2f}"

        except Exception as ex:
            lista_ventas_col.controls.append(ft.Text(f"Error al cargar ventas: {ex}", color=ft.Colors.RED))
        finally:
            page.splash = None
            page.update()

    # --- INICIALIZACIÓN ---
    cargar_ventas()

    return ft.Column(
        expand=True,
        controls=[
            ft.Row([
                ft.Text("Historial de Ventas", size=24, weight=ft.FontWeight.BOLD),
                ft.IconButton(
                    icon=ft.Icons.CALENDAR_MONTH,
                    tooltip="Filtrar por fecha",
                    on_click=lambda e: date_picker.pick_date()
                ),
                ft.IconButton(
                    icon=ft.Icons.REFRESH,
                    tooltip="Recargar / Mostrar todas",
                    on_click=cargar_ventas
                )
            ]),
            fecha_seleccionada_text,
            ft.Divider(),
            total_ventas_text,
            lista_ventas_col
        ]
    )