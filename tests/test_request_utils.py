import pathlib

from app.request_utils import (
    extract_process_kwargs,
    extract_response_items
)


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
        'origin': 'an_origin',
    }
    expected_response = {
        'imageId': 'an_image_id',
        'jobId': 'a_job_id',
        'origin': 'an_origin',
    }
    assert extract_response_items(request) == expected_response
