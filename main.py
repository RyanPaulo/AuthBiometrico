from view.login import Login
import flet as ft

class AuthBiometrico:

    if __name__ == '__main__':
        login = Login()
        ft.app(target=login.main)


import flet as ft
import os
import sys

from models.connector_bd import Connector_BD
from view.login import Treatment_User, Login


# from main import AuthBiometrico


class Access:
    def main(self, page: ft.Page):
        # ... your other setup code ...

        def btn_close(e):
            Treatment_User().logout()
            e.page.window_close()

            # Restart the app from main.py
            os.execv(sys.executable, [sys.executable, "main.py"])

        # Update the close button with the updated function
        ft.TextButton(
            text='Sair',
            style=ft.ButtonStyle(color='black'),
            on_click=btn_close,
        )

        # ... rest of your code ...
