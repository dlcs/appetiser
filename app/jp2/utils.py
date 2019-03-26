import decimal
import logging

logger = logging.getLogger(__name__)


def scale_dimensions_to_fit(width: int, height: int, req_width: int, req_height: int) -> (int, int):
    """ For a given width and height, scale these such that they will fit within
        the required height and width by reducing them by an appropriate scale
        factor.
        Setting the precision of the Decimal context _may_ be included to allow
        for parity with .net components that use this precision (i.e. no off-by-one
        scaling issues).
        """
    if width <= req_width and height <= req_height:
        logger.debug('(%s, %s): Dimensions do not need scaling.')
        return width, height
    decimal.getcontext().prec = 17
    dec_width = decimal.Decimal(width)
    dec_height = decimal.Decimal(height)
    dec_req_width = decimal.Decimal(req_width)
    dec_req_height = decimal.Decimal(req_height)
    scale = min(dec_req_width/dec_width, dec_req_height/dec_height)
    logger.debug('(%s, %s): to fit within (%s, %s) requires a scale factor of %s',
                 dec_width, dec_height, dec_req_width, dec_req_height, scale)
    scaled_int_width = int((dec_width * scale).to_integral_exact())
    scaled_int_height = int((dec_height * scale).to_integral_exact())
    logger.debug('(%s, %s): scaled to (%s, %s)', dec_width,
                 dec_height, scaled_int_width, scaled_int_height)
    return scaled_int_width, scaled_int_height
