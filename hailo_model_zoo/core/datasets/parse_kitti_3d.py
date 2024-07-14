import tensorflow as tf

from hailo_model_zoo.core.factory import DATASET_FACTORY

DEPTH_WIDTH = 1242
DEPTH_HEIGHT = 375


@DATASET_FACTORY.register(name="kitti_3d")
def parse_record(serialized_example):
    """Parse serialized example of TfRecord and extract dictionary of all the information"""
    features = tf.io.parse_single_example(
        serialized_example,
        features={
            "height": tf.io.FixedLenFeature([], tf.int64),
            "width": tf.io.FixedLenFeature([], tf.int64),
            "image_name": tf.io.FixedLenFeature([], tf.string),
            "image_jpeg": tf.io.FixedLenFeature([], tf.string),
        },
    )

    height = tf.cast(features["height"], tf.int32)
    width = tf.cast(features["width"], tf.int32)
    image_name = tf.cast(features["image_name"], tf.string)

    image = tf.cast(tf.image.decode_jpeg(features["image_jpeg"], channels=3), tf.uint8)
    image_shape = tf.stack([height, width, 3])
    image = tf.reshape(image, image_shape)
    image_info = {"image_name": image_name}
    return [image, image_info]
