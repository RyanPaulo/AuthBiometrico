import os
import sys
import flet as ft


from models.connector_bd import Connector_BD
from view.login import Treatment_User, Login
# from main import AuthBiometrico



#Class responsavel por desenhar a tela de 'Acesso' e suas funções
#Onde cotem os dados que os usuarioa estao tentando acessar
class Access:
    def main(self, page: ft.Page):
        page.window_width = 1200
        page.window_height = 800
        page.theme_mode = 'dark'
        page.vertical_alignment = 'center'
        page.horizontal_alignment = 'center'
        page.window.resizable = False
        page.window_center()

        info_container = ft.Column()
        options_container = ft.Column()

        # Função para checar o nivel de acesso
        def consult_level():
            db = Connector_BD()
            log = Treatment_User().get_user()

            if not log:
                return

            # Consultar no banco de dados o numero de registro de quem esta logado
            db.mycursor.execute("SELECT number_registration FROM login WHERE username = %s", (log,))
            result = db.mycursor.fetchone()

            if result and result[0].endswith("02"):  # Se o numero de registro tiver final 02 exibir botao refente
                if not level02_btn.visible:
                    title_text.color = ft.colors.BLUE
                    level02_btn.visible = True
            elif result and result[0].endswith("03"):  # Se o numero de registro tiver final 03 exibir botao refente
                if not level03_btn_1.visible and not level03_btn_2.visible and not level02_btn.visible:
                    title_text.color = ft.colors.BLACK
                    level02_btn.visible = True
                    level03_btn_1.visible = True
                    level03_btn_2.visible = True
            else:
                if level02_btn.visible:
                    level02_btn.visible = False

                if level03_btn_1.visible and level03_btn_2.visible:
                    level03_btn_1.visible = False
                    level03_btn_2.visible = False

                title_text.color = ft.colors.WHITE

            db.mycursor.close()
            db.close()
            page.update()

        # Funções da ação dos botões
        def btn_esperanca(e):
            info_container.controls.clear()  # limpar o conteiner de informações
            info_container.controls.append(info_btn_esperanca)

            page.update()

        def btn_recanto(e):
            info_container.controls.clear()  # limpar o conteiner de informações
            info_container.controls.append(info_btn_recanto)

            page.update()

        def btn_a(e):
            info_container.controls.clear()  # limpar o conteiner de informações
            info_container.controls.append(info_btn_a)

            page.update()

        def btn_level02(e):
            info_container.controls.clear()  # limpar o conteiner de informações
            info_container.controls.append(info_btn_level02)

            page.update()

        def btn_level03(e):
            info_container.controls.clear()  # limpar o conteiner de informações
            info_container.controls.append(info_btn_level03)

            page.update()

        def btn_levell03(e):
            info_container.controls.clear()  # limpar o conteiner de informações
            info_container.controls.append(info_btn_levell03)

            page.update()

        def btn_close(e):
            Treatment_User().logout()

            e.page.window_close()

            os.execv(sys.executable, [sys.executable, "main.py"])


        #
        title_text = ft.Text(
            value='Ministério do Meio Ambiente',
            weight='bold',
            size=50,
            color='white',
            text_align=ft.TextAlign.CENTER,
            font_family='Times new roman',
        )

        info_btn_esperanca = ft.Text(
            value='''
                "ID": "001",
                "Nome da Propriedade": "Fazenda Esperança",
                "Localização": "São Paulo, Ribeirão Preto",
                "Tipo de Cultura": "Soja",
                "Uso de Agrotóxicos Permitidos": "Sim",
                "Área Cultivada (ha)": "250"
            ''',
            size=20,
            color='black',
        )

        info_btn_recanto = ft.Text(
            value='''
                Teste recanto#####
                ####
                ####
                ####
            ''',
            size=20,
            color='black',
        )

        info_btn_a = ft.Text(
            value='''
                Teste 01 a#####
                ####
                ####
                ####
            ''',
            size=20,
            color='black',
        )

        info_btn_level02 = ft.Text(
            value='''
                Teste 02#####
                ####
                ####
                ####
            ''',
            size=20,
            color='black',
        )

        info_btn_level03 = ft.Text(
            value='''
                Teste 03#####
                ####
                ####
                ####
            ''',
            size=20,
            color='black',
        )

        info_btn_levell03 = ft.Text(
            value='''
                Teste botão 03#####
                ####
                ####
                ####
            ''',
            size=20,
            color='black',
        )


        level01_btn_esperanca = ft.ElevatedButton(
            text='Dados da Fazenda Esperança',
            color='white',
            on_focus=ft.colors.BLUE_GREY_900,
            width=250,
            height=50,
            on_click=btn_esperanca,
        )

        level01_btn_recanto = ft.ElevatedButton(
            text='Dados da Fazenda Recanto',
            color='white',
            on_focus=ft.colors.BLUE_GREY_900,
            width=250,
            height=50,
            on_click=btn_recanto,
        )

        level01_btn_a = ft.ElevatedButton(
            text='Dados da Fazenda Novo Sol',
            color='white',
            on_focus=ft.colors.BLUE_GREY_900,
            width=250,
            height=50,
            on_click=btn_a,
        )

        level02_btn = ft.ElevatedButton(
            text='************ nivel02',
            color='white',
            on_focus=ft.colors.BLUE_GREY_900,
            width=250,
            height=50,
            on_click=btn_level02,
            visible=False,
        )

        level03_btn_1 = ft.ElevatedButton(
            text='************ nivel03',
            color='white',
            on_focus=ft.colors.BLUE_GREY_900,
            width=250,
            height=50,
            on_click=btn_level03,
            visible=False,
        )

        level03_btn_2 = ft.ElevatedButton(
            text='************ nivel03',
            color='white',
            on_focus=ft.colors.BLUE_GREY_900,
            width=250,
            height=50,
            on_click=btn_levell03,
            visible=False,
        )



        # Desenhando a tela de acesso
        screen_access = ft.Column([
            ft.Container(
                bgcolor=ft.colors.BLUE_GREY_900,
                width=page.window_width - 20,
                height=page.window_height - 70,
                border_radius=10,

                content=ft.Column([
                    ft.Container(
                        alignment=ft.alignment.center,
                        padding=ft.padding.only(top=5),

                        content=ft.Column([
                            title_text,
                        ])
                    ),

                    ft.Row(
                        controls=[

                            #Container para as opções
                            ft.Container(

                                bgcolor=ft.colors.GREY_300,
                                width=250,
                                height=630,
                                border_radius=10,

                                content=ft.Column([
                                    ft.Container(
                                        padding=ft.padding.only(
                                          top=3,
                                            bottom=3,
                                        ),
                                    ),

                                    ft.Text(
                                        text_align=ft.TextAlign.CENTER,
                                        value=' Opcões',
                                        weight='bold',
                                        size=20,
                                        color='black',
                                    ),

                                    level01_btn_esperanca,
                                    level01_btn_recanto,
                                    level01_btn_a,
                                    level02_btn,
                                    level03_btn_1,
                                    level03_btn_2,

                                    ft.Container(
                                        ft.TextButton(
                                            text='Sair',
                                            style=ft.ButtonStyle(color='black',),
                                            on_click=btn_close,
                                        ),
                                        alignment=ft.alignment.bottom_right,
                                        padding=ft.padding.only(top=10),
                                    ),


                                ]),
                                ref=options_container,
                            ),

                            #Container para exibir as informações
                            ft.Container(
                                bgcolor=ft.colors.GREY_300,
                                width=880,
                                height=630,
                                border_radius=10,
                                padding=ft.padding.only(top=20),
                                content=info_container,
                            ),
                        ], alignment=ft.MainAxisAlignment.CENTER),
                ])
            )
        ])

        consult_level()
        page.add(screen_access)
        page.update(screen_access)


if __name__ == '__main__':
    access = Access()
    ft.add(target=access.main)