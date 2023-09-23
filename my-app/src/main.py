import itertools
import flet as ft
from flet import (
    Page,
    UserControl,
    Column,
    colors,
    theme,
    Container,
    Row,
    AppBar,
    FilledButton,
    IconButton,
    icons,
    Text,
    TextField,
    Tabs,
    Tab,
    Icon
) 
from app_layout import AppLayout

import json


class DataAnalisisApp(UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.expand = True

        self.appbar = AppBar(
            leading=ft.Icon(ft.icons.ANALYTICS),
            leading_width=40,
            title=ft.Text(
                value="Data Analysis App",
                text_align="start"
            ),
            center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                Container(
                    content=Row(
                        controls=[
                            FilledButton(
                                data="Graphic",
                                text="График",
                                icon="add",
                                on_click=self.open_dlg_modal
                            ),
                            FilledButton(
                                data="Image",
                                text="Изображение",
                                icon="add",
                                on_click=self.open_dlg_modal
                            ),
                        ],
                    ),
                    margin=10
                )
            ],
        )
        self.page.appbar = self.appbar
        self.dlg_modal_add_tab = ft.AlertDialog(
            modal=True,
            title=ft.Text("Добавить вкладку"),
            content=TextField(label="Название вкладки", autofocus=True, on_submit=self.add_tab),
            actions = [
                ft.TextButton("Добавить", on_click=self.add_tab),
                ft.TextButton("Отмена", on_click=self.close_dlg)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        self.tabs_bar = Tabs()
        self.graphic_area = Row(
            controls=[
                Container(
                    border=ft.border.all(colors.BLACK),
                    content=Column(
                        controls=[
                            Container(
                                border=ft.border.all(colors.BLACK),
                                content=Column(
                                    controls=[
                                        Text("Данные"),
                                        Row(
                                            controls=[
                                                ft.Dropdown(
                                                    options=[
                                                        ft.dropdown.Option("Trends"),
                                                        ft.dropdown.Option("Загрузить свои данные"),
                                                    ]
                                                ),
                                                IconButton(icon="add", on_click=None),
                                            ]
                                        )
                                    ]
                                )
                            ),
                            Container(
                                border=ft.border.all(colors.BLACK),
                                content=Column(
                                    controls=[
                                        Text("Обработка"),
                                        Row(
                                            controls=[
                                                ft.Dropdown(
                                                    options=[
                                                        ft.dropdown.Option("Смешение"),
                                                        ft.dropdown.Option("Шум"),
                                                    ]
                                                ),
                                                IconButton(icon="add", on_click=None),
                                            ]
                                        )
                                    ]
                                )
                            ),
                            Container(
                                border=ft.border.all(colors.BLACK),
                                content=Column(
                                    controls=[
                                        Text("Анализ"),
                                        Row(
                                            controls=[
                                                ft.Dropdown(
                                                    options=[
                                                        ft.dropdown.Option("Аналитическая функция 1"),
                                                        ft.dropdown.Option("Аналитическая функция 2"),
                                                        ft.dropdown.Option("Аналитическая функция 3"),
                                                    ]
                                                ),
                                                IconButton(icon="add", on_click=None),
                                            ]
                                        )
                                    ]
                                )
                            )
                        ]
                    )
                ),
                Container(
                    border=ft.border.all(colors.BLACK),
                    content=Column(
                        controls=[
                            Row(
                                controls=[
                                    Text('Параметры'),
                                    IconButton(icon="KEYBOARD_ARROW_LEFT"),
                                    IconButton(icon="KEYBOARD_ARROW_RIGHT"),
                                ]
                            ),
                            Column(
                                controls=[
                                    Text('Параметр 1'),
                                    Text('Параметр 2'),
                                    Text('Параметр 3')
                                ]
                            )
                        ]
                    )
                ),
                Container(
                    border=ft.border.all(colors.BLACK),
                    content=Column(
                        controls=[
                            Tabs(
                                tabs=[
                                    Tab(text="Tab 1",),
                                    Tab(text="Tab 2",),
                                    Tab(text="Tab 3",)
                                ]
                            )
                        ]
                    )
                )
            ]
        )
        self.image_area = Row(
            controls=[
                Text('Область для работы с изображениями')
            ]
        )


    def build(self):
        # self.layout = AppLayout(
        #     app=self,
        #     page=self.page,
        #     tabs=self.tabs
        # )
        # return self.
        return self.tabs_bar
    
    def add_tab(self, e):
        button_name = self.dlg_modal_add_tab.data
        pic = "question_mark"
        tab_content = None
        match button_name:
            case "Graphic":
                pic = "area_chart"
                tab_content = self.graphic_area
            case "Image":
                pic = "image"
                tab_content = self.image_area
            
        text = self.dlg_modal_add_tab.content.value
        text = text if text else 'Вкладка ' + button_name
        

        tab_ref = ft.Ref[Tab]()
        tab = Tab(
            ref=tab_ref,
            tab_content=Row(
                controls=[
                    Icon(name=pic),
                    Text(value=text),
                    IconButton(icon=icons.CLOSE, data=tab_ref, on_click=self.delete_tab),
                ]
            ),
            content=tab_content
        )
        self.tabs_bar.tabs.append(tab)
        self.tabs_bar.selected_index = len(self.tabs_bar.tabs) - 1
        self.close_dlg(self)
    
    def delete_tab(self, e):
        deleted_tab = e.control.data.current
        self.tabs_bar.tabs.remove(deleted_tab)
        self.update()


    def open_dlg_modal(self, e):
        button_name = e.control.data
        match button_name:
            case "Graphic":
                self.dlg_modal_add_tab.title.value = "Добавить график"
            case "Image":
                self.dlg_modal_add_tab.title.value = "Добавить изображение"
            case _:
                self.dlg_modal_add_tab.title.value = "Добавить вкладку"
        
        self.dlg_modal_add_tab.data = button_name
        self.page.dialog = self.dlg_modal_add_tab
        self.dlg_modal_add_tab.open = True
        self.page.update()

    def close_dlg(self, e):
        self.dlg_modal_add_tab.open = False
        self.dlg_modal_add_tab.data = ''
        self.dlg_modal_add_tab.content.value = ''
        self.page.update()
        self.update()



def main(page: Page):
    page.title = "Data Analysis App"
    page.padding = 0
    # page.bgcolor = colors.BLUE_200
    app = DataAnalisisApp(page)
    page.add(app)
    page.update()

ft.app(main)

