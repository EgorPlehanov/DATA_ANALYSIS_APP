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
    alignment,
    Markdown,
)
from function_card import FunctionCard
import flet as ft
from model import Model


class GraphicArea(Row):
    def __init__(self, app, page: Page):
        super().__init__()
        self.app = app
        self.page = page
        self.spacing = 0

        # Ссылка на выбранную функцию
        self.ref_function_card = Ref[Container]()

        # Списоки функций блоков (данные/обработка/анализ)
        self.list_functions_data = []
        self.list_functions_edit = []
        self.list_functions_analis = []

        # Ссылки на выпадающие списки блоков (данные/обработка/анализ)
        self.ref_dropdown_data = Ref[Dropdown]()
        self.ref_dropdown_edit = Ref[Dropdown]()
        self.ref_dropdown_analis = Ref[Dropdown]()

        # Блок данных из меню работы с функциями
        self.function_menu_data = Container(
            # border=border.all(color=colors.GREEN),
            bgcolor=colors.BLUE_GREY_900,
            padding=5,
            content=Column(
                controls=[
                    Markdown(value="### Данные"),
                    Row(
                        controls=[
                            Dropdown(
                                ref=self.ref_dropdown_data,
                                dense=True,
                                value=Model.get_functions_by_type('data')[0]['key'],
                                options=[
                                    dropdown.Option(key=option['key'], text=option['name'])
                                    for option in Model.get_functions_by_type('data')
                                ]
                            ),
                            IconButton(icon="add", on_click=lambda _: self.add_function_to_list(
                                    self.ref_dropdown_data,
                                    self.list_functions_data,
                                    self.list_results_data,
                                    'data'
                                )
                            ),
                        ]
                    ),
                    Column(
                        controls=self.list_functions_data
                    )
                ]
            )
        )

        # Блок обработки из меню работы с функциями
        self.function_menu_edit = Container(
            bgcolor=colors.BLUE_GREY_900,
            padding=5,
            # border=border.all(colors.BLACK),
            content=Column(
                controls=[
                    Markdown(value="### Обработка"),
                    Row(
                        controls=[
                            Dropdown(
                                ref=self.ref_dropdown_edit,
                                dense=True,
                                # value=Model.get_functions_by_type('edit')[0]['key'],
                                options=[
                                    dropdown.Option(key=option['key'], text=option['name'])
                                    for option in Model.get_functions_by_type('edit')
                                ]
                            ),
                            IconButton(icon="add", on_click=lambda _: self.add_function_to_list(
                                    self.ref_dropdown_edit,
                                    self.list_functions_edit,
                                    self.list_results_edit,
                                    'edit'
                                )
                            ),
                        ]
                    ),
                    Column(
                        controls=self.list_functions_edit
                    )
                ]
            )
        )

        # Блок анализа из меню работы с функциями
        self.function_menu_analis = Container(
            bgcolor=colors.BLUE_GREY_900,
            padding=5,
            # border=border.all(colors.BLACK),
            content=Column(
                controls=[
                    Markdown(value="### Анализ"),
                    Row(
                        controls=[
                            Dropdown(
                                ref=self.ref_dropdown_analis,
                                dense=True,
                                # value=Model.get_functions_by_type('analis')[0]['key'],
                                options=[
                                    dropdown.Option(key=option['key'], text=option['name'])
                                    for option in Model.get_functions_by_type('analis')
                                ]
                            ),
                            IconButton(icon="add", on_click=lambda _: self.add_function_to_list(
                                    self.ref_dropdown_analis,
                                    self.list_functions_analis,
                                    self.list_results_analis,
                                    'analitic'
                                )
                            ),
                        ]
                    ),
                    Column(
                        controls=self.list_functions_analis
                    )
                ]
            )
        )

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
                    self.function_menu_data,
                    self.function_menu_edit,
                    self.function_menu_analis,
                ]
            )
        )

        # Список параметров функций блоков (данные/обработка/анализ)
        self.list_function_parameters=[]

        # Меню работы с параметрами
        self.parameters_menu = Container(
            padding=5,
            alignment=alignment.top_center,
            bgcolor=colors.BLACK12,
            border=border.all(colors.BLACK),
            content=Column(
                tight=True,
                scroll=ScrollMode.AUTO,
                controls=self.list_function_parameters
            )
        )

        # Списки результатов для блоков области результатов (данные/обработка/анализ)
        self.list_results_data = []
        self.list_results_edit = []
        self.list_results_analis = []

        # Ссылки на блоки в разделе результатов (данные/обработка/анализ)
        self.ref_results_view_data = Ref[Column]()
        self.ref_results_view_edit = Ref[Column]()
        self.ref_results_view_analis = Ref[Column]()

        # Вкладка данных из области результатов
        self.results_view_tab_data =  Tab(
            text="Данные",
            content=Container(
                border=border.all(color=colors.GREEN),
                expand=False,
                padding=10,
                content=Column(
                    tight=True,
                    scroll=ScrollMode.AUTO,
                    ref = self.ref_results_view_data,
                    controls=self.list_results_data
                ),
            ),
        )

        # Вкладка обработки из области результатов
        self.results_view_tab_edit = Tab(
            text="Обработка",
            content=Container(
                expand=True,
                border=border.all(color=colors.YELLOW),
                padding=10,
                content=Column(
                    tight=True,
                    scroll=ScrollMode.AUTO,
                    ref = self.ref_results_view_edit,
                    controls=self.list_results_edit
                )
            )
        )

        # Вкладка анализа из области результатов
        self.results_view_tab_analis = Tab(
            text="Анализ",
            content=Container(
                expand=True,
                border=border.all(color=colors.RED),
                padding=10,
                content=Column(
                    tight=True,
                    scroll=ScrollMode.AUTO,
                    ref = self.ref_results_view_analis,
                    controls=self.list_results_analis
                )
            )
        )

        # Область вывода результатов
        self.results_view = Container(
            expand=True,
            border=border.all(colors.BLACK),
            content=Tabs(
                tabs=[
                    self.results_view_tab_data,
                    self.results_view_tab_edit,
                    self.results_view_tab_analis,
                ]
            ),
        )

        # Содержимое виджета
        self.controls = [
            self.function_menu,
            self.parameters_menu,
            self.results_view,
        ]


    def add_function_to_list(
            self,
            ref: Ref[Dropdown],
            list_functions: List[FunctionCard],
            list_results: List[Container],
            function_type: str
        ) -> None:
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
        # Добавляем параметры функции в список
        self.list_function_parameters.append(function_card.get_parameters())
        list_results.append(function_card.get_result_view())
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
        reslut_view_to_remove = function_to_remove.ref_result_view.current
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
                self.list_results_data.remove(reslut_view_to_remove)
            case 'edit':
                self.list_functions_edit.remove(function_to_remove)
                self.list_results_edit.remove(reslut_view_to_remove)
            case 'analitic':
                self.list_functions_analis.remove(function_to_remove)
                self.list_results_edit.remove(reslut_view_to_remove)
        
        self.update()

