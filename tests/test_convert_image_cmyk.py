from .utils import (
    convert_test_runner,
)


def test_convert_cmyk_image(appetiser_service, fixtures_dir, output_dir):
    convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="10_02_18.jpg",
        expected_jp2_name="10_02_18.jp2",
        optimisation="kdu_med",
        operation="image-only",
        thumb_iiif_sizes=None,
        expected_thumb_sizes=None,
    )
