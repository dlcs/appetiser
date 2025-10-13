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


def test_convert_thumbnails_empty(appetiser_service, fixtures_dir, output_dir):
    convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="Ms_W_102/fol_73r_detail.jpg",
        expected_jp2_name=None,
        optimisation="kdu_med",
        operation="derivatives-only",
        thumb_iiif_sizes=[],
        expected_thumb_sizes=[],
    )


def test_convert_thumbnails_none_feasible(appetiser_service, fixtures_dir, output_dir):
    convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="Ms_W_102/fol_73r_detail.jpg",
        expected_jp2_name=None,
        optimisation="kdu_med",
        operation="derivatives-only",
        thumb_iiif_sizes=["10000,10000", "!5000,5000", "10000,", ",10000"],
        expected_thumb_sizes=[],
    )


def test_convert_thumbnails_same_size(appetiser_service, fixtures_dir, output_dir):
    convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="Ms_W_102/fol_73r_detail.jpg",
        expected_jp2_name=None,
        optimisation="kdu_med",
        operation="derivatives-only",
        thumb_iiif_sizes=["1609,2398"],
        expected_thumb_sizes=[],
    )


def test_convert_thumbnails_marginal_larger(
    appetiser_service, fixtures_dir, output_dir
):
    convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="Ms_W_102/fol_73r_detail.jpg",
        expected_jp2_name=None,
        optimisation="kdu_med",
        operation="derivatives-only",
        thumb_iiif_sizes=["1610,2399"],
        expected_thumb_sizes=[],
    )


def test_convert_thumbnails_marginal_smaller(
    appetiser_service, fixtures_dir, output_dir
):
    convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="Ms_W_102/fol_73r_detail.jpg",
        expected_jp2_name=None,
        optimisation="kdu_med",
        operation="derivatives-only",
        thumb_iiif_sizes=["1608,2397"],
        expected_thumb_sizes=[
            {
                "width": 1608,
                "height": 2397,
            },
        ],
    )


def test_convert_thumbnails_smaller_same_height_width(
    appetiser_service, fixtures_dir, output_dir
):
    convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="Ms_W_102/fol_73r_detail.jpg",
        expected_jp2_name=None,
        optimisation="kdu_med",
        operation="derivatives-only",
        thumb_iiif_sizes=["1000,1000", "!1000,1000", "^1000,1000"],
        expected_thumb_sizes=[
            {
                "width": 1000,
                "height": 1000,
            },
            {
                "width": 671,
                "height": 1000,
            },
        ],
    )


def test_convert_thumbnails_smaller_different_height_width(
    appetiser_service, fixtures_dir, output_dir
):
    convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="Ms_W_102/fol_73r_detail.jpg",
        expected_jp2_name=None,
        optimisation="kdu_med",
        operation="derivatives-only",
        thumb_iiif_sizes=["1000,2000", "!1000,2000", "^1000,2000"],
        expected_thumb_sizes=[
            {
                "width": 1000,
                "height": 2000,
            },
            {
                "width": 1342,
                "height": 2000,
            },
        ],
    )


def test_convert_thumbnails_upscale_width_height(
    appetiser_service, fixtures_dir, output_dir
):
    convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="Ms_W_102/fol_73r_detail.jpg",
        expected_jp2_name=None,
        optimisation="kdu_med",
        operation="derivatives-only",
        thumb_iiif_sizes=["^3000,3000"],
        expected_thumb_sizes=[
            {
                "width": 3000,
                "height": 3000,
            },
        ],
    )


def test_convert_thumbnails_upscale_width(appetiser_service, fixtures_dir, output_dir):
    convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="Ms_W_102/fol_73r_detail.jpg",
        expected_jp2_name=None,
        optimisation="kdu_med",
        operation="derivatives-only",
        thumb_iiif_sizes=["^3000,"],
        expected_thumb_sizes=[
            {
                "width": 3000,
                "height": 4471,
            },
        ],
    )


def test_convert_thumbnails_upscale_height(appetiser_service, fixtures_dir, output_dir):
    convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="Ms_W_102/fol_73r_detail.jpg",
        expected_jp2_name=None,
        optimisation="kdu_med",
        operation="derivatives-only",
        thumb_iiif_sizes=["^,3000"],
        expected_thumb_sizes=[
            {
                "width": 2013,
                "height": 3000,
            },
        ],
    )
