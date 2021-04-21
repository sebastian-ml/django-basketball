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
    available_fields = ['verbose_name', 'help_text']
    model_meta = cls._meta.get_fields()
    fields_info = {}

    for field in model_meta:
        fields_info[field.name] = {}

        for available_field in available_fields:
            if available_field in args:
                fields_info[field.name][available_field] = getattr(field, available_field)

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


def get_stats_fields_meta(model):
    """
    Get stats fields meta information. Remove unnecesary fields.

    Return:
    field_names = {
            'field_name': {
                'verbose_name': 'field_verbose_name',
                'help_text': 'field_help_text',
            }
        }
    """
    stats_fields_meta_info = get_model_fields_meta_info(model,
                                                        'verbose_name',
                                                        'help_text')

    unnecesary_fields = ['id', 'player', 'game']
    for field_name in unnecesary_fields:
        del stats_fields_meta_info[field_name]

    return stats_fields_meta_info
