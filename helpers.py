def get_model_fields_with_verbose_names(cls):
    """
    Return model field names with corresponding verbose names.django where to store helper function

    Return:
        field_names = {
            'field_name': 'field_verbose_name',
            'field_name2': 'field_verbose_name2',
        }
    """
    model_meta = cls._meta.get_fields()
    field_names = {}

    for field in model_meta:
        field_names[field.name] = field.verbose_name

    return field_names
