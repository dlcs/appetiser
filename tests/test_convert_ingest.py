from .utils import (
    convert_test_runner,
)


def test_convert_ingest_jpg(appetiser_service, fixtures_dir, output_dir):
    convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="Ms_W_102/fol_73r_detail.jpg",
        expected_jp2_name="fol_73r_detail.jp2",
        optimisation="kdu_med",
        operation="ingest",
        thumb_iiif_sizes=["!1000,1000"],
        expected_thumb_sizes=[
            {
                "width": 671,
                "height": 1000,
            }
        ],
    )


def test_convert_ingest_tiff(appetiser_service, fixtures_dir, output_dir):
    convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="Ms_W_102/fol_73v_detail.tiff",
        expected_jp2_name="fol_73v_detail.jp2",
        optimisation="kdu_med",
        operation="ingest",
        thumb_iiif_sizes=["!1000,1000"],
        expected_thumb_sizes=[
            {
                "width": 567,
                "height": 1000,
            }
        ],
    )


def test_convert_ingest_bmp(appetiser_service, fixtures_dir, output_dir):
    convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="Ms_W_102/fol_74r_detail.bmp",
        expected_jp2_name="fol_74r_detail.jp2",
        optimisation="kdu_med",
        operation="ingest",
        thumb_iiif_sizes=["!1000,1000"],
        expected_thumb_sizes=[
            {
                "width": 707,
                "height": 1000,
            }
        ],
    )


def test_convert_ingest_png(appetiser_service, fixtures_dir, output_dir):
    convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="Ms_W_102/fol_78v_detail.png",
        expected_jp2_name="fol_78v_detail.jp2",
        optimisation="kdu_med",
        operation="ingest",
        thumb_iiif_sizes=["!1000,1000"],
        expected_thumb_sizes=[
            {
                "width": 795,
                "height": 1000,
            }
        ],
    )


def test_convert_ingest_landscape_img(appetiser_service, fixtures_dir, output_dir):
    convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="1280_752_landscape.jpg",
        expected_jp2_name="1280_752_landscape.jp2",
        optimisation="kdu_med",
        operation="ingest",
        thumb_iiif_sizes=[
            "!100,100",
            "!200,200",
            "!400,400",
            "!1024,1024",
            "!1064,1064",
        ],
        expected_thumb_sizes=[
            {
                "width": 1064,
                "height": 625,
            },
            {
                "width": 1024,
                "height": 602,
            },
            {
                "width": 400,
                "height": 235,
            },
            {
                "width": 200,
                "height": 118,
            },
            {
                "width": 100,
                "height": 59,
            },
        ],
    )
