import sys,os,dlib,csv,math,subprocess
import numpy as np
import matplotlib.pyplot as plt
from scipy import misc
from sklearn.externals import joblib

# Fix for headless machines:
import matplotlib 
matplotlib.use('Agg') 


path_to = os.path.abspath(__file__ + "/..")


#Function that takes the image path as input, and returns a dictionary of Facial Landmarks
def get_landmarks(image_path, detector, predictor):
    reference_28_vector = {}
    img = misc.imread(image_path)
    dets = detector(img, 1)
    for k, d in enumerate(dets):
        shape = predictor(img, d)
        new_points={}
        for i in range(68):
            x_point = shape.part(i).x
            y_point = shape.part(i).y
            point_array = np.array((x_point,y_point))
            new_points[i+1] = point_array

    reference_28_vector[image_path] = new_points
    return reference_28_vector

#Function to calculate the Feature Vectors of the test image based on a Pre-defined Delaunay Triangulation
#Returns a list of Area Features for each face present in the image
def delaunay_feature_vector(reference_28_vector,triangle_points):
	distance_l1_l17 = np.linalg.norm(reference_28_vector[1]-reference_28_vector[17])
	Area_Features = []
	for triangle in triangle_points:
		distance_0_1 = np.linalg.norm(reference_28_vector[int(triangle[0])]-reference_28_vector[int(triangle[1])])
		distance_1_2 = np.linalg.norm(reference_28_vector[int(triangle[1])]-reference_28_vector[int(triangle[2])])
		distance_0_2 = np.linalg.norm(reference_28_vector[int(triangle[0])]-reference_28_vector[int(triangle[2])])
		norm_distance_0_1 = distance_0_1/distance_l1_l17
		norm_distance_1_2 = distance_1_2/distance_l1_l17
		norm_distance_0_2 = distance_0_2/distance_l1_l17
		semi_perimeter = (norm_distance_0_1+norm_distance_0_2+norm_distance_1_2)/2.0
		area = math.sqrt(semi_perimeter*(semi_perimeter-norm_distance_0_1)*(semi_perimeter-norm_distance_1_2)*(semi_perimeter-norm_distance_0_2))
		Area_Features.append(area)
	return Area_Features


#Function to calculate the Feature Vectors based on the Distances between Landmarks obtained from get_landmarks function
#Returns a list of landmark features for each face present in the image
def landmark_feature_vector(reference_28_vector):
    distance_l1_l17 = np.linalg.norm(reference_28_vector[1]-reference_28_vector[17])
    features=[]
    for i in range(1,69):
        for j in range(i+1,69):
            features.append(np.linalg.norm(reference_28_vector[i]-reference_28_vector[j])/distance_l1_l17)
    return features


#Function to integrate both Area Features and Landmark Distance features into a single feature vector
#Returns a cumulative Feature Vector
def generate_feature_vector(image_path,reference_28_vector,triangle_points):
	Feature_Vector = []
	Combined_Features = []
	Area_Features = delaunay_feature_vector(reference_28_vector[image_path],triangle_points)
	Landmark_Features = landmark_feature_vector(reference_28_vector[image_path])
	for landmark in Landmark_Features:
		Combined_Features.append(landmark)
	for area in Area_Features:
		Combined_Features.append(area)
	Feature_Vector.append(Combined_Features)	
	return Feature_Vector


#Function to check if atleast one face exists in the image
#Returns dictionary with the pixel coordinates of the Detection Square of each face
def check_if_face(face_image, detector):
    img = misc.imread(face_image)
    dets = detector(img, 1)
    print("Number of faces detected: {}".format(len(dets)))
    face_dict = {}
    if len(dets)==0:
    	face_dict['No Face'] = -1
    	return face_dict
    for k, d in enumerate(dets):
        face_dict[k] = {'left':d.left(),'top':d.top(),'right':d.right(),'bottom':d.bottom()}
    return face_dict


#Model Trained on Tensorflow architecture using Transfer Learning
#Returns a positive score and a negative score for the input image
def Inception_Model(test_image):
	#This is the Cloned Tensorflow Directory
	os.chdir('/home/varunb/tensorclone/tensorflow')
	get_label_scores = 'bazel-bin/tensorflow/examples/label_image/label_image --graph=/home/varunb/tmp2/output_graph_9.pb --labels=/home/varunb/tmp2/labels_output_9.txt --output_layer=final_result --image='+test_image
	label_scores = subprocess.check_output(get_label_scores,shell=True)
	only_scores = label_scores.split(' ')
	if only_scores[1] == "(positive):":
		positive_score = only_scores[2]
		negative_score = only_scores[4]
	else:
		negative_score = only_scores[2]
		positive_score = only_scores[4]
	return positive_score,negative_score


def get_sentiment(test_image, detector, predictor):
	face_dict = {}
	faceAbsent=0
	face_dict = check_if_face(test_image, detector)

	#If face does not exist, Use only the Tensorflow Architecture
	#Mark FaceAbsent as True
	for key in face_dict:
		if key == 'No Face':
			faceAbsent=1
			positive_inception_score,negative_inception_score = Inception_Model(test_image)

	#If Face Exists, Use both Face Emotion Recognition and Inception Model
	if faceAbsent==0:
		img = misc.imread(test_image)
	
		#Delaunay_Traingles.csv contains a Pre-Defined Delaunay Triangulation that is used to generate Area Features of the test image
		reader = csv.reader(open(path_to + "/features/Delaunay_Triangles.csv"),delimiter=',')
		
		triangle_points = []
		for row in reader:
			if '-99999' not in row:
				triangle_points.append((row[0],row[1],row[2]))
	
		#Load the Trained Random Forest Classifier Model
		clf = joblib.load(path_to + '/features/Combined_RFClassifier.pkl')
		
		positive_probability = 0
		negative_probability = 0
		score_dict = {}
		for face_number in face_dict:
			if len(face_dict)>1:
				height_padding = 0.25*(face_dict[face_number]['bottom'] - face_dict[face_number]['top'])
				width_padding = 0.25*(face_dict[face_number]['right']-face_dict[face_number]['left'])
				cropped_image = img[face_dict[face_number]['top']-int(height_padding):face_dict[face_number]['bottom']+int(height_padding),face_dict[face_number]['left']-int(width_padding):face_dict[face_number]['right']+int(width_padding)]
				plt.imsave('face_'+str(face_number)+'.jpg',cropped_image)
				image_path = os.getcwd() + '/face_'+str(face_number)+'.jpg'
			else:
				image_path = test_image
			
			try:
				image_landmarks = get_landmarks(image_path, detector, predictor)
				feature_vector = generate_feature_vector(image_path,image_landmarks,triangle_points)
			
			#It may so happen that even when a face is detected, its landmarks may not be completely detected due to some obstruction on the face
			#This catches such an exception
			except Exception,e:
				print e
				continue
	
			result = clf.predict_proba(feature_vector)
			positive_probability += result[0][1]
			negative_probability += result[0][0]
			score_dict[face_number] = (result[0][1],result[0][0])
			if len(face_dict)>1:
				os.remove(image_path)
	
		positive_probability = positive_probability/len(face_dict)
		negative_probability = negative_probability/len(face_dict)
	
		positive_inception_score,negative_inception_score = Inception_Model(test_image)
	
	
	#Populating the JSON that holds the Image Sentiment
	image_sentiment_json = {}
	
	if faceAbsent==1:
		image_sentiment_json["Face"] = {}
	
	elif faceAbsent==0:
		image_sentiment_json["Face"] = {}
		for face_number in score_dict:
			image_sentiment_json["Face"]["Face_"+str(face_number)] = {}
			image_sentiment_json["Face"]["Face_"+str(face_number)]["Positive"] = round(score_dict[face_number][0],3)
			image_sentiment_json["Face"]["Face_"+str(face_number)]["Negative"] = round(score_dict[face_number][1],3)
		image_sentiment_json["Face"]["Average"] = {}
		image_sentiment_json["Face"]["Average"]["Positive"] = round(positive_probability,3)
		image_sentiment_json["Face"]["Average"]["Negative"] = round(negative_probability,3)
	
	image_sentiment_json["Inception"] = {}
	image_sentiment_json["Inception"]["Positive"] = float(positive_inception_score.split('\n')[0])
	image_sentiment_json["Inception"]["Negative"] = float(negative_inception_score.split('\n')[0])
	image_sentiment_json["Filename"] = test_image.split('/')[-1]
	
	return image_sentiment_json


if __name__ == "__main__":
	test_image = sys.argv[1]
	#Shape Predictor used for Facial Detection
	predictor_path = path_to + '/features/shape_predictor_68_face_landmarks.dat'
	#DLIB's Facial and Shape Predictor
	detector = dlib.get_frontal_face_detector()
	predictor = dlib.shape_predictor(predictor_path)
	print get_sentiment(test_image, detector, predictor)
