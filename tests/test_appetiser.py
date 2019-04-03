
def test_ping(appetiser_client):
    response = appetiser_client.get('/ping')
    assert response.json == {'status': 'working'}


def test_convert_null(appetiser_client):
    post_json = {'dummy': 'data'}
    expected_response = {
        'status': 'error',
        'message': 'Unknown operation',
    }

    response = appetiser_client.post('/convert', json=post_json)
    assert response.json == expected_response


def test_convert_invalid_operation(appetiser_client):
    post_json = {
        'imageId': 'an_image_id',
        'jobId': 'a_job_id',
        'source': 'path/to/image.jpeg',
        'destination': 'path/to/image.jp2',
        'thumbDir': 'path/to/thumbnails/',
        'operation': 'an_invalid_operation',
        'optimisation': 'an_optimisation',
        'origin': 'an_origin',
    }

    expected_response = {
        'status': 'error',
        'message': 'Unknown operation',
        'imageId': 'an_image_id',
        'jobId': 'a_job_id',
        'optimisation': 'an_optimisation',
        'origin': 'an_origin',
    }

    response = appetiser_client.post('/convert', json=post_json)
    assert response.json == expected_response

def test_convert_jpg(appetiser_client, fixtures_dir, temp_dir):
    img_name = 'fol_73r_detail'
    img_src = fixtures_dir.joinpath('Ms_W_102', img_name).with_suffix('.jpg')
    img_dest = temp_dir.joinpath(img_name).with_suffix('.jp2')
    thumb_dir = temp_dir
    post_json = {
        'imageId': img_name,
        'jobId': img_name + '_job',
        'source': str(img_src),
        'destination': str(img_dest),
        'thumbSizes': [1000, 2000, 30, 600],
        'thumbDir': str(thumb_dir),
        'operation': 'ingest',
        'optimisation': 'kdu_med',
        'origin': 'an_origin',
    }

    expected_response = {
        'imageId': 'fol.73r_detail',
        'jobId': 'fol.73r_detail_job',
        'optimisation': 'an_optimisation',
        'origin': 'an_origin',
    }

    response = appetiser_client.post('/convert', json=post_json)
    print(response.json)
    print(expected_response)
    assert response.json == expected_response
