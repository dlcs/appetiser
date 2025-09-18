from .utils import (
    convert_test_runner,
)


def test_convert_image_only_jpg(appetiser_service, fixtures_dir, output_dir):
    convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="Ms_W_102/fol_73r_detail.jpg",
        expected_jp2_name="fol_73r_detail.jp2",
        optimisation="kdu_med",
        operation="image-only",
        thumb_iiif_sizes=None,
        expected_thumb_sizes=None,
    )


def test_convert_image_only_tiff(appetiser_service, fixtures_dir, output_dir):
    convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="Ms_W_102/fol_73v_detail.tiff",
        expected_jp2_name="fol_73v_detail.jp2",
        optimisation="kdu_med",
        operation="image-only",
        thumb_iiif_sizes=None,
        expected_thumb_sizes=None,
    )


def test_convert_image_only_bmp(appetiser_service, fixtures_dir, output_dir):
    convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="Ms_W_102/fol_74r_detail.bmp",
        expected_jp2_name="fol_74r_detail.jp2",
        optimisation="kdu_med",
        operation="image-only",
        thumb_iiif_sizes=None,
        expected_thumb_sizes=None,
    )


def test_convert_image_only_png(appetiser_service, fixtures_dir, output_dir):
    convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="Ms_W_102/fol_78v_detail.png",
        expected_jp2_name="fol_78v_detail.jp2",
        optimisation="kdu_med",
        operation="image-only",
        thumb_iiif_sizes=None,
        expected_thumb_sizes=None,
    )
