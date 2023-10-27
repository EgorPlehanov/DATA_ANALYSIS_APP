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

            data_spikes_df = pd.concat([df, spikes_df]).groupby('x', as_index=False).sum()
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