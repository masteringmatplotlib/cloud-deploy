import boto
from boto import s3

import matplotlib as mpl
if  os.environ.get("EROS_SCENE_ID") == "true":
    mpl.use("Agg")

import eros


bucket_name = os.environ.get("S3_BUCKET_NAME")
scene_id = os.environ.get("EROS_SCENE_ID")
s3_path = os.environ.get("S3_PATH")
s3_title = os.environ.get("S3_IMAGE_TITLE")
s3_filename = os.environ.get("S3_IMAGE_FILENAME")
s3_image_type = os.environ.get("S3_IMAGE_TYPE", "").lower()
access_key = os.environ.get("AWS_ACCESS_KEY_ID")
secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")


def progress_callback(complete, total):
    print("{0}/{1}".format(100 * complete / total, 100))


def s3_extract_rgb():
    return eros.extract_rgb(s3_path, scene_id)


def s3_extract_swir2nirg():
    return eros.extract_swir2nirg(s3_path, scene_id)


def s3_image(img, title="", filename="", **kwargs):
    (_, localfile) = tempfile.mkstemp(suffix=".png")
    print("Generating scene image ...")
    eros.show_image(img, title, localfile, **kwargs)
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
