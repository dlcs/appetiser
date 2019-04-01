import pathlib

from app.json_utils import (
    _b64_encode_json,
    _remap_dict_values,
    _get_scale_factors,
    _iiif_image_info_json,
    extract_process_kwargs,
    extract_response_items,
    add_iiif_info_json,
)


def test__b64_encode_json():
    assert b'e30=' == _b64_encode_json({})


def test__remap_dict_values():
    def plus_one(x):
        return x + 1

    initial_dict = {'a': 1, 'b': 2, 'c': 3}
    expected_dict = {'a': 2, 'y': 2, 'z': 4}
    mapping = (
        ('a', 'a', lambda x: x + 1),
        ('b', 'y', None),
        ('c', 'z', plus_one)
    )
    assert _remap_dict_values(initial_dict, mapping) == expected_dict


def test__get_scale_factors():
    scale_factors = _get_scale_factors(1, 2048)
    assert scale_factors == [1, 2, 4, 8]
    scale_factors = _get_scale_factors(2048, 1)
    assert scale_factors == [1, 2, 4, 8]
    scale_factors = _get_scale_factors(1, 2056)
    assert scale_factors == [1, 2, 4, 8, 16]


def test__iiif_image_info_json():
    expected_image_info = {
        '@context': 'http://iiif.io/api/image/2/context.json',
        '@id': 'an_identifier',
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
    image_info = _iiif_image_info_json(
        'an_identifier',
        3000,
        2056
    )
    assert expected_image_info == image_info


def test_extract_process_kwargs_none():
    request = {
        'destination': '',
        'imageId': '',
        'jobId': '',
        'operation': '',
        'optimisation': '',
        'origin': '',
        'source': '',
        'thumbDir': '',
        'thumbSizes': '',
    }
    expected_kwargs = {}
    assert extract_process_kwargs(request) == expected_kwargs
    assert extract_process_kwargs(expected_kwargs) == expected_kwargs


def test_extract_process_kwargs_paths():
    request = {
        'destination': '/path/to/image.jpeg',
        'imageId': '',
        'jobId': '',
        'operation': '',
        'optimisation': '',
        'origin': '',
        'source': '',
        'thumbDir': '/thumb/dir/',
        'thumbSizes': '',
    }
    expected_kwargs = {
        'dest_path': pathlib.Path('/path/to/image.jpeg'),
        'thumbnail_dir': pathlib.Path('/thumb/dir/')
    }
    assert extract_process_kwargs(request) == expected_kwargs


def test_extract_process_kwargs_sizes():
    request = {
        'thumbSizes': ['1', 2, '3', 4],
    }
    expected_kwargs = {
        'thumbnail_sizes': [1, 2, 3, 4]
    }
    assert extract_process_kwargs(request) == expected_kwargs


def test_extract_process_kwargs_full():
    request = {
        'destination': '/path/to/image.jp2',
        'imageId': 'an_image_id',
        'jobId': 'a_job_id',
        'operation': 'ingest',
        'optimisation': 'kdu_high',
        'origin': 'an_origin',
        'source': '/path/to/image.jpeg',
        'thumbDir': '/thumb/dir/',
        'thumbSizes': [100, 400, 800],
    }
    expected_kwargs = {
        'dest_path': pathlib.Path('/path/to/image.jp2'),
        'image_id': 'an_image_id',
        'operation': 'ingest',
        'kakadu_optimisation': 'kdu_high',
        'source_path': pathlib.Path('/path/to/image.jpeg'),
        'thumbnail_dir': pathlib.Path('/thumb/dir/'),
        'thumbnail_sizes': [100, 400, 800]
    }
    assert extract_process_kwargs(request) == expected_kwargs


def test_extract_response_items():
    request = {
        'destination': '/path/to/image.jpeg',
        'imageId': 'an_image_id',
        'jobId': 'a_job_id',
        'optimisation': 'an_optimisation',
        'origin': 'an_origin',
    }
    expected_response = {
        'imageId': 'an_image_id',
        'jobId': 'a_job_id',
        'optimisation': 'an_optimisation',
        'origin': 'an_origin',
    }
    assert extract_response_items(request) == expected_response


def test_add_iiif_info_json_null():
    response = {'imageId': 'an_identifier'}
    expected_response = {'imageId': 'an_identifier'}
    assert add_iiif_info_json(response) == expected_response


def test_add_iiif_info_json():
    response = {
        'imageId': 'an_identifier',
        'height': 300,
        'width': 400
    }
    expected_response = {
        'imageId': 'an_identifier',
        'height': 300,
        'width': 400,
        'infoJson': b'eyJAY29udGV4dCI6ICJodHRwOi8vaWlpZi5pby9hcGkvaW1hZ2UvMi9jb250ZXh0'
        b'Lmpzb24iLCAiQGlkIjogImFuX2lkZW50aWZpZXIiLCAicHJvdG9jb2wiOiAiaHR0'
        b'cDovL2lpaWYuaW8vYXBpL2ltYWdlIiwgIndpZHRoIjogNDAwLCAiaGVpZ2h0Ijog'
        b'MzAwLCAidGlsZXMiOiBbeyJ3aWR0aCI6IDI1NiwgInNjYWxlRmFjdG9ycyI6IFsx'
        b'LCAyXX1dLCAicHJvZmlsZSI6IFsiaHR0cDovL2lpaWYuaW8vYXBpL2ltYWdlLzIv'
        b'bGV2ZWwxLmpzb24iLCB7ImZvcm1hdHMiOiBbImpwZyJdLCAicXVhbGl0aWVzIjog'
        b'WyJuYXRpdmUiLCAiY29sb3IiLCAiZ3JheSJdLCAic3VwcG9ydHMiOiBbInJlZ2lv'
        b'bkJ5UGN0IiwgInNpemVCeUZvcmNlZFdoIiwgInNpemVCeVdoIiwgInNpemVBYm92'
        b'ZUZ1bGwiLCAicm90YXRpb25CeTkwcyIsICJtaXJyb3JpbmciLCAiZ3JheSJdfV19',
    }
    assert add_iiif_info_json(response) == expected_response
