from pandas import DataFrame


class ModelDataPreparation:
    @staticmethod
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


    @staticmethod
    def create_result_dict(
            data: DataFrame = None,
            type: str = None,
            initial_data: dict = None,
            extra_data: dict = None,
            error_message: str = None,
            view_chart: bool = None,
            view_histogram: bool = None,
            view_table_horizontal: bool = None,
            view_table_vertical: bool = None,
            main_view: str = None,
            in_list: bool = False
        ) -> dict:
        result_dict = {}

        if data is not None:
            result_dict['data'] = ModelDataPreparation.round_and_clip_dataframe(data)
            
        if initial_data:
            result_dict['initial_data'] = initial_data

        if extra_data:
            result_dict['extra_data'] = extra_data

        if type:
            initial_data_type = ''
            if initial_data is not None:
                initial_data_type_list = [data.get('type') for data in initial_data if data and 'type' in data]
                initial_data_type = f" ({'; '.join(initial_data_type_list)})" if len(initial_data_type_list) > 0 else ''

            result_dict['type'] = f'{type}{initial_data_type}'

        if error_message:
            result_dict['error_message'] = error_message

        view_list = []
        if view_chart:
            view_list.append('chart')
        if view_histogram:
            view_list.append('histogram')
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