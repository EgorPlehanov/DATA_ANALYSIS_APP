import itertools
from typing import Any
import pandas as pd
import sympy as sp
import ast
import re
import flet as ft
from flet import (
    AnimationCurve,
    BorderSide,
    ChartAxis,
    ChartGridLines,
    ChartPointLine,
    Checkbox,
    Column,
    Container,
    CrossAxisAlignment,
    DataCell,
    DataColumn,
    DataRow,
    DataTable,
    Dropdown,
    FontWeight,
    Icon,
    IconButton,
    ElevatedButton,
    LabelPosition,
    LineChart,
    LineChartData,
    LineChartDataPoint,
    MainAxisAlignment,
    Markdown,
    MarkdownExtensionSet,
    Ref,
    Row,
    ScrollMode,
    Slider,
    Switch,
    Text,
    UserControl,
    animation,
    border,
    colors,
    dropdown,
    icons,
    margin,
    padding,
    TextField,
    FilePicker,
    FilePickerResultEvent,
    FilePickerFileType,
    TextAlign,
    KeyboardType,
    TextStyle,
)
from function import Function



class FunctionCard(UserControl):
    id_counter = itertools.count()
        
    def __init__(self, graphic_area, app, page, function_name, function_type, on_change_selected, on_click_delete):
        super().__init__()
        self.app = app
        self.page = page
        self.graphic_area = graphic_area
        self.function_id = next(FunctionCard.id_counter)
        self.function_type = function_type
        self.function_name = function_name
        self.function_name_formatted = f'{self.function_name} (id: {self.function_id}, type: {self.function_type})'
        self.selected = False
        self.list_dependent_functions = []
        self.provider_function = None

        # Функции обработчики нажатий на кнопки карточки функции 
        self.on_change_selected = on_change_selected
        self.on_click_delete = on_click_delete

        # Функция карточки
        self.function = Function(self.function_name)

        # Содержимое карточки функции
        self.ref_card_parameters_text = Ref[Markdown]()
        self.ref_card_result_data = Ref[Markdown]()

        # Представление карточки функции
        self.card_view = Container(
            content=self._create_card_content(),
            data=self,
            on_click=self.on_change_selected,
            border = border.all(color=colors.BLACK),
            bgcolor = colors.BLACK54,
            border_radius = 10,
            padding=5,
        )

        # Представление списка параметров
        self.ref_parameters_view = Ref[Column]()
        self.parameters_view = Container(
            content=Column(
                controls=self._get_parameters_view_list(),
                ref=self.ref_parameters_view,
                tight=True,
            ),
            visible=False,
            data=self,
            padding=10,
            width=350,
        )

        # Представление результатов функции
        self.ref_result_view = Ref[Container]()
        self.result_view = Container(
            content=self._get_result_view_list(),
            ref=self.ref_result_view,
            data=self,
            border_radius=10,
            bgcolor=colors.BLACK26,
            padding=padding.only(left=10, top=10, right=20, bottom=10),
            key=self.function_id,
        )
        

    def build(self) -> Container:
        '''
        Возвращает представление карточки функции
        '''
        return self.card_view


    def _create_card_content(self) -> Column:
        '''
        Coздает содержимое карточки функции
        '''
        ref_card_result = Ref[Column]()
        ref_card_result_show_button = Ref[IconButton]()
        card_title = Row(
            controls=[
                Row(
                    controls=[
                        Markdown(
                            extension_set=MarkdownExtensionSet.GITHUB_WEB,
                            value = f'#### Функция (*id:* ***{self.function_id}***)\n**{self.function.name}** (*{", ".join(self.function.parameters_names)}*)'
                        ),
                    ],
                    expand=True,
                    wrap=True,
                ),
                IconButton(
                    icon=icons.DELETE,
                    data=self,
                    on_click=self.on_click_delete
                )
            ],
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=CrossAxisAlignment.START,
        )
        card_parameters = Markdown(
            animate_size=200,
            ref=self.ref_card_parameters_text,
            extension_set=MarkdownExtensionSet.GITHUB_WEB,
            value=self._get_card_parameters_text()
        )
        card_result_title = Row(
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                Markdown(
                    value="#### Результат:"
                ),
                IconButton(
                    icon=icons.KEYBOARD_ARROW_DOWN,
                    ref=ref_card_result_show_button,
                    data={
                        'control': ref_card_result,
                        'button': ref_card_result_show_button,
                    },
                    on_click=self._change_function_result_visible
                ),
            ]
        )
        card_result_data = Container(
            animate_size=animation.Animation(200, AnimationCurve.FAST_OUT_SLOWIN),
            content=Column(
                ref=ref_card_result,
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
                                        Icon(name='KEYBOARD_ARROW_UP')
                                    ]
                                ),
                                data={
                                    'control': ref_card_result,
                                    'button': ref_card_result_show_button,
                                },
                                on_click=self._change_function_result_visible
                            ),
                        ]
                    )
                ]
            )
        )
        card_content = Column(
            expand=True,
            controls=[
                card_title,
                card_parameters,
                card_result_title,
                card_result_data
            ]
        )
        return card_content


    def change_selected(self, e) -> None:
        '''
        Изменяет свойства карточки в зависимости от того выбрана она или нет
        '''
        if self.selected:
            self.card_view.border = border.all(color=colors.BLACK)
            self.card_view.bgcolor = colors.BLACK54
            self.result_view.border = None
            self.parameters_view.visible = False
        else:
            self.card_view.border = border.all(color=colors.BLUE)
            self.card_view.bgcolor = colors.BLACK26
            self.result_view.border = border.all(color=colors.BLUE)
            self.parameters_view.visible = True
        self.selected = not self.selected
        self.update()


    def _change_function_result_visible(self, e) -> None:
        '''
        Изменяет видимость результатов в карточке функции
        '''
        result_block = e.control.data
        result_control = result_block.get('control').current
        result_button = result_block.get('button').current

        result_control.visible = not result_control.visible

        if result_control.visible:
            result_button.icon = icons.KEYBOARD_ARROW_UP
        else:
            result_button.icon = icons.KEYBOARD_ARROW_DOWN
        self.update()
    

    def update_function_card(self, update_parameters: bool = False) -> None:
        '''
        Обновляет текст параметров в карточки функции
        '''
        # ПЕРЕДЕЛАТЬ ОБНОВЛЕНИЕ ДАННЫХ ГРАФИКОВ БЕЗ ПЕРЕСОЗДАНИЯ ОБЕКТОВ ГРАФИКОВ
        # dataframe = self.function.result
        # data_points_list = []
        # for df in dataframe:
        #     data = df['data']
        #     data_points_list.append(
        #         [
        #             LineChartDataPoint(x, y) for x, y in zip(data.iloc[:, 0], data.iloc[:, 1])
        #         ]
        #     )
        # self.ref_result_view_LineChartData.current.data_points = data_points
        if update_parameters:
            self.ref_parameters_view.current.controls = self._get_parameters_view_list()
            self.function._calculate()

        self.ref_result_view.current.content = self._get_result_view_list()
        self.ref_card_parameters_text.current.value = self._get_card_parameters_text()
        self.ref_card_result_data.current.value = self._get_card_parameters_result()

        self.update()
        self.graphic_area.update()

        for dependent_function in self.list_dependent_functions:
            dependent_function.update_function_card(update_parameters=True)

        


    def get_parameters(self) -> Container:
        '''
        Возвращает список параметров для отображения на экране

        Returns:
            Container: Контейнер, содержащий представление списка параметров
        '''
        return self.parameters_view


    def _get_parameters_view_list(self) -> list:
        '''
        Создает список предствалений параметров для отображения на экране

        Returns:
            list: Список представлений параметров
        '''
        # Создание списка представлений параметров
        parameters_view_list = [
            Row(controls=[Markdown(value="### Параметры")])
        ]

        # Получение текущих параметров
        current_parameters = self.function.get_parameters_dict()

        # Цикл по всем параметрам
        for param_name, param in self.function.parameters_info.items():
            param_editor = None
            param_type = param.get('type')
            match param_type:
                case "dropdown":
                    param_editor = Dropdown(
                        dense=True,
                        label=param.get('title'),
                        options=[
                            dropdown.Option(key=option.get('key'), text=option.get('text'))
                            for option in param.get('options', [])
                        ],
                        value=current_parameters[param_name],
                        data={'param_name': param_name},
                        on_change=self._on_change_dropdown_value
                    )

                case 'dropdown_function_data':
                    function_card_list = []
                    if self.function.type in ['edit', 'analitic']:
                        function_card_list.extend(self.graphic_area.list_functions_data)
                    if self.function.type == 'analitic':
                        function_card_list.extend(self.graphic_area.list_functions_edit)

                    options = param.get('options', {'Не выбраны': {'function_name': 'Не выбраны', 'value': []}}).copy()
                    options.update({
                        function_card.function_name_formatted: {
                            'function_name': function_card.function_name_formatted,
                            'value': function_card
                        }
                        for function_card in function_card_list
                    })
                    
                    dropdown_value = 'Не выбраны'
                    value_to_print = 'Не выбраны []'

                    current_value = current_parameters[param_name]
                    # Проверка не удаленно ли текущее значение из списка
                    if current_value in options.values():
                        dropdown_value = current_value.get('function_name')
                        function_card = current_value.get('value')

                        if isinstance(function_card, FunctionCard):
                            function_card = function_card.function.result
                        value_to_print = f"{dropdown_value}: {[elem.get('type') for elem in function_card]}"
                    # else:
                    #     # Установка дефолтного значения
                    #     self.function.set_parameter_value(param_name, options[dropdown_value], 'Не выбраны []')
                        # self.update_function_card()
                    self.function.set_parameter_value(param_name, options[dropdown_value], value_to_print)
                    

                    param_editor = Dropdown(
                        dense=True,
                        label=param.get('title'),
                        options=[
                            dropdown.Option(key=key, text=key)
                            for key in options.keys()
                        ],
                        value=dropdown_value,
                        data={
                            'param_name': param_name,
                            'data': options
                        },
                        on_change=self._on_change_dropdown_function_value,
                    )

                case "slider":                    
                    ref_slider_text = Ref[Text]()
                    slider_divisions = int((param.get('max', 0) - param.get('min', 0)) / param.get('step', 1))
                    param_editor = Column(
                        controls=[
                            Text(
                                ref=ref_slider_text,
                                value=f'{param.get("title")}: {current_parameters[param_name]}',
                            ),
                            Slider(
                                min=param.get('min'),
                                max=param.get('max'),
                                value=current_parameters[param_name],
                                divisions=slider_divisions,
                                label='{value}',
                                data={
                                    "slider_text": ref_slider_text,
                                    'param_title': param.get("title"),
                                    'param_name': param_name,
                                    'round_digits': param.get('round_digits', 3)
                                },
                                on_change_end=self._on_change_slider_value,
                            )
                        ],
                    )

                case 'checkbox':
                    checkboxes = param.get('checkboxes', [])
                    ref_checkboxes = [Ref[Checkbox]() for _ in range(len(checkboxes))]
                    param_editor = Column(
                        controls=[
                            Checkbox(
                                label=checkbox.get('label'),
                                value=checkbox.get('default_value'),
                                ref=ref_checkboxes[idx],
                                data={
                                    'key': checkbox.get('key'),
                                    'ref_checkboxes': ref_checkboxes,
                                    'param_name': param_name,
                                },
                                on_change=self._on_change_checkbox_value
                            )
                            for idx, checkbox in enumerate(checkboxes)
                        ]
                    )

                case 'switch':
                    param_editor = Row(
                        controls=[
                            Text(value=param.get('title')),
                            Switch(
                                label_position=LabelPosition.LEFT,
                                value=current_parameters[param_name],
                                data={'param_name': param_name},
                                on_change=self._on_change_switch_value,
                            )
                        ],
                        expand=True,
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                    )
                    
                case 'text_field':
                    param_editor = TextField(
                        label=param.get('label', ''),
                        prefix_text=param.get('prefix_text', ''),
                        hint_text=param.get('hint_text', ''),
                        hint_style=TextStyle(italic=True),
                        helper_text=param.get('helper_text', ''),
                        dense=True,
                        autocorrect=param.get('autocorrect', False),
                        value=current_parameters[param_name],
                        data={
                            'param_name': param_name,
                            'text_type': param.get('text_type', ''),
                        },
                        on_change=self._is_text_field_value_valid,
                        on_blur=self._on_change_text_field_value,
                        on_submit=self._on_change_text_field_value,
                    )

                case 'file_picker':
                    ref_files = Ref[Column]()
                    pick_files_dialog = FilePicker(
                        data={
                            'param_name': param_name,
                            'ref_files': ref_files
                        },
                        on_result=self.on_file_picker_result,
                    )
                    self.page.overlay.append(pick_files_dialog)
                    self.page.update()

                    pick_files_params = param.get('pick_files_parameters', {})
                    param_editor = Row(
                        controls=[
                            Column(
                                controls=[
                                    Text(value=param.get('title', '')),
                                    Column(
                                        controls=[
                                            Text(f"{file['name']} ({self._convert_size(file['size'])})")
                                            for file in current_parameters.get(param_name, [])
                                        ],
                                        ref=ref_files,
                                    ),
                                    ElevatedButton(
                                        text=param.get('button_text', ''),
                                        icon=icons.UPLOAD_FILE,
                                        on_click=lambda _: pick_files_dialog.pick_files(
                                            dialog_title = pick_files_params.get('dialog_title'),
                                            initial_directory = pick_files_params.get('initial_directory'),
                                            file_type = pick_files_params.get('file_type', FilePickerFileType.ANY)
                                                if param.get('allowed_extensions') is None else FilePickerFileType.CUSTOM,
                                            allowed_extensions = pick_files_params.get('allowed_extensions'),
                                            allow_multiple = pick_files_params.get('allow_multiple'),
                                        ),
                                    ),
                                ]
                            )
                        ],
                        expand=True,
                    )
                
                case 'textfields_datatable':
                    ref_data_table = Ref[DataTable]()
                    ref_delete_button = Ref[IconButton]()

                    column_names = param.get('columns', [])
                    columns = [
                        DataColumn(
                            label=Text(values.get('name', key)),
                            tooltip=values.get('tooltip')
                        )
                        for key, values in column_names.items()
                    ]
                    rows = [
                        DataRow(
                            cells=[
                                DataCell(TextField(
                                    value=str(value),
                                    expand=True,
                                    border_radius=0,
                                    border_color=colors.with_opacity(0.0, colors.PRIMARY),
                                    text_align=TextAlign.CENTER,
                                    keyboard_type=KeyboardType.NUMBER,
                                    focused_color=colors.BLUE,
                                    data={
                                        'param_name': param_name,
                                        'text_type': 'number',
                                        'ref_data_table': ref_data_table,
                                        'column_name': column_name
                                    },
                                    on_change=self._is_text_field_value_valid,
                                    on_blur=self._on_change_textfields_datatable_cell_value,
                                    on_submit=self._on_change_textfields_datatable_cell_value,
                                ))
                                for column_name, value in row_values.items()
                            ],
                            data={
                                'ref_data_table': ref_data_table,
                                'ref_delete_button': ref_delete_button,
                            },
                            on_select_changed=self.on_textfields_datatable_select_changed
                        )
                        for row_idx, row_values in current_parameters[param_name].items()
                    ]

                    param_editor = Column(
                        controls=[
                            Markdown(value=param.get('title', '')),
                            DataTable(
                                columns=columns,
                                rows=rows,
                                ref=ref_data_table,
                                width=310,
                                column_spacing=0,
                                horizontal_margin=0,
                                border_radius=10,
                                border=border.all(1, colors.with_opacity(0.5, colors.ON_SURFACE)),
                                vertical_lines=BorderSide(1, colors.with_opacity(0.3, colors.ON_SURFACE)),
                                horizontal_lines=BorderSide(1, colors.with_opacity(0.3, colors.ON_SURFACE)),
                                show_checkbox_column=True,
                                checkbox_horizontal_margin=0,
                            ),
                            Row(
                                controls=[
                                    IconButton(
                                        icon=icons.PLAYLIST_ADD,
                                        tooltip="Добавить строку",
                                        data={
                                            'ref_data_table': ref_data_table,
                                            "ref_delete_button": ref_delete_button,
                                            'param_name': param_name,
                                            'column_names': column_names.keys(),
                                        },
                                        on_click=self.add_textfields_datatable_row,
                                    ),
                                    IconButton(
                                        icon=icons.DELETE_SWEEP,
                                        tooltip="Удалить выбранные строки",
                                        ref=ref_delete_button,
                                        disabled=True,
                                        data={'ref_data_table': ref_data_table},
                                        on_click=self.delete_textfields_datatable_rows,
                                    )
                                ],
                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                            )
                        ],
                    ) 
                    
            # Добавление представления параметра в список
            parameters_view_list.append(
                Container(
                    content=param_editor,
                    data=param_type,
                    padding=10,
                    border_radius=10,
                    border=border.all(1, colors.with_opacity(0.05, colors.SECONDARY)),
                    bgcolor=colors.BLACK12
                )
            )
        return parameters_view_list


    def _on_change_slider_value(self, e) -> None:
        '''
        Обнавляет значение параметра в экземпляре класса Function, заголовке слайдера и карточке функции
        '''
        # ЕСЛИ БУДЕТ ЛАГАТЬ ПЕРЕПИСАТЬ НА ОБНОВЛЕНИЕ ПАРАМЕТРОВ ФУНКЦИИ ПО КНОПКЕ
        slider_title_control = e.control.data.get('slider_text').current
        slider_title_text = e.control.data.get('param_title')
        param_name = e.control.data.get('param_name')
        round_digits = e.control.data.get('round_digits', 3)
        param_value = round(e.control.value, round_digits)

        slider_title_control.value = f"{slider_title_text}: {param_value}"
        self.function.set_parameter_value(param_name, param_value)

        self.update_function_card()


    def _on_change_dropdown_value(self, e) -> None:
        '''
        Обновляет значение параметра в экземпляре класса Function и карточке функции
        '''
        param_name = e.control.data.get('param_name')
        param_value = e.control.value
        self.function.set_parameter_value(param_name, param_value)

        self.update_function_card()


    def _on_change_dropdown_function_value(self, e) -> None:
        '''
        Обновляет значение параметра в экземпляре класса Function и карточке функции
        '''
        param_name = e.control.data.get('param_name')
        dropdown_value = e.control.value
        param_value = e.control.data.get('data').get(dropdown_value)

        function_card = param_value.get('value')
        if isinstance(function_card, FunctionCard):
            function_card.list_dependent_functions.append(self)
            self.provider_function = function_card

            function_card = function_card.function.result

        self.function.set_parameter_value(
            param_name, param_value, f"{param_value.get('function_name')}: {[elem.get('type') for elem in function_card]}"
        )
        self.update_function_card()

    
    def _on_change_checkbox_value(self, e) -> None:
        '''
        Обновляет значение параметр в экземпляре класса Function
        Изменяет список выбранных чекбоксов
        '''
        checkbox_key = e.control.data.get('key')
        checkbox_value = e.control.value
        param_name = e.control.data.get('param_name')

        param_current_value = self.function.get_parameter_value(param_name).get('value', [])
        if checkbox_value:
            param_current_value.append(checkbox_key)
        else:
            param_current_value.remove(checkbox_key)
        self.function.set_parameter_value(param_name, param_current_value)
        self.update_function_card()
    

    def _on_change_switch_value(self, e) -> None:
        '''
        Обновляет значение параметра переключателя в экземпляре класса Function
        '''
        switch_value = e.control.value
        param_name = e.control.data.get('param_name')
        self.function.set_parameter_value(param_name, switch_value)

        self.update_function_card()


    def _is_text_field_value_valid(self, e) -> None:
        '''
        Проверка валидности значения текстового поля
        '''
        text_type = e.control.data.get('text_type')
        text_field_value = e.control.value
        
        error_message = ''
        if text_field_value != '':
            match text_type:
                case 'function':
                    if text_field_value:
                        if not re.match(f"^[a-z0-9+\-*/()., ]*$", text_field_value):
                            error_message = f"Ошибка: Недопустимые символы в функции"
                        else:
                            try:
                                ast.parse(text_field_value)
                                sp.sympify(text_field_value, evaluate=False)
                                sp.parse_expr(text_field_value)
                            except Exception as exeption:
                                error_message = f"Ошибка: {exeption}"
                case 'int_number':
                    if not text_field_value.isnumeric():
                        error_message = f"Не целое число"
                case 'number':
                    try:
                        float(text_field_value)
                    except ValueError:
                        error_message = f"Неверный формат числа"

        e.control.error_text = error_message
        e.control.update()


    def _on_change_text_field_value(self, e) -> None:
        '''
        Обновляет значение параметра текстового поля в экземпляре класса Function
        '''
        if e.control.error_text:
            return
        text_field_value = e.control.value
        param_name = e.control.data.get('param_name')
        self.function.set_parameter_value(
            param_name, text_field_value,
            text_field_value.replace('**', '\*\*') if text_field_value else 'Нет значения'
        )
        self.update_function_card()


    def _convert_size(self, size):
        '''
        Конвертирует размер в байтах в строку
        '''
        if not size:
            return "0 байт"
        if size < 1024:
            return f"{size} байт"
        elif size < 1024 * 1024:
            return f"{size / 1024:.2f} КБ"
        elif size < 1024 * 1024 * 1024:
            return f"{size / (1024 * 1024):.2f} МБ"
        else:
            return f"{size / (1024 * 1024 * 1024):.2f} ГБ"


    def on_file_picker_result(self, e: FilePickerResultEvent):
        '''
        Обновляет список файлов в параметре экземпляра класса Function
        '''
        files_list = []
        if e.files is not None:
            for file in e.files:
                files_list.append({
                    'name': file.name,
                    'path': file.path,
                    'size': file.size,
                })

            files = e.control.data.get('ref_files').current
            files.controls = [
                Text(f"{file['name']} ({self._convert_size(file['size'])})")
                for file in files_list
            ]

            param_name = e.control.data.get('param_name')
            self.function.set_parameter_value(
                param_name, files_list, [file['name'] for file in files_list]
            )
            self.update_function_card()


    def on_textfields_datatable_select_changed(self, e) -> None:
        '''
        Изменяет выделение нажатой строки в таблице
        '''
        e.control.selected = not e.control.selected
        e.control.update()

        data_table_control = e.control.data.get('ref_data_table').current
        delete_button_control = e.control.data.get('ref_delete_button').current
        
        select_rows_count = len([row for row in data_table_control.rows if row.selected])
        delete_button_control.disabled = select_rows_count == 0
        delete_button_control.update()


    def add_textfields_datatable_row(self, e) -> None:
        '''
        Добавляет строку в таблицу
        '''
        ref_data_table = e.control.data.get('ref_data_table')
        ref_delete_button = e.control.data.get('ref_delete_button')
        param_name = e.control.data.get('param_name')
        column_names = e.control.data.get('column_names')

        data_table_control = ref_data_table.current
        data_table_control.rows.append(
            DataRow(
                cells=[
                    DataCell(TextField(
                        expand=True,
                        border_radius=0,
                        border_color=colors.with_opacity(0.0, colors.PRIMARY),
                        text_align=TextAlign.CENTER,
                        keyboard_type=KeyboardType.NUMBER,
                        focused_color=colors.BLUE,
                        data={
                            'param_name': param_name,
                            'text_type': 'number',
                            'ref_data_table': ref_data_table,
                            'column_name': column_name
                        },
                        on_change=self._is_text_field_value_valid,
                        on_blur=self._on_change_textfields_datatable_cell_value,
                        on_submit=self._on_change_textfields_datatable_cell_value,
                    ))
                    for column_name in column_names
                ],
                data={
                    'ref_data_table': ref_data_table,
                    'ref_delete_button': ref_delete_button,
                },
                on_select_changed=self.on_textfields_datatable_select_changed
            )
        )
        data_table_control.update()

    
    def delete_textfields_datatable_rows(self, e) -> None:
        '''
        Удаляет выбранные строки в таблице
        '''
        data_table_control = e.control.data.get('ref_data_table').current
        data_table_control.rows = [row for row in data_table_control.rows if not row.selected]
        data_table_control.update()

        e.control.disabled = True
        e.control.update()


    def _on_change_textfields_datatable_cell_value(self, e) -> None:
        '''
        Обновляет значение параметра при обновлении значения ячейки таблицы
        '''
        rows = e.control.data.get('ref_data_table').current.rows

        # Проверка на наличе некоректных данных в ячейках
        error_text_list = [cell.content.error_text for row in rows for cell in row.cells if cell.content.error_text]
        if len(error_text_list) > 0:
            return
        
        # Берем только строки, в которых все ячейки заполнены
        rows = [row for row in rows if len([1 for cell in row.cells if cell.content.value != '']) == len(row.cells)]
        
        textfields_datatable_value = {
            idx: {
                cell.content.data.get('column_name'): float(cell.content.value)
                for cell in row.cells
            }
            for idx, row in enumerate(rows)
        }

        param_name = e.control.data.get('param_name')
        self.function.set_parameter_value(
            param_name, textfields_datatable_value,
            str(textfields_datatable_value).replace('**', '\*\*') if textfields_datatable_value else 'Нет значения'
        )
        self.update_function_card()


    def _get_card_parameters_text(self) -> str:
        '''
        Возвращает текст с параметрами для карточки функции
        '''
        parameters = self.function.get_parameters_dict(to_print=True)

        formatted_parameters = []
        for param, item in parameters.items():
            formatted_item = f"*{param}*:\u00A0**{item}**"
            formatted_parameters.append(formatted_item)

        parameters_text = "; ".join(formatted_parameters)
        return '#### Параметры:\n' + parameters_text + '\n'
    
    
    def _get_card_parameters_result(self, max_rows=10) -> str:
        df_list = self.function.result
        if not df_list:
            return '***Нет данных***'
        
        markdown_table_list = []
        for df in df_list:
            data = df.get('data', None)
            if data is None:
                continue

            data_type = df.get('type', 'Не определено')
            data_title = 'Данные для графика: ***' + data_type + '***\n\n'

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
        return '\n\n'.join(markdown_table_list) if len(markdown_table_list) > 0 else '***Нет данных***'


    def _get_result_view_list(self) -> Column:
        dataframe_list = self.function.result
        result_view = None

        if not dataframe_list:
            result_view = Row(
                alignment=MainAxisAlignment.CENTER,
                controls=[
                    Text(value='Нет данных для построения графиков функции ' + self.function_name, weight=FontWeight.BOLD, size=20),
                ]
            )
            return result_view
        
        colors_list = ['green', 'blue', 'red', 'yellow', 'purple',
                       'orange', 'pink', 'brown', 'cyan', 'magenta',
                       'teal', 'gray', 'black', 'lime', 'olive',
                       'violet']

        graphs_cnt = len(dataframe_list)
        grid = []
        row = []
        for idx in range(1, graphs_cnt + 1):
            row.append(self._get_result_element_view(dataframe_list[idx - 1], colors_list[(idx - 1) % len(colors_list)]))

            if (
                graphs_cnt <= 3 or len(row) == 3 or idx == graphs_cnt
                or (graphs_cnt % 3 == 1 and graphs_cnt - idx < 3 and len(row) == 2)
            ):
                grid.append(Row(controls=row, vertical_alignment=CrossAxisAlignment.START))
                row = []
        
        result_view = Column(
            controls=[
                Row(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        Text(value=f"График{'и' if graphs_cnt > 1 else ''} функции {self.function_name}", weight=FontWeight.BOLD, size=20),
                    ]
                ),
                Column(controls=grid),
            ]
        )
        return result_view
    

    def _get_result_element_view(self, dataframe, color='green') -> Container:
        if not dataframe:
            return None
        
        element_controls = []

        error_message = dataframe.get('error_message')
        if error_message:
            element_controls.append(
                self._get_result_error_message(error_message)
            )
        
        view_list = dataframe.get('view')
        if 'chart' in view_list:
            element_controls.append(self._get_function_result_graphic(dataframe, color=color))
        if 'table_data' in view_list:
            element_controls.append(self._get_datatable_data(dataframe))
        if 'table_statistics' in view_list:
            element_controls.append(self._get_datatable_statistics(dataframe))

        extra_data = dataframe.get('extra_data')
        if extra_data:
            extra_data_name = extra_data.get('type')
            extra_data_control = self._get_result_element_view(extra_data, color=color)
            extra_data_view = self._get_dropdown_conteiner_for_control(
                control=extra_data_control,
                button_name=f"Показать дополнительные данные:{(f' ***{extra_data_name.strip()}***')}",
                is_open=False,
            )
            element_controls.append(extra_data_view)

        initial_data = dataframe.get('initial_data')
        if initial_data:
            initial_data_name = initial_data.get('type')
            initial_data_control = self._get_result_element_view(initial_data, color=color)
            initial_data_view = self._get_dropdown_conteiner_for_control(
                control=initial_data_control,
                button_name=f"Показать исходные данные:{(f' ***{initial_data_name.strip()}***')}",
                is_open=False,
            )
            element_controls.append(initial_data_view)

        return Column(expand=True, controls=element_controls)
    

    def _get_result_error_message(self, error_message):
        error_message_view = Container(
            content=Row(
                controls=[
                    Icon(name=icons.ERROR_OUTLINE, color=colors.RED),
                    Row(
                        expand=True,
                        wrap=True,
                        controls=[
                            Text(
                                value=f'Ошибка: {error_message}', 
                                color=colors.RED, 
                                weight=FontWeight.BOLD, 
                                size=16, 
                                max_lines=3
                            ),
                        ]
                    )
                ],
                expand=True,
            ),
            bgcolor=colors.with_opacity(0.05, colors.RED),
            border=border.all(width=1,color=colors.RED),
            border_radius=10,
            padding=10,
            margin=margin.only(left=10),
        )
        return error_message_view



    def _get_function_result_graphic(self, dataframe, column_names=None, color=None, graphic_curved=False, max_points_count = 1500) -> Container:
        df = dataframe.get('data')
        graphic_title = dataframe.get('type')

        data_series = []

        if color is None:
            color = colors.LIGHT_GREEN

        if column_names is None:
            column_names = df.columns.tolist()  # Получаем названия столбцов из датафрейма

        if len(df) > max_points_count:
            step = round(len(df) / max_points_count)
            df = df.iloc[::int(step)]

        data_points = [
            LineChartDataPoint(x, y)
            for x, y in zip(df.iloc[:, 0], df.iloc[:, 1])
        ]

        data_series.append(
            LineChartData(
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
                width=1, color=colors.with_opacity(0.2, colors.ON_SURFACE),
            ),
            vertical_grid_lines=ChartGridLines(
                width=1, color=colors.with_opacity(0.2, colors.ON_SURFACE),
            ),
            tooltip_bgcolor=colors.with_opacity(0.8, colors.BLACK38),
            expand=True,
        )

        chart_view = Row(controls=[chart])
        if dataframe.get('main_view') != 'chart':
            chart_view = self._get_dropdown_conteiner_for_control(
                control=chart,
                button_name=f"Показать график:{(f' ***{graphic_title.strip()}***')}"
            )
        return chart_view


    def _get_datatable_data(self, dataframe) -> Container:
        '''
        Сзодает горизонтальную таблицу данных с прокруткой значений по горизонтали
        '''
        df = dataframe.get('data')
        df_name = dataframe.get('type')
        transposed_df = df.transpose()

        # Создайте таблицу с заголовками (первый столбец)
        header_table = DataTable(
            columns=[DataColumn(Text(""))],
            rows=[
                DataRow([DataCell(Text(str(idx)))])
                for idx in transposed_df.index
            ],
            border=border.only(right=BorderSide(1, color=colors.with_opacity(0.2, colors.ON_SURFACE))),
            horizontal_margin=10,
            heading_row_height=40,
            data_row_max_height=40,
        )

        # Создайте таблицу с данными (остальные столбцы)
        data_table = DataTable(
            columns=[
                DataColumn(Text(str(col)), numeric=True)
                for col in transposed_df.columns
            ],
            rows=[
                DataRow(
                    cells=[
                        DataCell(content=Text(str(value)) if not pd.isna(value) else '')
                        for value in transposed_df.loc[idx]
                    ]
                )
                for idx in transposed_df.index
            ],
            column_spacing=15,
            heading_row_height=40,
            data_row_max_height=40,
            vertical_lines=BorderSide(1, color=colors.with_opacity(0.05, colors.ON_SURFACE))
        )
        
        datatable = Container(
            expand=True,
            content=Row(
                spacing=0,
                controls=[
                    header_table,
                    Row(
                        expand=True,
                        tight=True,
                        scroll=ScrollMode.ADAPTIVE,
                        controls=[data_table]
                    )
                ]
            ),
            border=border.all(1, colors.with_opacity(0.5, colors.ON_SURFACE)),
            border_radius=10,
        )
        # data_table = Markdown(    # ПОПЫТКА ОТОБРАЖАТЬ ГРАФИКИ, ТАКОЙ СПОСОБ БЫ УСКОРИЛ РАБОТУ, ОДНАКО СЕЙЧАС ОТОБРАЖАЕТСЯ НЕКОРРЕКТНО
        #     expand=True,
        #     value=transposed_df.to_markdown(),
        #     extension_set=MarkdownExtensionSet.GITHUB_WEB,
        # )

        datatable_viwe = Row(controls=[datatable])
        if dataframe.get('main_view') != 'table_data':
            datatable_viwe = self._get_dropdown_conteiner_for_control(
                control=datatable,
                button_name=f"Показать таблицу данных:{(f' ***{df_name.strip()}***')}"
            )
        return datatable_viwe
    

    def _get_datatable_statistics(self, dataframe) -> Container:
        '''
        Сзодает вертикальную таблицу для вывода данных
        '''
        df = dataframe.get('data')
        df_name = dataframe.get('type')
        columns = [DataColumn(Text(col)) for col in df.columns]
        rows = []

        for _, row in df.iterrows():
            cells = [DataCell(Text(str(value))) for value in row]
            rows.append(DataRow(cells=cells))

        datatable = DataTable(
            columns=columns,
            rows=rows,
            border=border.all(1, colors.with_opacity(0.5, colors.ON_SURFACE)),
            vertical_lines=BorderSide(1, color=colors.with_opacity(0.05, colors.ON_SURFACE)),
            border_radius=10,
            expand=True,
        )

        datatable_viwe = Row(controls=[datatable])
        if dataframe.get('main_view') != 'table_statistics':
            datatable_viwe = self._get_dropdown_conteiner_for_control(
                control=datatable,
                button_name=f"Показать таблицу статистических параметров:{(f' ***{df_name.strip()}***')}"
            )
        return datatable_viwe
    

    def _get_dropdown_conteiner_for_control(self, control, button_name='Показать', is_open=True) -> Container:
        '''
        Создает контейнер с кнопкой для скрытия/открытия переданного виджета
        '''
        ref_control = Ref[Container]()

        button = IconButton(
            icon=icons.KEYBOARD_ARROW_UP,
            data={
                'control': ref_control,
                'name': button_name,
            },
            on_click=self._change_control_visible
        )
        if not is_open:
            button.icon = None
            button.expand = True
            button.content = Row(
                controls=[
                    Icon(name='KEYBOARD_ARROW_DOWN'),
                    Row(
                        expand=True,
                        wrap=True,
                        controls=[Markdown(value=button_name)]
                    )
                ]
            )

        dropdown_conteiner = Container(
            content=Row(
                controls=[
                    button,
                    Container(
                        ref=ref_control,
                        expand=True,
                        content=control,
                        visible=is_open
                    )
                ],
                vertical_alignment=CrossAxisAlignment.START,
                spacing=0,
            ),
            animate_size=animation.Animation(200, AnimationCurve.FAST_OUT_SLOWIN),
            border_radius=10,
            # margin=margin.only(left=10),
        )
        return dropdown_conteiner


    def _change_control_visible(self, e) -> None:
        data = e.control.data
        control = data.get('control').current
        button = e.control
        button_name = data.get('name')

        control.visible = not control.visible

        if control.visible:
            button.icon = icons.KEYBOARD_ARROW_UP
            button.expand = False
            button.content = None
        else:
            button.icon = None
            button.expand = True
            button.content = Row(
                controls=[
                    Icon(name='KEYBOARD_ARROW_DOWN'),
                    Row(
                        expand=True,
                        wrap=True,
                        controls=[
                            Markdown(value=button_name),
                            # Text(value=button_name, max_lines=3),
                        ]
                    )
                ]
            )
        self.graphic_area.update()


    def get_result_view(self) -> Container:
        return self.result_view
    