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


def test_convert_empty_body(appetiser_service):
    endpoint = f"{appetiser_service}/convert"
    # Setup test params
    status = 422
    post_json = {}
    expected_response_json = {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "jobId"],
                "msg": "Field required",
                "input": {},
            },
            {
                "type": "missing",
                "loc": ["body", "imageId"],
                "msg": "Field required",
                "input": {},
            },
            {
                "type": "missing",
                "loc": ["body", "origin"],
                "msg": "Field required",
                "input": {},
            },
            {
                "type": "missing",
                "loc": ["body", "source"],
                "msg": "Field required",
                "input": {},
            },
            {
                "type": "missing",
                "loc": ["body", "operation"],
                "msg": "Field required",
                "input": {},
            },
        ]
    }
    # Test JSON response
    response = httpx.post(endpoint, headers=TEST_HEADERS, json=post_json)
    response_json = response.json()
    assert response.status_code == status
    assert response_json == expected_response_json


def test_convert_invalid_operation(appetiser_service, fixtures_dir):
    endpoint = f"{appetiser_service}/convert"
    # Setup test params
    status = 422
    post_json = {
        "imageId": "an_image_id",
        "jobId": "a_job_id",
        "origin": "an_origin",
        "source": str(fixtures_dir.container_path / "Ms_W_102/fol_73r_detail.jpg"),
        "operation": "fake_operation",
    }

    expected_response_json = {
        "detail": [
            {
                "type": "enum",
                "loc": ["body", "operation"],
                "msg": "Input should be 'ingest', 'image-only' or 'derivatives-only'",
                "input": "fake_operation",
                "ctx": {"expected": "'ingest', 'image-only' or 'derivatives-only'"},
            },
        ]
    }

    # Test JSON response
    response = httpx.post(endpoint, headers=TEST_HEADERS, json=post_json)
    response_json = response.json()
    assert response.status_code == status
    assert response_json == expected_response_json


def test_convert_invalid_optimisation(appetiser_service, fixtures_dir):
    endpoint = f"{appetiser_service}/convert"
    # Setup test params
    status = 422
    post_json = {
        "imageId": "an_image_id",
        "jobId": "a_job_id",
        "origin": "an_origin",
        "source": str(fixtures_dir.container_path / "Ms_W_102/fol_73r_detail.jpg"),
        "operation": "ingest",
        "optimisation": "kdu_fake",
    }

    expected_response_json = {
        "detail": [
            {
                "type": "enum",
                "loc": ["body", "optimisation"],
                "msg": "Input should be 'kdu_low', 'kdu_med', 'kdu_med_layers', 'kdu_high' or 'kdu_max'",
                "input": "kdu_fake",
                "ctx": {
                    "expected": "'kdu_low', 'kdu_med', 'kdu_med_layers', 'kdu_high' or 'kdu_max'"
                },
            }
        ]
    }

    # Test JSON response
    response = httpx.post(endpoint, headers=TEST_HEADERS, json=post_json)
    response_json = response.json()
    assert response.status_code == status
    assert response_json == expected_response_json


def test_convert_non_existant_source(appetiser_service, fixtures_dir):
    endpoint = f"{appetiser_service}/convert"
    # Setup test params
    status = 422
    post_json = {
        "imageId": "an_image_id",
        "jobId": "a_job_id",
        "origin": "an_origin",
        "source": str(fixtures_dir.container_path / "non_existant.jpg"),
        "operation": "ingest",
        "optimisation": "kdu_med",
    }

    expected_response_json = {
        "detail": [
            {
                "type": "path_not_file",
                "loc": ["body", "source"],
                "msg": "Path does not point to a file",
                "input": "/test_fixtures/non_existant.jpg",
            },
        ]
    }
    # Test JSON response
    response = httpx.post(endpoint, headers=TEST_HEADERS, json=post_json)
    response_json = response.json()
    assert response.status_code == status
    assert response_json == expected_response_json


def test_convert_non_existant_thumdir(appetiser_service, fixtures_dir):
    endpoint = f"{appetiser_service}/convert"
    # Setup test params
    status = 422
    post_json = {
        "imageId": "an_image_id",
        "jobId": "a_job_id",
        "origin": "an_origin",
        "source": str(fixtures_dir.container_path / "Ms_W_102/fol_73r_detail.jpg"),
        "thumbDir": str(fixtures_dir.container_path / "non_existant_thumbnails_dir/"),
        "operation": "ingest",
        "optimisation": "kdu_med",
    }

    expected_response_json = {
        "detail": [
            {
                "type": "path_not_directory",
                "loc": ["body", "thumbDir"],
                "msg": "Path does not point to a directory",
                "input": "/test_fixtures/non_existant_thumbnails_dir",
            },
        ]
    }
    # Test JSON response
    response = httpx.post(endpoint, headers=TEST_HEADERS, json=post_json)
    response_json = response.json()
    assert response.status_code == status
    assert response_json == expected_response_json
