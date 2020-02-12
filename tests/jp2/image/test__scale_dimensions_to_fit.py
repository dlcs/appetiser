from app.jp2.image import _scale_dimensions_to_fit


def test_scale_dimensions_to_fit_smaller():
    width = 100
    height = 200
    required = 200
    assert (width, height) == _scale_dimensions_to_fit(
        width, height, required, required
    )


def test_scale_dimensions_to_fit_half():
    width = 100
    height = 200
    required = 100
    expected_width = 50
    expected_height = 100
    assert (expected_width, expected_height) == _scale_dimensions_to_fit(
        width, height, required, required
    )


def test_scale_dimensions_to_fit_half_width():
    width = 200
    height = 100
    required = 100
    expected_width = 100
    expected_height = 50
    assert (expected_width, expected_height) == _scale_dimensions_to_fit(
        width, height, required, required
    )


def test_scale_dimensions_to_fit_third():
    width = 100
    height = 300
    required = 100
    expected_width = 33
    expected_height = 100
    assert (expected_width, expected_height) == _scale_dimensions_to_fit(
        width, height, required, required
    )


def test_scale_dimensions_to_fit_third_round_up():
    width = 101
    height = 300
    required = 100
    expected_width = 34
    expected_height = 100
    assert (expected_width, expected_height) == _scale_dimensions_to_fit(
        width, height, required, required
    )
