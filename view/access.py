import os
import sys
import flet as ft
from models.connector_bd import Connector_BD
from view.login import Treatment_User

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

        def btn_novo_sol(e):
            info_container.controls.clear()  # limpar o conteiner de informações
            info_container.controls.append(info_btn_sol)

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
      Fazenda Esperança

    • ID: 001
    • Nome da Propriedade: Fazenda Esperança
    • Localização: São Paulo, Ribeirão Preto
    • Tipo de Cultura: Soja
    • Uso de Agrotóxicos: Permitido
    • Área Cultivada: 250 hectares
    • Proprietário: João da Silva
    • Número de Funcionários: 25
    • Certificações Ambientais: Sim (ISO 14001)
    • Sistema de Irrigação: Irrigação por aspersão
    • Ano de Fundação: 2005
    • Observações: Fazenda com práticas sustentáveis e uso moderado 
    de agrotóxicos.
            ''',
            size=25,
            color='black',
        )

        info_btn_recanto = ft.Text(
            value='''
    Fazenda Recanto

    • ID: 002
    • Nome da Propriedade: Fazenda Recanto
    • Localização: Minas Gerais, Uberlândia
    • Tipo de Cultura: Milho
    • Uso de Agrotóxicos: Não permitido
    • Área Cultivada: 180 hectares
    • Proprietário: Maria Oliveira
    • Número de Funcionários: 15
    • Certificações Ambientais: Sim (Orgânico)
    • Sistema de Irrigação: Irrigação por gotejamento
    • Ano de Fundação: 2012
    • Observações: Fazenda orgânica, sem uso de agrotóxicos, com foco em 
    práticas de agricultura regenerativa.
            ''',
            size=25,
            color='black',
        )

        info_btn_sol = ft.Text(
            value='''
    Fazenda Novo Sol

    • ID: 003
    • Nome da Propriedade: Fazenda Novo Sol
    • Localização: Paraná, Maringá
    • Tipo de Cultura: Cana-de-açúcar
    • Uso de Agrotóxicos: Permitido
    • Área Cultivada: 300 hectares
    • Proprietário: Carlos Souza
    • Número de Funcionários: 40
    • Certificações Ambientais: Em processo de certificação (Renovável)
    • Sistema de Irrigação: Irrigação automatizada
    • Ano de Fundação: 1998
    • Observações: Fazenda com produção em larga escala e tecnologia 
    avançada de manejo de solo e água.
            ''',
            size=25,
            color='black',
        )

        info_btn_level02 = ft.Text(
            value='''
        Fazenda Esperança
        • ID: 001
        • Nome da Propriedade: Fazenda Esperança
        • Localização: São Paulo, Ribeirão Preto
        • Tipo de Cultura: Soja
        • Agrotóxicos usados: Glifosato, Paraquate, Atrazina, Glufosinato, 2,4-D, 
        Óleo mineral
        • Lucro do ultimo mes: R$ 3 bilhão 
        • Crientes : Danone
            
         Fazenda Recanto
        • ID: 002
        • Nome da Propriedade: Fazenda Recanto
        • Localização: Minas Gerais, Uberlândia
        • Tipo de Cultura: Milho
        • Uso de Agrotóxicos: Não permitido
        • Lucro do ultimo mes: R$ 5 bilhão 
        • Crientes : Nestlé
        
        Fazenda Novo Sol
        • ID: 003
        • Nome da Propriedade: Fazenda Novo Sol
        • Tipo de Cultura: Cana-de-açúcar
        • Agrotóxicos usados: sulfentrazone, imazapir, trifloxissulfurom sódico, 
        paraquate, tebutiurom e imazapique
        • Lucro do ultimo mes: R$ 1 bilhão 
        • Crientes : Raizen
                ''',
            size=15,
            color='black',
        )

        info_btn_level03 = ft.Image(
            src='img/comparativo.jpg',
            height=500,
        )

        info_btn_levell03 = ft.Text(
            spans=[
                ft.TextSpan(
                    '''
                    Funcionario: Ryan Paulo Silva
                    • Função: Gerente Administrativo
                    • Número de Regidtro : 55902
                    • RA: G571AAF-4
                    • Turma: CC6Q33
                    ''',
                    style=ft.TextStyle(size=20, color="black"),
                ),
                ft.TextSpan(
                    "Acessar Documeto\n",
                    style=ft.TextStyle(
                        size=10,
                        color="blue",
                        decoration=ft.TextDecoration.UNDERLINE
                    ),
                    on_click=lambda _: page.launch_url("https://www.linkedin.com/in/ryan-paulo-aa0b24175/")
                ),
                ft.TextSpan(
                    '''
                    Funcionario: Leo Cordeiro Sutil
                    • Função: Auxilie Administrativo
                    • Número de Regidtro : 55901
                    • RA: N0368J0
                    • Turma: CC5P33
                    ''',
                    style=ft.TextStyle(size=20, color="black"),
                ),
                ft.TextSpan(
                    "Acessar Documeto\n",
                    style=ft.TextStyle(
                        size=10,
                        color="blue",
                        decoration=ft.TextDecoration.UNDERLINE
                    ),
                    on_click=lambda _: page.launch_url("https://www.instagram.com/leoh.cordeiro?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw==")
                ),
                ft.TextSpan(
                    '''
                    Funcionario: ISABELLE RAMOS CEDRO 
                    • Função: Ministre do Meio Ambiente
                    • Número de Regidtro : 55803
                    • RA: F346CJ4
                    • Turma: CC6P33
                    ''',
                    style=ft.TextStyle(size=20, color="black"),
                ),
                ft.TextSpan(
                    "Acessar Documeto",
                    style=ft.TextStyle(
                        size=10,
                        color="blue",
                        decoration=ft.TextDecoration.UNDERLINE
                    ),
                    on_click=lambda _: page.launch_url(
                        "https://www.instagram.com/isacedro_?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw==")
                ),
            ]
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
            on_click=btn_novo_sol,
        )

        level02_btn = ft.ElevatedButton(
            text='Relatórios Detalhados',
            color='white',
            on_focus=ft.colors.BLUE_GREY_900,
            width=250,
            height=50,
            on_click=btn_level02,
            visible=False,
        )

        level03_btn_1 = ft.ElevatedButton(
            text='Comparativo de Lucro',
            color='white',
            on_focus=ft.colors.BLUE_GREY_900,
            width=250,
            height=50,
            on_click=btn_level03,
            visible=False,
        )

        level03_btn_2 = ft.ElevatedButton(
            text='Funcionários do Ministério',
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
                                # padding=ft.padding.only(top=2),
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






