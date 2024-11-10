import bcrypt
import flet as ft
import mysql

from models.connector_bd import Connector_BD
from models.auth_biometric import Img_Biometric

#Class responsavel por desenhar a tela 'Primeiro Acesso' e suas funções
class First_Access:
    def main(self, page: ft.Page):
        page.window_width=800
        page.window_height=800
        page.theme_mode='dark'
        page.vertical_alignment='center'
        page.horizontal_alignment='center'
        page.window.resizable=False
        page.window_center()


        #Inicio das funções e a criação da caixa de dialogo

        def btn_img_bio_nivel01(e):
            global print_byte
            img = Img_Biometric("Img/bio_pol_LM1.jpg")
            byte = img.img_to_byte()
            print_byte = byte

            print("Imagem biometria Ryan. Acesso nivel 01")
            dialog_select_img.open = False
            page.update()

        def btn_img_bio_nivel02(e):
            global print_byte
            img = Img_Biometric("Img/bio_ind_L.jpg")
            byte = img.img_to_byte()
            print_byte = byte

            print("Imagem biometria Leo. Acesso nivel 02")
            dialog_select_img.open = False
            page.update()

        def btn_img_bio_nivel03(e):
            global print_byte
            img = Img_Biometric("Img/bio_ind_R.jpg")
            byte = img.img_to_byte()
            print_byte = byte

            print("Imagem biometria Isa. Acesso nivel 03")
            dialog_select_img.open = False
            page.update()

        def close_dialog(e):
            dialog_select_img.open = False
            page.update()



        #Criando dialog para selecionar a image da biometria
        dialog_select_img = ft.AlertDialog(
            bgcolor=ft.colors.BLUE_GREY_900,
            modal=True,
            title=ft.Text('Selecione sua Biometria'),
            content=ft.Column([
                # Criando o primeiro botao, com a imagem do nivel 01
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Image(
                            src='img/bio_pol_LM1.jpg',
                            width=80,
                            height=80,
                            fit=ft.ImageFit.CONTAIN,
                            border_radius=10,
                        ),
                        ft.Text('Biometria  ', size=20),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    bgcolor=ft.colors.BLUE_GREY_900,
                    width=350,
                    height=80,
                    on_click=btn_img_bio_nivel01,
                ),

                # Criando o segundo botao, com a imagem do nivel 02
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Image(
                            src='img/bio_ind_L.jpg',
                            width=80,
                            height=80,
                            fit=ft.ImageFit.CONTAIN,
                            border_radius=10,
                        ),
                        ft.Text('Biometria  ', size=20),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    bgcolor=ft.colors.BLUE_GREY_900,
                    width=350,
                    height=80,
                    on_click=btn_img_bio_nivel02,
                ),

                # Criando o terceiro botao, com a imagem do nivel 03
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Image(
                            src='img/bio_ind_R.jpg',
                            width=80,
                            height=80,
                            fit=ft.ImageFit.CONTAIN,
                            border_radius=10,
                        ),
                        ft.Text('Biometria  ', size=20),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    bgcolor=ft.colors.BLUE_GREY_900,
                    width=350,
                    height=80,
                    on_click=btn_img_bio_nivel03,
                ),
            ], alignment='center', spacing=10),
            actions=[
                ft.TextButton('Fechar', on_click=close_dialog),
            ]
        )

#Inicio das funções e a criação da tela 'Primeiro acesso'


        def record_access_db(access_user, access_num_registration, access_password, print_byte):
            db = Connector_BD()

            crypt_passw = bcrypt.hashpw(access_password.value.encode(), bcrypt.gensalt())

            sql = "INSERT INTO login (username, number_registration, passw, fingerprint_image) VALUES (%s, %s, %s, %s)"
            query = (access_user.value, access_num_registration.value, crypt_passw, print_byte)

            try:
                db.mycursor.execute(sql, query)
                db.mydb.commit()
                return True
            except mysql.connector.Error as err:
                print("Erro ao inserir no banco: {}".format(err))
                page.snack_bar = ft.SnackBar(
                    content=ft.Text(value='Error {}'.format(err)),
                    bgcolor='red',
                    action='OK',
                    duration=5000
                )
                page.snack_bar.open = True
                return False

        def btn_registration_bio(e):
            page.dialog = dialog_select_img
            dialog_select_img.open = True
            page.update()


        def btn_register(e):
            global print_byte
            if access_user.value == '' or access_num_registration.value == '' or access_password.value == '' or access_confirm_password.value == '' :
                print("Preencha todos os campos!!")
                page.snack_bar = ft.SnackBar(
                    content=ft.Text(value='Preencha todos os campos'),
                    bgcolor='red',
                    action='OK',
                    duration=3000
                )
                page.snack_bar.open = True
                page.update()
            else:
                if access_password.value == access_confirm_password.value:
                    success = record_access_db(access_user, access_num_registration, access_password, print_byte)

                    if success:
                        print("Dados salvos com sucesso!")
                        page.snack_bar = ft.SnackBar(
                            content=ft.Text(value='Dados salvos com sucesso!'),
                            bgcolor='green',
                            action='OK',
                            duration=3000
                        )
                        page.snack_bar.open = True
                        from view.login import Login

                        login = Login()
                        login.main(page)
                        screen_first_access.visible = False
                        page.update()
                    else:
                        print("Erro ao salvar os dados ")
                        page.snack_bar = ft.SnackBar(
                            content=ft.Text(value='Erro ao salvar os dados!'),
                            bgcolor='red',
                            action='OK',
                            duration=3000
                        )
                        page.snack_bar.open = True

                    access_user.value = None
                    access_num_registration.value = None
                    access_password.value = None
                    access_confirm_password.value = None
                    page.update()
                else:
                    print("As senha tem que ser iguais!")




        def btn_back(e):
            from view.login import Login

            login = Login()
            login.main(page)
            screen_first_access.visible = False
            page.update()


        access_user = ft.TextField(
            hint_text='Usuario',
            width=350,
            height=50,
            border_radius=30,
            prefix_icon=ft.icons.PERSON,
            keyboard_type=ft.KeyboardType.EMAIL,
            bgcolor='black',
        )

        access_num_registration = ft.TextField(
            hint_text='Numero do Registro',
            width=350,
            height=50,
            border_radius=30,
            prefix_icon=ft.icons.CONTACT_PAGE,
            # keyboard_type=ft.KeyboardType.EMAIL,
            bgcolor='black',
        )

        access_password = ft.TextField(
            hint_text='Senha',
            width=350,
            height=50,
            border_radius=30,
            prefix_icon=ft.icons.LOCK,
            password=True,
            can_reveal_password=True,
            keyboard_type=ft.KeyboardType.VISIBLE_PASSWORD,
            bgcolor='black',

        )

        access_confirm_password = ft.TextField(
            hint_text='Confirme a senha',
            width=350,
            height=50,
            border_radius=30,
            prefix_icon=ft.icons.LOCK,
            password=True,
            can_reveal_password=True,
            keyboard_type=ft.KeyboardType.VISIBLE_PASSWORD,
            # keyboard_type=ft.KeyboardType.EMAIL,
            bgcolor='black',
        )

        #Criando Tela de primeiro acesso
        screen_first_access  = ft.Column([
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
                                    top=25,
                                    bottom=12,
                                ),

                                content=ft.Column([
                                    ft.Text(
                                        value='Primeiro Acesso',
                                        weight='bold',
                                        size=25,
                                        color='black',
                                    )
                                ])
                            ),
                            ft.Column([
                                access_user,
                                access_num_registration,
                                access_password,
                                access_confirm_password,

                            ], spacing=8),

                            ft.Column([
                                ft.ElevatedButton(
                                    text='Cadastrar Biometria',
                                    color='white',
                                    width=350,
                                    height=50,
                                    on_click=btn_registration_bio,
                                    icon='fingerprint',
                                ),

                                ft.ElevatedButton(
                                    text='Registrar',
                                    color='white',
                                    width=350,
                                    height=50,
                                    on_click=btn_register,
                                    icon=ft.icons.CONTACT_PAGE
                                ),

                                ft.Container(
                                    content=ft.TextButton('Voltar',
                                                          style=ft.ButtonStyle(color='black'),
                                                          on_click=btn_back,
                                                          ),
                                    alignment=ft.alignment.bottom_right,
                                    padding=ft.padding.only(right=10, top=100),
                                ),

                            ], horizontal_alignment='center'),
                        ], horizontal_alignment='center'),
                    )
                ], horizontal_alignment='center', alignment='center'),
            )
        ])

        page.add(screen_first_access)




if __name__ == '__main__':
    access = First_Access()
    ft.app(target=access.main)