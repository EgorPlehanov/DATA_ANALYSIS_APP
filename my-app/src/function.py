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
            param_value = param_info.get('default_value')
            if isinstance(param_value, (list, dict, set)):
                param_value = copy.deepcopy(param_value)
            value_to_print = param_info.get('default_value_to_print', param_value)
            setattr(self, param_name, {'value': param_value, 'value_to_print': value_to_print})

        self._calculate()


    def get_parameter_value(self, param_name) -> Any:
        '''
        Получение значения параметра по его имени
        '''
        return getattr(self, param_name)


    def set_parameter_value(self, param_name, value, value_to_print = None) -> None:
        '''
        Установка значения параметра по его имени
        '''
        if value_to_print is None:
            value_to_print = value
        param_value = {'value': value, 'value_to_print': value_to_print}
        setattr(self, param_name, param_value)
        self._calculate()


    def get_parameters_dict(self, to_print: bool = False) -> dict:
        '''
        Возвращает словарь текущих параметраметров функции
        '''
        value_key = 'value_to_print' if to_print else 'value'
            
        parameters = {}
        for param_name in self.parameters_names:
            parameters[param_name] = self.get_parameter_value(param_name).get(value_key)
        return parameters


    def _calculate(self) -> None:
        """
        Выполняет расчет функции и возвращает результат.
        """
        # Содаем словарь параметров со значениями
        parameters = self.get_parameters_dict()
        if not parameters:
            self.result = []
        else:
            self.result = self.function(**parameters)
