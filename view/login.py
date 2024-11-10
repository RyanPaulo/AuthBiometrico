from cmath import e

import bcrypt
import flet as ft
import mysql

from models.connector_bd import Connector_BD

#Class responsavel por desenhar a tela de 'Login' e suas funções

print_byte = None
user = None

class Login():
    def main(self, page: ft.Page):
        page.window_width = 800
        page.window_height = 750
        page.theme_mode = 'dark'
        page.vertical_alignment = 'center'
        page.horizontal_alignment = 'center'
        page.window.resizable = False
        page.window_center()

        user =  Treatment_User()


        def btn_check(e):
            from view.verification import Verification
            verification = Verification()
            success = verification_login(login_user, login_passw)

            try:
                if success:
                    user.set_user(login_user.value)
                    verification.main(page)

                    screen_login.visible = False
                    page.snack_bar = ft.SnackBar(
                        content=ft.Text(value='Acesso verificado com sucesso!'),
                        bgcolor='green',
                        action='OK',
                        duration=3000
                    )
                    page.snack_bar.open = True
                    print("Login efetuado com sucesso!")
                else:
                    print("Erro ao verificar login!")
                    page.snack_bar = ft.SnackBar(
                        content=ft.Text(value='Erro ao verificar acesso!'),
                        bgcolor='red',
                        action='OK',
                        duration=3000
                    )
                    page.snack_bar.open = True


            except Exception as e:
                print("Erro ao tentar logar: {} ".format(e))
                page.snack_bar = ft.SnackBar(
                    content=ft.Text(value='Error: {}'.format(e)),
                    bgcolor='red',
                    action='OK',
                    duration=5000
                )
                page.snack_bar.open = True

            login_user.value = None
            login_passw.value = None
            page.update()

        # Função que verificar se a o email e a senha estão no BD e se são do mesmmo cadatro
        def verification_login(login_user, login_passw):
            global user

            user = login_user.value
            passw = login_passw.value
            db = Connector_BD()

            sql = "SELECT * FROM login WHERE username = %s"
            query = (login_user.value,)

            try:
                db.mycursor.execute(sql, query)
                myresult = db.mycursor.fetchone()

                if myresult:

                    stored_password = myresult[3]
                    # comparar a senha armazenada no 3 indice do BD com a senha fornecida
                    if bcrypt.checkpw(passw.encode(), stored_password.encode()):
                        return True
                    else:
                        print("Senha incorreta")
                        page.snack_bar = ft.SnackBar(
                            content=ft.Text(value='Senha incorreta!'),
                            bgcolor='red',
                            action='OK',
                            duration=3000
                        )
                        page.snack_bar.open = True
                        return False
                else:
                    print("Usuario não encontrado")
                    page.snack_bar = ft.SnackBar(
                        content=ft.Text(value='Usuario não encontrado!'),
                        bgcolor='red',
                        action='OK',
                        duration=3000
                    )
                    page.snack_bar.open = True
                    return False
            except mysql.connector.Error as err:
                print("Erro ao acessar o banco de dados: {}".format(err))
                page.snack_bar = ft.SnackBar(
                    content=ft.Text(value='Error: {}'.format(err)),
                    bgcolor='red',
                    action='OK',
                    duration=5000
                )
                page.snack_bar.open = True
                return False




        def btn_first_access(e):
            from view.first_access import First_Access
            first_access = First_Access()
            first_access.main(page)
            first_access.visible = True

            screen_login.visible = False
            page.update()

        def on_key_down(e):
            btn_check(e)


        login_user = ft.TextField(
            hint_text='Usuario',
            width=350,
            height=50,
            border_radius=30,
            prefix_icon=ft.icons.PERSON,
            keyboard_type=ft.KeyboardType.EMAIL,
            bgcolor='black'
        )

        login_passw = ft.TextField(
            hint_text='Password',
            width=350,
            height=50,
            border_radius=30,
            prefix_icon=ft.icons.LOCK,
            password=True,
            can_reveal_password=True,
            keyboard_type=ft.KeyboardType.VISIBLE_PASSWORD,
            bgcolor='black',
            on_blur=on_key_down,


        )


        screen_login = ft.Column([
            ft.Container(
                bgcolor=ft.colors.BLUE_GREY_900,
                width=page.window_width - 30,
                height=page.window_height - 70,
                border_radius=10,

                content=ft.Column([
                    ft.Container(
                        bgcolor=ft.colors.GREY_500,
                        width=450,
                        height=600,
                        border_radius=10,

                        content=ft.Column([
                            ft.Container(
                                padding=ft.padding.only(
                                    top=50,
                                    bottom=50,
                                ),

                                content=ft.Column([
                                    ft.Text(
                                        value='Ministério do \nMeio Ambiente', # Texto principal
                                        weight='bold',
                                        size=50,
                                        color='black',
                                        font_family='Times new roman',
                                    ),
                                ])
                            ),

                            ft.Column([
                                login_user,
                                login_passw,
                            ], spacing=8),

                            ft.ElevatedButton(
                                text='Verificar',
                                color='white',
                                width=350,
                                height=50,
                                on_click=btn_check,
                            ),

                            ft.Container(
                                content=ft.TextButton('Primeiro acesso',
                                    style=ft.ButtonStyle(color='black'),
                                    on_click=btn_first_access,
                                ),
                                alignment=ft.alignment.bottom_right,
                                padding=ft.padding.only(right=10, top=100),
                            ),
                        ], horizontal_alignment='center'),
                    ),
                ], horizontal_alignment='center', alignment='center'),
            )
        ])

        page.add(screen_login)

class Treatment_User:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Treatment_User, cls).__new__(cls)
            cls._instance.user = None
        return cls._instance

    def set_user(self, user):
        self.user = user

    def get_user(self):
        return self.user

    def logout(self):
        self.user = None
        print("Desconectado.... ")



if __name__ == '__main__':
    login = Login()
    ft.app(target=login)
