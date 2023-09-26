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
import flet as ft
from model import Model
import datetime


class FunctionCard(UserControl):
    def __init__(self, graphic_area, app, page, name, change_selected_function, on_click_delete):
        super().__init__()
        self.app = app
        self.page = page
        self.graphic_area = graphic_area
        self.name = name
        self.selected = False
        self.change_selected_function = change_selected_function
        self.on_click_delete = on_click_delete
        # self.ref = Ref[FunctionCard]()
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
                                    data=self,
                                    on_click=self.on_click_delete
                                )
                            ]
                        ),
                        Markdown(
                            value="; ".join(f"*{param['title']}*: **{param['value']}**" for param in self.parameters.values())+'.'+datetime.datetime.now().strftime("%H:%M:%S"),
                        )
                    ]
                )
            ]
        )
        self.card_view = Container(
            content=self.card_content,
            data=self,
            on_click=self.change_selected_function,
            border = border.all(color=colors.BLACK),
            bgcolor = colors.BLACK54,
            border_radius = 10,
            padding=5,
        )
        self.parameters_view = Container(
            visible=False,
            data=self,
            content=Column(
                controls=self._get_parameters_view_list()
            )
        )
        

    def build(self):
        return self.card_view

    def change_selected(self, e):
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
        parameters_view_list = [
            Row(
                controls=[
                    Text(value="Параметры",)
                ]
            )
        ]
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
                case 'file_picker':
                    param_editor=[
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
    #     self.function_card.bgcolor = colors.BLACK26
    #     self.update()

