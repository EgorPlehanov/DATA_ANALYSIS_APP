import numpy as np
import pandas as pd
import sympy as sp
import csv

from ..model_data_preparation import ModelDataPreparation as DataPrepare


class DataFunctions:
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
            data = DataFunctions.trend_function_linear_rising(t, a, b)
        elif type == "linear_falling":
            data = DataFunctions.trend_function_linear_falling(t, a, b)
        elif type == "nonlinear_rising":
            data = DataFunctions.trend_function_nonlinear_rising(t, a, b)
        elif type == "nonlinear_falling":
            data = DataFunctions.trend_function_nonlinear_falling(t, a, b)

        df = pd.DataFrame({'x': t, 'y': data})
        return DataPrepare.create_result_dict(
            data=df,
            type=type,
            view_chart=True,
            view_table_horizontal=show_table_data,
            in_list=True
        )
    

    def multi_trend(type_list, a, b, step, N, show_table_data=False) -> list:
        if len(type_list) == 0:
            return DataPrepare.create_result_dict(error_message="Нет данных для построения графика", in_list=True)
        
        df_list = []
        for type in type_list:
            df_list.append(*DataFunctions.trend(type, a, b, step, N, show_table_data))
        return df_list
    

    def combinate_trend(type_list, a, b, step, N, show_table_data=False) -> list:
        num_parts = len(type_list)
        if num_parts == 0:
            return DataPrepare.create_result_dict(error_message="Нет данных для построения графика", in_list=True)

        # Разделить период t на равные части
        t_parts = np.array_split(np.arange(0, N, step), num_parts)

        df_list = []
        previous_end_value = None
        for i, type in enumerate(type_list):
            # Сгенерировать данные для каждой части
            data = []
            if type == "linear_rising":
                data = DataFunctions.trend_function_linear_rising(t_parts[i], a, b)
            elif type == "linear_falling":
                data = DataFunctions.trend_function_linear_falling(t_parts[i], a, b)
            elif type == "nonlinear_rising":
                data = DataFunctions.trend_function_nonlinear_rising(t_parts[i], a, b)
            elif type == "nonlinear_falling":
                data = DataFunctions.trend_function_nonlinear_falling(t_parts[i], a, b)

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
    

    def custom_function(expression, N, step, show_table_data=False) -> list:

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


    def data_download(input_data, show_table_data=False) -> list:
        if not (len(input_data) > 0 and isinstance(input_data[0], dict)):
            return DataPrepare.create_result_dict(in_list=True)

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
        error_message = None
        if delta_t > 1 / (2 * f0):
            error_message = f"Некоректное значение временного интервала, delta_t <= 1/(2*f0): delta_t = {delta_t}, 1/(2*f0) = {round(1 / (2 * f0), 5)}"

        k = np.arange(0, N)
        y_values = A0 * np.sin(2 * np.pi * f0 * delta_t * k)
        harm_data = pd.DataFrame({'x': k, 'y': y_values})

        return DataPrepare.create_result_dict(
            data=harm_data,
            type='harm',
            error_message=error_message,
            view_chart=True,
            view_table_horizontal=show_table_data,
            in_list=True,
        )
    

    def poly_harm(N: int, A_f_data: list, delta_t: float, show_table_data=False) -> list:
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

        poly_harm_data = pd.DataFrame({'x': k, 'y': y_values})

        return DataPrepare.create_result_dict(
            data=poly_harm_data,
            type='poly_harm',
            error_message=error_message,
            view_chart=True,
            view_table_horizontal=show_table_data,
            in_list=True,
        )
