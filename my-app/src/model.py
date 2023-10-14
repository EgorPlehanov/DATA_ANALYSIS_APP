import numpy as np
import sympy as sp
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
        '''
        Округляет и удаляет значения больше заданного порога в датафрейме
        '''
        def round_and_clip(value):
            if isinstance(value, (int, float)):
                return round(value, decimal_places) if value <= max_value else max_value
            else:
                return value
            
        return df.map(round_and_clip)


    def get_result_dict(
            data: DataFrame = None,
            type: str = None,
            initial_data: dict = None,
            error_message: str = None,
            view_chart: bool = None,
            view_table_horizontal: bool = None,
            view_table_vertical: bool = None,
            main_view: str = None,
            in_list: bool = False
        ) -> dict:
        result_dict = {}

        if data is not None:
            result_dict['data'] = Model.round_and_clip_dataframe(data)
            
        if initial_data:
            result_dict['extra_data'] = initial_data

        if type:
            initial_data_type = f" ({initial_data.get('type', '')})" if initial_data else ''
            result_dict['type'] = f'{type}{initial_data_type}'

        if error_message:
            result_dict['error_message'] = error_message

        view_list = []
        if view_chart:
            view_list.append('chart')
        if view_table_horizontal:
            view_list.append('table_data')
        if view_table_vertical:
            view_list.append('table_statistics')
        result_dict['view'] = view_list

        if main_view and main_view in view_list:
            result_dict['main_view'] = main_view
        elif len(view_list) > 0:
            result_dict['main_view'] = view_list[0]

        if in_list:
            return [result_dict]
        return result_dict

    
    # ========== DATA FUNCTIONS ==========

    def trend_function_linear_rising(t, a, b):
        return a * t + b

    def trend_function_linear_falling(t, a, b):
        return -a * t + b

    def trend_function_nonlinear_rising(t, a, b):
        return b * np.exp(a * t)

    def trend_function_nonlinear_falling(t, a, b):
        return b * np.exp(-a * t)


    def trend(type, a, b, step, N, show_table_data=False) -> list:
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
        return Model.get_result_dict(
            data=df,
            type=type,
            view_chart=True,
            view_table_horizontal=show_table_data,
            in_list=True
        )
    

    def multi_trend(type_list, a, b, step, N, show_table_data=False) -> list:
        if len(type_list) == 0:
            return Model.get_result_dict(error_message="Нет данных для построения графика", in_list=True)
        
        df_list = []
        for type in type_list:
            df_list.append(*Model.trend(type, a, b, step, N, show_table_data))
        return df_list
    

    def combinate_trend(type_list, a, b, step, N, show_table_data=False) -> list:
        num_parts = len(type_list)
        if num_parts == 0:
            return Model.get_result_dict(error_message="Нет данных для построения графика", in_list=True)

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
        return Model.get_result_dict(
            data=combined_df,
            type=' -> '.join(type_list),
            view_chart=True,
            view_table_horizontal=show_table_data,
            in_list=True,
        )
    

    def custom_function(expression, N, step, show_table_data=False) -> list:

        if not expression:
            return Model.get_result_dict(error_message="Не задана расчетная функция", in_list=True)
        
        x = sp.symbols('x')

        math_expression = sp.sympify(expression)
        function = sp.lambdify(x, math_expression, "numpy")

        x_values = np.arange(0, N * step, step)
        y_values = [function(x) for x in x_values]

        data = pd.DataFrame({'x': x_values, 'y': y_values})

        return Model.get_result_dict(
            data=data,
            type='custom_function',
            view_chart=True,
            view_table_horizontal=show_table_data,
            in_list=True,
        )


    def data_download(input_data, show_table_data=False) -> list:
        print(input_data)
        return Model.get_result_dict(in_list=True)
    
    # ========== EDIT FUNCTIONS ==========

    def noise(data, N, R, delta, show_table_data=False) -> list:
        N = int(N)
        # Генерация случайного шума в заданном диапазоне [-R, R]
        noise_data = np.random.uniform(-R, R, N)
        # Пересчет данных в заданный диапазон R
        min_val = np.min(noise_data)
        max_val = np.max(noise_data)
        normalized_noise = ((noise_data - min_val) / (max_val - min_val) - 0.5) * 2 * R

        t = np.arange(0, N * delta, delta)
        noised_data = pd.DataFrame({'x': t, 'y': normalized_noise})
        return Model.get_result_dict(
            data=noised_data,
            type='noise',
            view_chart=True,
            view_table_horizontal=show_table_data,
            in_list=True,
        )


    def my_noise(data, N, R, delta, show_table_data=False) -> list:
        N = int(N)

        current_time = int(time.time())
        random.seed(current_time)

        custom_noise_data = [random.uniform(-R, R) for _ in range(N)]
    
        t = np.arange(0, N * delta, delta)
        noised_data = pd.DataFrame({'x': t, 'y': custom_noise_data})
        return Model.get_result_dict(
            data=noised_data,
            type='my_noise',
            view_chart=True,
            view_table_horizontal=show_table_data,
            in_list=True,
        )
    

    def shift(data, C, N1, N2, show_table_data=False) -> dict:
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
        function_data = data.get('value').function.result
        for df_dict in function_data:
            df = df_dict.get('data', None)
            if df is None:
                continue
            N = len(df)

            error_message = ''
            if N1 < 0 or N2 > N:
                error_message = f'Некорректное значение N1 или N2: 0 <= N1 <= N2 <= {N}, значения N1 = {N1}, N2 = {N2}'

            if N1 > N and N2 > N:
                error_message = f'Некорректные значения N1 и N2: N1 и N2 должны быть <= {N}, значения N1 = {N1}, N2 = {N2}'
                result_list.append(Model.get_result_dict(error_message=error_message))
                continue

            shifted_df = df.get('y').copy()
            shifted_df[N1:N2+1] += C
            shifted_df = pd.DataFrame({'x': df.get('x').copy(), 'y': shifted_df})
            result_list.append(Model.get_result_dict(
                data=shifted_df,
                type='shift',
                initial_data = df_dict,
                error_message=error_message,
                view_chart=True,
                view_table_horizontal=show_table_data,
            ))
        return result_list
        

    def spikes(N, M, R, Rs, show_table_data=False) -> list:
        """
        Генерирует M случайных выбросов (спайков) на интервале [0, N] со случайными амплитудами.

        :param N: Длина данных
        :param M: Количество выбросов
        :param R: Опорное значение
        :param Rs: Диапазон варьирования амплитуды
        """
        N, M = int(N), int(M)
        if N < M:
            return Model.get_result_dict(error_message=f'Некорректное количество выбросов: M должно быть <= N. M = {M}, N = {N}', in_list=True)

        error_message = ""
        if M < 0.005 * N or M > 0.01 * N:
            error_message = f'Некорректное количество выбросов: M должно быть в пределах [{0.005*N}, {0.01*N}]'
        
        data = np.zeros(N)
        spike_indices = np.random.choice(N, M, replace=False)
        spike_amplitudes = R + np.random.uniform(-Rs, Rs, M)
        spike_signs = np.random.choice([-1, 1], M)  # Выбираем случайный знак для выбросов
        data[spike_indices] = spike_signs * spike_amplitudes
        spikes_df = pd.DataFrame({'x': np.arange(N), 'y': data})
        return Model.get_result_dict(
            data=spikes_df,
            type='spikes',
            error_message=error_message,
            view_chart=True,
            view_table_horizontal=show_table_data,
            in_list=True,
        )
        

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
        function_data = data.get('value').function.result
        for df_dict in function_data:
            df = df_dict.get('data', None)
            if df is None:
                continue
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
            result_list.append(Model.get_result_dict(
                data=stats_df,
                type='statistics',
                initial_data = df_dict,
                view_table_vertical=True,
            ))
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
        function_data = data.get('value').function.result
        for df_dict in function_data:
            df = df_dict.get('data', None)
            if df is None:
                continue
            y = df.get('y').copy()
            N = len(y)

            error_message = ''
            if M > N:
                error_message = f'Некорректное кол-во интервалов: M должен быть <= N. M = {M}, N = {N}'
                result_list.append(Model.get_result_dict(error_message=error_message))
                continue
            
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
            result_list.append(Model.get_result_dict(
                data=stats_df,
                type='stationarity',
                initial_data = df_dict,
                view_table_vertical=True,
            ))
        return result_list

    
    functions_info = {
    # ========== DATA FUNCTIONS ==========
        "trend": {
            "function": trend,
            'type': 'data',
            'name': 'trend',
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
                    "max": 5.0,
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
                    "max": 10,
                    "step": 1,
                    "default_value": 1,
                },
                "N": {
                    "type": "slider",
                    "title": "Длина данных (N)",
                    "min": 100,
                    "max": 5000,
                    "step": 100,
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
            'function': multi_trend,
            'type': 'data',
            'name': 'multi_trend',
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
                    "min": 100,
                    "max": 5000,
                    "step": 100,
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
            'function': combinate_trend,
            'type': 'data',
            'name': 'combinate_trend',
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
                    "min": 100,
                    "max": 5000,
                    "step": 100,
                    "default_value": 600,
                },
                'show_table_data': {
                    "type": "switch",
                    "title": "Показывать таблицу данных?",
                    'default_value': False
                },
            }
        },

        'custom_function': {
            'function': custom_function,
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
                    "min": 100,
                    "max": 5000,
                    "step": 100,
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
            'function': data_download,
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
                        'allowed_extensions': ['csv'],
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

    # ========== EDIT FUNCTIONS ==========

        'noise': {
            'function': noise,
            'type': 'edit',
            'name': 'Случайный шум',
            'parameters': {
                'data': {
                    "type": "dropdown",
                    "title": "Выбор данных",
                    "options": [
                        {
                            "key": None,
                            "text": "Не выбрана",
                        },
                    ],
                    "default_value": None,
                },
                'N': {
                    "type": "slider",
                    "title": "Длина данных (N)",
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
            'function': my_noise,
            'type': 'edit',
            'name': 'Мой случайный шум',
            'parameters': {
                'data': {
                    "type": "dropdown",
                    "title": "Выбор данных",
                    "options": [
                        {
                            "key": None,
                            "text": "Не выбрана",
                        },
                    ],
                    "default_value": None,
                },
                'N': {
                    "type": "slider",
                    "title": "Длина данных (N)",
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
            'function': shift,
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
                    "min": 0,
                    "max": 5000,
                    "step": 1,
                    "default_value": 100,
                },
                'N2': {
                    "type": "slider",
                    "title": "Cмещение до (N2)",
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
            'function': spikes,
            'type': 'edit',
            'name': 'Одиночные выбросы',
            'parameters': {
                'N': {
                    "type": "slider",
                    "title": "Длина данных (N)",
                    "min": 10,
                    "max": 10000,
                    "step": 10,
                    "default_value": 1000,
                },
                'M': {
                    "type": "slider",
                    "title": "Количество выбросов (M)",
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

        # ========== ANALITIC FUNCTIONS ==========

        'statistics': {
            'function': statistics,
            'type': 'analitic',
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
            'function': stationarity,
            'type': 'analitic',
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
                    "min": 2,
                    "max": 1000,
                    "step": 1,
                    "default_value": 100,
                }
            }
        }
    }
