from typing import Any
import flet as ft
from flet import (
    UserControl,
    Container,
    Row,
    Column,
    MainAxisAlignment,
    Text,
    IconButton,
    icons,
    Markdown,
    border,
    colors,
    Dropdown,
    dropdown,
    Ref,
    Slider,
)
from function import Function



class FunctionCard(UserControl):
    def __init__(self, graphic_area, app, page, function_name, function_type, on_change_selected, on_click_delete):
        super().__init__()
        self.app = app
        self.page = page
        self.graphic_area = graphic_area
        self.function_name = function_name
        self.function_type = function_type
        self.selected = False

        # Функции обработчики нажатий на кнопки карточки функции 
        self.on_change_selected = on_change_selected
        self.on_click_delete = on_click_delete

        # self.ref = Ref[FunctionCard]()

        # Функция карточки
        self.function = Function(self.function_name)
        # self.function = Model.get_info(name, return_type='function')
        # self.parameters = Model.get_info(name, return_type='parameters')
        # self.parameters_names = list(self.parameters.keys())

        # Установка атрибутов класса на основе параметров функции
        # for param_name, param_info in self.parameters.items():
            # self.set_parameter_value(self, param_name, param_info['value'])
            # setattr(self, param_name, param_info['value'])

        # Содержимое карточки функции
        self.ref_card_parameters_text = Ref[Markdown]()
        self.card_content = Column(
            expand=True,
            controls=[
                Row(
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        Text(value='Функция: ' + self.function.name + ' (' + ', '.join(self.function.parameters_names) + ')'),
                        IconButton(
                            icon=icons.DELETE,
                            data=self,
                            on_click=self.on_click_delete
                        )
                    ]
                ),
                Markdown(
                    ref=self.ref_card_parameters_text,
                    value=self._get_card_parameters_text()
                )
            ]
        )

        # Представление карточки функции
        self.card_view = Container(
            content=self.card_content,
            data=self,
            on_click=self.on_change_selected,
            border = border.all(color=colors.BLACK),
            bgcolor = colors.BLACK54,
            border_radius = 10,
            padding=5,
        )

        # Представление списка параметров
        self.parameters_view = Container(
            visible=False,
            data=self,
            content=Column(
                controls=self._get_parameters_view_list()
            )
        )
        

    def build(self) -> Container:
        '''
        Возвращает представление карточки функции
        
        Returns:
            Container: Представление карточки функции
        '''
        return self.card_view


    def change_selected(self, e) -> None:
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
    

    def _get_parameters_view_list(self) -> list:
        '''
        Создает список предствалений параметров для отображения на экране

        Returns:
            list: Список представлений параметров
        '''
        # Создание списка представлений параметров
        parameters_view_list = [
            Row(
                controls=[
                    Text(value="Параметры",)
                ]
            )
        ]

        # Получение текущих параметров
        current_parameters = self.function.get_parameters_dict()

        # Цикл по всем параметрам
        for param_name, param in self.function.parameters_info.items():
            param_editor = None
            match param['type']:
                case "dropdown":
                    param_editor = [
                        Dropdown(
                            dense=True,
                            label=param['title'],
                            options=[
                                dropdown.Option(key=option['key'], text=option['text']) for option in param['options']
                            ],
                            value=current_parameters[param_name],
                            on_change=None#self._change_dropdown_title
                        )
                    ]
                case "slider":                    
                    ref_slider_text = Ref[Text]()
                    slider_divisions = int((param['max'] - param['min']) / param['step'])
                    param_editor = [
                        Column(
                            controls=[
                                Text(
                                    ref=ref_slider_text,
                                    value=f'{param["title"]}: {current_parameters[param_name]}',
                                ),
                                Slider(
                                    min=param['min'],
                                    max=param['max'],
                                    value=current_parameters[param_name],
                                    divisions=slider_divisions,
                                    label='{value}',
                                    data={
                                        "slider_text": ref_slider_text,
                                        'param_title': param["title"],
                                        'param_name': param_name
                                    },
                                    on_change=self._change_slider_title,
                                )
                            ]
                        )
                    ]
                case 'file_picker':
                    param_editor = [
                        Column(
                            controls=[
                                Text(
                                    value=f'{param["title"]}',
                                ),
                                ft.FilePicker(
                                    on_upload=None
                                )
                            ]
                        )
                    ]

            # Добавление представления параметра в список
            parameters_view_list.append(
                Row(
                    controls=param_editor
                )
            )
        return parameters_view_list


    def get_parameters(self) -> Container:
        '''
        Возвращает список параметров для отображения на экране

        Returns:
            Container: Контейнер, содержащий представление списка параметров
        '''
        return self.parameters_view


    def _change_slider_title(self, e) -> None:
        '''
        Обнавляет значение параметра в заголовке слайдера

        Args:
            e (Event): Событие изменения слайдера.
        '''
        slider_title = e.control.data['slider_text'].current
        slider_param_title = e.control.data['param_title']
        slider_param_name = e.control.data['param_name']
        slider_param_value = round(e.control.value, 3)

        slider_title.value = f"{slider_param_title}: {slider_param_value}"
        self.function.set_parameter_value(slider_param_name, slider_param_value) # ЕСЛИ БУДЕТ ЛАГАТЬ ПЕРЕПИСАТЬ НА ОБНОВЛЕНИЕ ПАРАМЕТРОВ ФУНКЦИИ ПО КНОПКЕ
        
        self.update_card_parameters_text()
        self.graphic_area.update()


    def _get_card_parameters_text(self) -> str:
        '''
        Возвращает текст с параметрами для карточки функции
        '''
        # \u00A0 - Unicode символ неразмеренного пробела
        return '### Параметры:\n' + "; ".join([f"*{param}*:\u00A0**{value}**" for param, value in self.function.get_parameters_dict().items()]) + '.\n' \
             + '### Результат:\n' + str(self.function.result)
    

    def update_card_parameters_text(self) -> None:
        '''
        Обновляет текст параметров в карточки функции
        '''
        self.ref_card_parameters_text.current.value = self._get_card_parameters_text()
        self.update()


