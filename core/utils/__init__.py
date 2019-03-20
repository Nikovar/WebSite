from collections import OrderedDict as od


def dict_merge(old_dict, new_dict):
    for key, new_attrs in new_dict.items():
        attr = old_dict.get(key, {})
        attr.update(new_attrs)
        old_dict[key] = attr
    return old_dict


def error_packer(errors):
    # wtf, yea! x)
    wtf_list = [err['message'] for err_list in errors.get_json_data().values() for err in err_list if 'message' in err]
    d = od.fromkeys(wtf_list)
    d.pop('', None)  # because of the blank lines in 'translated_error_messages' (in fields definitions)
    return list(d.keys())
