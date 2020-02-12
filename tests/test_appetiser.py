from PIL import Image


def test_ping(appetiser_client):
    response = appetiser_client.get("/ping")
    assert response.json == {"status": "working"}


def test_convert_null(appetiser_client):
    post_json = {"dummy": "data"}
    expected_response = {
        "status": "error",
        "message": "Unknown operation",
    }

    response = appetiser_client.post("/convert", json=post_json)
    assert response.json == expected_response


def test_convert_invalid_operation(appetiser_client):
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

    expected_response = {
        "status": "error",
        "message": "Unknown operation",
        "imageId": "an_image_id",
        "jobId": "a_job_id",
        "optimisation": "an_optimisation",
        "origin": "an_origin",
    }

    response = appetiser_client.post("/convert", json=post_json)
    assert response.json == expected_response


def test_convert_no_operation(appetiser_client):
    post_json = {
        "imageId": "an_image_id",
        "jobId": "a_job_id",
        "source": "path/to/image.jpeg",
        "destination": "path/to/image.jp2",
        "thumbDir": "path/to/thumbnails/",
        "optimisation": "an_optimisation",
        "origin": "an_origin",
    }

    expected_response = {
        "status": "error",
        "message": "Unknown operation",
        "imageId": "an_image_id",
        "jobId": "a_job_id",
        "optimisation": "an_optimisation",
        "origin": "an_origin",
    }

    response = appetiser_client.post("/convert", json=post_json)
    assert response.json == expected_response


def _convert_test_runner(
    appetiser_client, temp_dir, img_src, optimisation, thumb_sizes
):
    img_name = img_src.stem
    img_dest = temp_dir.joinpath(img_name).with_suffix(".jp2")
    thumb_dir = temp_dir
    post_json = {
        "imageId": img_name,
        "jobId": img_name + "_job",
        "source": str(img_src),
        "destination": str(img_dest),
        "thumbSizes": thumb_sizes,
        "thumbDir": str(thumb_dir),
        "operation": "ingest",
        "optimisation": optimisation,
        "origin": img_name + "_origin",
    }
    orig_image = Image.open(img_src)
    response = appetiser_client.post("/convert", json=post_json)
    print(response.json)
    assert response.json["imageId"] == img_name
    assert response.json["jobId"] == img_name + "_job"
    assert response.json["origin"] == img_name + "_origin"
    assert response.json["jp2"] == str(img_dest)
    assert response.json["height"] == orig_image.height
    assert response.json["width"] == orig_image.width
    if thumb_sizes:
        for size, thumb_dict in zip(
            sorted(thumb_sizes),
            sorted(response.json["thumbs"], key=lambda x: max(x["height"], x["width"])),
        ):
            assert size == max(thumb_dict["height"], thumb_dict["width"])
            assert (
                str(
                    thumb_dir.joinpath("{}_{}".format(img_name, size)).with_suffix(
                        ".jpg"
                    )
                )
                == thumb_dict["path"]
            )
    else:
        assert response.json["thumbs"] == []


def test_convert_jpg(appetiser_client, fixtures_dir, temp_dir):
    _convert_test_runner(
        appetiser_client,
        temp_dir,
        fixtures_dir.joinpath("Ms_W_102/fol_73r_detail.jpg"),
        "kdu_med",
        [30, 600, 400, 100],
    )


def test_convert_tiff(appetiser_client, fixtures_dir, temp_dir):
    _convert_test_runner(
        appetiser_client,
        temp_dir,
        fixtures_dir.joinpath("Ms_W_102/fol_73v_detail.tiff"),
        "kdu_med",
        [30, 600, 400, 100],
    )


def test_convert_bmp(appetiser_client, fixtures_dir, temp_dir):
    _convert_test_runner(
        appetiser_client,
        temp_dir,
        fixtures_dir.joinpath("Ms_W_102/fol_74r_detail.bmp"),
        "kdu_med",
        [30, 600, 400, 100],
    )


def test_convert_pbm(appetiser_client, fixtures_dir, temp_dir):
    _convert_test_runner(
        appetiser_client,
        temp_dir,
        fixtures_dir.joinpath("Ms_W_102/fol_74v_detail.pbm"),
        "kdu_med",
        [30, 600, 400, 100],
    )


def test_convert_pgm(appetiser_client, fixtures_dir, temp_dir):
    _convert_test_runner(
        appetiser_client,
        temp_dir,
        fixtures_dir.joinpath("Ms_W_102/fol_75r_detail.pgm"),
        "kdu_med",
        [30, 600, 400, 100],
    )


def test_convert_ppm(appetiser_client, fixtures_dir, temp_dir):
    _convert_test_runner(
        appetiser_client,
        temp_dir,
        fixtures_dir.joinpath("Ms_W_102/fol_75v_detail.ppm"),
        "kdu_med",
        [30, 600, 400, 100],
    )
