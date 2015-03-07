"""
Sample Python library for working with the Landsat data from EROS/USGS.
"""
import glob
import os
import os.path
import tempfile

import typecheck

import numpy as np
import matplotlib as mpl
if  os.environ.get("EROS_SCENE_ID") == "true":
    mpl.use("Agg")
import matplotlib.pyplot as plt

from skimage import io, exposure
import skimage as ski

import boto
from boto import s3


BAND_COASTAL_AEROSOL = 1
BAND_BLUE = 2
BAND_GREEN = 3
BAND_RED = 4
BAND_NEAR_IR = 5
BAND_SW_IR_1 = 6
BAND_SW_IR_2 = 7
BAND_PANCHROM = 8
BAND_CIRRUS = 9
BAND_LW_IR_1 = 10
BAND_LW_IR_2 = 11


bucket_name = os.environ.get("S3_BUCKET_NAME")
scene_id = os.environ.get("EROS_SCENE_ID")
s3_path = os.environ.get("S3_PATH")
s3_title = os.environ.get("S3_IMAGE_TITLE")
s3_filename = os.environ.get("S3_IMAGE_FILENAME")
s3_image_type = os.environ.get("S3_IMAGE_TYPE", "").lower()
access_key = os.environ.get("AWS_ACCESS_KEY_ID")
secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")


def inclusive(min, max):
    return lambda x: x in range(min, max + 1)


@typecheck.typecheck
def read_band(path, scene_id, n: inclusive(1, 11)):
    """Load Landsat 8 band

    Input: path - full path to the scene data directory
           scene_id - Landsat scene ID
           n - integer in the range 1-11
    Output: img - 2D array of uint16 type"""
    ext = ".TIF"
    band_name = "_B" + str(n) + ext
    if path.startswith("http"):
        filename = os.path.join(path, scene_id + band_name)
    else:
        filename = os.path.join(path, scene_id, scene_id + band_name)
    return ski.io.imread(filename)


def extract_rgb(path, scene_id):
    red = read_band(path, scene_id, BAND_RED)
    green = read_band(path, scene_id, BAND_GREEN)
    blue = read_band(path, scene_id, BAND_BLUE)
    return np.dstack((red, green, blue))


def extract_swir2nirg(path, scene_id):
    red = read_band(path, scene_id, BAND_SW_IR_2)
    green = read_band(path, scene_id, BAND_NEAR_IR)
    blue = read_band(path, scene_id, BAND_GREEN)
    return np.dstack((red, green, blue))


def show_image(img, title="", filename="", **kwargs):
    """Show image

    Input: img - 3D array of uint16 type
    title - string"""
    fig = plt.figure(**kwargs)
    fig.set_facecolor('white')
    plt.imshow(img / 65535)
    plt.title(title)
    if filename:
        plt.savefig(filename)
    else:
        plt.show()


def show_color_hist(rgb_image, xlim=None, ylim=None, **kwargs):
    (fig, axes) = plt.subplots(**kwargs)
    fig.set_facecolor('white')
    for color, channel in zip('rgb', np.rollaxis(rgb_image, axis=-1)):
        counts, centers = ski.exposure.histogram(channel)
        plt.plot(centers[1::], counts[1::], color=color)
    if xlim:
        axes.set_xlim(xlim)
    if ylim:
        axes.set_ylim(ylim)
    plt.show()


def update_image(image, r_limits, g_limits, b_limits):
    image_he = np.empty(image.shape, dtype='uint16')
    for channel, lim in enumerate([r_limits, g_limits, b_limits]):
        image_he[:, :, channel] = ski.exposure.rescale_intensity(
            image[:, :, channel], lim)
    return image_he


def progress_callback(complete, total):
    print("{0}/{1}".format(100 * complete / total, 100))


def s3_extract_rgb():
    return extract_rgb(s3_path, scene_id)


def s3_extract_swir2nirg():
    return extract_swir2nirg(s3_path, scene_id)

    
def s3_image(img, title="", filename="", **kwargs):
    (_, localfile) = tempfile.mkstemp(suffix=".png")
    print("Generating scene image ...")
    show_image(img, title, localfile, **kwargs)
    print("Saving image to S3 ...")
    conn = boto.connect_s3(access_key, secret_key)
    key = s3.key.Key(conn.get_bucket(bucket_name))
    key.key = filename
    key.set_contents_from_filename(
        localfile, cb=progress_callback, num_cb=5)


def s3_image_rgb():
    s3_image(s3_extract_rgb(), s3_title, s3_filename)


def s3_image_swir2nirg():
    s3_image(s3_extract_swir2nirg(), s3_title, s3_filename)


def s3_generate_image():
    if s3_image_type == "rgb":
        s3_image_rgb()
    elif s3_image_type == "swir2nirg":
        s3_image_swir2nirg()
