import base64
import json
import logging
import typing

logger = logging.getLogger(__name__)


def _get_scale_factors(width: int, height: int, tile_size: int = 256) -> [int]:
    """ Derives a set of resolution scaling factors for an image using a
        given tile_size.
        v. https://iiif.io/api/image/2.0/#image-information
        """
    dimension = max(width, height)
    factors = [1]
    while dimension > tile_size:
        dimension //= 2
        factors.append(factors[-1] * 2)
    return factors


def _b64_encode_json(json_data: typing.Any) -> bytes:
    """ Dumps a json data structure to a string and encodes it using
        Base64.
        """
    return base64.b64encode(json.dumps(json_data).encode('utf-8'))


def iiif_image_info_json(jpeg_info_id: str, height: int, width: int, tile_size: int = 256) -> dict:
    """ Constructs a IIIF Image Information JSON response using
        v. https://iiif.io/api/image/2.0/#image-information
        """
    scale_factors = _get_scale_factors(width, height, tile_size)
    return {
        '@context': 'http://iiif.io/api/image/2/context.json',
        '@id': jpeg_info_id,
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
