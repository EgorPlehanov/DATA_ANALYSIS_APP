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
    Page,
    Slider,
    icons,
    MainAxisAlignment
)
from model import Model
import datetime


class FunctionCard(UserControl):
    def __init__(self, graphic_area, app, page, name, on_click_fun=None):
        super().__init__()
        self.app = app
        self.page = page
        self.graphic_area = graphic_area
        self.name = name
        self.selected = False
        self.on_click = on_click_fun
        self.ref = None
        self.function = Model.get_info(name, return_type='function')
        self.parameters = Model.get_info(name, return_type='parameters')

        # self.parameters_text = Text(
        #     size=10,
        #     selectable=True,
        #     no_wrap=False,
        #     # value=str(self.parameters)
        #     value = "; ".join([f"{param['title']}: {param['value']}" for param in self.parameters.values()])
        # )
        self.card_content = Row(
            controls=[
                Column(
                    expand=True,
                    controls=[
                        Row(
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                Text(value='Функция: ' + self.name),
                                IconButton(
                                    icon=icons.DELETE,
                                    on_click=None
                                )
                            ]
                        ),
                        ft.Markdown(
                            value="; ".join(f"*{param['title']}*: **{param['value']}**" for param in self.parameters.values())+'.'+datetime.datetime.now().strftime("%H:%M:%S"),
                        )
                    ]
                )
            ]
        )
        self.card_view = Container(
            content=self.card_content,
            data=self,
            on_click=self.on_click,
            # on_click=self.my_on_click,
            border = border.all(color=colors.BLACK),
            bgcolor = colors.BLACK54,
            border_radius = 10,
            padding=5,
        )

        
        self.parameters_view = Container(
            visible=False,
            content=Column(
                controls=self._get_parameters_view_list()
            )
        )
        

    def build(self):
        return self.card_view

    def my_on_click(self, e):
        if self.selected:
            self.card_view.border = border.all(color=colors.BLACK)
            self.card_view.bgcolor = colors.BLACK54
            self.parameters_view.visible = False
        else:
            self.card_view.border = border.all(color=colors.BLUE)
            self.card_view.bgcolor = colors.BLACK26
            self.parameters_view.visible = True
        self.selected = not self.selected
        self.update()

    def get_parameters(self):
        return self.parameters_view
    

    def _get_parameters_view_list(self):
        parameters_view_list = []
        for param in self.parameters.values():
            param_editor = None
            match param['type']:
                case "dropdown":
                    param_editor = [
                        Dropdown(
                            dense=True,
                            label = param['title'],
                            options=[dropdown.Option(key=option, text=option) for option in param['options']],
                            value=param['options'][0],
                        )
                    ]
                case "slider":
                    ref_slider_text = Ref[Text]()
                    param_editor = [
                        Column(
                            controls=[
                                Text(
                                    ref=ref_slider_text,
                                    value=f'{param["title"]}: {param["value"]}',
                                ),
                                Slider(
                                    min=param['min'],
                                    max=param['max'],
                                    value=param['value'],
                                    divisions=int((param['max'] - param['min']) / param['step']),
                                    label='{value}',
                                    data={"slider_text": ref_slider_text, 'slider_name': param['title']},
                                    on_change=self._slider_changed,
                                )
                            ]
                        )
                    ]
                    
            parameters_view_list.append(
                Row(
                    controls=param_editor
                )
            )
        return parameters_view_list
    
    def _slider_changed(self, e):
        e.control.data['slider_text'].current.value = f"{e.control.data['slider_name']}: {round(e.control.value, 3)}"
        self.graphic_area.update()

    # def my_on_click(self, e):
    #     self.function_card.border = border.all(color=colors.BLUE)
    #     self.function_card.bgcolor = colors.BLACK26
    #     self.update()



# =======================================================================



class GraphicArea(Row):
    def __init__(self, app, page : Page):
        super().__init__()
        self.app = app
        self.page = page
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
            border=border.all(color=colors.ORANGE),
            alignment=ft.alignment.top_center,
            width=350,
            content=Column(
                tight=True,
                scroll=ScrollMode.AUTO,
                controls=[
                    Container(
                        border=border.all(color=colors.GREEN),
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
            alignment=ft.alignment.top_center,
            border=border.all(colors.BLACK),
            content=Column(
                tight=True,
                scroll=ScrollMode.AUTO,
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
                selected_function.my_on_click(e)
            function_card.my_on_click(e)
            self.ref_function_card.current = function_card
        self.update()