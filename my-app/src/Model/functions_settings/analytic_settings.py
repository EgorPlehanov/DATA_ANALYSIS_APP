from ..functions.analytic_functions import AnalyticFunctions


functions_info = {
    'statistics': {
        'function': AnalyticFunctions.statistics,
        'type': 'analytic',
        'name': 'Статистические данные',
        'parameters': {
            'data': {
                "type": "dropdown_function_data",
                "title": "Выбор набора данных",
                "options": {'Не выбраны': {'function_name': 'Не выбраны', 'value': []}},
                "default_value": {'function_name': 'Не выбраны', 'value': []},
                "default_value_to_print": 'Не выбраны: []',
            },
        }
    },

    'stationarity': {
        'function': AnalyticFunctions.stationarity,
        'type': 'analytic',
        'name': 'Стационарность',
        'parameters': {
            'data': {
                "type": "dropdown_function_data",
                "title": "Выбор набора данных",
                "options": {'Не выбраны': {'function_name': 'Не выбраны', 'value': []}},
                "default_value": {'function_name': 'Не выбраны', 'value': []},
                "default_value_to_print": 'Не выбраны: []',
            },
            'M': {
                "type": "slider",
                "title": "Количество интервалов (M)",
                'text_type': 'int_number',
                "min": 2,
                "max": 100,
                "step": 1,
                'round_digits': 0,
                "default_value": 10,
            }
        }
    },

    'hist': {
        'function': AnalyticFunctions.hist,
        'type': 'analytic',
        'name': 'Плотность вероятности',
        'parameters': {
            'data': {
                "type": "dropdown_function_data",
                "title": "Выбор набора данных",
                "options": {'Не выбраны': {'function_name': 'Не выбраны', 'value': []}},
                "default_value": {'function_name': 'Не выбраны', 'value': []},
                "default_value_to_print": 'Не выбраны: []',
            },
            'M': {
                "type": "slider",
                "title": "Количество интервалов (M)",
                'text_type': 'int_number',
                "min": 1,
                "max": 100,
                "step": 1,
                'round_digits': 0,
                "default_value": 10,
            },
            'is_density': {
                "type": "switch",
                "title": "Показывать плотность вероятности?",
                'default_value': True
            },
            'show_table_data': {
                "type": "switch",
                "title": "Показывать таблицу данных?",
                'default_value': True
            },
        }
    },

    'acf': {
        'function': AnalyticFunctions.acf,
        'type': 'analytic',
        'name': "Автокорреляция/Ковариация",
        'parameters': {
            'data': {
                "type": "dropdown_function_data",
                "title": "Выбор набора данных",
                "options": {'Не выбраны': {'function_name': 'Не выбраны', 'value': []}},
                "default_value": {'function_name': 'Не выбраны', 'value': []},
                "default_value_to_print": 'Не выбраны: []',
            },
            "function_type": {
                "type": "dropdown",
                "title": "Тип коэффициента",
                "options": [
                    {
                        "key": "autocorrelation",
                        "text": "Автокорреляция",
                    },
                    {
                        "key": "covariance",
                        "text": "Ковариация",
                    }
                ],
                "default_value": "autocorrelation",
            },
            'show_table_data': {
                "type": "switch",
                "title": "Показывать таблицу данных?",
                'default_value': False
            },
        }
    },

    "ccf": {
        'function': AnalyticFunctions.ccf,
        'type': 'analytic',
        'name': 'Кросс-корреляция',
        'parameters': {
            'first_data': {
                "type": "dropdown_function_data",
                "title": "Выбор набора данных",
                "options": {'Не выбраны': {'function_name': 'Не выбраны', 'value': []}},
                "default_value": {'function_name': 'Не выбраны', 'value': []},
                "default_value_to_print": 'Не выбраны: []',
            },
            'second_data': {
                "type": "dropdown_function_data",
                "title": "Выбор набора данных",
                "options": {'Не выбраны': {'function_name': 'Не выбраны', 'value': []}},
                "default_value": {'function_name': 'Не выбраны', 'value': []},
                "default_value_to_print": 'Не выбраны: []',
            },
            'show_table_data': {
                "type": "switch",
                "title": "Показывать таблицу данных?",
                'default_value': False
            },
        }
    },

    'fourier': {
        'function': AnalyticFunctions.fourier,
        'type': 'analytic',
        'name': 'Прямое преобразование Фурье',
        'parameters': {
            'data': {
                "type": "dropdown_function_data",
                "title": "Выбор набора данных",
                "options": {'Не выбраны': {'function_name': 'Не выбраны', 'value': []}},
                "default_value": {'function_name': 'Не выбраны', 'value': []},
                "default_value_to_print": 'Не выбраны: []',
            },
            'show_table_data': {
                "type": "switch",
                "title": "Показывать таблицу данных?",
                'default_value': False
            },
            'show_calculation_table': {
                "type": "switch",
                "title": "Показывать расчетную таблицу?",
                'default_value': False
            },
        }
    },

    'spectr_fourier': {
        'function': AnalyticFunctions.spectr_fourier,
        'type': 'analytic',
        'name': 'Амплитудный спектр Фурье',
        'parameters': {
            'data': {
                "type": "dropdown_function_data",
                "title": "Выбор набора данных",
                "options": {'Не выбраны': {'function_name': 'Не выбраны', 'value': []}},
                "default_value": {'function_name': 'Не выбраны', 'value': []},
                "default_value_to_print": 'Не выбраны: []',
            },
            'delta_t': {
                "type": "slider",
                "title": "Шаг дисеретизации (delta_t)",
                'round_digits': 5,
                "min": 0.0001,
                "max": 0.01,
                "step": 0.0001,
                "default_value": 0.0005,
            },
            'L_window': {
                "type": "slider",
                "title": "Длина окна (L_window)",
                'text_type': 'int_number',
                "min": 0,
                "max": 1000,
                "step": 1,
                'round_digits': 0,
                "default_value": 0,
            },
            'show_table_data': {
                "type": "switch",
                "title": "Показывать таблицу данных?",
                'default_value': False
            },
        }
    }

}