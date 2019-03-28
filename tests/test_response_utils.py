from app.response_utils import (
    _get_scale_factors,
    iiif_image_info_json,
    b64_encode_json
)


def test_get_scale_factors():
    scale_factors = _get_scale_factors(1, 2048)
    assert scale_factors == [1, 2, 4, 8]
    scale_factors = _get_scale_factors(2048, 1)
    assert scale_factors == [1, 2, 4, 8]
    scale_factors = _get_scale_factors(1, 2056)
    assert scale_factors == [1, 2, 4, 8, 16]


def test_iiif_image_info_json():
    expected_image_info = {
        '@context': 'http://iiif.io/api/image/2/context.json',
        '@id': 'some_identifier',
        'protocol': 'http://iiif.io/api/image',
        'width': 2056,
        'height': 3000,
        'tiles': [{
            'width': 256,
            'scaleFactors': [1, 2, 4, 8, 16]
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
    image_info = iiif_image_info_json(
        'some_identifier',
        3000,
        2056
    )
    assert expected_image_info == image_info


def test_b64_encode_json():
    assert b'e30=' == b64_encode_json({})
