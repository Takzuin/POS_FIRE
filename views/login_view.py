import flet as ft
from firebase_admin import auth
from dbf.databasefire import verify_user_credentials, get_user_info

class LoginView(ft.Column):
    def __init__(self, page, on_login_success=None):
        super().__init__(spacing=30, expand=True, alignment=ft.MainAxisAlignment.CENTER)
        self.page = page
        self.on_login_success = on_login_success  # Callback para cambiar a AppLayout

        self.email_field = ft.TextField(label="Correo electrónico", width=400)
        self.password_field = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=400)
        self.login_button = ft.ElevatedButton(text="Iniciar Sesión", on_click=self.login, width=200)
        self.message = ft.Text(value="", color=ft.Colors.RED, size=14)

        self.controls.extend([
            ft.Container(
                content=ft.Column([
                    ft.Text("Sistema POS", size=30, weight=ft.FontWeight.BOLD),
                    ft.Text("Iniciar sesión con tu cuenta", size=16),
                    self.email_field,
                    self.password_field,
                    self.login_button,
                    self.message
                ], alignment=ft.MainAxisAlignment.CENTER),
                alignment=ft.alignment.center,
                padding=ft.padding.all(40),
                bgcolor=ft.Colors.WHITE,
                border_radius=20,
                shadow=ft.BoxShadow(
                    spread_radius=2,
                    blur_radius=10,
                    color=ft.Colors.BLACK12,
                    offset=ft.Offset(0, 4)
                )
            )
        ])

    def login(self, e):
        email = self.email_field.value.strip()
        password = self.password_field.value.strip()

        if not email or not password:
            self.message.value = "Por favor ingresa tu correo y contraseña."
            self.update()
            return

        self.message.value = "Verificando..."
        self.update()

        uid = verify_user_credentials(email, password)
        if uid:
            user_info = get_user_info(uid)
            self.page.session.set("user", user_info)
            self.message.value = f"Bienvenido, {user_info['display_name'] or 'Usuario'}"
            self.message.color = ft.Colors.GREEN
            self.update()

            if self.on_login_success:
                self.on_login_success()  # Cambio de vista
        else:
            self.message.value = "Correo o contraseña inválidos."
            self.message.color = ft.Colors.RED
            self.update()
