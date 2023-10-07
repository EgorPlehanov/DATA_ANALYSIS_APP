import numpy as np
import pandas as pd
from pandas import (
    DataFrame
)
import scipy.stats as stats
from statsmodels.tsa.stattools import adfuller
import time
import random



class Model:
    @staticmethod
    def get_info(name, return_type='all') -> dict:
        if name in Model.functions_info:
            info = Model.functions_info[name]
            if return_type == 'function':
                return info.get('function')
            elif return_type == 'parameters':
                return info.get('parameters')
            elif return_type == 'type':
                return info.get('type')
            elif return_type == 'all':
                return info
        return None
    
    @staticmethod
    def get_functions_by_type(type):
        data_functions = []
        for key, info in Model.functions_info.items():
            if info.get('type') == type:
                data_functions.append({'key': key, 'name': info.get('name', key)})
        return data_functions
    
    def round_and_clip_dataframe(df: DataFrame, max_value: int = 1000000000, decimal_places: int = 4) -> DataFrame:
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
            'view': ['chart'],
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
            'type': ' -> '.join(type_list),
            'view': ['chart'],
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
            'view': ['chart']#, 'table_data'],
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
            'view': ['chart']#, 'table_data'],
        }]
    

    def shift(data, C, N1, N2) -> dict:
        """
        Сдвигает данные data в интервале [N1, N2] на константу C.

        :param data: Входные данные (сгенерированные в блоке данных)
        :param C: Значение сдвига
        :param N1: Начальный индекс интервала
        :param N2: Конечный индекс интервала
        :return: Сдвинутые данные в виде структуры {'data': DataFrame, 'type': 'shift'}
        """
        if data.get('function_name') == 'Не выбраны' or not data.get('value'):
            return []

        N1, N2 = int(N1), int(N2)
        if N1 > N2:
            N1, N2 = N2, N1

        result_list = []

        for df_dict in data.get('value'):
            df = df_dict.get('data')
            N = len(df)

            error_message = ''
            if N1 < 0 or N2 > N:
                error_message = f'Некорректное значение N1 или N2: 0 <= N1 <= N2 <= {N}, значения N1 = {N1}, N2 = {N2}'

            if N1 > N and N2 > N:
                error_message = f'Некорректные значения N1 и N2: N1 и N2 должны быть <= {N}, значения N1 = {N1}, N2 = {N2}'
                print(error_message)
                return [{
                    'type': f'shift ({df_dict.get("type")})',
                    'error_message': error_message
                }] 

            shifted_df = df.get('y').copy()
            shifted_df[N1:N2+1] += C
            shifted_df = pd.DataFrame({'x': df.get('x').copy(), 'y': shifted_df})
            shifted_df = Model.round_and_clip_dataframe(shifted_df)

            result_list.append({
                'data': shifted_df,
                'type': f'shift ({df_dict.get("type")})',
                'view': ['chart'], #'table_data'],
                'extra_data': df_dict,
                'error_message': error_message,
            })
        return result_list


    def spikes(N, M, R, Rs) -> list:
        """
        Генерирует M случайных выбросов (спайков) на интервале [0, N] со случайными амплитудами.

        :param N: Длина данных
        :param M: Количество выбросов
        :param R: Опорное значение
        :param Rs: Диапазон варьирования амплитуды
        :return: Данные с выбросами в виде структуры {'data': DataFrame, 'type': 'spikes'}
        """
        N, M = int(N), int(M)
        error_message = ""
        if M < 0.005 * N or M > 0.01 * N:
            error_message = f' - некорректное количество выбросов: M должно быть в пределах [{0.005*N}, {0.01*N}]'
        
        data = np.zeros(N)
        spike_indices = np.random.choice(N, M, replace=False)
        spike_amplitudes = R + np.random.uniform(-Rs, Rs, M)
        spike_signs = np.random.choice([-1, 1], M)  # Выбираем случайный знак для выбросов
        data[spike_indices] = spike_signs * spike_amplitudes
        spikes_df = pd.DataFrame({'x': np.arange(N), 'y': data})
        spikes_df = Model.round_and_clip_dataframe(spikes_df)
        return [{
            'data': spikes_df,
            'type': 'spikes' + error_message,
            'view': ['chart', 'table_data'],
        }]

    # ========== ANALITIC FUNCTIONS ==========

    def statistics(data) -> list:
        """
        Рассчитывает статистические характеристики данных.

        :param data: Данные для анализа (представленные в виде DataFrame)
        :return: DataFrame с рассчитанными статистическими характеристиками
        """
        if data.get('function_name') == 'Не выбраны' or not data.get('value'):
            return []

        result_list = []
        for df_dict in data.get('value'):
            df = df_dict.get('data')
            y = df.get('y').copy()

            # N = len(y)
            min_value = np.min(y)
            max_value = np.max(y)
            mean = np.mean(y)
            variance = np.var(y, ddof=1)  # Используем ddof=1 для несмещенной оценки дисперсии
            std_dev = np.sqrt(variance)
            
            # Рассчет асимметрии и коэффициента асимметрии
            mu3 = np.mean((y - mean) ** 3)
            delta3 = np.power(variance, 1.5)
            skewness = mu3 / delta3
            skewness_coeff = skewness / np.power(variance, 1.5)
            
            # Рассчет эксцесса и коэффициента эксцесса
            mu4 = np.mean((y - mean) ** 4)
            kurtosis = mu4 / np.power(variance, 2)
            kurtosis_coeff = kurtosis / (variance ** 2) - 3

            # Рассчет Среднего квадрата и Среднеквадратической ошибки
            squared_mean = np.mean(y ** 2)
            rmse = np.sqrt(variance)

            stats_df = pd.DataFrame({
                'Параметр': ['Тип', 'Минимум', 'Максимум', 'Среднее', 'Дисперсия', 'Стандартное отклонение', 'Асимметрия (A)',
                            'Коэффициент асимметрии', 'Эксцесс (Э)', 'Куртозис', 'Средний квадрат (СК)', 'Среднеквадратическая ошибка'],
                'Значение': [df_dict.get('type')] + list(map(lambda x: round(x, 5),
                    [min_value, max_value, mean, variance, std_dev, skewness,
                    skewness_coeff, kurtosis, kurtosis_coeff, squared_mean, rmse]))
            })
           
            result_list.append({
                'data': stats_df,
                'type': f'statistics ({df_dict.get("type")})',
                'view': ['table_statistics'],
                'extra_data': df_dict
            })
        return result_list
    

    def stationarity(data, M) -> list:
        """
        Оценивает стационарность данных.

        :param data: Данные для анализа (представленные в виде DataFrame)
        :param M: Количество интервалов
        :return: True, если данные стационарны, иначе False
        """
        if data.get('function_name') == 'Не выбраны' or not data.get('value'):
            return []
        
        M = int(M)

        result_list = []
        for df_dict in data.get('value'):
            df = df_dict.get('data')
            y = df.get('y').copy()
            N = len(y)

            error_message = ''
            if M > N:
                error_message = f' - некорректное кол-во интервалов: M <= {N} (N)'
                result_list.append({})
            
            intervals = np.array_split(y, M)
            means = np.array([np.mean(interval) for interval in intervals])
            std_deviations = np.array([np.std(interval) for interval in intervals])

            is_stationarity = True
            for i in range(M):
                if not is_stationarity:
                    break

                for j in range(i + 1, M):
                    delta_mean = abs(means[i] - means[j])
                    delta_std_dev = abs(std_deviations[i] - std_deviations[j])

                    if delta_mean >= 0.05 * np.ptp(y) or delta_std_dev >= 0.05 * np.ptp(y):
                        is_stationarity = False
                        break
            res = adfuller(y)
            # print(res)
            is_stationarity_2 = res[1] < 0.05
            stats_df = pd.DataFrame({
                'Параметр': ['Стационарность', 'Стационарность'],
                'Значение': [str(is_stationarity), str(is_stationarity_2)]
            })
            # 'Процесс ' + ('' if is_stationarity else 'НЕ ') + 'стационарный'
            result_list.append({
                'data': stats_df,
                'type': 'statistics' + error_message,
                'view': ['table_statistics'],
                'extra_data': df_dict
            })
        return result_list

    
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
                    "title": "Выбор данных",
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
                    "title": "Выбор данных",
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

        'shift': {
            'function': shift,
            'type': 'edit',
            'name': 'Сдвиг',
            'parameters': {
                'data': {
                    "title": "Выбор набора данных",
                    "type": "dropdown_function_data",
                    "options": {'Не выбраны': {'function_name': 'Не выбраны', 'value': []}},
                    "default_value": {'function_name': 'Не выбраны', 'value': []},
                },
                'C': {
                    "title": "Cмещение данных C",
                    "type": "slider",
                    "min": -1000,
                    "max": 1000,
                    "step": 0.1,
                    "default_value": 200,
                },
                'N1': {
                    "title": "Cмещение от N1",
                    "type": "slider",
                    "min": 0,
                    "max": 5000,
                    "step": 1,
                    "default_value": 100,
                },
                'N2': {
                    "title": "Cмещение до N2",
                    "type": "slider",
                    "min": 0,
                    "max": 5000,
                    "step": 1,
                    "default_value": 500,
                },
            }
        },

        'spikes': {
            'function': spikes,
            'type': 'edit',
            'name': 'Одиночные выбросы',
            'parameters': {
                'N': {
                    "title": "Длина данных N",
                    "type": "slider",
                    "min": 10,
                    "max": 10000,
                    "step": 10,
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
                },
            }

        },

        # ========== ANALITIC FUNCTIONS ==========

        'statistics': {
            'function': statistics,
            'type': 'analitic',
            'name': 'Статистические данные',
            'parameters': {
                'data': {
                    "title": "Выбор набора данных",
                    "type": "dropdown_function_data",
                    "options": {'Не выбраны': {'function_name': 'Не выбраны', 'value': []}},
                    "default_value": {'function_name': 'Не выбраны', 'value': []},
                },
            }
        },

        'stationarity': {
            'function': stationarity,
            'type': 'analitic',
            'name': 'Стационарность',
            'parameters': {
                'data': {
                    "title": "Выбор набора данных",
                    "type": "dropdown_function_data",
                    "options": {'Не выбраны': {'function_name': 'Не выбраны', 'value': []}},
                    "default_value": {'function_name': 'Не выбраны', 'value': []},
                },
                'M': {
                    "title": "Количество интервалов M",
                    "type": "slider",
                    "min": 2,
                    "max": 5000,
                    "step": 1,
                    "default_value": 100,
                }
            }
        }
    }
