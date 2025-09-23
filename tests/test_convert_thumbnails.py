from .utils import (
    convert_test_runner,
)


def test_convert_thumbnails_height_width(appetiser_service, fixtures_dir, output_dir):
    convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="Ms_W_102/fol_73r_detail.jpg",
        expected_jp2_name=None,
        optimisation="kdu_med",
        operation="derivatives-only",
        thumb_iiif_sizes=["!1000,1000"],
        expected_thumb_sizes=[
            {
                "width": 671,
                "height": 1000,
            }
        ],
    )


def test_convert_thumbnails_width_only(appetiser_service, fixtures_dir, output_dir):
    convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="Ms_W_102/fol_73r_detail.jpg",
        expected_jp2_name=None,
        optimisation="kdu_med",
        operation="derivatives-only",
        thumb_iiif_sizes=["1000,"],
        expected_thumb_sizes=[
            {
                "width": 1000,
                "height": 1490,
            }
        ],
    )


def test_convert_thumbnails_height_only(appetiser_service, fixtures_dir, output_dir):
    convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="Ms_W_102/fol_73r_detail.jpg",
        expected_jp2_name=None,
        optimisation="kdu_med",
        operation="derivatives-only",
        thumb_iiif_sizes=[",1000"],
        expected_thumb_sizes=[
            {
                "width": 671,
                "height": 1000,
            }
        ],
    )


def test_convert_thumbnails_mix_1000(appetiser_service, fixtures_dir, output_dir):
    convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="Ms_W_102/fol_73r_detail.jpg",
        expected_jp2_name=None,
        optimisation="kdu_med",
        operation="derivatives-only",
        thumb_iiif_sizes=["!1000,1000", "1000,", ",1000"],
        expected_thumb_sizes=[
            {
                "width": 1000,
                "height": 1490,
            },
            {
                "width": 671,
                "height": 1000,
            },
        ],
    )
