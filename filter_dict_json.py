def filter_dict(data: dict, extract):
    try:
        if isinstance(extract, list):
            while extract:
                if result := filter_dict(data, extract.pop(0)):
                    return result
        shadow_data = data.copy()
        for key in extract.split('.'):
            if str(key).isnumeric():
                key = int(key)
            shadow_data = shadow_data[key]
        return shadow_data
    except (IndexError, KeyError, AttributeError, TypeError):
        return None