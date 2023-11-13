import numpy as np
import pandas as pd
import time
import random
from pandas import DataFrame

from ..model_data_preparation import ModelDataPreparation as DataPrepare



class EditFunctions:
    def generate_noise(N: int, R: float, delta: float, x_values: np.ndarray = None) -> DataFrame:
        '''
        Генерация случайного шума в заданном диапазоне [-R, R]
        '''
        noise_data = np.random.uniform(-R, R, N)
        # Пересчет данных в заданный диапазон R
        min_val, max_val = np.min(noise_data), np.max(noise_data)
        normalized_noise = ((noise_data - min_val) / (max_val - min_val) - 0.5) * 2 * R
        if x_values is None:
            x_values = np.arange(0, N * delta, delta)
        return DataFrame({'x': x_values, 'y': normalized_noise})


    def noise(data, N, R, delta, show_table_data=False) -> list:
        '''
        Добавляет шум к выбранному набору данных
        '''
        N = int(N)
        if data.get('function_name') == 'Не выбраны' or not data.get('value'):
            return DataPrepare.create_result_dict(
                data=EditFunctions.generate_noise(N, R, delta),
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
            
            noised_df = EditFunctions.generate_noise(N, R, delta, df['x'].values)
            noised_data = DataPrepare.create_result_dict(
                data=noised_df,
                type='noise',
                view_chart=True,
                view_table_horizontal=show_table_data,
            )

            data_noised_df = pd.concat([df, noised_df]).groupby('x', as_index=False).sum()
            result_list.append(DataPrepare.create_result_dict(
                data=data_noised_df,
                type='noise',
                initial_data=[df_dict],
                extra_data=noised_data,
                view_chart=True,
                view_table_horizontal=show_table_data,
            ))
        return result_list


    def generate_my_noise(N: int, R: float, delta: float, x_values: np.ndarray = None) -> DataFrame:
        '''
        Генерация случайного шума в заданном диапазоне [-R, R] (Моя реализация)
        '''
        current_time = int(time.time())
        random.seed(current_time)

        custom_noise_data = [random.uniform(-R, R) for _ in range(N)]

        if x_values is None:
            x_values = np.arange(0, N * delta, delta)
        return pd.DataFrame({'x': x_values, 'y': custom_noise_data})


    def my_noise(data, N, R, delta, show_table_data=False) -> list:
        '''
        Добавляет шум к выбранному набору данных (Моя реализация)
        '''
        N = int(N)

        if data.get('function_name') == 'Не выбраны' or not data.get('value'):
            return DataPrepare.create_result_dict(
                data=EditFunctions.generate_my_noise(N, R, delta),
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
            
            my_noised_df = EditFunctions.generate_my_noise(N, R, delta, df['x'].values)
            my_noised_data = DataPrepare.create_result_dict(
                data=my_noised_df,
                type='noise',
                view_chart=True,
                view_table_horizontal=show_table_data,
            )

            data_noised_df = pd.concat([df, my_noised_df]).groupby('x', as_index=False).sum()
            result_list.append(DataPrepare.create_result_dict(
                data=data_noised_df,
                type='noise',
                initial_data=[df_dict],
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
                result_list.append(DataPrepare.create_result_dict(error_message=error_message))
                continue

            shifted_df = df.get('y').copy()
            shifted_df[N1:N2+1] += C
            shifted_df = pd.DataFrame({'x': df.get('x').copy(), 'y': shifted_df})
            result_list.append(DataPrepare.create_result_dict(
                data=shifted_df,
                type='shift',
                initial_data = [df_dict],
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
                return DataPrepare.create_result_dict(error_message=f'Некорректное количество выбросов: M должно быть <= N. M = {M}, N = {N}', in_list=True)

            error_message = None
            if M < 0.005 * N or M > 0.01 * N:
                error_message = f'Некорректное количество выбросов: M должно быть в пределах [{round(0.005*N)}, {round(0.01*N)}]'
            
            return DataPrepare.create_result_dict(
                data=EditFunctions.generate_spikes(N, M, R, Rs),
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
                result_list.append(DataPrepare.create_result_dict(
                    error_message=f'Некорректное количество выбросов: M должно быть <= N. M = {M}, N = {N}', in_list=True
                ))

            error_message = None
            if M < 0.005 * N or M > 0.01 * N:
                error_message = f'Некорректное количество выбросов: M должно быть в пределах [{round(0.005*N)}, {round(0.01*N)}]'
            
            spikes_df = EditFunctions.generate_spikes(N, M, R, Rs)
            spikes_data = DataPrepare.create_result_dict(
                data=spikes_df,
                type='spikes',
                error_message=error_message,
                view_chart=True,
                view_table_horizontal=show_table_data,
            )

            data_spikes_df = pd.DataFrame({'x': df.get('x').copy(), 'y': df['y'] + spikes_df['y']})
            result_list.append(DataPrepare.create_result_dict(
                data=data_spikes_df,
                type='spikes',
                initial_data=[df_dict],
                extra_data=spikes_data,
                error_message=error_message,
                view_chart=True,
                view_table_horizontal=show_table_data,
            ))
        return result_list
    

    def add_model(first_data, second_data, show_table_data=False) -> list:
        '''
        Поэлементно складывает два набора данных
        '''
        if (
            first_data.get('function_name') == 'Не выбраны' or not first_data.get('value')
            or second_data.get('function_name') == 'Не выбраны' or not second_data.get('value')
        ):
            return []
        
        result_list = []
        first_function_data = first_data.get('value').function.result
        second_function_data = second_data.get('value').function.result

        for first_df_dict in first_function_data:
            first_df = first_df_dict.get('data', None)
            if first_df is None:
                continue

            first_values = first_df.get('y').copy()
            first_N = len(first_values)

            for second_df_dict in second_function_data:
                second_df = second_df_dict.get('data', None)
                if second_df is None:
                    continue

                second_values = second_df.get('y').copy()
                second_N = len(second_values)

                N = first_N if first_N < second_N else second_N

                result_df = pd.DataFrame({'x': np.arange(0, N), 'y': first_values.iloc[:N] + second_values.iloc[:N]})
                result_list.append(DataPrepare.create_result_dict(
                    data=result_df,
                    type='add_model',
                    initial_data=[first_df_dict, second_df_dict],
                    view_chart=True,
                    view_table_horizontal=show_table_data,
                ))
        return result_list
    

    def mult_model(first_data, second_data, show_table_data=False) -> list:
        '''
        Поэлементно перемножает два набора данных
        '''
        if (
            first_data.get('function_name') == 'Не выбраны' or not first_data.get('value')
            or second_data.get('function_name') == 'Не выбраны' or not second_data.get('value')
        ):
            return []
        
        result_list = []
        first_function_data = first_data.get('value').function.result
        second_function_data = second_data.get('value').function.result

        for first_df_dict in first_function_data:
            first_df = first_df_dict.get('data', None)
            if first_df is None:
                continue

            first_values = first_df.get('y').copy()
            first_N = len(first_values)

            for second_df_dict in second_function_data:
                second_df = second_df_dict.get('data', None)
                if second_df is None:
                    continue

                second_values = second_df.get('y').copy()
                second_N = len(second_values)

                N = first_N if first_N < second_N else second_N

                result_df = pd.DataFrame({'x': np.arange(0, N), 'y': first_values.iloc[:N] * second_values.iloc[:N]})
                result_list.append(DataPrepare.create_result_dict(
                    data=result_df,
                    type='mult_model',
                    initial_data=[first_df_dict, second_df_dict],
                    view_chart=True,
                    view_table_horizontal=show_table_data,
                ))
        return result_list
    

    def anti_shift(data, show_table_data=False):
        if data.get('function_name') == 'Не выбраны' or not data.get('value'):
            return []
        
        result_list = []
        function_data = data.get('value').function.result
        for df_dict in function_data:
            df = df_dict.get('data', None)
            if df is None:
                continue
            
            y_values = df.get('y').copy()
            mean_value = np.mean(y_values)
            y_values -= mean_value

            proc_data_df = pd.DataFrame({'x': df.get('x').copy(), 'y': y_values})
            result_list.append(DataPrepare.create_result_dict(
                data=proc_data_df,
                type='anti_shift',
                initial_data=[df_dict],
                view_chart=True,
                view_table_horizontal=show_table_data,
            ))
        return result_list
    

    def anti_spike(data, R, show_table_data=False):
        if data.get('function_name') == 'Не выбраны' or not data.get('value'):
            return []
        
        result_list = []
        function_data = data.get('value').function.result
        for df_dict in function_data:
            df = df_dict.get('data', None)
            if df is None:
                continue
            
            y_values = df.get('y').copy()
            N = len(y_values)

            proc_data = np.copy(y_values)
            for i in range(1, N-1):
                if abs(y_values[i] - y_values[i-1]) > R and abs(y_values[i] - y_values[i+1]) > R:
                    proc_data[i] = (y_values[i-1] + y_values[i+1]) / 2

            proc_data_df = pd.DataFrame({'x': df.get('x').copy(), 'y': proc_data})
            result_list.append(DataPrepare.create_result_dict(
                data=proc_data_df,
                type='anti_spike',
                initial_data=[df_dict],
                view_chart=True,
                view_table_horizontal=show_table_data,
            ))
        return result_list


    def anti_trend_linear(data, show_table_data=False):
        if data.get('function_name') == 'Не выбраны' or not data.get('value'):
            return []
        
        result_list = []
        function_data = data.get('value').function.result
        for df_dict in function_data:
            df = df_dict.get('data', None)
            if df is None:
                continue
            
            y_values = df.get('y').copy()
            x_values = df.get('x').copy()
        
            # Подгонка линейного тренда к данным
            linear_trend = np.polyfit(x_values, y_values, 1)
            linear_fit = np.polyval(linear_trend, x_values)
            
            # Удаление линейного тренда путем вычитания линейной подгонки
            detrended_data = y_values - linear_fit
            
            # Вычисление первой производной (градиента) отдетрендированных данных
            derivative = np.gradient(detrended_data)

            proc_data_df = pd.DataFrame({'x': x_values, 'y': derivative})
            result_list.append(DataPrepare.create_result_dict(
                data=proc_data_df,
                type='anti_trend_linear',
                initial_data=[df_dict],
                view_chart=True,
                view_table_horizontal=show_table_data,
            ))
        return result_list
    

    def anti_trend_non_linear(data, W, show_table_data=False):
        if data.get('function_name') == 'Не выбраны' or not data.get('value'):
            return []
        
        result_list = []
        function_data = data.get('value').function.result
        for df_dict in function_data:
            df = df_dict.get('data', None)
            if df is None:
                continue
            
            y_values = df.get('y').copy()
            '''
            Реализовать выделения и удаления нелинейного тренда методом скользящего среднего из данных аддитивной модели
            '''

            proc_data_df = pd.DataFrame({'x': df.get('x').copy(), 'y': y_values})
            result_list.append(DataPrepare.create_result_dict(
                data=proc_data_df,
                type='anti_trend_non_linear',
                initial_data=[df_dict],
                view_chart=True,
                view_table_horizontal=show_table_data,
            ))
        return result_list
    

    def anti_noise(data, M, show_table_data=False):
        if data.get('function_name') == 'Не выбраны' or not data.get('value'):
            return []
        
        result_list = []
        function_data = data.get('value').function.result
        for df_dict in function_data:
            df = df_dict.get('data', None)
            if df is None:
                continue
            
            y_values = df.get('y').copy()
            '''
            Реализовать подавления случайного шума методом накопления
            '''

            proc_data_df = pd.DataFrame({'x': df.get('x').copy(), 'y': y_values})
            result_list.append(DataPrepare.create_result_dict(
                data=proc_data_df,
                type='anti_noise',
                initial_data=[df_dict],
                view_chart=True,
                view_table_horizontal=show_table_data,
            ))
        return result_list
    