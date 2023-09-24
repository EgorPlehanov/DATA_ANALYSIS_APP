import flet as ft
from flet import (
    Row,
    Container,
    colors,
    border,
    Column,
    ScrollMode,
    Text,
    Dropdown,
    dropdown,
    IconButton,
    Tabs,
    Tab,
    Ref,
    UserControl,
)

class Function(UserControl):
    def __init__(self, app, graphic_area, name):
        super().__init__()
        self.app = app
        self.graphic_area = graphic_area
        self.name = name
        self.content = Column(
            tight=True,
            controls=[
                Row(
                    controls=[
                        Text(value=self.name),
                    ]
                ),
                Row(
                    controls=[
                        Text(value="""
Параметр1 : **"""+self.name+"""**
Параметр2 : **"""+self.name+"""**
Параметр3 : **"""+self.name+"""**
"""),
                    ]
                )
            ]
        )

    def build(self):
        return Container(
            content=self.content,
            on_click=self.my_on_click,
            border = border.all(color=colors.BLUE)
        )

    def my_on_click(self, e):
        print('self.name: ', self.name)
        # self.name = '111111111111111111'
        # self.update()

    # def my_on_hover(self):
    #     self.bgcolor = colors.GREEN



class GraphicArea(Row):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.list_functions_data = []
        self.list_functions_edit = []
        self.list_functions_analis = []
        self.list_function_parameters=[]
        self.ref_dropdown_data = Ref[Dropdown]()
        self.ref_dropdown_edit = Ref[Dropdown]()
        self.ref_dropdown_analis = Ref[Dropdown]()
        self.controls = [
            Container(
                bgcolor=colors.BLACK26,
                border=border.all(color=colors.ORANGE),
                alignment=ft.alignment.top_center,
                width=350,
                content=Column(
                    tight=True,
                    scroll=ScrollMode.AUTO,
                    controls=[
                        Container(
                            border=border.all(color=colors.GREEN),
                            expand=False,
                            bgcolor=colors.BLUE_GREY_900,
                            padding=5,
                            # border=border.all(colors.BLACK),
                            content=Column(
                                # expand=False,
                                controls=[
                                    Text("Данные"),
                                    Row(
                                        alignment=ft.MainAxisAlignment.NONE,
                                        controls=[
                                            Dropdown(
                                                ref=self.ref_dropdown_data,
                                                dense=True,
                                                options=[
                                                    dropdown.Option(key='trend', text="Trends"),
                                                    dropdown.Option(key='download', text="Загрузить свои данные"),
                                                ]
                                            ),
                                            IconButton(icon="add", on_click=lambda _: self.add_function_to_list(self.ref_dropdown_data, self.list_functions_data)),
                                        ]
                                    ),
                                    Column(
                                        tight=True,
                                        controls=self.list_functions_data
                                    )
                                    # Container(
                                        # expand=True,
                                    #     border=border.all(color=colors.PINK),
                                    #     content=Column(
                                    #         tight=True,
                                    #         controls=self.list_functions_data
                                    #     )
                                    # )
                                ]
                            )
                        ),
                        Container(
                            bgcolor=colors.BLUE_GREY_900,
                            padding=5,
                            # border=border.all(colors.BLACK),
                            content=Column(
                                controls=[
                                    Text("Обработка"),
                                    Row(
                                        controls=[
                                            Dropdown(
                                                ref=self.ref_dropdown_edit,
                                                dense=True,
                                                options=[
                                                    dropdown.Option("Смешение"),
                                                    dropdown.Option("Шум"),
                                                ]
                                            ),
                                            IconButton(icon="add", on_click=lambda _: self.add_function_to_list(self.ref_dropdown_edit, self.list_functions_edit)),
                                        ]
                                    ),
                                    Column(
                                        controls=self.list_functions_edit
                                    )
                                ]
                            )
                        ),
                        Container(
                            bgcolor=colors.BLUE_GREY_900,
                            padding=5,
                            # border=border.all(colors.BLACK),
                            content=Column(
                                controls=[
                                    Text("Анализ"),
                                    Row(
                                        controls=[
                                            Dropdown(
                                                ref=self.ref_dropdown_analis,
                                                dense=True,
                                                options=[
                                                    dropdown.Option("Аналитическая функция 1"),
                                                    dropdown.Option("Аналитическая функция 2"),
                                                    dropdown.Option("Аналитическая функция 3"),
                                                ]
                                            ),
                                            IconButton(icon="add", on_click=lambda _: self.add_function_to_list(self.ref_dropdown_analis, self.list_functions_analis)),
                                        ]
                                    ),
                                    Column(
                                        controls=self.list_functions_analis
                                    )
                                ]
                            )
                        ),
                    ]
                )
            ),
            Container(
                border=border.all(colors.BLACK),
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
                            controls=self.list_function_parameters
                        )
                    ]
                )
            ),
            Container(
                expand=True,
                border=border.all(colors.BLACK),
                content=Column(
                    controls=[
                        Tabs(
                            tabs=[
                                Tab(text="Tab 1",),
                                Tab(text="Tab 2",),
                                Tab(text="Tab 3",)
                            ]
                        ),
                        Container(
                            expand=True,
                            border=border.all(colors.BLACK),
                            content=Row(
                                controls=self.list_functions_data
                                # [
                                #     Text('График')
                                # ]
                            )
                        )

                    ]
                )
            )
        ]

    def add_function_to_list(self, ref: Ref[Dropdown], list_functions):
        function_name = ref.current.value
        if function_name:
            list_functions.append(Function(self.app, self, function_name))
            self.update()
