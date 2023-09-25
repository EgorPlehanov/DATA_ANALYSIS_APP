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
    Page,
    alignment
)
from function_card import FunctionCard
import flet as ft



class GraphicArea(Row):
    def __init__(self, app, page : Page):
        super().__init__()
        self.app = app
        self.page = page
        self.spacing = 0
        self.ref_function_card = Ref[Container]()
        self.list_functions_data = []
        self.list_functions_edit = []
        self.list_functions_analis = []
        self.list_function_parameters=[]
        self.ref_dropdown_data = Ref[Dropdown]()
        self.ref_dropdown_edit = Ref[Dropdown]()
        self.ref_dropdown_analis = Ref[Dropdown]()
        self.function_menu = Container(
            bgcolor=colors.BLACK26,
            # border=border.all(color=colors.ORANGE),
            alignment=alignment.top_center,
            width=350,
            content=Column(
                tight=True,
                scroll=ScrollMode.AUTO,
                controls=[
                    Container(
                        # border=border.all(color=colors.GREEN),
                        bgcolor=colors.BLUE_GREY_900,
                        padding=5,
                        content=Column(
                            controls=[
                                Text("Данные"),
                                Row(
                                    controls=[
                                        Dropdown(
                                            ref=self.ref_dropdown_data,
                                            dense=True,
                                            value="trend",
                                            options=[
                                                dropdown.Option(key='trend', text="Trends"),
                                                dropdown.Option(key='download', text="Загрузить свои данные"),
                                            ]
                                        ),
                                        IconButton(icon="add", on_click=lambda _: self.add_function_to_list(self.ref_dropdown_data, self.list_functions_data)),
                                    ]
                                ),
                                Column(
                                    controls=self.list_functions_data
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
        )
        self.parameters_menu = Container(
            padding=5,
            alignment=alignment.top_center,
            bgcolor=colors.BLACK12,
            border=border.all(colors.BLACK),
            content=Column(
                tight=True,
                scroll=ScrollMode.AUTO,
                controls=[
                    Row(
                        controls=[
                            # Text('Параметры'),
                            # IconButton(icon="KEYBOARD_ARROW_LEFT"),
                            # IconButton(icon="KEYBOARD_ARROW_RIGHT"),
                        ]
                    ),
                    Column(
                        controls=self.list_function_parameters
                    )
                ]
            )
        )
        self.controls = [
            self.function_menu,
            self.parameters_menu,
            Container(
                expand=True,
                border=border.all(colors.BLACK),
                content=Tabs(
                    tabs=[
                        Tab(
                            text="Данные",
                            content=Container(
                                border=border.all(color=colors.GREEN),
                                expand=False,
                                bgcolor=colors.BLUE_GREY_900,
                                padding=5,
                                content=Row(
                                    controls=[
                                        Text('Тренды'),
                                    ]
                                ),
                            ),
                        ),
                        Tab(
                            text="Обработка",
                            content=Container(
                                expand=True,
                                border=border.all(colors.BLACK),
                                content=Row(
                                    controls=[
                                        Text('График')
                                    ]
                                )
                            )
                        ),
                        Tab(
                            text="Анализ",
                            content=Container(
                                expand=True,
                                border=border.all(colors.BLACK),
                                content=Row(
                                    controls=[]#self.list_function_parameters
                                )
                            )
                        )
                    ]
                ),
            )
        ]

    def add_function_to_list(self, ref: Ref[Dropdown], list_functions):
        function_name = ref.current.value
        if function_name:
            function_card = FunctionCard(self, self.app, self.page, function_name, self.change_selected_function)
            list_functions.append(function_card)
            self.list_function_parameters.append(function_card.get_parameters())
            self.update()


    def change_selected_function(self, e):

        function_card = e.control.data
        selected_function = self.ref_function_card.current
        
        if function_card != selected_function:
            if selected_function is not None:
                selected_function.on_click_selected(e)
            self.ref_function_card.current = function_card
        else:
            self.ref_function_card.current = None
        
        function_card.on_click_selected(e)
        self.update()