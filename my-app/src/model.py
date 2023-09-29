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
    

    def trend_function_linear_rising(t, a, b):
        return -a * t + b

    def trend_function_linear_falling(t, a, b):
        return a * t + b

    def trend_function_nonlinear_rising(t, a, b):
        return b * np.exp(-a * t)

    def trend_function_nonlinear_falling(t, a, b):
        return -b * np.exp(-a * t)

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

        # return t, data
        df = pd.DataFrame({'t': t, 'data': data})
        return df
    
    def data_download(input_data):
        pass

    
Model.functions_info = {
        "trend": {
            "function": Model.trend,
            "parameters": {
                "type": {
                    "title": "Тип тренда",
                    "type": "dropdown",
                    "options": [
                        {
                            "key": "linear_rising",
                            "text": "linear_rising",
                        },
                        {
                            "key": "linear_falling",
                            "text": "linear_falling",
                        },
                        {
                            "key": "nonlinear_rising",
                            "text": "nonlinear_rising",
                        },
                        {
                            "key": "nonlinear_falling",
                            "text": "nonlinear_falling",
                        }
                    ],
                    "default_value": "linear_rising",
                },
                "a": {
                    "title": "Параметр a",
                    "type": "slider",
                    "min": 0.1,
                    "max": 10.0,
                    "step": 0.1,
                    "default_value": 1.0,
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
                    "max": 10000,
                    "step": 100,
                    "default_value": 100,
                },
            }
        },
        'data_download': {
            'function': Model.data_download,
            'parameters': {
                'input_data': {
                    "title": "Выбор файла данных",
                    "type": "file_picker",
                    "default_value": None,
                }
            }
        }
    }
