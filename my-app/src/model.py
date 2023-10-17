import numpy as np
import sympy as sp
import pandas as pd
import csv
from pandas import (
    DataFrame
)
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
            try:
                numeric_value = value
                if isinstance(numeric_value, (str)):
                    numeric_value = float(value.replace(',', '.'))
                return round(numeric_value, decimal_places) if numeric_value <= max_value else max_value
            except ValueError:
                return value
            
        return df.map(round_and_clip)


    def get_result_dict(
            data: DataFrame = None,
            type: str = None,
            initial_data: dict = None,
            extra_data: dict = None,
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
            result_dict['initial_data'] = initial_data

        if extra_data:
            result_dict['extra_data'] = extra_data

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
        if not (len(input_data) > 0 and isinstance(input_data[0], dict)):
            return Model.get_result_dict(in_list=True)

        result_list = []
        for file in input_data:
            file_name = file.get('name', '')
            file_path = file.get('path', '')

            # Определение формата файла на основе расширения
            file_extension = file_path.split('.')[-1].lower()
            
            try:
                if file_extension == 'csv':
                    # Определение разделителя
                    with open(file_path, 'r', newline='') as csvfile:
                        sample_data = csvfile.read(1024)
                        sniffer = csv.Sniffer()
                        delimiter = sniffer.sniff(sample_data).delimiter
                    # Чтение CSV файла с указанием определенного разделителя
                    df = pd.read_csv(file_path, delimiter=delimiter)

                elif file_extension in ('xls', 'xlsx', 'xlsm', 'xlsb', 'odf', 'ods', 'odt'):
                    df = pd.read_excel(file_path)

                elif file_extension == 'json':
                    df = pd.read_json(file_path)

                elif file_extension == 'txt':
                    df = pd.read_table(file_path, sep=';')

                else:
                    result_list.append(Model.get_result_dict(
                        error_message=f"Формат {file_extension} не поддерживается ",
                        type=f'data_download({file_name})'
                    ))
                    continue
            except Exception as e:
                result_list.append(Model.get_result_dict(
                    error_message=f"При чтении файла '{file_name}' произошла ошибка: {str(e)}",
                    type=f'data_download({file_name})'
                ))
                continue

            if df.empty:
                result_list.append(Model.get_result_dict(
                    error_message=f"Файл '{file_name}' пуст",
                    type=f'data_download({file_name})'
                ))
                continue

            result_list.append(Model.get_result_dict(
                data=df,
                type=f'data_download({file_name})',
                view_chart=True,
                view_table_horizontal=show_table_data,
            ))
        return result_list
    

    def harm(N: int, A0: float, f0: float, delta_t: float, show_table_data=False) -> list:
        error_message = None
        if delta_t > 1 / (2 * f0):
            error_message = f"Некоректное значение временного интервала, delta_t <= 1/(2*f0): delta_t = {delta_t}, 1/(2*f0) = {round(1 / (2 * f0), 5)}"

        k = np.arange(0, N)
        y_values = A0 * np.sin(2 * np.pi * f0 * delta_t * k)
        harm_data = pd.DataFrame({'x': k, 'y': y_values})

        return Model.get_result_dict(
            data=harm_data,
            type='harm',
            error_message=error_message,
            view_chart=True,
            view_table_horizontal=show_table_data,
            in_list=True,
        )
    

    def poly_harm(N: int, A_f_data: list, delta_t: float, show_table_data=False) -> list:

        max_fi = max([params['f'] for params in A_f_data.values()])
        error_message = None
        if delta_t > 1 / (2 * max_fi):
            error_message = "Некоректное значение временного интервала.\nОно должно удовлетворять условию: " \
                + f"delta_t <= 1 / (2 * max(fi)): delta_t = {delta_t}, 1 / (2 * max(fi)) = {round(1 / (2 * max_fi), 5)}"


        k = np.arange(0, N)
        y_values = np.zeros(N)
        for params in A_f_data.values():
            y_values += params['A'] * np.sin(2 * np.pi * params['f'] * delta_t * k)

        poly_harm_data = pd.DataFrame({'x': k, 'y': y_values})

        return Model.get_result_dict(
            data=poly_harm_data,
            type='poly_harm',
            error_message=error_message,
            view_chart=True,
            view_table_horizontal=show_table_data,
            in_list=True,
        )
    
    # ========== EDIT FUNCTIONS ==========

    def generate_noise(N: int, R: float, delta: float, x_values: np.ndarray = None) -> DataFrame:
        # Генерация случайного шума в заданном диапазоне [-R, R]
        noise_data = np.random.uniform(-R, R, N)
        # Пересчет данных в заданный диапазон R
        min_val, max_val = np.min(noise_data), np.max(noise_data)
        normalized_noise = ((noise_data - min_val) / (max_val - min_val) - 0.5) * 2 * R
        if x_values is None:
            x_values = np.arange(0, N * delta, delta)
        return DataFrame({'x': x_values, 'y': normalized_noise})


    def noise(data, N, R, delta, show_table_data=False) -> list:
        N = int(N)
        if data.get('function_name') == 'Не выбраны' or not data.get('value'):
            return Model.get_result_dict(
                data=Model.generate_noise(N, R, delta),
                type='noise',
                view_chart=True,
                view_table_horizontal=show_table_data,
                in_list=True,
            )
        
        result_list = []
        function_data = data.get('value').function.result
        for df_dict in function_data:
            df = df_dict.get('data', None)
            if df is None:
                continue

            N = len(df)
            
            noised_df = Model.generate_noise(N, R, delta, df['x'].values)
            noised_data = Model.get_result_dict(
                data=noised_df,
                type='noise',
                view_chart=True,
                view_table_horizontal=show_table_data,
            )

            data_noised_df = pd.concat([df, noised_df]).groupby('x', as_index=False).sum()
            result_list.append(Model.get_result_dict(
                data=data_noised_df,
                type='noise',
                initial_data=df_dict,
                extra_data=noised_data,
                view_chart=True,
                view_table_horizontal=show_table_data,
            ))
        return result_list


    def generate_my_noise(N: int, R: float, delta: float, x_values: np.ndarray = None) -> DataFrame:
        current_time = int(time.time())
        random.seed(current_time)

        custom_noise_data = [random.uniform(-R, R) for _ in range(N)]

        if x_values is None:
            x_values = np.arange(0, N * delta, delta)
        return pd.DataFrame({'x': x_values, 'y': custom_noise_data})


    def my_noise(data, N, R, delta, show_table_data=False) -> list:
        N = int(N)

        if data.get('function_name') == 'Не выбраны' or not data.get('value'):
            return Model.get_result_dict(
                data=Model.generate_my_noise(N, R, delta),
                type='my_noise',
                view_chart=True,
                view_table_horizontal=show_table_data,
                in_list=True,
            )

        result_list = []
        function_data = data.get('value').function.result
        for df_dict in function_data:
            df = df_dict.get('data', None)
            if df is None:
                continue

            N = len(df)
            
            my_noised_df = Model.generate_my_noise(N, R, delta, df['x'].values)
            my_noised_data = Model.get_result_dict(
                data=my_noised_df,
                type='noise',
                view_chart=True,
                view_table_horizontal=show_table_data,
            )

            data_noised_df = pd.concat([df, my_noised_df]).groupby('x', as_index=False).sum()
            result_list.append(Model.get_result_dict(
                data=data_noised_df,
                type='noise',
                initial_data=df_dict,
                extra_data=my_noised_data,
                view_chart=True,
                view_table_horizontal=show_table_data,
            ))
        return result_list
    

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


    def generate_spikes(N: int, M: int, R: float, Rs: float) -> DataFrame:
        spike_indices = np.random.choice(N, M, replace=False)
        spike_amplitudes = R + np.random.uniform(-Rs, Rs, M)
        spike_signs = np.random.choice([-1, 1], M)  # Выбираем случайный знак для выбросов
        data_values = np.zeros(N)
        data_values[spike_indices] = spike_signs * spike_amplitudes
        return DataFrame({'x': np.arange(N), 'y': data_values})


    def spikes(data, N, M, R, Rs, show_table_data=False) -> list:
        """
        Генерирует M случайных выбросов (спайков) на интервале [0, N] со случайными амплитудами.

        :param data: Входные данные
        :param N: Длина данных
        :param M: Количество выбросов
        :param R: Опорное значение
        :param Rs: Диапазон варьирования амплитуды
        """
        N, M = int(N), int(M)

        if data.get('function_name') == 'Не выбраны' or not data.get('value'):
            if N < M:
                return Model.get_result_dict(error_message=f'Некорректное количество выбросов: M должно быть <= N. M = {M}, N = {N}', in_list=True)

            error_message = None
            if M < 0.005 * N or M > 0.01 * N:
                error_message = f'Некорректное количество выбросов: M должно быть в пределах [{round(0.005*N)}, {round(0.01*N)}]'
            
            return Model.get_result_dict(
                data=Model.generate_spikes(N, M, R, Rs),
                type='spikes',
                error_message=error_message,
                view_chart=True,
                view_table_horizontal=show_table_data,
                in_list=True,
            )
        
        result_list = []
        function_data = data.get('value').function.result
        for df_dict in function_data:
            df = df_dict.get('data', None)
            if df is None:
                continue

            N = len(df)
            if N < M:
                result_list.append(Model.get_result_dict(
                    error_message=f'Некорректное количество выбросов: M должно быть <= N. M = {M}, N = {N}', in_list=True
                ))

            error_message = None
            if M < 0.005 * N or M > 0.01 * N:
                error_message = f'Некорректное количество выбросов: M должно быть в пределах [{round(0.005*N)}, {round(0.01*N)}]'
            
            spikes_df = Model.generate_spikes(N, M, R, Rs)
            spikes_data = Model.get_result_dict(
                data=spikes_df,
                type='spikes',
                error_message=error_message,
                view_chart=True,
                view_table_horizontal=show_table_data,
            )

            data_spikes_df = pd.concat([df, spikes_df]).groupby('x', as_index=False).sum()
            result_list.append(Model.get_result_dict(
                data=data_spikes_df,
                type='spikes',
                initial_data=df_dict,
                extra_data=spikes_data,
                error_message=error_message,
                view_chart=True,
                view_table_horizontal=show_table_data,
            ))
        return result_list
        

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
            
            y_min = np.min(y)
            if y_min < 0:
                y = y[:] - y_min

            intervals = np.array_split(y, M)
            intervals_means = np.array([np.mean(interval) for interval in intervals])
            intervals_std = np.array([np.std(interval) for interval in intervals])

            df_mean = np.mean(y)
            df_std = np.std(y)

            is_stationarity = True
            for i in range(M):
                if not is_stationarity:
                    break

                for j in range(i + 1, M):
                    delta_mean = abs(intervals_means[i] - intervals_means[j])
                    delta_std_dev = abs(intervals_std[i] - intervals_std[j])

                    if (delta_mean / df_mean) > 0.05 or (delta_std_dev / df_std) > 0.05:
                        is_stationarity = False
                        break

            stats_df = pd.DataFrame({
                'Параметр': ['Стационарность'],
                'Значение': [f"Процесс {'' if is_stationarity else 'НЕ '}стационарный"]
            })
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

        'harm': {
            'function': harm,
            'type': 'data',
            'name': 'Гармонический процесс',
            'parameters': {
                "N": {
                    "type": "slider",
                    "title": "Длина данных (N)",
                    "min": 100,
                    "max": 5000,
                    "step": 10,
                    "default_value": 1000,
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
            'function': poly_harm,
            'type': 'data',
            'name': 'Полигармонический процесс',
            'parameters': {
                "N": {
                    "type": "slider",
                    "title": "Длина данных (N)",
                    "min": 100,
                    "max": 5000,
                    "step": 10,
                    "default_value": 1000,
                },
                "A_f_data": {
                    "type": "textfields_datatable",
                    "title": "Амплитуда (A) и частота (f)",
                    "columns": {
                        "A": {
                            'name': 'A, Гц',
                            'tooltip': 'Амплитуда гармонического процесса',
                        },
                        "f": {
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
                        'allowed_extensions': ['csv', 'xls', 'xlsx', 'xlsm', 'xlsb', 'odf', 'ods', 'odt', 'json', 'txt'],
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
                    "type": "dropdown_function_data",
                    "title": "Выбор набора данных",
                    "options": {'Не выбраны': {'function_name': 'Не выбраны', 'value': []}},
                    "default_value": {'function_name': 'Не выбраны', 'value': []},
                    "default_value_to_print": 'Не выбраны: []',
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
                    "type": "dropdown_function_data",
                    "title": "Выбор набора данных",
                    "options": {'Не выбраны': {'function_name': 'Не выбраны', 'value': []}},
                    "default_value": {'function_name': 'Не выбраны', 'value': []},
                    "default_value_to_print": 'Не выбраны: []',
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
                    "max": 100,
                    "step": 1,
                    "default_value": 10,
                }
            }
        }
    }
