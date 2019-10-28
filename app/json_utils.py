import base64
import json
import logging
import pathlib
import typing

logger = logging.getLogger(__name__)


def _b64_encode_json(json_data: typing.Any) -> bytes:
    """ Dumps a json data structure to a string and encodes it using
        Base64.
        """
    logger.debug('Base64 encoding: %s', json_data)
    return base64.b64encode(json.dumps(json_data).encode('utf-8')).decode('utf-8')


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
            logger.debug('%s has value "%s"', from_key, value)
            if func:
                logger.debug('%s being applied to %s', func, value)
                value = func(value)
            logger.debug('%s assigned value %s', to_key, value)
            result_dict[to_key] = value
        else:
            logger.debug('%s not present in source dict.', from_key)
    return result_dict


def _get_scale_factors(width: int, height: int, tile_size: int = 256) -> [int]:
    """ Derives a set of resolution scaling factors for an image using a
        given tile_size.
        v. https://iiif.io/api/image/2.0/#image-information
        """
    dimension = max(width, height)
    logger.debug('Calculating scale factors tile_size %s within %s',
                 tile_size, dimension)
    factors = [1]
    while dimension > tile_size:
        dimension //= 2
        factors.append(factors[-1] * 2)
    logger.debug('Scale factors %s for tile_size %s within %s',
                 factors, tile_size, dimension)
    return factors


def _iiif_image_info_json(image_id: str, height: int, width: int, tile_size: int = 256) -> dict:
    """ Constructs a IIIF Image Information JSON response using
        v. https://iiif.io/api/image/2.0/#image-information
        """
    scale_factors = _get_scale_factors(width, height, tile_size)
    logger.debug('Generating IIIF Image Information JSON for %s (%s, %s) %s',
                 image_id, width, height, scale_factors)
    return {
        '@context': 'http://iiif.io/api/image/2/context.json',
        '@id': image_id,
        'protocol': 'http://iiif.io/api/image',
        'width': width,
        'height': height,
        'tiles': [{
            'width': tile_size,
            'scaleFactors': scale_factors
        }],
        'profile': [
            'http://iiif.io/api/image/2/level1.json',
            {
                'formats': ['jpg'],
                'qualities': ['native', 'color', 'gray'],
                'supports': [
                    'regionByPct',
                    'sizeByForcedWh',
                    'sizeByWh',
                    'sizeAboveFull',
                    'rotationBy90s',
                    'mirroring',
                    'gray'
                ]
            }
        ]
    }


def extract_process_kwargs(convert_request_json: dict) -> dict:
    """ Extracts items from the initial response and formats them into
        the kwargs required for the process function.
        """
    _mappings = (
        ('source',       'source_path',         pathlib.Path),
        ('destination',  'dest_path',           pathlib.Path),
        ('thumbDir',     'thumbnail_dir',       pathlib.Path),
        ('thumbSizes',   'thumbnail_sizes', lambda x: list(map(int, x))),
        ('optimisation', 'optimisation', None),
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
        ('jobId',        'jobId',        None),
        ('origin',       'origin',       None),
        ('optimisation', 'optimisation', None),
        ('imageId',      'imageId',      None),
    )
    logger.debug('Extracting request items for inclusion the response.')
    return _remap_dict_values(convert_request_json, _mappings)


def add_iiif_info_json(response: dict) -> dict:
    """ Adds the IIIF Image Information to the response if there
        is sufficient information to construct it.
        """
    iiif_image_info_json_args = [
        response.get('imageId'),
        response.get('height'),
        response.get('width')
    ]
    if all(iiif_image_info_json_args):
        logger.debug('%s: all args present to generate IIIF info json',
                     iiif_image_info_json_args[0])
        response['infoJson'] = _b64_encode_json(
            _iiif_image_info_json(*iiif_image_info_json_args)
        )
    return response
