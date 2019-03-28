import pathlib
import logging

logger = logging.getLogger(__name__)


def _remap_dict_values(input_dict: dict, mappings: (tuple)) -> dict:
    """ Undertakes the mapping of a value found at `from_key` in `input_dict`
        to `to_key` in a new dictionary. If `func` is provided then that callable
        will be applied to `value` - to be used for casting to a type or sanitising
        the value.
        `to_key` will not be created in the new dict if no value is found for `from_key`
        in `input_dict`.
        `mappings` should consist of an iterable of tuples in the form:
        (from_key, to_key, func or None)
        """
    result_dict = {}
    for from_key, to_key, func in mappings:
        value = input_dict.get(from_key)
        if value:
            logger.debug('%s: has value "%s"', from_key, value)
            if func:
                logger.debug('%s: being applied to %s', func, value)
                value = func(value)
            logger.debug('%s: assigned value %s', to_key, value)
            result_dict[to_key] = value
        else:
            logger.debug('%s: not present in source dict.', from_key)
    return result_dict


def extract_process_kwargs(convert_request_json: dict) -> dict:
    """ Extracts items from the initial response and formats them into
        the kwargs required for the process function.
        """
    _mappings = (
        ('source',       'source_path',         pathlib.Path),
        ('destination',  'dest_path',           pathlib.Path),
        ('thumbDir',     'thumbnail_dir',       pathlib.Path),
        ('thumbSizes',   'thumbnail_sizes', lambda x: list(map(int, x))),
        ('optimisation', 'kakadu_optimisation', None),
        ('imageId',      'image_id',            None),
        ('operation',    'operation',           None)
    )
    logger.debug('Extracting process kwargs.')
    return _remap_dict_values(convert_request_json, _mappings)


def extract_response_items(convert_request_json: dict) -> dict:
    """ Extracts items from the initial request that are to be included
        in the response.
        """
    _mappings = (
        ('jobId',   'jobId',   None),
        ('origin',  'origin',  None),
        ('imageId', 'imageId', None),
    )
    logger.debug('Extracting request items for the response.')
    return _remap_dict_values(convert_request_json, _mappings)
