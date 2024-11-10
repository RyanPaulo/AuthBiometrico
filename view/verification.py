import os
import sys
import cv2
import flet as ft
from  view.login import Treatment_User
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

        def btn_img_bio_nivel01(e):
            compare_img = "img/bio_pol_LM1.jpg"
            verification_img(compare_img)

            print('Imagem biometria Ryan Selecionada.')
            dialog_verifi_select_img.open = False
            page.update()

        def btn_img_bio_nivel02(e):
            compare_img = "img/bio_ind_L.jpg"
            verification_img(compare_img)

            print('Imagem biometria Ryan Selecionada.')
            dialog_verifi_select_img.open = False
            page.update()

        def btn_img_bio_nivel03(e):
            compare_img = "img/bio_ind_R.jpg"
            verification_img(compare_img)

            print('Imagem biometria Ryan Selecionada.')
            dialog_verifi_select_img.open = False
            page.update()
        
        
        def verification_img(compare_img):
            biometrics = Img_Biometric(compare_img)
            db = Connector_BD()

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

            converted_img = biometrics.byte_to_img(record[0])

            if converted_img is not None and cv2.norm(converted_img, biometrics.img, cv2.NORM_L2) < 10000:
                from view.access import Access

                a = Access()
                a.main(page)

                screen_verification.visible = False
                dialog_verifi_select_img.open = False
                page.update()

                print("Autenticação biometrica bem-sucedida!")
                page.snack_bar = ft.SnackBar(
                    content=ft.Text(value=f'Acesso autorizado ao {user}'),
                    bgcolor='green',
                    action='OK',
                    duration=3000
                )
                page.snack_bar.open = True
            else:
                print("autenticação falhou.")
                page.snack_bar = ft.SnackBar(
                    content=ft.Text(value='Autenticação falhou!'),
                    bgcolor='red',
                    action='OK',
                    duration=3000
                )
                page.snack_bar.open = True

            db.mycursor.close()
            db.close()
            dialog_verifi_select_img.open = False
            page.update()

        def btn_close_dialod(e):
            dialog_verifi_select_img.open = False
            page.update()


        dialog_verifi_select_img = ft.AlertDialog(
            bgcolor=ft.colors.BLUE_GREY_900,
            modal=True,
            title=ft.Text('Selecione sua biometria.'),
            content=ft.Column([
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Image(
                            src='img/bio_pol_LM1.jpg',
                            width=80,
                            height=80,
                            fit=ft.ImageFit.CONTAIN,
                            border_radius=10
                        ),
                        ft.Text('Biometria', size=20),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    bgcolor=ft.colors.BLUE_GREY_900,
                    width=350,
                    height=80,
                    on_click=btn_img_bio_nivel01,
                ),

                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Image(
                            src='img/bio_ind_L.jpg',
                            width=80,
                            height=80,
                            fit=ft.ImageFit.CONTAIN,
                            border_radius=10
                        ),
                        ft.Text('Biometria', size=20),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    bgcolor=ft.colors.BLUE_GREY_900,
                    width=350,
                    height=80,
                    on_click=btn_img_bio_nivel02
                ),

                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Image(
                            src='img/bio_ind_R.jpg',
                            width=80,
                            height=80,
                            fit=ft.ImageFit.CONTAIN,
                            border_radius=10
                        ),
                        ft.Text('Biometria', size=20),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    bgcolor=ft.colors.BLUE_GREY_900,
                    width=350,
                    height=80,
                    on_click=btn_img_bio_nivel03,
                ),

            ], alignment='center', spacing=10),
            actions=[
                ft.TextButton('Fechar', on_click=btn_close_dialod),

            ])

        #Funções da tela de verificação

        def btn_verication_bio(e):
            page.dialog = dialog_verifi_select_img
            dialog_verifi_select_img.open = True
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