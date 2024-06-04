class Scope:
    def __init__(self, function_definition=None, source_position=None, params_values_list=None):
        self.local_variables = {}
        if function_definition:
            self.function_name = function_definition.identifier
            self.return_value_type = function_definition.return_type
        else:
            self.function_name = None
            self.return_value_type = None
        self.return_value = None

        if function_definition:
            for param, param_value in zip(function_definition.arguments, params_values_list):
                # self.local_variables[param[1].value] = (param_value[0], param_value[1])
                self.local_variables[param[1].value] = param_value

    # def check_return_value(self, value, source_position) -> bool:
    #     print(f"return_value: {self.return_value_type}")
    #     print(f"value: {value}")
    #     if self.return_value_type is None:
    #     self.return_value = value
    #     return True

    # funkcja ma contex ktory zawiera scopy
    # program ma stos contektoew