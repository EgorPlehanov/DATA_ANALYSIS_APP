import numpy as np
import pandas as pd



class Model:
    @staticmethod
    def get_info(name, return_type='both'):
        if name in Model.functions_info:
            info = Model.functions_info[name]
            if return_type == 'function':
                return info['function']
            elif return_type == 'parameters':
                return info['parameters']
            elif return_type == 'both':
                return info
        return None
    
    @staticmethod
    def get_functions_by_type(type):
        data_functions = []
        for key, info in Model.functions_info.items():
            if info.get('type') == type:
                data_functions.append({'key': key, 'name': info.get('name', key)})
        return data_functions
    

    def trend_function_linear_rising(t, a, b):
        return a * t + b

    def trend_function_linear_falling(t, a, b):
        return -a * t + b

    def trend_function_nonlinear_rising(t, a, b):
        return b * np.exp(a * t)

    def trend_function_nonlinear_falling(t, a, b):
        return b * np.exp(-a * t)


    def trend(type, a, b, step, N):
        t = np.arange(0, N, step)
        data = None

        if type == "linear_rising":
            data = Model.trend_function_linear_rising(t, a, b)
        elif type == "linear_falling":
            data = Model.trend_function_linear_falling(t, a, b)
        elif type == "nonlinear_rising":
            data = Model.trend_function_nonlinear_rising(t, a, b)
        elif type == "nonlinear_falling":
            data = Model.trend_function_nonlinear_falling(t, a, b)

        df = pd.DataFrame({'x': t, 'y': data})
        df = df[df['y'] <= 1000000000]
        df = df.round({'x': 4, 'y': 4})
        return [{
            'data': df,
            'type': type,
        }]
    

    def multi_trend(type_list, a, b, step, N):
        if len(type_list) == 0:
            return []
        
        df_list = []
        for type in type_list:
            df_list.append(*Model.trend(type, a, b, step, N))
        return df_list
    

    def combinate_trend(type_list, a, b, step, N):
        num_parts = len(type_list)
        if num_parts == 0:
            return []

        # Разделить период t на равные части
        t_parts = np.array_split(np.arange(0, N, step), num_parts)

        df_list = []
        previous_end_value = None
        for i, type in enumerate(type_list):
            # Сгенерировать данные для каждой части
            data = []
            if type == "linear_rising":
                data = Model.trend_function_linear_rising(t_parts[i], a, b)
            elif type == "linear_falling":
                data = Model.trend_function_linear_falling(t_parts[i], a, b)
            elif type == "nonlinear_rising":
                data = Model.trend_function_nonlinear_rising(t_parts[i], a, b)
            elif type == "nonlinear_falling":
                data = Model.trend_function_nonlinear_falling(t_parts[i], a, b)

            if previous_end_value is not None:
                shift = previous_end_value - data[0]
                data = [value + shift for value in data]

            df_list.append(pd.DataFrame({'x': t_parts[i], 'y': data}))

            # Обновите значение последнего элемента для следующей итерации
            previous_end_value = data[-1]
            
        # Объединить результаты
        combined_df = pd.concat(df_list, ignore_index=True)
        combined_df = combined_df[combined_df['y'] <= 1000000000]
        combined_df = combined_df.round({'x': 4, 'y': 4})
        return [{
            'data': combined_df,
            'type': ' -> '.join(type_list)
        }]


    def data_download(input_data):
        pass

    
Model.functions_info = {
        "trend": {
            "function": Model.trend,
            'type': 'data',
            'name': 'trend',
            "parameters": {
                "type": {
                    "title": "Тип тренда",
                    "type": "dropdown",
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
                    "title": "Параметр a",
                    "type": "slider",
                    "min": 0.01,
                    "max": 10.0,
                    "step": 0.01,
                    "default_value": 0.01,
                },
                "b": {
                    "title": "Параметр b",
                    "type": "slider",
                    "min": 0.1,
                    "max": 10.0,
                    "step": 0.1,
                    "default_value": 1.0,
                },
                "step": {
                    "title": "Интервал Δ",
                    "type": "slider",
                    "min": 1,
                    "max": 10,
                    "step": 1,
                    "default_value": 1,
                },
                "N": {
                    "title": "Длина данных N",
                    "type": "slider",
                    "min": 100,
                    "max": 5000,
                    "step": 100,
                    "default_value": 1000,
                },
            }
        },


        'multi_trend': {
            'function': Model.multi_trend,
            'type': 'data',
            'name': 'multi_trend',
            'parameters': {
                "type_list": {
                    "title": "Тип тренда",
                    "type": "checkbox",
                    "checkboxes": [
                        {
                            "key": "linear_rising",
                            "label": "linear_rising",
                            'default_value': True,
                        },
                        {
                            "key": "linear_falling",
                            "label": "linear_falling",
                            'default_value': True,
                        },
                        {
                            "key": "nonlinear_rising",
                            "label": "nonlinear_rising",
                            'default_value': True,
                        },
                        {
                            "key": "nonlinear_falling",
                            "label": "nonlinear_falling",
                            'default_value': True,
                        }
                    ],
                    "default_value": ["linear_rising", "linear_falling", "nonlinear_rising", "nonlinear_falling"],
                },
                "a": {
                    "title": "Параметр a",
                    "type": "slider",
                    "min": 0.01,
                    "max": 10.0,
                    "step": 0.01,
                    "default_value": 0.01,
                },
                "b": {
                    "title": "Параметр b",
                    "type": "slider",
                    "min": 0.1,
                    "max": 10.0,
                    "step": 0.1,
                    "default_value": 1.0,
                },
                "step": {
                    "title": "Интервал Δ",
                    "type": "slider",
                    "min": 1,
                    "max": 15,
                    "step": 1,
                    "default_value": 1,
                },
                "N": {
                    "title": "Длина данных N",
                    "type": "slider",
                    "min": 100,
                    "max": 5000,
                    "step": 100,
                    "default_value": 1000,
                },
            }
        },


        'combinate_trend': {
            'function': Model.combinate_trend,
            'type': 'data',
            'name': 'combinate_trend',
            'parameters': {
                "type_list": {
                    "title": "Тип тренда",
                    "type": "checkbox",
                    "checkboxes": [
                        {
                            "key": "linear_rising",
                            "label": "linear_rising",
                            'default_value': True,
                        },
                        {
                            "key": "linear_falling",
                            "label": "linear_falling",
                            'default_value': True,
                        },
                        {
                            "key": "nonlinear_rising",
                            "label": "nonlinear_rising",
                            'default_value': True,
                        },
                        {
                            "key": "nonlinear_falling",
                            "label": "nonlinear_falling",
                            'default_value': True,
                        }
                    ],
                    "default_value": ["linear_rising", "linear_falling", "nonlinear_rising", "nonlinear_falling"],
                },
                "a": {
                    "title": "Параметр a",
                    "type": "slider",
                    "min": 0.01,
                    "max": 10.0,
                    "step": 0.01,
                    "default_value": 0.01,
                },
                "b": {
                    "title": "Параметр b",
                    "type": "slider",
                    "min": 0.1,
                    "max": 10.0,
                    "step": 0.1,
                    "default_value": 1.0,
                },
                "step": {
                    "title": "Интервал Δ",
                    "type": "slider",
                    "min": 1,
                    "max": 15,
                    "step": 1,
                    "default_value": 1,
                },
                "N": {
                    "title": "Длина данных N",
                    "type": "slider",
                    "min": 100,
                    "max": 5000,
                    "step": 100,
                    "default_value": 1000,
                },
            }
        },


        'data_download': {
            'function': Model.data_download,
            'type': 'data',
            'name': 'Загрузить свой набор данных',
            'parameters': {
                'input_data': {
                    "title": "Выбор файла данных",
                    "type": "file_picker",
                    "default_value": None,
                }
            }
        }
    }
