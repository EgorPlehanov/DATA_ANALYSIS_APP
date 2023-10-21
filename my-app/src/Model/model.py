from .settings.data_settings import functions_info as data_functions_info
from .settings.edit_settings import functions_info as edit_functions_info
from .settings.analytic_settings import functions_info as analytic_functions_info



class Model:
    functions_info = {
        'data': data_functions_info,
        'edit': edit_functions_info,
        'analytic': analytic_functions_info
    }

    @staticmethod
    def get_info(name, return_type='all') -> dict:
        for info_dict in Model.functions_info.values():
            if name in info_dict:
                info = info_dict[name]
                return info.get(return_type, info) if return_type != 'all' else info
        return None
    
    @staticmethod
    def get_functions_by_type(type):
        data_functions = []
        for key, info in Model.functions_info.get(type, {}).items():
            data_functions.append({'key': key, 'name': info.get('name', key)})
        return data_functions
   