import pandas as pd
from typing import Any
from model import Model
import copy



class Function:
    def __init__(self, name):
        self.name = name
        self.function = Model.get_info(self.name, return_type='function')
        self.type = Model.get_info(self.name, return_type='type')
        self.parameters_info = Model.get_info(self.name, return_type='parameters')
        self.parameters_names = list(self.parameters_info.keys())

        for param_name, param_info in self.parameters_info.items():
            param_value = param_info['default_value']
            if isinstance(param_value, (list, dict, set)):
                param_value = copy.deepcopy(param_value)
            setattr(self, param_name, param_value)
        
        self._calculate()


    def get_parameter_value(self, param_name) -> Any:
        '''
        Получение значения параметра по его имени
        '''
        return getattr(self, param_name)


    def set_parameter_value(self, param_name, value) -> None:
        '''
        Установка значения параметра по его имени
        '''
        setattr(self, param_name, value)
        self._calculate()


    def get_parameters_dict(self) -> dict:
        '''
        Возвращает словарь текущих параметраметров функции
        '''
        parameters = {}
        for param_name in self.parameters_names:
            parameters[param_name] = self.get_parameter_value(param_name)
        return parameters


    def _calculate(self) -> None:
        """
        Выполняет расчет функции и возвращает результат.

        Returns:
            Any: Результат выполнения функции.
        """
        # Содаем словарь параметров со значениями
        parameters = self.get_parameters_dict()
        if not parameters:
            self.result = []
        else:
            self.result = self.function(**parameters)
