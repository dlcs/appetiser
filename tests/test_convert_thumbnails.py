import httpx
from PIL import (
    Image,
)


TEST_HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}


def _convert_test_runner(
    appetiser_service, output_dir, fixtures_dir, img_path, optimisation, thumb_sizes
):

    endpoint = f"{appetiser_service}/convert"
    # Setup test params
    status = 200

    img_src = fixtures_dir.container_path / img_path

    img_dest = output_dir.container_path / img_src.with_suffix(".jp2").name
    post_json = {
        "imageId": f"{img_src.name}",
        "jobId": f"{img_src.stem}_job",
        "origin": f"{img_src.stem}_origin",
        "source": f"{img_src}",
        "destination": f"{img_dest}",
        "thumbSizes": thumb_sizes,
        "thumbDir": f"{output_dir.container_path}",
        "operation": "ingest",
        "optimisation": optimisation,
    }
    orig_img_src = fixtures_dir.host_path / img_path
    orig_image = Image.open(orig_img_src)

    expected_response_json = {
        "imageId": f"{img_src.name}",
        "jobId": f"{img_src.stem}_job",
        "origin": f"{img_src.stem}_origin",
        "jp2": f"{img_dest}",
        "height": orig_image.height,
        "width": orig_image.width,
    }
    # Test JSON response
    response = httpx.post(endpoint, headers=TEST_HEADERS, json=post_json)
    response_json = response.json()

    print(response_json)
    assert response.status_code == status

    for key, expected_value in expected_response_json.items():
        assert response_json[key] == expected_value
    if thumb_sizes:
        for size, thumb_dict in zip(
            sorted(thumb_sizes),
            sorted(response_json["thumbs"], key=lambda x: max(x["height"], x["width"])),
        ):
            assert size == max(thumb_dict["height"], thumb_dict["width"])
            assert (
                thumb_dict["path"]
                == f"{output_dir.container_path}/{img_src.stem}_{size}.jpg"
            )
    else:
        assert response.json["thumbs"] == []


def test_convert_jpg(appetiser_service, fixtures_dir, output_dir):
    _convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="Ms_W_102/fol_73r_detail.jpg",
        optimisation="kdu_med",
        thumb_sizes=[30, 600, 400, 100],
    )


def test_convert_tiff(appetiser_service, fixtures_dir, output_dir):
    _convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="Ms_W_102/fol_73v_detail.tiff",
        optimisation="kdu_med",
        thumb_sizes=[30, 600, 400, 100],
    )


def test_convert_bmp(appetiser_service, fixtures_dir, output_dir):
    _convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="Ms_W_102/fol_74r_detail.bmp",
        optimisation="kdu_med",
        thumb_sizes=[30, 600, 400, 100],
    )


def test_convert_pbm(appetiser_service, fixtures_dir, output_dir):
    _convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="Ms_W_102/fol_74v_detail.pbm",
        optimisation="kdu_med",
        thumb_sizes=[30, 600, 400, 100],
    )


def test_convert_pgm(appetiser_service, fixtures_dir, output_dir):
    _convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="Ms_W_102/fol_75r_detail.pgm",
        optimisation="kdu_med",
        thumb_sizes=[30, 600, 400, 100],
    )


def test_convert_ppm(appetiser_service, fixtures_dir, output_dir):
    _convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="Ms_W_102/fol_75v_detail.ppm",
        optimisation="kdu_med",
        thumb_sizes=[30, 600, 400, 100],
    )


def test_convert_rgb(appetiser_service, fixtures_dir, output_dir):
    _convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="Ms_W_102/fol_77v_detail.rgb",
        optimisation="kdu_med",
        thumb_sizes=[30, 600, 400, 100],
    )


def test_convert_png(appetiser_service, fixtures_dir, output_dir):
    _convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="Ms_W_102/fol_78v_detail.png",
        optimisation="kdu_med",
        thumb_sizes=[30, 600, 400, 100],
    )


def test_convert_rgba(appetiser_service, fixtures_dir, output_dir):
    _convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="Ms_W_102/fol_79v_detail.rgba",
        optimisation="kdu_med",
        thumb_sizes=[30, 600, 400, 100],
    )
