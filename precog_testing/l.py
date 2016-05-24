from pymongo import MongoClient
import os

path_to = os.path.abspath(__file__ + "/..")


def run_inference_on_images(path, num_top_predictions = 3, db_name = "analysis", collection_name = "tags"):
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
  coln = db.getCollectionNames()

  if left in coln:
    i = 0
    while (coln + str(i)) in coln:
      i += 1

  if right in coln:
    i = 0
    while (coln + str(i)) in coln:
      i += 1

  table = db[collection_name]


  for image in os.listdir(path):
    image_data = tf.gfile.FastGFile(path + "/" + image, 'rb').read()

    predictions = sess.run(softmax_tensor,
                           {'DecodeJpeg/contents:0': image_data})
    predictions = np.squeeze(predictions)
        # Creates node ID --> English string lookup.
    node_lookup = NodeLookup()

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

    # Push to DB
    table.insert_one( { "filename": image, "tensorflow_tag": tag, "tensorflow_confidence": confidence} )

    return True
