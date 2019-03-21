from collections import OrderedDict as od


def kwargs_merge(kwargs, another_kwargs):
    for key, args in another_kwargs.items():
        new_args = kwargs.get(key, {})
        new_args.update(args)
        kwargs[key] = new_args
    return kwargs


def error_packer(errors):
    all_errors_list = []
    for err_list in errors.get_json_data().values():
        for err in err_list:
            if 'message' in err:
                all_errors_list.append(err['message'])
    d = od.fromkeys(all_errors_list)  # this is for uniqueness and saving old order
    d.pop('', None)  # because of the blank lines in 'translated_error_messages' (in fields definitions)
    return list(d.keys())
