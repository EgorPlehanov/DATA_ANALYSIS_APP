import numpy as np
import pandas as pd
import sympy as sp
import csv

from ..model_data_preparation import ModelDataPreparation as DataPrepare


class DataFunctions:
    def trend(type: str, a: float, b: float, step: float, N: int, show_table_data: bool=False) -> list:
        '''
        Создает графики тренда

        :param type: Тип тренда
        :param a: Коэффициент a
        :param b: Коэффициент b
        :param step: Шаг генерации данных
        :param N: Длина данных

        trend types:
            linear_rising - Линейно восходящий
            linear_falling - Линейно нисходящий
            nonlinear_rising - Нелинейно восходящий
            nonlinear_falling - Нелинейно нисходящий
        '''
        trend_type_to_function = {
            "linear_rising": lambda t, a, b: a * t + b,
            "linear_falling": lambda t, a, b: -a * t + b,
            "nonlinear_rising": lambda t, a, b: b * np.exp(a * t),
            "nonlinear_falling": lambda t, a, b: b * np.exp(-a * t),
        }

        t = np.arange(0, N * step, step)

        data = None
        if type in trend_type_to_function:
            data = trend_type_to_function[type](t, a, b)

        df = pd.DataFrame({'x': t, 'y': data})
        return DataPrepare.create_result_dict(
            data=df,
            type=type,
            view_chart=True,
            view_table_horizontal=show_table_data,
            in_list=True
        )
    

    def multi_trend(type_list: list, a: float, b: float, step: float, N: int, show_table_data: bool=False) -> list:
        '''
        Создает графики нескольких функций тренда

        :param type_list: Список типов функций тренда
        :param a: Коэффициент a
        :param b: Коэффициент b
        :param step: Шаг генерации данных
        :param N: Длина данных
        '''
        if len(type_list) == 0:
            return DataPrepare.create_result_dict(error_message="Нет данных для построения графика", in_list=True)
        
        df_list = []
        for type in type_list:
            df_list.append(*DataFunctions.trend(type, a, b, step, N, show_table_data))
        return df_list
    

    def combinate_trend(type_list: list, a: float, b: float, step: float, N: int, show_table_data: bool=False) -> list:
        '''
        Создает график комбинированной функции тренда

        :param type_list: Список типов функций тренда
        :param a: Коэффициент a
        :param b: Коэффициент b
        :param step: Шаг генерации данных
        :param N: Длина данных
        '''
        num_parts = len(type_list)
        if num_parts == 0:
            return DataPrepare.create_result_dict(error_message="Нет данных для построения графика", in_list=True)

        trend_type_to_function = {
            "linear_rising": lambda t, a, b: a * t + b,
            "linear_falling": lambda t, a, b: -a * t + b,
            "nonlinear_rising": lambda t, a, b: b * np.exp(a * t),
            "nonlinear_falling": lambda t, a, b: b * np.exp(-a * t),
        }

        # Разделить период t на равные части
        t_parts = np.array_split(np.arange(0, N * step, step), num_parts)

        df_list = []
        previous_end_value = None
        for i, type in enumerate(type_list):
            # Сгенерировать данные для каждой части
            data = []

            if type not in trend_type_to_function:
                continue
            data = trend_type_to_function[type](t_parts[i], a, b)

            # Смещение начала графика до уровня конца предыдущей части
            if previous_end_value is not None:
                shift = previous_end_value - data[0]
                data = [value + shift for value in data]

            df_list.append(pd.DataFrame({'x': t_parts[i], 'y': data}))

            # Обновите значение последнего элемента для следующей итерации
            previous_end_value = data[-1]
            
        # Объединить результаты
        combined_df = pd.concat(df_list, ignore_index=True)
        return DataPrepare.create_result_dict(
            data=combined_df,
            type=' -> '.join(type_list),
            view_chart=True,
            view_table_horizontal=show_table_data,
            in_list=True,
        )
    

    def custom_function(expression: str, N: int, step: int, show_table_data: bool=False) -> list:
        '''
        Создает набор данных по расчетной функции

        :param expression: Расчетная функция
        :param N: Длина данных
        :param step: Шаг генерации данных
        '''
        if not expression:
            return DataPrepare.create_result_dict(error_message="Не задана расчетная функция", in_list=True)
        
        x = sp.symbols('x')

        math_expression = sp.sympify(expression)
        function = sp.lambdify(x, math_expression, "numpy")

        x_values = np.arange(0, N * step, step)
        y_values = [function(x) for x in x_values]

        data = pd.DataFrame({'x': x_values, 'y': y_values})

        return DataPrepare.create_result_dict(
            data=data,
            type='custom_function',
            view_chart=True,
            view_table_horizontal=show_table_data,
            in_list=True,
        )


    def data_download(input_data: list, show_table_data: bool=False) -> list:
        '''
        Обрабатывает данные из файлов

        :param input_data: Список файлов
        '''
        if not (len(input_data) > 0 and isinstance(input_data[0], dict)):
            return DataPrepare.create_result_dict(in_list=True)

        result_list = []
        for file in input_data:
            file_name = file.get('name', '')
            file_path = file.get('path', '')

            # Определение формата файла на основе расширения
            file_extension = file_path.split('.')[-1].lower()
            
            try:
                match file_extension:
                    case 'csv':
                        # Определение разделителя
                        with open(file_path, 'r', newline='') as csvfile:
                            sample_data = csvfile.read(1024)
                            sniffer = csv.Sniffer()
                            delimiter = sniffer.sniff(sample_data).delimiter
                        # Чтение CSV файла с указанием определенного разделителя
                        df = pd.read_csv(file_path, delimiter=delimiter)
                    case 'xls' | 'xlsx' | 'xlsm' | 'xlsb' | 'odf' | 'ods' | 'odt':
                        df = pd.read_excel(file_path)

                    case 'json':
                        df = pd.read_json(file_path)

                    case 'txt':
                        df = pd.read_table(file_path, sep=';')

                    case 'dat':
                        with open(file_path, "rb") as file:
                            binary_data = file.read()
                        float_data = np.frombuffer(binary_data, dtype=np.float32)

                        df = pd.DataFrame({'x': np.arange(0, len(float_data)), 'y': float_data})
                    
                    case _:
                        result_list.append(DataPrepare.create_result_dict(
                            error_message=f"Формат {file_extension} не поддерживается",
                            type=f'data_download({file_name})'
                        ))
                        continue
            except Exception as e:
                result_list.append(DataPrepare.create_result_dict(
                    error_message=f"При чтении файла '{file_name}' произошла ошибка: {str(e)}",
                    type=f'data_download({file_name})'
                ))
                continue

            if df.empty:
                result_list.append(DataPrepare.create_result_dict(
                    error_message=f"Файл '{file_name}' пуст",
                    type=f'data_download({file_name})'
                ))
                continue

            result_list.append(DataPrepare.create_result_dict(
                data=df,
                type=f'data_download({file_name})',
                view_chart=True,
                view_table_horizontal=show_table_data,
            ))
        return result_list
    

    def harm(N: int, A0: float, f0: float, delta_t: float, show_table_data=False) -> list:
        '''
        Создает гармонический процесс

        :param N: Длина данных
        :param A0: Амплитуда
        :param f0: Частота
        :param delta_t: Шаг генерации данных
        '''
        error_message = None
        if delta_t > 1 / (2 * f0):
            error_message = f"Некоректное значение временного интервала, delta_t <= 1/(2*f0): delta_t = {delta_t}, 1/(2*f0) = {round(1 / (2 * f0), 5)}"

        k = np.arange(0, N)
        y_values = A0 * np.sin(2 * np.pi * f0 * delta_t * k)
        harm_data = pd.DataFrame({'x': delta_t * k, 'y': y_values})

        return DataPrepare.create_result_dict(
            data=harm_data,
            type='harm',
            error_message=error_message,
            view_chart=True,
            view_table_horizontal=show_table_data,
            in_list=True,
        )
    

    def poly_harm(N: int, A_f_data: list, delta_t: float, show_table_data=False) -> list:
        '''
        Создает полигормонический процесс

        :param N: Длина данных
        :param A_f_data: Список Амплитуд и Частот
        :param delta_t: Шаг генерации данных
        '''
        if len(A_f_data) == 0:
            return DataPrepare.create_result_dict(error_message="Нет данных об амплитуде и частоте для построения графика", in_list=True)

        max_fi = max([params['f'] for params in A_f_data.values()])
        error_message = None
        if delta_t > 1 / (2 * max_fi):
            error_message = "Некоректное значение временного интервала.\nОно должно удовлетворять условию: " \
                + f"delta_t <= 1 / (2 * max(fi)): delta_t = {delta_t}, 1 / (2 * max(fi)) = {round(1 / (2 * max_fi), 5)}"

        N = int(N)
        k = np.arange(0, N)
        y_values = np.zeros(N)
        for params in A_f_data.values():
            y_values += params['A'] * np.sin(2 * np.pi * params['f'] * delta_t * k)

        poly_harm_data = pd.DataFrame({'x': delta_t * k, 'y': y_values})

        return DataPrepare.create_result_dict(
            data=poly_harm_data,
            type='poly_harm',
            error_message=error_message,
            view_chart=True,
            view_table_horizontal=show_table_data,
            in_list=True,
        )
    