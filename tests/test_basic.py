import httpx


TEST_HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}


def test_ping(appetiser_service):
    endpoint = f"{appetiser_service}/ping"
    # Setup test params
    status = 200

    # Test JSON response
    response = httpx.get(endpoint, headers=TEST_HEADERS)
    response_json = response.json()
    assert response.status_code == status
    assert response_json == {"status": "working"}


def test_convert_null(appetiser_service):
    endpoint = f"{appetiser_service}/convert"
    # Setup test params
    status = 200
    post_json = {"dummy": "data"}
    expected_response_json = {
        "status": "error",
        "message": "Unknown operation",
    }
    # Test JSON response
    response = httpx.post(endpoint, headers=TEST_HEADERS, json=post_json)
    response_json = response.json()
    assert response.status_code == status
    assert response_json == expected_response_json


def test_convert_invalid_operation(appetiser_service):
    endpoint = f"{appetiser_service}/convert"
    # Setup test params
    status = 200
    post_json = {
        "imageId": "an_image_id",
        "jobId": "a_job_id",
        "source": "path/to/image.jpeg",
        "destination": "path/to/image.jp2",
        "thumbDir": "path/to/thumbnails/",
        "operation": "an_invalid_operation",
        "optimisation": "an_optimisation",
        "origin": "an_origin",
    }

    expected_response_json = {
        "status": "error",
        "message": "Unknown operation",
        "imageId": "an_image_id",
        "jobId": "a_job_id",
        "optimisation": "an_optimisation",
        "origin": "an_origin",
    }

    # Test JSON response
    response = httpx.post(endpoint, headers=TEST_HEADERS, json=post_json)
    response_json = response.json()
    assert response.status_code == status
    assert response_json == expected_response_json
