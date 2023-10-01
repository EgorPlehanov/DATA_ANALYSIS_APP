import numpy as np
import pandas as pd
import time
import random



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
    
    def round_and_clip_dataframe(df, max_value: int = 1000000000, decimal_places: int = 4) -> pd.DataFrame:
    # Округление значений в датафрейме
        df = df.round(decimal_places)

        # Удаление значений больше заданного порога
        for col in df.columns:
            df = df[df[col] <= max_value]

        return df

    
    # ========== DATA FUNCTIONS ==========

    def trend_function_linear_rising(t, a, b):
        return a * t + b

    def trend_function_linear_falling(t, a, b):
        return -a * t + b

    def trend_function_nonlinear_rising(t, a, b):
        return b * np.exp(a * t)

    def trend_function_nonlinear_falling(t, a, b):
        return b * np.exp(-a * t)


    def trend(type, a, b, step, N) -> list:
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
        df = Model.round_and_clip_dataframe(df)
        return [{
            'data': df,
            'type': type,
        }]
    

    def multi_trend(type_list, a, b, step, N) -> list:
        if len(type_list) == 0:
            return []
        
        df_list = []
        for type in type_list:
            df_list.append(*Model.trend(type, a, b, step, N))
        return df_list
    

    def combinate_trend(type_list, a, b, step, N) -> list:
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
        combined_df = Model.round_and_clip_dataframe(combined_df)
        return [{
            'data': combined_df,
            'type': ' -> '.join(type_list)
        }]


    def data_download(input_data):
        pass
    
    # ========== EDIT FUNCTIONS ==========

    def noise(data, N, R, delta) -> list:
        N = int(N)
        # Генерация случайного шума в заданном диапазоне [-R, R]
        noise_data = np.random.uniform(-R, R, N)
        # Пересчет данных в заданный диапазон R
        min_val = np.min(noise_data)
        max_val = np.max(noise_data)
        normalized_noise = ((noise_data - min_val) / (max_val - min_val) - 0.5) * 2 * R

        t = np.arange(0, N * delta, delta)
        noised_data = pd.DataFrame({'x': t, 'y': normalized_noise})
        noised_data = Model.round_and_clip_dataframe(noised_data)
        return [{
            'data': noised_data,
            'type': 'noise',
        }]

    def myNoise(data, N, R, delta) -> list:
        N = int(N)

        current_time = int(time.time())
        random.seed(current_time)

        custom_noise_data = [random.uniform(-R, R) for _ in range(N)]
    
        t = np.arange(0, N * delta, delta)
        noised_data = pd.DataFrame({'x': t, 'y': custom_noise_data})
        noised_data = Model.round_and_clip_dataframe(noised_data)
        return [{
            'data': noised_data,
            'type': 'myNoise',
        }]
    
    def shift(inData, N, C, N1, N2) -> dict:
        """
        Сдвигает данные inData в интервале [N1, N2] на константу C.

        :param inData: Входные данные (numpy массив)
        :param N: Длина данных
        :param C: Значение сдвига
        :param N1: Начальный индекс интервала
        :param N2: Конечный индекс интервала
        :return: Сдвинутые данные в виде структуры {'data': DataFrame, 'type': 'shift'}
        """
        if N1 < 0 or N2 >= N:
            print("Некорректные значения N1 и N2")
            return []

        shifted_data = inData.copy()
        shifted_data[N1:N2+1] += C
        shifted_df = pd.DataFrame({'x': np.arange(N), 'y': shifted_data})
        shifted_df = Model.round_and_clip_dataframe(shifted_df)
        return [{
            'data': shifted_df,
            'type': 'shift'
        }]

    def spikes(N, M, R, Rs) -> list:
        """
        Генерирует M случайных выбросов (спайков) на интервале [0, N] со случайными амплитудами.

        :param N: Длина данных
        :param M: Количество выбросов
        :param R: Опорное значение
        :param Rs: Диапазон варьирования амплитуды
        :return: Данные с выбросами в виде структуры {'data': DataFrame, 'type': 'spikes'}
        """
        N = int(N)
        M = int(M)
        error_message = ""
        if M < 0.005 * N or M > 0.01 * N:
            error_message = f' - некорректное количество выбросов: M должно быть в пределах [{0.005*N}, {0.01*N}]'
            # return []
        
        data = np.zeros(N)
        spike_indices = np.random.choice(N, M, replace=False)
        spike_amplitudes = R + np.random.uniform(-Rs, Rs, M)
        spike_signs = np.random.choice([-1, 1], M)  # Выбираем случайный знак для выбросов
        data[spike_indices] = spike_signs * spike_amplitudes
        spikes_df = pd.DataFrame({'x': np.arange(N), 'y': data})
        spikes_df = Model.round_and_clip_dataframe(spikes_df)
        return [{
            'data': spikes_df,
            'type': 'spikes' + error_message
        }]

    # ========== ANALYSIS FUNCTIONS ==========

    
    functions_info = {
    # ========== DATA FUNCTIONS ==========
        "trend": {
            "function": trend,
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
                    "default_value": 600,
                },
            }
        },

        'multi_trend': {
            'function': multi_trend,
            'type': 'data',
            'name': 'multi_trend',
            'parameters': {
                "type_list": {
                    "title": "Тип тренда",
                    "type": "checkbox",
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
                    "default_value": 600,
                },
            }
        },

        'combinate_trend': {
            'function': combinate_trend,
            'type': 'data',
            'name': 'combinate_trend',
            'parameters': {
                "type_list": {
                    "title": "Тип тренда",
                    "type": "checkbox",
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
                    "default_value": 600,
                },
            }
        },

        'data_download': {
            'function': data_download,
            'type': 'data',
            'name': 'Загрузить свой набор данных',
            'parameters': {
                'input_data': {
                    "title": "Выбор файла данных",
                    "type": "file_picker",
                    "default_value": None,
                }
            }
        },

    # ========== EDIT FUNCTIONS ==========

        'noise': {
            'function': noise,
            'type': 'edit',
            'name': 'Случайный шум',
            'parameters': {
                'data': {
                    "title": "Выбор функции данных",
                    "type": "dropdown",
                    "options": [
                        {
                            "key": None,
                            "text": "Не выбрана",
                        },
                    ],
                    "default_value": None,
                },
                'N': {
                    "title": "Длина данных N",
                    "type": "slider",
                    "min": 10,
                    "max": 5000,
                    "step": 10,
                    "default_value": 600,
                },
                'R': {
                    "title": "Параметр диапозона R",
                    "type": "slider",
                    "min": 0.1,
                    "max": 1000.0,
                    "step": 0.1,
                    "default_value": 0.1,
                },
                'delta': {
                    "title": "Интервал Δ",
                    "type": "slider",
                    "min": 1,
                    "max": 15,
                    "step": 1,
                    "default_value": 1,
                },
            }
        },

        'myNoise': {
            'function': myNoise,
            'type': 'edit',
            'name': 'Мой случайный шум',
            'parameters': {
                'data': {
                    "title": "Выбор функции данных",
                    "type": "dropdown",
                    "options": [
                        {
                            "key": None,
                            "text": "Не выбрана",
                        },
                    ],
                    "default_value": None,
                },
                'N': {
                    "title": "Длина данных N",
                    "type": "slider",
                    "min": 10,
                    "max": 5000,
                    "step": 10,
                    "default_value": 600,
                },
                'R': {
                    "title": "Параметр диапозона R",
                    "type": "slider",
                    "min": 0.1,
                    "max": 1000.0,
                    "step": 0.1,
                    "default_value": 0.1,
                },
                'delta': {
                    "title": "Интервал Δ",
                    "type": "slider",
                    "min": 1,
                    "max": 15,
                    "step": 1,
                    "default_value": 1,
                },
            }
        },

        # 'shift': {
        #     'function': shift,
        #     'type': 'edit',
        #     'name': 'Сдвиг',
        #     'parameters': {
        #         'inData': {
                    
        #         },
        #         'N': {
                    
        #         },
        #         'C': {
                    
        #         },
        #         'N1': {
                    
        #         },
        #         'N2': {
                    
        #         },
        #     }
        # },

        'spikes': {
            'function': spikes,
            'type': 'edit',
            'name': 'Одиночные выбросы',
            'parameters': {
                'N': {
                    "title": "Длина данных N",
                    "type": "slider",
                    "min": 100,
                    "max": 10000,
                    "step": 100,
                    "default_value": 1000,
                },
                'M': {
                    "title": "Количество выбросов M",
                    "type": "slider",
                    "min": 1,
                    "max": 100,
                    "step": 1,
                    "default_value": 10,
                },
                'R': {
                    "title": "Опорное значение R",
                    "type": "slider",
                    "min": 1,
                    "max": 10000,
                    "step": 1,
                    "default_value": 1000,
                },
                'Rs': {
                    "title": "Длина данных Rs",
                    "type": "slider",
                    "min": 1,
                    "max": 1000,
                    "step": 1,
                    "default_value": 500,
                }
            }

        }

        # ========== ANALYSIS FUNCTIONS ==========


    }
