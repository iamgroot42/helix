from precog_testing import classify_image
from multiprocessing import Process
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "Up!"


@app.route("/analyze",  methods=['POST'])
def analyze():
	# jobs = []
	imagefile = request.files['imagefile']
	return str(classify_image.tensor_inference(imagefile.stream.read()))
	# Inceptionv3 tag
	# jobs.append(Process(target = tensor_inference, args=(odd, path,"temporary_storage",left,)))


if __name__ == "__main__":
	# Load inception v3 graph into memory
    classify_image.ready_graph()
    app.run()
