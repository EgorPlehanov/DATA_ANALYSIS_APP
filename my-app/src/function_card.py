import random
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
    MarkdownExtensionSet,
    LineChart,
    ChartAxis,
    LineChartDataPoint,
    LineChartData,
    ChartGridLines,
    ChartPointLine,
    Checkbox,
    padding,
    FontWeight,
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

        # Функция карточки
        self.function = Function(self.function_name)

        # Содержимое карточки функции
        self.ref_card_parameters_text = Ref[Markdown]()
        self.ref_card_result = Ref[Column]()
        self.ref_card_result_show_button = Ref[IconButton]()
        self.ref_card_result_data = Ref[Markdown]()
        self.card_content = Column(
            expand=True,
            controls=[
                Row(
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        Markdown(
                            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                            value='#### Функция:\n**' + self.function.name + '** (' + ', '.join(self.function.parameters_names) + ')',
                        ),
                        IconButton(
                            icon=icons.DELETE,
                            data=self,
                            on_click=self.on_click_delete
                        )
                    ]
                ),
                Markdown(
                    ref=self.ref_card_parameters_text,
                    extension_set=MarkdownExtensionSet.GITHUB_WEB,
                    value=self._get_card_parameters_text()
                ),
                Row(
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        Markdown(
                            value="#### Результат:"
                        ),
                        IconButton(
                            icon=icons.KEYBOARD_ARROW_DOWN,
                            ref=self.ref_card_result_show_button,
                            data={
                                'control': self.ref_card_result,
                                'button': self.ref_card_result_show_button,
                            },
                            on_click=self._change_function_result_visible
                        ),
                    ]
                ),
                Column(
                    ref=self.ref_card_result,
                    visible=False,
                    controls=[
                        Markdown(
                            ref=self.ref_card_result_data,
                            extension_set=MarkdownExtensionSet.GITHUB_WEB,
                            value=self._get_card_parameters_result()
                        ),
                        Row(
                            alignment=MainAxisAlignment.END,
                            controls=[
                                IconButton(
                                    content=Row(
                                        controls=[
                                            Text(value="Скрыть результат"),
                                            ft.Icon(name='KEYBOARD_ARROW_UP')
                                        ]
                                    ),
                                    data={
                                        'control': self.ref_card_result,
                                        'button': self.ref_card_result_show_button,
                                    },
                                    on_click=self._change_function_result_visible
                                ),
                            ]
                        )
                    ]
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

        # Представление результатов функции
        self.ref_result_view = Ref[Container]()
        self.ref_result_view_LineChartData = Ref[LineChartData]()
        self.result_view = Container(
            ref=self.ref_result_view,
            data=self,
            bgcolor=colors.BLACK26,
            border_radius=10,
            padding=padding.only(left=5, top=10, right=20, bottom=10),
            content=self._get_result_view_list()
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
            self.result_view.border = None
        else:
            self.card_view.border = border.all(color=colors.BLUE)
            self.card_view.bgcolor = colors.BLACK26
            self.parameters_view.visible = True
            self.result_view.border = border.all(color=colors.BLUE)
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
                    Markdown(value="### Параметры")
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
                                dropdown.Option(key=option['key'], text=option['text'])
                                for option in param['options']
                            ],
                            value=current_parameters[param_name],
                            data={
                                'param_name': param_name
                            },
                            on_change=self._on_dropdown_change
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
                case 'checkbox':
                    ref_checkbox = [Ref[Checkbox]() for _ in range(len(param['checkboxes']))]
                    param_editor = [
                        Column(
                            controls=[
                                Checkbox(
                                    label=checkbox['label'],
                                    value=checkbox['default_value'],
                                    ref=ref_checkbox[idx],
                                    data={
                                        'key': checkbox['key'],
                                        'ref_checkboxes': ref_checkbox,
                                        'param_name': param_name,
                                    },
                                    on_change=self._on_checkbox_change
                                )
                                for idx, checkbox in enumerate(param['checkboxes'])
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
        Обнавляет значение параметра в экземпляре класса Function, заголовке слайдера и карточке функции

        Args:
            e (Event): Событие изменения слайдера.
        '''
        slider_title = e.control.data['slider_text'].current
        slider_param_title = e.control.data['param_title']
        slider_param_name = e.control.data['param_name']
        slider_param_value = round(e.control.value, 3)

        slider_title.value = f"{slider_param_title}: {slider_param_value}"
        self.function.set_parameter_value(slider_param_name, slider_param_value) # ЕСЛИ БУДЕТ ЛАГАТЬ ПЕРЕПИСАТЬ НА ОБНОВЛЕНИЕ ПАРАМЕТРОВ ФУНКЦИИ ПО КНОПКЕ
        
        self.update_function_card()
        self.graphic_area.update()


    def _on_dropdown_change(self, e) -> None:
        '''
        Обновляет значение параметра в экземпляре класса Function и карточке функции
        '''
        dropdown_param_name = e.control.data['param_name']
        dropdown_param_value = e.control.value
        
        self.function.set_parameter_value(dropdown_param_name, dropdown_param_value)

        self.update_function_card()
        self.graphic_area.update()

    
    def _on_checkbox_change(self, e) -> None:

        checkbox_key = e.control.data['key']
        checkbox_value = e.control.value
        checkbox_param_name = e.control.data['param_name']

        checkbox_param_value = self.function.get_parameter_value(checkbox_param_name)
        if checkbox_value:
            checkbox_param_value.append(checkbox_key)
        else:
            checkbox_param_value.remove(checkbox_key)
        
        self.function.set_parameter_value(checkbox_param_name, checkbox_param_value)

        self.update_function_card()
        self.graphic_area.update()


    def _get_card_parameters_text(self) -> str:
        '''
        Возвращает текст с параметрами для карточки функции
        '''
        # \u00A0 - Unicode символ неразмеренного пробела
        return '#### Параметры:\n' + "; ".join([f"*{param}*:\u00A0**{value}**" for param, value in self.function.get_parameters_dict().items()]) + '\n'
    
    
    def _get_card_parameters_result(self, max_rows=10):
        df_list = self.function.result
        if not df_list:
            return '***Нет данных***'
        
        markdown_table_list = []
        for df in df_list:
            data_title = 'Данные для графика: ***' + df['type'] + '***\n\n'
            data = df['data']

            if len(data) <= max_rows:
                markdown_table = data.to_markdown()
            else:
                df_head = data.head(max_rows // 2)
                df_tail = data.tail(max_rows // 2)

                tail_rows = []
                for idx, row in df_tail.iterrows():
                    row_text = f'| {idx} | ' + " | ".join(map(str, row)) + ' |'
                    tail_rows.append(row_text)

                table_separator = '\n|' + '|'.join(['...'] * (data.shape[1] + 1)) + '|\n' if data.shape[0] > 10 else ""
                markdown_table = data_title + df_head.to_markdown() + table_separator + '\n'.join(tail_rows)
                
            markdown_table_list.append(markdown_table)
        return '\n\n'.join(markdown_table_list)


    def _change_function_result_visible(self, e) -> None:
        result_block = e.control.data
        result_control = result_block['control'].current
        result_button = result_block['button'].current

        result_control.visible = not result_control.visible

        if result_control.visible:
            result_button.icon = icons.KEYBOARD_ARROW_UP
        else:
            result_button.icon = icons.KEYBOARD_ARROW_DOWN
        self.update()


    def update_function_card(self) -> None:
        '''
        Обновляет текст параметров в карточки функции
        '''
        dataframe = self.function.result
        # ПЕРЕДЕЛАТЬ ОБНОВЛЕНИЕ ДАННЫХ ГРАФИКОВ БЕЗ ПЕРЕСОЗДАНИЯ ОБЕКТОВ ГРАФИКОВ
        data_points_list = []
        for df in dataframe:
            data = df['data']
            data_points_list.append(
                [
                    LineChartDataPoint(x, y) for x, y in zip(data.iloc[:, 0], data.iloc[:, 1])
                ]
            )
        # self.ref_result_view_LineChartData.current.data_points = data_points
        self.ref_result_view.current.content = self._get_result_view_list()
        self.ref_card_parameters_text.current.value = self._get_card_parameters_text()
        self.ref_card_result_data.current.value = self._get_card_parameters_result()
        self.update()



    def _get_result_view_list(self) -> Column:
        dataframe_list = self.function.result
        if not dataframe_list:
            return Row(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        Text(value='Нет данных для построения графиков функции ' + self.function_name, weight=FontWeight.BOLD, size=20),
                    ]
                )
        
        colors_list = ['green', 'blue', 'red', 'yellow', 'purple',
                       'orange', 'pink', 'brown', 'cyan', 'magenta']

        graphs_cnt = len(dataframe_list)
        grid = []
        row = []
        for idx in range(1, graphs_cnt + 1):
            row.append(self._get_function_result_graphic(dataframe_list[idx - 1], color=colors_list[idx - 1]))
            if (
                graphs_cnt <= 3 
                or len(row) == 3
                or (graphs_cnt % 3 == 1 and graphs_cnt - idx < 3 and len(row) == 2)
                or idx == graphs_cnt
            ):
                grid.append(Row(controls=row))
                row = []
        
        result_view = Column(
            controls=
            [
                Row(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        Text(value='График' + ('и' if graphs_cnt > 1 else '') + ' функции ' + self.function_name, weight=FontWeight.BOLD, size=20),
                    ]
                ),
                *grid
            ]
        )
        return result_view
    

    def get_result_view(self) -> Container:
        return self.result_view
    

    def _get_function_result_graphic(self, dataframe, column_names=None, color=None, graphic_curved=False):
        df = dataframe['data']
        graphic_title = dataframe['type']

        data_series = []

        if color is None:
            color = colors.LIGHT_GREEN

        if column_names is None:
            column_names = df.columns.tolist()  # Получаем названия столбцов из датафрейма

        data_points = [
            LineChartDataPoint(x, y)
            for x, y in zip(df.iloc[:, 0], df.iloc[:, 1])
        ]

        data_series.append(
            LineChartData(
                ref=self.ref_result_view_LineChartData,
                data_points=data_points,
                stroke_width=1,
                color=color,
                curved=graphic_curved,
                stroke_cap_round=True,
                selected_below_line=ChartPointLine(
                    color=colors.ON_SURFACE,
                    width=1,
                    dash_pattern=[10, 5],
                )
            )
        )

        chart = LineChart(
            data_series=data_series,
            left_axis=ChartAxis(
                title=Text(value=column_names[1]),
                title_size=20,
                labels_size=50,
            ),
            bottom_axis=ChartAxis(
                title=Text(column_names[0]),
                title_size=20,
                labels_size=30
            ),
            top_axis=ChartAxis(
                title=Text(value=graphic_title, size=20),
                title_size=30,
                show_labels=False,
            ),
            border=border.all(1, colors.with_opacity(0.5, colors.ON_SURFACE)),
            horizontal_grid_lines=ChartGridLines(
                width=1,
                color=colors.with_opacity(0.2, colors.ON_SURFACE), 
            ),
            vertical_grid_lines=ChartGridLines(
                width=1,
                color=colors.with_opacity(0.2, colors.ON_SURFACE),
            ),
            tooltip_bgcolor=colors.with_opacity(0.8, colors.BLACK38),
            expand=True,
        )

        return chart

