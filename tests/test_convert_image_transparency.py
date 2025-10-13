from .utils import (
    convert_test_runner,
)


def test_convert_image_with_transparency(appetiser_service, fixtures_dir, output_dir):
    convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="sloth.png",
        expected_jp2_name="sloth.jp2",
        optimisation="kdu_med",
        operation="ingest",
        thumb_iiif_sizes=["!100,100", "500,", ",1000"],
        expected_thumb_sizes=[
            {
                "width": 100,
                "height": 71,
            },
            {
                "width": 500,
                "height": 353,
            },
            {
                "width": 1415,
                "height": 1000,
            },
        ],
    )
