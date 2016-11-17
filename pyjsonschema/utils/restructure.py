import json
import re

def _nestify_helper(sub_schema, full_schema, new_dict, key_path, refs):
    for key, value in sub_schema.items():
        key_path += '/' + key
        if isinstance(value, dict) and '$ref' in value:
            ref_schema, ref_path = _resolve_refs(full_schema, value['$ref'])
            refs.append(ref_path)
            value = dict(value, **ref_schema)
            del value['$ref']

        if isinstance(value, dict) and key_path not in refs:
            new_dict[key] = {}
            _nestify_helper(value, full_schema, new_dict[key], key_path, refs)

        elif key_path not in refs:
            new_dict[key] = value
        key_path = key_path[:key_path.rstrip('/').rfind('/')]
    return new_dict


def _resolve_refs(schema, pointer):
    # ref_schema = return schema pointed to by $ref

    pointer = pointer.lstrip(u"#").lstrip(u"/")
    pointer = '/' + pointer

    return ref_schema, str(pointer)


def nestify(schema):
    return _nestify_helper(schema, schema, {}, '', [])






