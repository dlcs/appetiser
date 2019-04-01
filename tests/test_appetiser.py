
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
