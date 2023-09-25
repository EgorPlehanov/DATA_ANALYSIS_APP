import numpy as np


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

        return t, data

    
Model.functions_info = {
        "trend": {
            "function": Model.trend,
            "parameters": {
                "type": {
                    "title": "Тип тренда",
                    "type": "dropdown",
                    "options": ["linear_rising", "linear_falling", "nonlinear_rising", "nonlinear_falling"],
                    "default": "linear_rising",
                    "value": "linear_rising",
                },
                "a": {
                    "title": "Параметр a",
                    "type": "slider",
                    "min": 0.1,
                    "max": 10.0,
                    "divisions": 0.1,
                    "default": 1.0,
                    "value": 1.0
                },
                "b": {
                    "title": "Параметр b",
                    "type": "slider",
                    "min": 0.1,
                    "max": 10.0,
                    "divisions": 0.1,
                    "default": 1.0,
                    "value": 1.0
                },
                "step": {
                    "title": "Интервал Δ",
                    "type": "slider",
                    "min": 1,
                    "max": 10,
                    "divisions": 1,
                    "default": 1,
                    "value": 1
                },
                "N": {
                    "title": "Длина данных N",
                    "type": "slider",
                    "min": 100,
                    "max": 10000,
                    "divisions": 100,
                    "default": 100,
                    "value": 100
                },
            }
        },
    }
