import app.jp2.processors

def test__parse_processor_name():
    kdu_optimisations = [
            'kdu_low',
            'kdu_med',
            'kdu_med_layers',
            'kdu_high',
            'kdu_max',
            ]
    openjpeg_optimisations = [
            'openjpeg_low',
            'openjpeg_med',
            'openjpeg_high',
            ]

    for optimisation in kdu_optimisations:
        assert app.jp2.processors._parse_processor_name(optimisation) == 'kdu'
    for optimisation in openjpeg_optimisations:
        assert app.jp2.processors._parse_processor_name(optimisation) == 'openjpeg'
