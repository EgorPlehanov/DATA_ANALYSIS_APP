from typing import Any
from model import Model



class Function:
    def __init__(self, name):
        self.name = name
        self.function = Model.get_info(self.name, return_type='function')
        self.parameters_info = Model.get_info(self.name, return_type='parameters')
        self.parameters_names = list(self.parameters_info.keys())

        for param_name, param_info in self.parameters_info.items():
            setattr(self, param_name, param_info['default_value'])

        self.result = self.calculate()


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
        self.calculate()


    def get_parameters_dict(self) -> dict:
        '''
        Возвращает словарь текущих параметраметров функции
        '''
        parameters = {}
        for param_name in self.parameters_names:
            parameters[param_name] = self.get_parameter_value(param_name)
        return parameters


    def calculate(self) -> Any:
        """
        Выполняет расчет функции и возвращает результат.

        Returns:
            Any: Результат выполнения функции.
        """
        # Содаем словарь параметров со значениями
        parameters = self.get_parameters_dict()

        self.result = self.function(**parameters)
        # Вызоваем функцию function с полученными параметрами и возвращаем результат
        return self.result
