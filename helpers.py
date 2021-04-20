def get_model_fields_meta_info(cls, *args):
    """
    Return model field names with corresponding meta information like verbose_name, help_text

    Return:
        field_names = {
            'field_name': {
                'verbose_name': 'field_verbose_name',
                'help_text': 'field_help_text',
            }
        }
    """
    model_meta = cls._meta.get_fields()
    fields_info = {}

    for field in model_meta:
        if 'verbose_name' in args:
            fields_info[field.name] = {}
            fields_info[field.name]['verbose_name'] = field.verbose_name
        if 'help_text' in args:
            fields_info[field.name] = {}
            fields_info[field.name]['help_text'] = field.help_text

    return fields_info


def flatten_dict(dict, value_key):
    """
    Transform two level dict into one level dict.

    Return:
        {'field1': 'value1',}
    """
    flattened_dict = {}

    for k, v in dict.items():
        flattened_dict[k] = v[value_key]

    return flattened_dict
