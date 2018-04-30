# import libraries and packages
import os
import cv2
import time
import argparse
import multiprocessing
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image

import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

## helper function
def detect_objects(image_np, sess, detection_graph, category_index):
    category_index = category_index
    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
    image_np_expanded = np.expand_dims(image_np, axis=0)
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

    # Each box represents a part of the image where a particular object was detected.
    boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

    # Each score represent how level of confidence for each of the objects.
    # Score is shown on the result image, together with the class label.
    scores = detection_graph.get_tensor_by_name('detection_scores:0')
    classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

    # Actual detection.
    (boxes, scores, classes, num_detections) = sess.run(
        [boxes, scores, classes, num_detections],
        feed_dict={image_tensor: image_np_expanded})
    #
    # print('detected objects:')
    # for classe in classes:
    #     print(classe)
    # for score in scores:
    #     print(score)

    # Which objects were found?

    dict_label_map = {
        1: "person",
        2: "bicycle",
        3: "car",
        4: "motorcycle",
        5: "airplane",
        6: "bus",
        7: "train",
        8: "truck",
        9: "boat",
        10: "traffic light",
        11: "fire hydrant",
        13: "stop sign",
        14: "parking meter",
        15: "bench",
        16: "bird",
        17: "cat",
        18: "dog",
        19: "horse",
        20: "sheep",
        21: "cow",
        22: "elephant",
        23: "bear",
        24: "zebra",
        25: "giraffe",
        27: "backpack",
        28: "umbrella",
        31: "handbag",
        32: "tie",
        33: "suitcase",
        34: "frisbee",
        35: "skis",
        36: "snowboard",
        37: "sports ball",
        38: "kite",
        40: "baseball bat",
        41: "skateboard",
        42: "surfboard",
        43: "tennis racket",
        44: "bottle",
        46: "wine glass",
        47: "cup",
        48: "fork",
        49: "knife",
        50: "spoon",
        51: "bowl",
        52: "banana",
        53: "apple",
        54: "sandwich",
        55: "orange",
        56: "broccoli",
        57: "carrot",
        58: "hot dog",
        59: "pizza",
        60: "donut",
        61: "cake",
        62: "chair",
        63: "couch",
        64: "potted plant",
        65: "bed",
        67: "dining table",
        70: "toilet",
        72: "tv",
        74: "mouse",
        75: "remote",
        76: "keyboard",
        77: "cell phone",
        78: "microwave",
        79: "oven",
        80: "toaster",
        81: "sind",
        82: "refrigerator",
        84: "book",
        85: "clock",
        86: "vase",
        87: "scissors",
        88: "teddy bear",
        89: "hair drier",
        90: "toothbrush" }

    dict_detected_objects = list()

    list_sc_cl = list(zip(scores[0], classes[0]))

    for i, (score, classe) in enumerate(list_sc_cl):
        if score > 0.5:
            dict_detected_objects.append({score, dict_label_map[classe]})

    # Visualization of the results of a detection.
    vis_util.visualize_boxes_and_labels_on_image_array(
        image_np,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=5)
    return image_np, dict_detected_objects

def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)

## this is the upload function used in the webapp
def object_detection_for_upload(filename):
    ### setup
    CWD_PATH = os.getcwd()
    filepath = os.path.join('static', 'uploads', filename)

    # Path to frozen detection graph. This is the actual model that is used for the object detection.
    MODEL_NAME = 'ssd_mobilenet_v1_coco_11_06_2017'
    PATH_TO_CKPT = os.path.join(CWD_PATH, 'models', 'research', 'object_detection', MODEL_NAME, 'frozen_inference_graph.pb')

    # List of the strings that is used to add correct label for each box.
    PATH_TO_LABELS = os.path.join(CWD_PATH, 'models', 'research', 'object_detection', 'data', 'mscoco_label_map.pbtxt')

    NUM_CLASSES = 90

    # Loading label map
    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)

    category_index = label_map_util.create_category_index(categories)

    ## First test on images
    # TODO: remove, since no test are needed
    # PATH_TO_TEST_IMAGES_DIR = os.path.join(CWD_PATH, 'models', 'research', 'object_detection', 'test_images')
    # TEST_IMAGE_PATHS = [ os.path.join(PATH_TO_TEST_IMAGES_DIR, 'image{}.jpg'.format(i)) for i in range(1, 3) ]
    #
    # for image in range(0, len(TEST_IMAGE_PATHS)):
    #     TEST_IMAGE_PATHS[image] = TEST_IMAGE_PATHS[image].replace("\\", "/")

    # for image_path in TEST_IMAGE_PATHS:
    #image = Image.open('static/uploads/image2.jpg')
    #image_np = load_image_into_numpy_array(image)
    #plt.imshow(image_np)
    #print(image.size, image_np.shape)
    #
    # Size, in inches, of the output images.
    # TODO parse this by input file!
    # IMAGE_SIZE = (12, 8)
    image = Image.open(filepath)
    image_w = round(image.width / 48, 2)
    image_h = round(image.height / 48, 2)
    IMAGE_SIZE = (image_w, image_h)
    # print(IMAGE_SIZE)

    # Load a frozen TF model
    # TODO: get better model
    # !!!
    detection_graph = tf.Graph()

    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

    with detection_graph.as_default():
        with tf.Session(graph=detection_graph) as sess:
            # for image_path in TEST_IMAGE_PATHS:
            image = Image.open(filepath)
            image_np = load_image_into_numpy_array(image)
            image_process, detected_objects = detect_objects(image_np, sess, detection_graph, category_index)
            plt.figure(figsize=IMAGE_SIZE)
            newpath = os.path.join('static', 'uploads', 'rendered', filename)
            plt.imshow(image_process)
            plt.savefig(newpath, format="png")

    return detected_objects

# object_detection_for_upload('image2.jpg')

# ### TODO
# # Import everything needed to edit/save/watch video clips
# from moviepy.editor import VideoFileClip
# from IPython.display import HTML
