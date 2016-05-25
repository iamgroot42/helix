# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================


# Modified by : iamgroot42

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Fix for headless machines:
import matplotlib 
matplotlib.use('Agg') 

from pymongo import MongoClient
from os.path import abspath
from skimage import io
from multiprocessing import Process

import dlib
import exifread
import re
import os
import json
import numpy as np
import tensorflow as tf


path_to = abspath(__file__ + "/..")


class TensorLookup(object):
  """Converts integer node ID's to human readable labels."""

  def __init__(self,
               label_lookup_path=None,
               uid_lookup_path=None):
    if not label_lookup_path:
      label_lookup_path = path_to + '/NN_Data/imagenet_2012_challenge_label_map_proto.pbtxt'
    if not uid_lookup_path:
      uid_lookup_path = path_to + '/NN_Data/imagenet_synset_to_human_label_map.txt'
    self.node_lookup = self.load(label_lookup_path, uid_lookup_path)

  def load(self, label_lookup_path, uid_lookup_path):
    """Loads a human readable English name for each softmax node.

    Args:
      label_lookup_path: string UID to integer node ID.
      uid_lookup_path: string UID to human-readable string.

    Returns:
      dict from integer node ID to human-readable string.
    """
    if not tf.gfile.Exists(uid_lookup_path):
      tf.logging.fatal('File does not exist %s', uid_lookup_path)
    if not tf.gfile.Exists(label_lookup_path):
      tf.logging.fatal('File does not exist %s', label_lookup_path)

    # Loads mapping from string UID to human-readable string
    proto_as_ascii_lines = tf.gfile.GFile(uid_lookup_path).readlines()
    uid_to_human = {}
    p = re.compile(r'[n\d]*[ \S,]*')
    for line in proto_as_ascii_lines:
      parsed_items = p.findall(line)
      uid = parsed_items[0]
      human_string = parsed_items[2]
      uid_to_human[uid] = human_string

    # Loads mapping from string UID to integer node ID.
    node_id_to_uid = {}
    proto_as_ascii = tf.gfile.GFile(label_lookup_path).readlines()
    for line in proto_as_ascii:
      if line.startswith('  target_class:'):
        target_class = int(line.split(': ')[1])
      if line.startswith('  target_class_string:'):
        target_class_string = line.split(': ')[1]
        node_id_to_uid[target_class] = target_class_string[1:-2]

    # Loads the final mapping of integer node ID to human-readable string
    node_id_to_name = {}
    for key, val in node_id_to_uid.items():
      if val not in uid_to_human:
        tf.logging.fatal('Failed to locate: %s', val)
      name = uid_to_human[val]
      node_id_to_name[key] = name

    return node_id_to_name

  def id_to_string(self, node_id):
    if node_id not in self.node_lookup:
      return ''
    return self.node_lookup[node_id]


class CustomLookup(object):
  """Converts integer node ID's to human readable labels."""

  def __init__(self, uid_lookup_path = None):
    if not uid_lookup_path:
      uid_lookup_path = path_to + '/NN_Data/custom_labels.txt'
    self.node_lookup = self.load(uid_lookup_path)

  def load(self, uid_lookup_path):
    """Loads a human readable English name for each softmax node.

    Args:
      uid_lookup_path: string UID to human-readable string.

    Returns:
      dict from integer node ID to human-readable string.
    """
    if not tf.gfile.Exists(uid_lookup_path):
      tf.logging.fatal('File does not exist %s', uid_lookup_path)

    proto_as_ascii_lines = tf.gfile.GFile(uid_lookup_path).readlines()
    uid_to_human = {}
    uid = 1
    for line in proto_as_ascii_lines:
      uid_to_human[uid] = line.split('\n')[0]
      uid += 1

    return uid_to_human

  def id_to_string(self, node_id):
    if node_id not in self.node_lookup:
      return ''
    return self.node_lookup[node_id]


def create_tensor_graph():
  """Creates a graph from saved GraphDef file and returns a saver."""
  # Creates graph from saved graph_def.pb.
  with tf.gfile.FastGFile(path_to + '/NN_Data/classify_image_graph_def.pb', 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')


def create_custom_graph():
  """Creates a graph from saved GraphDef file and returns a saver."""
  with tf.gfile.FastGFile(path_to + '/NN_Data/custom_graph.pb', 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')


def custom_inference(path, db_name, collection_name, num_top_predictions = 3):
  """Runs inference on every image in given path.

  Args:
    path: Path to directory containing images.
    num_top_predictions: Number of top predictions to be picked
    db_name: Name of desired DB
    collection_name: Name of desired collection
    
  Returns:
    True, after all data has been pushed to DB
  """
  # Creates graph from saved GraphDef.
  create_custom_graph()
  
  # Prepare mongoDB for storing tags.
  client = MongoClient('mongodb://localhost:27017/')
  db = client[db_name]
  table = db[collection_name]

  with tf.Session() as sess:

    final_tensor = sess.graph.get_tensor_by_name('final_result:0')

    for image in os.listdir(path):
      image_data = tf.gfile.FastGFile(path + "/" + image, 'rb').read()
      img_exif = open(path + "/" + image)
      exif = exifread.process_file(img_exif)

    # Convert byte array to unicode (exif)
    for k in ['Image XPTitle', 'Image XPComment', 'Image XPAuthor', 'Image XPKeywords', 'Image XPSubject']:
      if k in exif:
        exif[k].values = u"".join(map(unichr, exif[k].values)).decode('utf-16')

      predictions = sess.run(final_tensor,
                           {'DecodeJpeg/contents:0': image_data})
      predictions = np.squeeze(predictions)
        # Creates node ID --> English string lookup.
      node_lookup = CustomLookup()

      top_k = predictions.argsort()[-num_top_predictions:][::-1]

      tags = {}

      for node_id in top_k:
        human_string = node_lookup.id_to_string(node_id)
        score = predictions[node_id]
        tags[human_string] = score

      # Picking top confidence value.
      tag = sorted(tags, key = tags.get, reverse = True)[0]
      confidence = float(tags[tag])
      # confidence = [ float(tags[c]) for c in tag]

      # EXIF data
      exif_data = { 'Image Make':"", 'Image Model':"", 'EXIF DateTimeOriginal':"" }
      attrs = ['Image Make', 'Image Model', 'EXIF DateTimeOriginal']
      for at in attrs:
        if at in exif:
          exif_data[at] = exif[at].values

      # Push to DB
      table.insert_one( { "filename": image, "custom_tag": tag, "custom_confidence": confidence, 
        "camera_make": exif_data['Image Make'], "camera_model": exif_data['Image Model'],
        "capture_date": exif_data['EXIF DateTimeOriginal'] } )

    return True


def tensor_inference(path, db_name, collection_name, num_top_predictions = 3):
  """Runs inference on every image in given path.

  Args:
    path: Path to directory containing images.
    num_top_predictions: Number of top predictions to be picked
    db_name: Name of desired DB
    collection_name: Name of desired collection

  Returns:
    True, after all data has been pushed to DB
  """
  # Creates graph from saved GraphDef.
  create_tensor_graph()
  
  # Prepare mongoDB for storing tags.
  client = MongoClient('mongodb://localhost:27017/')
  db = client[db_name]
  table = db[collection_name]

  with tf.Session() as sess:

    softmax_tensor = sess.graph.get_tensor_by_name('softmax:0')
    # Create face detector instance
    detector = dlib.get_frontal_face_detector()

    for image in os.listdir(path):
      image_data = tf.gfile.FastGFile(path + "/" + image, 'rb').read()
      img_p = io.imread(path + "/" + image)

      predictions = sess.run(softmax_tensor,
                           {'DecodeJpeg/contents:0': image_data})
      predictions = np.squeeze(predictions)
        # Creates node ID --> English string lookup.
      node_lookup = TensorLookup()

      top_k = predictions.argsort()[-num_top_predictions:][::-1]

      tags = {}

      for node_id in top_k:
        human_string = node_lookup.id_to_string(node_id)
        score = predictions[node_id]
        tags[human_string] = score

      # Picking top confidence value.
      tag = sorted(tags, key = tags.get, reverse = True)[0]
      confidence = float(tags[tag])
      # confidence = [ float(tags[c]) for c in tag]

      # Number of people
      dets = detector(img_p, 1) # Second argument is upscale factor (for better detection)

      # Push to DB.
      table.insert_one( { "filename": image, "tensorflow_tag": tag, "tensorflow_confidence": confidence,
      	"faces": len(dets)} )

    return True


def run_inference_on_images(path, db_name, collection_name, num_top_predictions = 3):
  """Runs inference on every image in given path.

  Args:
    path: Path to directory containing images.
    num_top_predictions: Number of top predictions to be picked
    db_name: Name of desired DB
    collection_name: Name of desired collection

  Returns:
    True, after all data has been pushed to DB
  """
  # Prepare mongoDB for storing tags.
  client = MongoClient('mongodb://localhost:27017/')
  exists = False
  left = "left"
  right = "right" 

  if "temporary_storage" in client.database_names():
    exists = True

  db = client["temporary_storage"]
  coln = db.collection_names()

  if left in coln:
    i = 0
    while (left + str(i)) in coln:
      i += 1
    left += str(i)

  if right in coln:
    i = 0
    while (right + str(i)) in coln:
      i += 1
    right += str(i)

  jobs = []
  jobs.append(Process(target = tensor_inference, args=(path,"temporary_storage",left,)))
  jobs.append(Process(target = custom_inference, args=(path,"temporary_storage",right,)))

  for j in jobs:
    j.start()

  for j in jobs:
    j.join()

  left_table = db[left]
  right_table = db[right]
  left_rows = left_table.find()
  right_rows = right_table.find()
  shared_data = {}

  for row in left_rows:
    x = row
    del x['_id']
    fname = x['filename']
    del x['filename']
    shared_data[fname] = x

  for row in right_rows:
    x = row
    del x['_id']
    fname = x['filename']
    del x['filename']
    for y in x.keys():
      shared_data[fname][y] = x[y]

    if exists:
      left_table.drop()
      right_table.drop()
    else:
      client.drop_database("temporary_storage")

  db = client[db_name]
  table = db[collection_name]
  for x in shared_data.keys():
    table.insert_one(shared_data[x])

  return True
