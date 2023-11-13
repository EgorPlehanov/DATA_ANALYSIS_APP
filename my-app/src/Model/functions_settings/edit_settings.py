from ..functions.edit_functions import EditFunctions


functions_info = {
    'noise': {
        'function': EditFunctions.noise,
        'type': 'edit',
        'name': 'Случайный шум',
        'parameters': {
            'data': {
                "type": "dropdown_function_data",
                "title": "Выбор набора данных",
                "options": {'Не выбраны': {'function_name': 'Не выбраны', 'value': []}},
                "default_value": {'function_name': 'Не выбраны', 'value': []},
                "default_value_to_print": 'Не выбраны: []',
            },
            'N': {
                "type": "slider",
                "title": "Длина данных (N)",
                'text_type': 'int_number',
                "min": 10,
                "max": 5000,
                "step": 10,
                "default_value": 600,
            },
            'R': {
                "type": "slider",
                "title": "Параметр диапозона (R)",
                "min": 0.1,
                "max": 1000.0,
                "step": 0.1,
                "default_value": 0.1,
            },
            'delta': {
                "type": "slider",
                "title": "Шаг по оси x (delta)",
                "min": 1,
                "max": 15,
                "step": 1,
                "default_value": 1,
            },
            'show_table_data': {
                "type": "switch",
                "title": "Показывать таблицу данных?",
                'default_value': False
            },
        }
    },

    'myNoise': {
        'function': EditFunctions.my_noise,
        'type': 'edit',
        'name': 'Мой случайный шум',
        'parameters': {
            'data': {
                "type": "dropdown_function_data",
                "title": "Выбор набора данных",
                "options": {'Не выбраны': {'function_name': 'Не выбраны', 'value': []}},
                "default_value": {'function_name': 'Не выбраны', 'value': []},
                "default_value_to_print": 'Не выбраны: []',
            },
            'N': {
                "type": "slider",
                "title": "Длина данных (N)",
                'text_type': 'int_number',
                "min": 10,
                "max": 5000,
                "step": 10,
                "default_value": 600,
            },
            'R': {
                "type": "slider",
                "title": "Параметр диапозона (R)",
                "min": 0.1,
                "max": 1000.0,
                "step": 0.1,
                "default_value": 0.1,
            },
            'delta': {
                "type": "slider",
                "title": "Шаг по оси x (delta)",
                "min": 1,
                "max": 15,
                "step": 1,
                "default_value": 1,
            },
            'show_table_data': {
                "type": "switch",
                "title": "Показывать таблицу данных?",
                'default_value': False
            },
        }
    },

    'shift': {
        'function': EditFunctions.shift,
        'type': 'edit',
        'name': 'Сдвиг',
        'parameters': {
            'data': {
                "type": "dropdown_function_data",
                "title": "Выбор набора данных",
                "options": {'Не выбраны': {'function_name': 'Не выбраны', 'value': []}},
                "default_value": {'function_name': 'Не выбраны', 'value': []},
                "default_value_to_print": 'Не выбраны: []',
            },
            'C': {
                "type": "slider",
                "title": "Cмещение данных (C)",
                "min": -1000,
                "max": 1000,
                "step": 0.1,
                "default_value": 200,
            },
            'N1': {
                "type": "slider",
                "title": "Cмещение от (N1)",
                'text_type': 'int_number',
                "min": 0,
                "max": 5000,
                "step": 1,
                "default_value": 100,
            },
            'N2': {
                "type": "slider",
                "title": "Cмещение до (N2)",
                'text_type': 'int_number',
                "min": 0,
                "max": 5000,
                "step": 1,
                "default_value": 500,
            },
            'show_table_data': {
                "type": "switch",
                "title": "Показывать таблицу данных?",
                'default_value': False
            },
        }
    },

    'spikes': {
        'function': EditFunctions.spikes,
        'type': 'edit',
        'name': 'Одиночные выбросы',
        'parameters': {
            'data': {
                "type": "dropdown_function_data",
                "title": "Выбор набора данных",
                "options": {'Не выбраны': {'function_name': 'Не выбраны', 'value': []}},
                "default_value": {'function_name': 'Не выбраны', 'value': []},
                "default_value_to_print": 'Не выбраны: []',
            },
            'N': {
                "type": "slider",
                "title": "Длина данных (N)",
                'text_type': 'int_number',
                "min": 10,
                "max": 10000,
                "step": 10,
                "default_value": 1000,
            },
            'M': {
                "type": "slider",
                "title": "Количество выбросов (M)",
                'text_type': 'int_number',
                "min": 1,
                "max": 100,
                "step": 1,
                "default_value": 10,
            },
            'R': {
                "type": "slider",
                "title": "Опорное значение (R)",
                "min": 1,
                "max": 10000,
                "step": 1,
                "default_value": 1000,
            },
            'Rs': {
                "type": "slider",
                "title": "Длина данных (Rs)",
                "min": 1,
                "max": 1000,
                "step": 1,
                "default_value": 500,
            },
            'show_table_data': {
                "type": "switch",
                "title": "Показывать таблицу данных?",
                'default_value': False
            },
        }
    },

    'add_model': {
        'function': EditFunctions.add_model,
        'type': 'edit',
        'name': 'Поэлементное сложение',
        'parameters': {
            'first_data': {
                "type": "dropdown_function_data",
                "title": "Выбор первого набора данных",
                "options": {'Не выбраны': {'function_name': 'Не выбраны', 'value': []}},
                "default_value": {'function_name': 'Не выбраны', 'value': []},
                "default_value_to_print": 'Не выбраны: []',
            },
            'second_data': {
                "type": "dropdown_function_data",
                "title": "Выбор второго набора данных",
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

    'mult_model': {
        'function': EditFunctions.mult_model,
        'type': 'edit',
        'name': 'Поэлементное умножение',
        'parameters': {
            'first_data': {
                "type": "dropdown_function_data",
                "title": "Выбор первого набора данных",
                "options": {'Не выбраны': {'function_name': 'Не выбраны', 'value': []}},
                "default_value": {'function_name': 'Не выбраны', 'value': []},
                "default_value_to_print": 'Не выбраны: []',
            },
            'second_data': {
                "type": "dropdown_function_data",
                "title": "Выбор второго набора данных",
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

    'anti_shift': {
        'function': EditFunctions.anti_shift,
        'type': 'edit',
        'name': 'Удаление смещения',
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
            }
        }
    },

    'anti_spike': {
        'function': EditFunctions.anti_spike,
        'type': 'edit',
        'name': 'Удаление выбросов',
        'parameters': {
            'data': {
                "type": "dropdown_function_data",
                "title": "Выбор набора данных",
                "options": {'Не выбраны': {'function_name': 'Не выбраны', 'value': []}},
                "default_value": {'function_name': 'Не выбраны', 'value': []},
                "default_value_to_print": 'Не выбраны: []',
            },
            'R': {
                "type": "slider",
                "title": "Пороговое значение диапозона (R)",
                "min": 1,
                "max": 10000,
                "step": 1,
                "default_value": 1000,
            },
            'show_table_data': {
                "type": "switch",
                "title": "Показывать таблицу данных?",
                'default_value': False
            }
        }
    },

    'anti_trend_linear': {
        'function': EditFunctions.anti_trend_linear,
        'type': 'edit',
        'name': 'Удаление линейного тренда',
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
            }
        }
    },

    'anti_trend_non_linear': {
        'function': EditFunctions.anti_trend_non_linear,
        'type': 'edit',
        'name': 'Удаление НЕ линейного тренда',
        'parameters': {
            'data': {
                "type": "dropdown_function_data",
                "title": "Выбор набора данных",
                "options": {'Не выбраны': {'function_name': 'Не выбраны', 'value': []}},
                "default_value": {'function_name': 'Не выбраны', 'value': []},
                "default_value_to_print": 'Не выбраны: []',
            },
            'W': {
                "type": "slider",
                "title": "Длина скользящего окна (W)",
                'text_type': 'int_number',
                "min": 1,
                "max": 5000,
                "step": 1,
                "default_value": 10,
            },
            'show_table_data': {
                "type": "switch",
                "title": "Показывать таблицу данных?",
                'default_value': False
            }
        }
    },

    'anti_noise': {
        'function': EditFunctions.anti_noise,
        'type': 'edit',
        'name': 'Gодавления случайного шума',
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
                "title": "Число реализаций (M)",
                'text_type': 'int_number',
                "min": 1,
                "max": 10000,
                "step": 1,
                "default_value": 10,
            },
            'show_table_data': {
                "type": "switch",
                "title": "Показывать таблицу данных?",
                'default_value': False
            }
        }
    }
}
