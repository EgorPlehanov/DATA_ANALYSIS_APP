import numpy as np
import pandas as pd
import re

from ..model_data_preparation import ModelDataPreparation as DataPrepare


class AnalyticFunctions:
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
            result_list.append(DataPrepare.create_result_dict(
                data=stats_df,
                type='statistics',
                initial_data = [df_dict],
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
                result_list.append(DataPrepare.create_result_dict(error_message=error_message))
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
            result_list.append(DataPrepare.create_result_dict(
                data=stats_df,
                type='stationarity',
                initial_data = [df_dict],
                view_table_vertical=True,
            ))
        return result_list
    
    
    def hist(data, M, is_density=True, show_table_data=False) -> list:
        '''
        Строит графики функции плотности распределения вероятностей
        '''
        if data.get('function_name') == 'Не выбраны' or not data.get('value'):
            return []
        
        M = int(M)
        
        result_list = []
        function_data = data.get('value').function.result
        for df_dict in function_data:
            df = df_dict.get('data', None)
            if df is None:
                continue
            
            counts, bin_edges = np.histogram(df.get('y').copy(), bins=M, density=is_density)
            bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

            axi_name = 'density' if is_density else 'count'
            hist_df = pd.DataFrame({'y': bin_centers, axi_name: counts})

            result_list.append(DataPrepare.create_result_dict(
                data=hist_df,
                type='hist',
                initial_data = [df_dict],
                view_histogram=True,
                view_table_horizontal=show_table_data,
            ))
        return result_list
    

    def acf(data, function_type, show_table_data=False) -> list:
        '''
        Автокорреляция/Ковариация
        '''
        if data.get('function_name') == 'Не выбраны' or not data.get('value'):
            return []
        
        result_list = []
        function_data = data.get('value').function.result
        for df_dict in function_data:
            df = df_dict.get('data', None)
            if df is None:
                continue

            y = df.get('y').copy()
            N = len(y)

            y_mean = np.mean(y)
            L_values = np.arange(0, N)
            ac_values = []

            for L in L_values:
                if function_type == 'autocorrelation':
                    ac = sum([(y[k] - y_mean) * (y[k + L] - y_mean) for k in range(0, N-L-1)]) / sum((y - y_mean)**2)
                elif function_type == 'covariance':
                    ac = np.sum([(y[k] - y_mean) * (y[k+L] - y_mean) for k in range(0, N-L-1)]) / N

                ac_values.append(ac)
            
            result_df = pd.DataFrame({'L': L_values, 'AC': ac_values})
            result_list.append(DataPrepare.create_result_dict(
                data=result_df,
                type=f"acf_{function_type}",
                initial_data = [df_dict],
                view_chart=True,
                view_table_horizontal=show_table_data,
            ))
        return result_list
    

    def ccf(first_data, second_data, show_table_data=False) -> list:
        '''
        Кросс-корреляция
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

                L_values = np.arange(0, N)
                first_mean = np.mean(first_values)
                second_mean = np.mean(second_values)
                
                ccf_values = []
                for L in L_values:
                    ccf_L = sum([(first_values[k] - first_mean) * (second_values[k + L] - second_mean) for k in range(0, N-L-1)]) / N
                    ccf_values.append(ccf_L)
                
                result_df = pd.DataFrame({'L': L_values, 'AC': ccf_values})
                result_list.append(DataPrepare.create_result_dict(
                    data=result_df,
                    type=f"ccf",
                    initial_data=[first_df_dict, second_df_dict],
                    view_chart=True,
                    view_table_horizontal=show_table_data,
                ))
        return result_list
    

    def get_fourier(y_values) -> pd.DataFrame:
        '''
        Вычисление прямого преобразования Фурье
        '''
        N = len(y_values)

        # Вычисление прямого преобразования Фурье
        real_part = np.zeros(N)  # Для действительной части
        imag_part = np.zeros(N)  # Для мнимой части

        for n in range(N):
            for k in range(len(y_values)):
                real_part[n] += y_values[k] * np.cos(2 * np.pi * n * k / N)
                imag_part[n] += y_values[k] * np.sin(2 * np.pi * n * k / N)            
        
        # Вычисление амплитудного спектра
        X_amp = [np.sqrt(real_part[k] ** 2 + imag_part[k] ** 2) for k in range(N)]
        return pd.DataFrame({'Re[Xn]': real_part, 'Im[Xn]': imag_part, '|Xn|': X_amp})


    def fourier(data, show_table_data=False, show_calculation_table=False) -> list:
        '''
        Построение прямого преобразования Фурье
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
            fourier_data = AnalyticFunctions.get_fourier(y_values)

            fourier_extra_data = None
            if show_calculation_table:
                fourier_extra_data = DataPrepare.create_result_dict(
                    data=fourier_data,
                    type='fourier',
                    view_table_horizontal=True,
                )

            fourier_df = pd.DataFrame({'n': np.arange(len(fourier_data)), '|Xn|': fourier_data['|Xn|']})
            result_list.append(DataPrepare.create_result_dict(
                data=fourier_df,
                type='fourier',
                extra_data=fourier_extra_data,
                initial_data = [df_dict],
                view_chart=True,
                view_table_horizontal=show_table_data,
            ))
        return result_list
    

    def spectr_fourier(data={}, delta_t=None, L_window=0, show_table_data=False) -> list:
        '''
        Построение амплитудного спектра Фурье на основе прямого преобразования Фурье
        '''
        if data.get('function_name') == 'Не выбраны' or not data.get('value'):
            return []
        
        L_window = int(L_window)
        result_list = []
        
        function_data = data.get('value').function.result
        for df_dict in function_data:
            df = df_dict.get('data', None)
            if df is None:
                continue
            
            y_values = df.get('y').copy()
            Xn_values = np.abs(np.fft.fft(
                y_values * np.concatenate([np.ones(len(y_values) - L_window), np.zeros(L_window)])
            ))

            N = len(Xn_values) // 2

            f_border = 1 / (2 * delta_t)
            delta_f = f_border / N
            frequencies = np.arange(N) * delta_f

            spectr_fourier_df = pd.DataFrame({'f': frequencies, '|Xn|': Xn_values[:N]})
            result_list.append(DataPrepare.create_result_dict(
                data=spectr_fourier_df,
                type='spectr_fourier',
                initial_data = [df_dict],
                view_chart=True,
                view_table_horizontal=show_table_data,
            ))
        return result_list


