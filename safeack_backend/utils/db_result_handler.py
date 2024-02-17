from sqlalchemy.orm.query import Query


def exclude_multiple_fields(data: dict, exclude_fields: list[str] = []) -> dict:
    """removes dict keys from the dict and returns dict"""
    exclude_fields.append('_sa_instance_state')
    for key in exclude_fields:
        data.pop(key, None)

    return data


def whitelist_multiple_fields(data: dict, fields):
    """
    Create a new dictionary with only the fields specified in the whitelist.

    Parameters:
    - original_dict: The original dictionary.
    - whitelist: A list of field names to include in the new dictionary.

    Returns:
    - A new dictionary containing only the whitelisted fields.
    """
    return {key: data[key] for key in fields if key in data}


def orm_query_response_to_dict(
    query: Query | list[Query], approach_type: str = 'whitelist', fields: list[str] = []
):
    """
    Converts orm query response to dict based on approach function and fields args.

    For whitelist approach_type, fields will be overwritten by _dict_fields_to_show from the record.
    """
    # whitelisted approach
    approach_func = whitelist_multiple_fields

    if approach_type == 'exclude':
        approach_func = exclude_multiple_fields

    results = []
    if isinstance(query, list):
        for record in query:
            fields = record._dict_fields_to_show if approach_type == 'whitelist' else fields
            results.append(approach_func(record.__dict__, fields))
    else:
        results.append(approach_func(query.dict(), fields))

    print('results:', results)
    return results
