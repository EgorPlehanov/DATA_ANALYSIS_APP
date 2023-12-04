import numpy as np
import pandas as pd
import time
import random
from pandas import DataFrame

from ..model_data_preparation import ModelDataPreparation as DataPrepare



class EditFunctions:
    def generate_noise(N: int, R: float, delta: float = None, x_values: np.ndarray = None) -> DataFrame:
        '''
        Генерация случайного шума в заданном диапазоне [-R, R]

        :param N: Длина данных
        :param R: Максимальное значение шума
        :param delta: Шаг генерации данных
        :param x_values: Значения x
        '''
        noise_data = np.random.uniform(-R, R, N)
        # Пересчет данных в заданный диапазон R
        min_val, max_val = np.min(noise_data), np.max(noise_data)
        normalized_noise = ((noise_data - min_val) / (max_val - min_val) - 0.5) * 2 * R
        if x_values is None:
            if delta is None:
                delta = 1
            x_values = np.arange(0, N * delta, delta)
        return DataFrame({'x': x_values, 'y': normalized_noise})


    def noise(data: dict, N: int, R: float, delta: float, show_table_data: bool=False) -> list:
        '''
        Добавляет шум к выбранному набору данных

        :param data: Набор данных
        :param N: Длина данных
        :param R: Максимальное значение шума
        :param delta: Шаг генерации данных
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

        :param N: Длина данных
        :param R: Максимальное значение шума
        :param delta: Шаг генерации данных
        :param x_values: Значения x
        '''
        current_time = int(time.time())
        random.seed(current_time)

        custom_noise_data = [random.uniform(-R, R) for _ in range(N)]

        if x_values is None:
            x_values = np.arange(0, N * delta, delta)
        return pd.DataFrame({'x': x_values, 'y': custom_noise_data})


    def my_noise(data: dict, N: int, R: float, delta: float, show_table_data: bool=False) -> list:
        '''
        Добавляет шум к выбранному набору данных (Моя реализация)

        :param data: Входные данные
        :param N: Длина данных (Используется для генерации если не задан набор данных)
        :param R: Максимальное значение шума 
        :param delta: Шаг генерации данных (Используется для генерации если не задан набор данных)
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
    

    def shift(data: dict, C: float, N1: int, N2: int, show_table_data: bool=False) -> dict:
        """
        Сдвигает данные data в интервале [N1, N2] на константу C.

        :param data: Входные данные (сгенерированные в блоке данных)
        :param C: Значение сдвига
        :param N1: Начальный индекс интервала
        :param N2: Конечный индекс интервала
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
        '''
        Генерирует M случайных выбросов (спайков) на интервале [0, N] со случайными амплитудами

        :param N: Длина данных
        :param M: Количество выбросов
        :param R: Опорное значение
        :param Rs: Диапазон варьирования амплитуды
        '''
        spike_indices = np.random.choice(N, M, replace=False)
        spike_amplitudes = R + np.random.uniform(-Rs, Rs, M)
        spike_signs = np.random.choice([-1, 1], M)  # Выбираем случайный знак для выбросов
        data_values = np.zeros(N)
        data_values[spike_indices] = spike_signs * spike_amplitudes
        return DataFrame({'x': np.arange(N), 'y': data_values})


    def spikes(data: dict, N: int, M: int, R: float, Rs: float, show_table_data: bool=False) -> list:
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
    

    def add_model(first_data: dict, second_data: dict, show_table_data: bool=False) -> list:
        '''
        Поэлементно складывает два набора данных

        :param first_data: Первый набор данных
        :param second_data: Второй набор данных
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
    

    def mult_model(first_data: dict, second_data: dict, show_table_data: bool=False) -> list:
        '''
        Поэлементно перемножает два набора данных

        :param first_data: Первый набор данных
        :param second_data: Второй набор данных
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
    

    def anti_shift(data: dict, show_table_data: bool=False):
        '''
        Убирает смещение данных

        :param data: Набор данных
        '''
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
    

    def anti_spike(data: dict, R: float, show_table_data: bool=False) -> list:
        '''
        Подавляет непровдопадобные значения методом 3-х точечной линейной интерполяции

        :param data: Набор данных
        :param R: Порог (для сравнения предыдущего и следующего значения с текущим)
        '''
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


    def anti_trend_linear(data: dict, show_table_data: bool=False):
        '''
        Убирает линейный тренд

        :param data: Набор данных
        '''
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
    

    def anti_trend_non_linear(data: dict, W: int, show_table_data: bool=False):
        '''
        Убирает нелинейный тренд (метод скользящего среднего)

        :param data: Набор данных
        :param W: Ширина окна
        '''
        if data.get('function_name') == 'Не выбраны' or not data.get('value'):
            return []
        
        W = int(W)
        
        result_list = []
        function_data = data.get('value').function.result
        for df_dict in function_data:
            df = df_dict.get('data', None)
            if df is None:
                continue
            
            y_values = df.get('y').copy()
            N = len(y_values) - W
            for n in range(N):
                y_values[n] -= sum(y_values[n:n+W]) / W

            proc_data_df = pd.DataFrame({'x': df.get('x').copy(), 'y': y_values})
            result_list.append(DataPrepare.create_result_dict(
                data=proc_data_df,
                type='anti_trend_non_linear',
                initial_data=[df_dict],
                view_chart=True,
                view_table_horizontal=show_table_data,
            ))
        return result_list
    

    def anti_noise(data: dict, M: dict, R: float, show_table_data: bool=False):
        '''
        Убирает случайный шум

        :param data: Набор данных
        :param M: Количество реализацй случайного шума
        '''
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
            N = len(y_values)

            extra_data = []
            std_deviation = []
            M_values = sorted([int(m['M']) for m in M.values()])
            for M in M_values:
                
                denoised_y = np.zeros(N)
                for _ in range(M):
                    noise = EditFunctions.generate_noise(N, R)['y']
                    denoised_y += noise + y_values.copy()
                denoised_y = denoised_y / (M)

                # Расчет стандартной ошибки
                std_deviation.append(np.std(denoised_y))

                # Добавление расчета для M случайных шумов
                M_denoised_df = pd.DataFrame({'x': x_values, 'y': denoised_y})
                extra_data.append(DataPrepare.create_result_dict(
                    data=M_denoised_df,
                    type=f'anti_noise(M={M})',
                    view_chart=True,
                    view_table_horizontal=show_table_data,
                ))

            # Добавление статистических данных
            extra_data.append(DataPrepare.create_result_dict(
                data=pd.DataFrame({'M': M_values, 'std': std_deviation}),
                type='anti_noise_M_std',
                view_table_horizontal=True,
            ))


            
            # y_values = df.get('y').copy()
            # x_values = df.get('x').copy()
            # N = len(y_values)

            # noised_df = EditFunctions.generate_noise(N, R, x_values=df['x'].values)
            # data_noised_df = pd.concat([df, noised_df]).groupby('x', as_index=False).sum()
            # data_noised_y = data_noised_df.get('y').copy()

            # std_deviation = []
            # extra_data = []
            # M_values = [int(m['M']) for m in M.values()]
            # for M in M_values:
            #     accumulated_noise = np.zeros(N)
            #     for _ in range(M):
            #         accumulated_noise += EditFunctions.generate_noise(N, R)['y']

            #     norm_noise = accumulated_noise / M
            #     denoised_data = norm_noise + y_values

            #     std_deviation.append(np.std(norm_noise))

            #     M_denoised_df = pd.DataFrame({'x': x_values, 'y': denoised_data})
            #     extra_data.append(DataPrepare.create_result_dict(
            #         data=M_denoised_df,
            #         type=f'anti_noise(M={M})',
            #         view_chart=True,
            #         view_table_horizontal=show_table_data,
            #     ))

            # extra_data.append(DataPrepare.create_result_dict(
            #     data=pd.DataFrame({'M': M_values, 'std': std_deviation}),
            #     type='anti_noise_M_std',
            #     view_table_horizontal=True,
            # ))

            result_list.append(DataPrepare.create_result_dict(
                data=df,
                type='anti_noise',
                # initial_data=[df_dict],
                extra_data=extra_data,
                view_chart=True,
                view_table_horizontal=show_table_data,
            ))
        return result_list
    

    def convol_model(first_data: dict, second_data: dict, M: int, show_table_data: bool=False):
        '''
        Дискретная светрка

        :param first_data: Первый набор данных
        :param second_data: Второй набор данных
        :param M: Ширина окна
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
                first_values = first_values[:N]
                second_values = second_values[:N]

                y = np.zeros(N + M)

                for k in range(N + M):
                    y[k] = sum([
                        first_values[k - m] * second_values[m]
                        for m in range(M)
                        if k - m >= 0 and k - m < N
                    ])

                y = y[M//2:-M//2]
                
                result_df = pd.DataFrame({'x': np.arange(0, len(y)), 'y': y})
                result_list.append(DataPrepare.create_result_dict(
                    data=result_df,
                    type=f"convol_model",
                    initial_data=[first_df_dict, second_df_dict],
                    view_chart=True,
                    view_table_horizontal=show_table_data,
                ))
        return result_list
    

    def scale_values(data: dict, new_min: float, new_max: float, show_table_data: bool=False):
        '''
        Нормирование значений

        :param data: Набор данных
        :param new_min: Новое минимальное значение
        :param new_max: Новое максимальное значение
        '''
        if data.get('function_name') == 'Не выбраны' or not data.get('value'):
            return []
        
        result_list = []
        function_data = data.get('value').function.result
        for df_dict in function_data:
            df = df_dict.get('data', None)
            if df is None:
                continue
            
            y_values = df.get('y').copy()

            min_val = np.min(y_values)
            max_val = np.max(y_values)
            
            normalized = new_min + ((y_values - min_val) * (new_max - new_min)) / (max_val - min_val)

            proc_data_df = pd.DataFrame({'x': df.get('x').copy(), 'y': normalized})
            result_list.append(DataPrepare.create_result_dict(
                data=proc_data_df,
                type='scale_values',
                initial_data=[df_dict],
                view_chart=True,
                view_table_horizontal=show_table_data,
            ))
        return result_list
    

    def normalize_values(data: dict, new_max: float, show_table_data: bool=False):
        '''
        Нормализация значений

        :param data: Набор данных
        :param new_min: Новое минимальное значение
        :param new_max: Новое максимальное значение
        '''
        if data.get('function_name') == 'Не выбраны' or not data.get('value'):
            return []
        
        result_list = []
        function_data = data.get('value').function.result
        for df_dict in function_data:
            df = df_dict.get('data', None)
            if df is None:
                continue
            
            y_values = df.get('y').copy()

            max_val = np.max(y_values)
            
            normalized = y_values / max_val * new_max

            proc_data_df = pd.DataFrame({'x': df.get('x').copy(), 'y': normalized})
            result_list.append(DataPrepare.create_result_dict(
                data=proc_data_df,
                type='normalize_values',
                initial_data=[df_dict],
                view_chart=True,
                view_table_horizontal=show_table_data,
            ))
        return result_list
    

    def extend_model(first_data: dict, second_data: dict, show_table_data: bool=False):
        '''
        Объединение двух наборов данных

        :param first_data: Первый набор данных
        :param second_data: Второй набор данных
        :param M: Ширина окна
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


            for second_df_dict in second_function_data:
                second_df = second_df_dict.get('data', None)
                if second_df is None:
                    continue

                first_x = first_df.get('x').copy()
                second_x = second_df.get('x').copy()

                first_y = first_df.get('y').copy()
                second_y = second_df.get('y').copy()

                second_x = second_x + np.max(first_x)

                result_x = np.concatenate((first_x[:-1], second_x))
                result_y = np.concatenate((first_y[:-1], second_y))

                result_df = DataFrame({'x': result_x, 'y': result_y})
                result_list.append(DataPrepare.create_result_dict(
                    data=result_df,
                    type="extend_model",
                    initial_data=[first_df_dict, second_df_dict],
                    view_chart=True,
                    view_table_horizontal=show_table_data,
                ))
        return result_list