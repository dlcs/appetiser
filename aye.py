from PIL import Image
from app.jp2.image import _correct_img_orientation
import logging
import sys
import os

log = logging.getLogger()
log.setLevel(logging.DEBUG)
stream = logging.StreamHandler(sys.stdout)
stream.setLevel(logging.DEBUG)
log.addHandler(stream)
src_dir = '/home/fmcc/Code/fmcc/exif-samples/jpg/orientation'
dest_dir = '/home/fmcc/naw/'


for f in os.listdir(src_dir):
    src = os.path.join(src_dir, f)
    dest = os.path.join(dest_dir, f)
    im = Image.open(src)
    _correct_img_orientation(im)
    im.save(os.path.join(dest_dir, f))
