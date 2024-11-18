import os
import sys
import cv2
import flet as ft
import mysql
from flet_core import FilePickerResultEvent, FilePicker
from view.login import Treatment_User, print_byte
from models.auth_biometric import Img_Biometric
from models.connector_bd import Connector_BD


#Class responsavel por desenhar a tela de 'Verificação' e suas funções
class Verification:
    def main (self, page: ft.Page):
        page.window_width=800
        page.window_height=800
        page.theme_mode='dark'
        page.vertical_alignment='center'
        page.horizontal_alignment='center'
        page.window.resizable=False
        page.window_center()

        treatment = Treatment_User()
        user = treatment.get_user()



# Funções da tela de verificação

        def verification_img(compare_img):
            biometrics = Img_Biometric(compare_img)
            db = Connector_BD()

            try:
                db.mycursor.execute("SELECT fingerprint_image FROM login WHERE username = %s", (user,))
                record = db.mycursor.fetchone()

                if record is None:
                    print(f"Erro: Nenhum dado encontrado para o usuario, {user}")
                    db.mycursor.close()
                    db.close()
                    return

                if record[0] is None:
                    print(f"Erro: Nenhuma imagem biometrica armazenada para este usuario, {user}.")
                    db.mycursor.close()
                    db.close()
                    return

                # Converte a imagem armazenada para o formato original
                converted_img = biometrics.byte_to_img(record[0])
                # Carrega a imagem adquiridia para a comparação
                acquisition_img = cv2.imread(compare_img)

                print("Biometria armazenada no banco de dados: ")
                print(converted_img[2])

                print("\nBiometria capturada para comparação: ")
                print(acquisition_img[2])


                if biometrics.match_fingerprints(converted_img):
                    from view.access import Access

                    a = Access()
                    a.main(page)

                    screen_verification.visible = False
                    page.update()

                    print("Autenticação biometrica bem-sucedida!")
                    page.snack_bar = ft.SnackBar(
                        content=ft.Text(value=f'Acesso autorizado ao {user}'),
                        bgcolor='green',
                        action='OK',
                        duration=3000
                    )
                    page.snack_bar.open = True
                    page.update()
                else:
                    print("autenticação falhou.")
                    page.snack_bar = ft.SnackBar(
                        content=ft.Text(value='Autenticação falhou!'),
                        bgcolor='red',
                        action='OK',
                        duration=3000
                    )
                    page.snack_bar.open = True
                    db.mycursor.reset(self)
                    page.update()

            except mysql.connector.Error as err:
                print(f"Erro ao acessar o banco de dados: {err}")
                return
            finally:
                if db.mycursor is not None:
                    db.mycursor.close()
                if db.mydb is not None:
                    db.close()

            page.update()


        def on_file_selected(event: FilePickerResultEvent):
            global print_byte

            if event.files:
                print_byte = event.files[0].path
                verification_img(print_byte)

                print("Biometria selecionada:", print_byte)
            else:
                print("Nenhuma img foi selecionada")

        file_picker = FilePicker(on_result=on_file_selected)
        page.overlay.append(file_picker)
        page.update()

        def btn_verication_bio(e):
            file_picker.pick_files(
                allow_multiple=False,
                file_type="image",

            )
            page.update()


        def btn_back(e):
            Treatment_User().logout()

            os.execv(sys.executable, [sys.executable, "main.py"])

            from view.login import Login
            login = Login()
            login.main(page)
            screen_verification.visible = False
            page.update()


        #Criar tela de verificação biometrica
        screen_verification = ft.Column([
            ft.Container(
                bgcolor=ft.colors.BLUE_GREY_900,
                width=page.window_width - 30,
                height=page.window_height - 70,
                border_radius=10,

                content=ft.Column([  # quadro principal
                    ft.Container(
                        bgcolor=ft.colors.GREY_500,
                        width=450,
                        height=600,
                        border_radius=10,
                        padding=ft.padding.only(top=20),

                        content=ft.Column([
                            ft.Container(
                                padding=ft.padding.only(
                                    top=10,
                                    bottom=12
                                ),

                                content=ft.Container(
                                    content=ft.Icon(
                                        name='fingerprint',
                                        size=250,
                                        color=ft.colors.BLUE_GREY_900
                                    ),
                                    alignment=ft.alignment.center,
                                    padding=ft.padding.only(bottom=15, top= 25)
                                ),
                            ),


                            ft.Column([

                                ft.ElevatedButton(
                                    text='Vericar Biometria por imagem',
                                    color='white',
                                    width=350,
                                    height=50,
                                    on_click=btn_verication_bio,
                                    icon='fingerprint'

                                ),

                            ]),
                            ft.Container(
                                content=ft.TextButton(
                                    'Voltar',
                                    style=ft.ButtonStyle(color='black'),
                                    on_click=btn_back,
                                ),
                                alignment=ft.alignment.bottom_right,
                                padding=ft.padding.only(right=10, top=150)
                            ),

                        ], horizontal_alignment='center', alignment=''),

                    )

                ], horizontal_alignment='center', alignment='center')
            )

        ])

        page.add(screen_verification)



if __name__ == '__main__':
    ver = Verification()
    ft.app(target=ver.main)