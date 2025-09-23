import httpx
from PIL import (
    Image,
)


def is_responsive_404(url):
    """
    Hit a non existing url, expect a 404.  Used to check the service is up as a fixture.
    :param url:
    :return:
    """
    try:
        response = httpx.get(url)
        if response.status_code == 404:
            return True
    except httpx.RequestError:
        return False


TEST_HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}


def convert_test_runner(
    appetiser_service,
    output_dir,
    fixtures_dir,
    img_path,
    expected_jp2_name,
    optimisation,
    operation,
    thumb_iiif_sizes,
    expected_thumb_sizes,
):

    endpoint = f"{appetiser_service}/convert"
    # Setup test params
    status = 200

    img_src = fixtures_dir.container_path / img_path
    img_dest = None
    if expected_jp2_name:
        img_dest = output_dir.container_path / expected_jp2_name

    thumb_dir = output_dir.container_path

    post_json = {
        "imageId": f"{img_src.name}",
        "jobId": f"{img_src.stem}_job",
        "origin": f"{img_src.stem}_origin",
        "source": f"{img_src}",
        "operation": operation,
        "optimisation": optimisation,
    }
    if thumb_iiif_sizes:
        post_json["thumbIIIFSizes"] = thumb_iiif_sizes

        post_json["thumbDir"] = f"{thumb_dir}"
    if img_dest:
        post_json["destination"] = str(img_dest)
    orig_img_src = fixtures_dir.host_path / img_path
    orig_image = Image.open(orig_img_src)

    expected_response_json = {
        "imageId": f"{img_src.name}",
        "jobId": f"{img_src.stem}_job",
        "origin": f"{img_src.stem}_origin",
        "height": orig_image.height,
        "width": orig_image.width,
    }
    if img_dest:
        expected_response_json["jp2"] = str(img_dest)
    # Test JSON response
    response = httpx.post(endpoint, headers=TEST_HEADERS, json=post_json)
    response_json = response.json()
    assert response.status_code == status
    for key, expected_value in expected_response_json.items():
        assert response_json[key] == expected_value
    if thumb_iiif_sizes and expected_thumb_sizes:
        for response_thumb_info, expected_thumb_size in zip(
            sorted(response_json["thumbs"], key=lambda x: x["width"]),
            sorted(expected_thumb_sizes, key=lambda x: x["width"]),
        ):
            expected_width = expected_thumb_size["width"]
            expected_height = expected_thumb_size["height"]
            assert response_thumb_info["path"] == str(
                thumb_dir / f"{img_src.stem}_{expected_width}_{expected_height}.jpg"
            )
            assert response_thumb_info["width"] == expected_width
            assert response_thumb_info["height"] == expected_height
    else:
        assert response_json.get("thumbs") == []
