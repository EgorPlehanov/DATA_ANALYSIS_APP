from typing import List
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
    def __init__(self, app, page: Page):
        super().__init__()
        self.app = app
        self.page = page
        self.spacing = 0

        # Ссылка на выбранную функцию
        self.ref_function_card = Ref[Container]()

        # Список функций блоков (данные/обработка/анализ)
        self.list_functions_data = []
        self.list_functions_edit = []
        self.list_functions_analis = []

        # Список параметров функций блоков (данные/обработка/анализ)
        self.list_function_parameters=[]

        # Ссылки на выпадающие списки блоков (данные/обработка/анализ)
        self.ref_dropdown_data = Ref[Dropdown]()
        self.ref_dropdown_edit = Ref[Dropdown]()
        self.ref_dropdown_analis = Ref[Dropdown]()

        self.function_menu_data_block = Container()

        # Меню работы с функциями
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
                                                dropdown.Option(key='data_download', text="Загрузить свои данные"),
                                            ]
                                        ),
                                        IconButton(icon="add", on_click=lambda _: self.add_function_to_list(self.ref_dropdown_data, self.list_functions_data, 'data')),
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
                                        IconButton(icon="add", on_click=lambda _: self.add_function_to_list(self.ref_dropdown_edit, self.list_functions_edit, 'edit')),
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
                                        IconButton(icon="add", on_click=lambda _: self.add_function_to_list(self.ref_dropdown_analis, self.list_functions_analis, 'analitic')),
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

        # Меню работы с параметрами
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

        # Область вывода результатов
        self.results_view = Container(
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

        # Содержимое виджета
        self.controls = [
            self.function_menu,
            self.parameters_menu,
            self.results_view,
        ]


    def add_function_to_list(self, ref: Ref[Dropdown], list_functions: List[FunctionCard], function_type: str) -> None:
        """
        Добавляет функцию в список.

        Args:
            ref (Ref[Dropdown]): Ссылка на выпадающий список.\n
            list_functions (List[FunctionCard]): Список функций блока (данные/обработка/анализ).
        """
        function_name = ref.current.value
        if not function_name:
            return

        function_card = FunctionCard(
            graphic_area=self,
            app=self.app,
            page=self.page,
            function_name=function_name,
            function_type=function_type,
            on_change_selected=self.change_selected_function,
            on_click_delete=self.delete_function,
        )

        # Добавляем в список для блока (данные/обработка/анализ)
        list_functions.append(function_card)
        # Добавляем параметры функции в списов
        self.list_function_parameters.append(function_card.get_parameters())
        self.update()


    def change_selected_function(self, e) -> None:
        '''
        Изменяет выделение функции при клике на нее в блоке функций (данные/обработка/анализ).

        Args:
            e (Event): Параметры события
        '''
        clicked_function_card = e.control.data
        selected_function = self.ref_function_card.current
        
        # Изменяем выделение нажатой функции
        clicked_function_card.change_selected(e)

        if clicked_function_card == selected_function:
            # Если нажата выбраная функция очищаем ссылку
            self.ref_function_card.current = None
        else:
            # Снимаем выделение с предыдущей выбранной функции, если она есть
            if selected_function is not None:
                selected_function.change_selected(e)
            
            # Устанавливаем ссылку на новую выбранную функцию
            self.ref_function_card.current = clicked_function_card

        self.update()


    def delete_function(self, e) -> None:
        '''
        Удаляет функцию из блока (данные/обработка/анализ)

        Args:
            e (Event): Параметры события
        '''
        function_to_remove = e.control.data
        selected_function = self.ref_function_card.current

        # Удаляем из выбранного
        if function_to_remove == selected_function:
            self.ref_function_card.current = None

        # Удаляем список параметров
        for item in self.list_function_parameters:
            if item.data == function_to_remove:
                self.list_function_parameters.remove(item)
                break 
        
        # Удаляем из списка функций
        match function_to_remove.function_type:
            case 'data':
                self.list_functions_data.remove(function_to_remove)
            case 'edit':
                self.list_functions_edit.remove(function_to_remove)
            case 'analitic':
                self.list_functions_analis.remove(function_to_remove)
        
        self.update()
