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

import os
import numpy as np
import tensorflow as tf


path_to = os.path.abspath(__file__ + "/..")


class SentimentLookup(object):
  """Converts integer node ID's to human readable labels."""

  def __init__(self, uid_lookup_path = None):
    if not uid_lookup_path:
      uid_lookup_path = path_to + '/features/labels_output_9.txt'
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
    # Adjust 0-1 indexing
    node_id += 1
    if node_id not in self.node_lookup:
      return ''
    return self.node_lookup[node_id]


def create_sentiment_graph():
  """Creates a graph from saved GraphDef file and returns a saver."""
  with tf.gfile.FastGFile(path_to + '/features/output_graph_9.pb', 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    senti_graph = tf.import_graph_def(graph_def, name='')
    return senti_graph


def sentiment_inference(senti_graph, image):
  """Runs inference on given image.

  Args:
    image: actual image

  Returns:
    Returns positive and negative sentiment scores.
  """

  with tf.Session(graph = senti_graph) as sess:

    final_tensor = sess.graph.get_tensor_by_name('final_result:0')
    try:
      predictions = sess.run(final_tensor,
                           {'DecodeJpeg/contents:0': image})
    except:
      return {}
      
    predictions = np.squeeze(predictions)
      # Creates node ID --> English string lookup.
    node_lookup = SentimentLookup()

    top_k = predictions.argsort()[-2:][::-1]

    tags = {}

    for node_id in top_k:
      human_string = node_lookup.id_to_string(node_id)
      score = predictions[node_id]
      tags[human_string] = score

    return tags
