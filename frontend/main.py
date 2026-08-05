from app import LegalDeskApp
from login_window import LoginWindow


def main():
    while True:
        login = LoginWindow()
        login.mainloop()
        if login.usuario is None:
            break  # se cerró la ventana sin iniciar sesión

        app = LegalDeskApp(login.usuario)
        app.mainloop()
        if not app.solicito_cerrar_sesion:
            break  # se cerró la app normalmente


if __name__ == "__main__":
    main()
