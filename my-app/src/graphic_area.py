from typing import List
from flet import (
    Row,
    Container,
    colors,
    border,
    Column,
    ScrollMode,
    Dropdown,
    dropdown,
    IconButton,
    Tabs,
    Tab,
    Ref,
    Page,
    alignment,
    Markdown,
    animation,
    AnimationCurve,
)
from function_card import FunctionCard
import flet as ft
from Model.model import Model


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
        self.list_functions_analytic = []

        # Списки результатов для блоков области результатов (данные/обработка/анализ)
        self.list_results_data = []
        self.list_results_edit = []
        self.list_results_analytic = []

        # Меню работы с функциями c блоками (данные/обработка/анализ)
        self.function_menu = Container(
            width=350,
            bgcolor=colors.BLACK26,
            alignment=alignment.top_center,
            content=Column(
                tight=True,
                scroll=ScrollMode.AUTO,
                spacing=5,
                controls=[
                    self._get_function_menu_block(
                        'data',
                        'Данные',
                        self.list_functions_data,
                        self.list_results_data,
                    ),
                    self._get_function_menu_block(
                        'edit',
                        'Обработка',
                        self.list_functions_edit,
                        self.list_results_edit,
                    ),
                    self._get_function_menu_block(
                        'analytic',
                        'Анализ',
                        self.list_functions_analytic,
                        self.list_results_analytic,
                    ),
                ]
            )
        )

        # Список параметров функций блоков (данные/обработка/анализ)
        self.list_function_parameters=[]
        
        # Меню работы с параметрами
        self.parameters_menu = Container(
            alignment=alignment.top_center,
            bgcolor=colors.BLACK12,
            animate_size=100,
            content=Column(
                tight=True,
                scroll=ScrollMode.AUTO,
                controls=self.list_function_parameters
            )
        )

        # Ссыкла на виджет вкладок результатов
        self.ref_result_view = Ref[Tabs]()

        self.ref_result_view_data = Ref[Column]()
        self.ref_result_view_edit = Ref[Column]()
        self.ref_result_view_analytic = Ref[Column]()

        self.ref_tab_count_indiator_data = Ref[Container]()
        self.ref_tab_count_indiator_edit = Ref[Container]()
        self.ref_tab_count_indiator_analytic = Ref[Container]()

        # Область вывода результатов с вкладками (данные/обработка/анализ)
        self.results_view = Container(
            expand=True,
            border=border.all(colors.BLACK),
            content=Tabs(
                scrollable=False,
                ref=self.ref_result_view,
                animation_duration=200,
                tabs=[
                    self._get_result_view_tab(
                        'Данные',
                        self.list_results_data,
                        self.ref_result_view_data,
                        self.ref_tab_count_indiator_data
                    ),
                    self._get_result_view_tab(
                        'Обработка',
                        self.list_results_edit,
                        self.ref_result_view_edit,
                        self.ref_tab_count_indiator_edit
                    ),
                    self._get_result_view_tab(
                        'Анализ',
                        self.list_results_analytic,
                        self.ref_result_view_analytic,
                        self.ref_tab_count_indiator_analytic
                    ),
                ],
            ),
        )

        # Содержимое виджета
        self.controls = [
            self.function_menu,
            self.parameters_menu,
            self.results_view,
        ]


    def _get_function_menu_block(
            self,
            function_type: str,
            block_name: str,
            list_functions: List,
            list_results: List,
        ) -> Container:
        '''
        Функция создает блока меню работы с функциями

        Args:
            function_type (str): Тип функций в блоке.
            block_name (str): Название блока.
            list_functions (List[FunctionCard]): Список функций блока.
            list_results (List[Container]): Список результатов.
        '''
        ref_dropdown = Ref[Dropdown]() # Ссылки на выпадающие списки блока
        dropdown_options = Model.get_functions_by_type(function_type)
        dropdown_default_value = dropdown_options[0].get('key') if dropdown_options else None
        
        # Блок из меню работы с функциями
        function_menu = Container(
            bgcolor=colors.BLUE_GREY_900,
            border_radius=10,
            padding=5,
            content=Column(
                controls=[
                    Markdown(value="### " + block_name),
                    Row(
                        controls=[
                            Dropdown(
                                ref=ref_dropdown,
                                dense=True,
                                value=dropdown_default_value,
                                options=[
                                    dropdown.Option(key=option.get('key'), text=option.get('name'))
                                    for option in dropdown_options
                                ]
                            ),
                            IconButton(icon="add", on_click=lambda _: self.add_function(
                                    ref_dropdown,
                                    list_functions,
                                    list_results,
                                    function_type
                                )
                            ),
                        ]
                    ),
                    Column(
                        animate_size=animation.Animation(200, AnimationCurve.FAST_OUT_SLOWIN),
                        controls=list_functions
                    )
                ]
            )
        )
        return function_menu
    
    
    def _get_result_view_tab(
            self,
            tab_name: str,
            list_results: List,
            ref_tab_result_view: Ref[Column],
            ref_tab_count_indiator: Ref[ft.Text]
        ) -> Tab:
        '''
        Функциия создания вкладки результатов
        '''
        results_view_tab =  Tab(
            text=tab_name,
            tab_content=Row(
                controls=[
                    ft.Text(tab_name),
                    Container(
                        content=ft.Text('0', size=12),
                        border=border.all(1, colors.with_opacity(0.1, ft.colors.ON_SURFACE)),
                        border_radius=10,
                        bgcolor=colors.with_opacity(0.05, ft.colors.ON_SURFACE),
                        padding=ft.padding.only(left=10, right=10, top=5, bottom=5),
                        visible=False,
                        ref=ref_tab_count_indiator
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            content=Container(
                expand=False,
                padding=10,
                content=Column(
                    tight=True,
                    scroll=ScrollMode.AUTO,
                    ref=ref_tab_result_view,
                    controls=list_results,
                ),
            ),
        )
        return results_view_tab
    

    def _on_change_result_view_tab_count(self, tab_name: str) -> None:
        '''
        Изменяет индикатор количества блоков на вкладке результатов
        '''
        match tab_name:
            case 'data':
                conntrol = self.ref_tab_count_indiator_data.current
                value = len(self.list_results_data)
            case 'edit':
                conntrol = self.ref_tab_count_indiator_edit.current
                value = len(self.list_results_edit)
            case 'analytic':
                conntrol = self.ref_tab_count_indiator_analytic.current
                value = len(self.list_results_analytic)
        conntrol.content.value = str(value)
        conntrol.visible = False if value == 0 else True


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

            # scroll_view = None
            match clicked_function_card.function_type:
                case 'data':
                    self.ref_result_view.current.selected_index = 0
                    # scroll_view = self.ref_result_view_data.current
                case 'edit':
                    self.ref_result_view.current.selected_index = 1
                    # scroll_view = self.ref_result_view_edit.current
                case 'analytic':
                    self.ref_result_view.current.selected_index = 2
                    # scroll_view = self.ref_result_view_analytic.current
            
            # ПРОКРУТКА ДО ЭЛЕМЕНТА В СПИСКЕ РЕЗУЛЬТАТОВ НЕ РАБОТЕТ
            # ПРОКРУТКА СРАБАТЫВАЕТ НА РОДИТЕЛЬСКИЕ ЭЛЕМЕНТЫ И ОКНО ПРОКРУЧИВАЕТСЯ МИМО НУЖНОГО МЕСТА
            # Блокируется auto_scroll=True, но тогда прокрутка всегда идет до конца
            # if scroll_view is not None:
            #     scroll_view.scroll_to(
            #         key=str(clicked_function_card.function_id),
            #         duration=500,
            #         # curve=animation.AnimationCurve.FAST_OUT_SLOWIN
            #     )
        self.update()


    def add_function(
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
            list_results (List[Container]): Список результатов блока (данные/обработка/анализ).
            function_type (str): Тип функции.
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

        # Добавляем в список для блоков функций и результатов (данные/обработка/анализ)
        list_functions.append(function_card)
        list_results.append(function_card.get_result_view())
        # Добавляем параметры функции в список
        self.list_function_parameters.append(function_card.get_parameters())
        
        self._on_change_result_view_tab_count(function_type)
        self.update_list_parametrs()
        self.update()


    def delete_function(self, e) -> None:
        '''
        Удаляет функцию из блока (данные/обработка/анализ)
        '''
        function_to_remove = e.control.data
        reslut_view_to_remove = function_to_remove.ref_result_view.current
        selected_function = self.ref_function_card.current

        # Удаляем ссылку на функцию из списка связанных у функции из которой берутся данные
        if function_to_remove.provider_function is not None:
            function_to_remove.provider_function.list_dependent_functions.remove(function_to_remove)

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
            case 'analytic':
                self.list_functions_analytic.remove(function_to_remove)
                self.list_results_analytic.remove(reslut_view_to_remove)

        self._on_change_result_view_tab_count(function_to_remove.function_type)
        self.update_list_parametrs(function_to_remove.list_dependent_functions)
        self.update()


    def update_list_parametrs(self, list_dependent_functions=None) -> None:
        '''
        Обновление списка параметров для функций у которых есть выбор данных из другого блока функций
        '''

        if isinstance(list_dependent_functions, list) and len(list_dependent_functions) > 0:
            # Вызывается при удалении функции, обновляет зависимые функции
            for dependent_function in list_dependent_functions:
                dependent_function.update_function_card(update_parameters=True)
        else:
            # Вызывается при добавлении новых функций
            for function_parameters in self.list_function_parameters:
                for parameter in function_parameters.content.controls:
                    if parameter.data in ['dropdown_function_data']:
                        function_parameters.data.update_function_card(update_parameters=True)
                        break
