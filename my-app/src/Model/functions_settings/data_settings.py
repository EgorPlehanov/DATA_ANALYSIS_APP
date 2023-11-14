from ..functions.data_functions import DataFunctions


functions_info = {
    "trend": {
        "function": DataFunctions.trend,
        'type': 'data',
        'name': 'Тренд',
        "parameters": {
            "type": {
                "type": "dropdown",
                "title": "Тип тренда",
                "options": [
                    {
                        "key": "linear_rising",
                        "text": "Линейно восходящий",
                    },
                    {
                        "key": "linear_falling",
                        "text": "Линейно нисходящий",
                    },
                    {
                        "key": "nonlinear_rising",
                        "text": "Нелинейно восходящий",
                    },
                    {
                        "key": "nonlinear_falling",
                        "text": "Нелинейно нисходящий",
                    }
                ],
                "default_value": "linear_rising",
            },
            "a": {
                "type": "slider",
                "title": "Параметр (a)",
                "min": 0.01,
                "max": 100,
                "step": 0.01,
                "default_value": 0.01,
            },
            "b": {
                "type": "slider",
                "title": "Параметр (b)",
                "min": 0.1,
                "max": 10.0,
                "step": 0.1,
                "default_value": 1.0,
            },
            "step": {
                "type": "slider",
                "title": "Шаг по оси x (step)",
                "min": 0.0001,
                "max": 10,
                "step": 1,
                "default_value": 1,
            },
            "N": {
                "type": "slider",
                "title": "Длина данных (N)",
                'text_type': 'int_number',
                "min": 100,
                "max": 5000,
                "step": 100,
                'round_digits': 0,
                "default_value": 600,
            },
            'show_table_data': {
                "type": "switch",
                "title": "Показывать таблицу данных?",
                'default_value': False
            },
        }
    },

    'multi_trend': {
        'function': DataFunctions.multi_trend,
        'type': 'data',
        'name': 'Мультитренд',
        'parameters': {
            "type_list": {
                "type": "checkbox",
                "title": "Тип тренда",
                "checkboxes": [
                    {
                        "key": "linear_rising",
                        "label": "Линейно восходящий",
                        'default_value': True,
                    },
                    {
                        "key": "linear_falling",
                        "label": "Линейно нисходящий",
                        'default_value': True,
                    },
                    {
                        "key": "nonlinear_rising",
                        "label": "Нелинейно восходящий",
                        'default_value': True,
                    },
                    {
                        "key": "nonlinear_falling",
                        "label": "Нелинейно нисходящий",
                        'default_value': True,
                    }
                ],
                "default_value": ["linear_rising", "linear_falling", "nonlinear_rising", "nonlinear_falling"],
            },
            "a": {
                "type": "slider",
                "title": "Параметр a",
                "min": 0.01,
                "max": 10.0,
                "step": 0.01,
                "default_value": 0.01,
            },
            "b": {
                "type": "slider",
                "title": "Параметр (b)",
                "min": 0.1,
                "max": 10.0,
                "step": 0.1,
                "default_value": 1.0,
            },
            "step": {
                "type": "slider",
                "title": "Шаг по оси x (step)",
                "min": 1,
                "max": 15,
                "step": 1,
                "default_value": 1,
            },
            "N": {
                "type": "slider",
                "title": "Длина данных (N)",
                'text_type': 'int_number',
                "min": 100,
                "max": 5000,
                "step": 100,
                'round_digits': 0,
                "default_value": 600,
            },
            'show_table_data': {
                "type": "switch",
                "title": "Показывать таблицу данных?",
                'default_value': False
            },
        }
    },

    'combinate_trend': {
        'function': DataFunctions.combinate_trend,
        'type': 'data',
        'name': 'Кусочная функция',
        'parameters': {
            "type_list": {
                "type": "checkbox",
                "title": "Тип тренда",
                "checkboxes": [
                    {
                        "key": "linear_rising",
                        "label": "Линейно восходящий",
                        'default_value': True,
                    },
                    {
                        "key": "linear_falling",
                        "label": "Линейно нисходящий",
                        'default_value': True,
                    },
                    {
                        "key": "nonlinear_rising",
                        "label": "Нелинейно восходящий",
                        'default_value': True,
                    },
                    {
                        "key": "nonlinear_falling",
                        "label": "Нелинейно нисходящий",
                        'default_value': True,
                    }
                ],
                "default_value": ["nonlinear_rising", "nonlinear_falling", "linear_rising", "linear_falling"],
            },
            "a": {
                "type": "slider",
                "title": "Параметр (a)",
                "min": 0.01,
                "max": 10.0,
                "step": 0.01,
                "default_value": 0.01,
            },
            "b": {
                "type": "slider",
                "title": "Параметр (b)",
                "min": 0.1,
                "max": 10.0,
                "step": 0.1,
                "default_value": 1.0,
            },
            "step": {
                "type": "slider",
                "title": "Шаг по оси x (step)",
                "min": 1,
                "max": 15,
                "step": 1,
                "default_value": 1,
            },
            "N": {
                "type": "slider",
                "title": "Длина данных (N)",
                'text_type': 'int_number',
                "min": 100,
                "max": 5000,
                "step": 100,
                'round_digits': 0,
                "default_value": 600,
            },
            'show_table_data': {
                "type": "switch",
                "title": "Показывать таблицу данных?",
                'default_value': False
            },
        }
    },

    'harm': {
        'function': DataFunctions.harm,
        'type': 'data',
        'name': 'Гармонический процесс',
        'parameters': {
            "N": {
                "type": "slider",
                "title": "Длина данных (N)",
                'text_type': 'int_number',
                "min": 100,
                "max": 5000,
                "step": 10,
                'round_digits': 0,
                "default_value": 1024,
            },
            "A0": {
                "type": "slider",
                "title": "Амплитуда (A0)",
                "min": 1,
                "max": 1000,
                "step": 1,
                "default_value": 100,
            },
            "f0": {
                "type": "slider",
                "title": "Частота (f0), Гц",
                "min": 1,
                "max": 1000,
                "step": 1,
                "default_value": 15,
            },
            "delta_t": {
                "type": "slider",
                "title": "Временной интервал (delta_t)",
                "min": 0.0001,
                "max": 0.01,
                "step": 0.0001,
                "round_digits": 5,
                "default_value": 0.0001,
            },
            'show_table_data': {
                "type": "switch",
                "title": "Показывать таблицу данных?",
                'default_value': False
            },
        }
    },

    'poly_harm': {
        'function': DataFunctions.poly_harm,
        'type': 'data',
        'name': 'Полигармонический процесс',
        'parameters': {
            "N": {
                "type": "slider",
                "title": "Длина данных (N)",
                'text_type': 'int_number',
                "min": 100,
                "max": 5000,
                "step": 10,
                'round_digits': 0,
                "default_value": 1000,
            },
            "A_f_data": {
                "type": "textfields_datatable",
                "title": "Амплитуда (A) и частота (f)",
                "columns": {
                    "A": {
                        'name': 'A',
                        'tooltip': 'Амплитуда гармонического процесса',
                    },
                    "f": {
                        'name': 'f, Гц',
                        'tooltip': 'Частота гармонического процесса в герцах (Гц)'
                    },
                },
                "default_value": {
                    0: {"A": 100, "f": 33},
                    1: {"A": 15, "f": 5},
                    2: {"A": 20, "f": 170},
                },
            },
            "delta_t": {
                "type": "slider",
                "title": "Временной интервал (delta_t)",
                "min": 0.0001,
                "max": 0.01,
                "step": 0.0001,
                "round_digits": 5,
                "default_value": 0.0001,
            },
            'show_table_data': {
                "type": "switch",
                "title": "Показывать таблицу данных?",
                'default_value': False
            },
        }
    },

    'custom_function': {
        'function': DataFunctions.custom_function,
        'type': 'data',
        'name': 'Задать свою функцию',
        'parameters': {
            'expression': {
                'type': 'text_field',
                'text_type': 'function',
                'label': 'Функция',
                'prefix_text': 'y = ',
                'hint_text': 'например: 1 + sin(x**2)',
                'helper_text': 'Функция должна содержать только аргумент x',
                'default_value': 'x',
            },
            "N": {
                "type": "slider",
                "title": "Длина данных (N)",
                'text_type': 'int_number',
                "min": 100,
                "max": 5000,
                "step": 100,
                'round_digits': 0,
                "default_value": 600,
            },
            "step": {
                "type": "slider",
                "title": "Шаг по оси x (step)",
                "min": 0.1,
                "max": 10,
                "step": 0.1,
                "default_value": 1,
            },
            'show_table_data': {
                "type": "switch",
                "title": "Показывать таблицу данных?",
                'default_value': False
            },
        }
    },

    'data_download': {
        'function': DataFunctions.data_download,
        'type': 'data',
        'name': 'Загрузить свой набор данных',
        'parameters': {
            'input_data': {
                "type": "file_picker",
                "title": "Набор данных",
                'button_text': 'Выбрать набор данных',
                'pick_files_parameters': {
                    'dialog_title': 'Выбор набора данных',
                    'initial_directory': None,
                    'file_type': None,
                    'allowed_extensions': ['csv', 'xls', 'xlsx', 'xlsm', 'xlsb', 'odf', 'ods', 'odt', 'json', 'txt', 'dat'],
                    'allow_multiple': True,
                },
                "default_value": [],
            },
            'show_table_data': {
                "type": "switch",
                "title": "Показывать таблицу данных?",
                'default_value': False
            },
        }
    },
}