from .utils import (
    convert_test_runner,
)


def test_convert_derivatives_only_jpg(appetiser_service, fixtures_dir, output_dir):
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


def test_convert_derivatives_only_tiff(appetiser_service, fixtures_dir, output_dir):
    convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="Ms_W_102/fol_73v_detail.tiff",
        expected_jp2_name=None,
        optimisation="kdu_med",
        operation="derivatives-only",
        thumb_iiif_sizes=["!1000,1000"],
        expected_thumb_sizes=[
            {
                "width": 567,
                "height": 1000,
            }
        ],
    )


def test_convert_derivatives_only_bmp(appetiser_service, fixtures_dir, output_dir):
    convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="Ms_W_102/fol_74r_detail.bmp",
        expected_jp2_name=None,
        optimisation="kdu_med",
        operation="derivatives-only",
        thumb_iiif_sizes=["!1000,1000"],
        expected_thumb_sizes=[
            {
                "width": 707,
                "height": 1000,
            }
        ],
    )


def test_convert_derivatives_only_png(appetiser_service, fixtures_dir, output_dir):
    convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="Ms_W_102/fol_78v_detail.png",
        expected_jp2_name=None,
        optimisation="kdu_med",
        operation="derivatives-only",
        thumb_iiif_sizes=["!1000,1000"],
        expected_thumb_sizes=[
            {
                "width": 795,
                "height": 1000,
            }
        ],
    )
