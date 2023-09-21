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
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Добавить вкладку"),
            content=TextField(label="Название вкладки", ),
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        self.tabs = Tabs(scrollable=True)


    def build(self):
        # self.layout = AppLayout(
        #     app=self,
        #     page=self.page,
        #     tabs=self.tabs
        # )
        # return self.
        return self.tabs
    
    def add_tab(self, e):
        button_name = e.control.data
        pic = "question_mark"
        if button_name == "Graphic":
            pic = "area_chart"
        elif button_name == "Image":
            pic = "image"
            
        text=self.dlg_modal.content.value
        
        tab = Tab(
            text=self.dlg_modal.content.value,
            tab_content=Row(
                controls=[
                    Icon(name=pic),
                    Text(value=text),
                    IconButton(icon=icons.CLOSE, on_click=None),
                ]
            ),
            content=Column(
                controls=[
                    Text("param1 "+text),
                    Text("param2 "+text),
                    Text("param3 "+text),
                ]
            ),
        )
        self.tabs.tabs.append(tab)
        self.close_dlg(self)
        

    def open_dlg_modal(self, e):
        button_name = e.control.data
        if button_name == "Graphic":
            self.dlg_modal.title.value = "Добавить график"
        elif button_name == "Image":
            self.dlg_modal.title.value  = "Добавить изображение"
        else:
            self.dlg_modal.title.value = "Добавить вкладку"

        self.dlg_modal.actions = [
            ft.TextButton("Добавить", data=button_name, on_click=self.add_tab),
            ft.TextButton("Отмена", data=button_name, on_click=self.close_dlg)
        ]
        
        self.page.dialog = self.dlg_modal
        self.dlg_modal.open = True
        self.page.update()

    def close_dlg(self, e):
        self.dlg_modal.open = False
        self.dlg_modal.content.value = ""
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

