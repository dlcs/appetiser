from .utils import (
    convert_test_runner,
)


def test_convert_ingest_kdu_low(appetiser_service, fixtures_dir, output_dir):
    convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="Ms_W_102/fol_73r_detail.jpg",
        expected_jp2_name="fol_73r_detail.jp2",
        optimisation="kdu_low",
        operation="ingest",
        thumb_iiif_sizes=["!1000,1000"],
        expected_thumb_sizes=[
            {
                "width": 671,
                "height": 1000,
            }
        ],
    )


def test_convert_ingest_kdu_med(appetiser_service, fixtures_dir, output_dir):
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


def test_convert_ingest_kdu_med_layers(appetiser_service, fixtures_dir, output_dir):
    convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="Ms_W_102/fol_73r_detail.jpg",
        expected_jp2_name="fol_73r_detail.jp2",
        optimisation="kdu_med_layers",
        operation="ingest",
        thumb_iiif_sizes=["!1000,1000"],
        expected_thumb_sizes=[
            {
                "width": 671,
                "height": 1000,
            }
        ],
    )


def test_convert_ingest_kdu_high(appetiser_service, fixtures_dir, output_dir):
    convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="Ms_W_102/fol_73r_detail.jpg",
        expected_jp2_name="fol_73r_detail.jp2",
        optimisation="kdu_high",
        operation="ingest",
        thumb_iiif_sizes=["!1000,1000"],
        expected_thumb_sizes=[
            {
                "width": 671,
                "height": 1000,
            }
        ],
    )


def test_convert_ingest_kdu_max(appetiser_service, fixtures_dir, output_dir):
    convert_test_runner(
        appetiser_service=appetiser_service,
        output_dir=output_dir,
        fixtures_dir=fixtures_dir,
        img_path="Ms_W_102/fol_73r_detail.jpg",
        expected_jp2_name="fol_73r_detail.jp2",
        optimisation="kdu_max",
        operation="ingest",
        thumb_iiif_sizes=["!1000,1000"],
        expected_thumb_sizes=[
            {
                "width": 671,
                "height": 1000,
            }
        ],
    )
