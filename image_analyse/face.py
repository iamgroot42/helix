# Author : Varun Bharadwaj
# Modified by : iamgroot42

# Note: Do not mess with the order of imports!

import os,dlib,csv,math
import numpy as np
from sklearn.externals import joblib

import sentiment

# Fix for headless machines:
import matplotlib 
matplotlib.use('Agg') 


path_to = os.path.abspath(__file__ + "/..")
clf = None
reader = None
predictor = None


#Function that takes the image path as input, and returns a dictionary of Facial Landmarks
def get_landmarks(img_array, detector):
    reference_28_vector = {}
    dets = detector(img_array, 1)
    ret_value = {}
    for k, d in enumerate(dets):
        shape = predictor(img_array, d)
        new_points = {}
        for i in range(68):
            x_point = shape.part(i).x
            y_point = shape.part(i).y
            point_array = np.array((x_point,y_point))
            new_points[i+1] = point_array
        ret_value = new_points

    return ret_value


#Function to calculate the Feature Vectors of the test image based on a Pre-defined Delaunay Triangulation
#Returns a list of Area Features for each face present in the image
def delaunay_feature_vector(reference_28_vector, triangle_points):
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
    distance_l1_l17 = np.linalg.norm(reference_28_vector[1] - reference_28_vector[17])
    features=[]
    for i in range(1, 69):
        for j in range(i+1, 69):
            features.append(np.linalg.norm(reference_28_vector[i] - reference_28_vector[j])/distance_l1_l17)

    return features


#Function to integrate both Area Features and Landmark Distance features into a single feature vector
#Returns a cumulative Feature Vector
def generate_feature_vector(reference_28_vector, triangle_points):
	Feature_Vector = []
	Combined_Features = []
	Area_Features = delaunay_feature_vector(reference_28_vector, triangle_points)
	Landmark_Features = landmark_feature_vector(reference_28_vector)
	for landmark in Landmark_Features:
		Combined_Features.append(landmark)
	for area in Area_Features:
		Combined_Features.append(area)
	Feature_Vector.append(Combined_Features)	

	return Feature_Vector


#Function to check if atleast one face exists in the image
#Returns dictionary with the pixel coordinates of the Detection Square of each face
def check_if_face(img_array, detector):
    dets = detector(img_array, 1)
    face_dict = {}
    if len(dets) == 0:
    	face_dict['No Face'] = -1
    	return face_dict
    for k, d in enumerate(dets):
        face_dict[k] = {'left':d.left(),'top':d.top(),'right':d.right(),'bottom':d.bottom()}

    return face_dict


#Model Trained on Tensorflow architecture using Transfer Learning
#Returns a positive score and a negative score for the input image
def Sentiment_Model(senti_graph, img):
	scores = sentiment.sentiment_inference(senti_graph, img)
	positive_score = float(scores['positive'])
	negative_score = float(scores['negative'])
	return positive_score, negative_score


# Loads graph(s) into memory
def ready():
	global clf
	global reader
	global predictor
	#Shape Predictor used for Facial Detection
	predictor_path = path_to + '/features/shape_predictor_68_face_landmarks.dat'
	predictor = dlib.shape_predictor(predictor_path)
	#Delaunay_Traingles.csv contains a Pre-Defined Delaunay Triangulation that is used to generate Area Features of the test image
	reader = csv.reader(open(path_to + "/features/Delaunay_Triangles.csv"), delimiter = ',')
	#Load the Trained Random Forest Classifier Model
	clf = joblib.load(path_to + '/features/Combined_RFClassifier.pkl')
	return sentiment.create_sentiment_graph()


# Returns a json with everything related to the sentiment
# associated with the input image
def get_sentiment(senti_graph, img, img_array):
	try:
		#DLIB's Facial and Shape Predictor
		detector = dlib.get_frontal_face_detector()
		face_dict = {}
		faceAbsent = 0
		face_dict = check_if_face(img_array, detector)
		positive_inception_score, negative_inception_score = Sentiment_Model(senti_graph, img)
		#If face does not exist, Use only the Tensorflow Architecture
		#Mark FaceAbsent as True
		for key in face_dict:
			if key == 'No Face':
				faceAbsent = 1

		#If Face Exists, Use both Face Emotion Recognition and Inception Model
		if faceAbsent == 0:
		
			triangle_points = []
			for row in reader:
				if '-99999' not in row:
					triangle_points.append((row[0],row[1],row[2]))
		
			positive_probability = 0
			negative_probability = 0
			score_dict = {}
			denominator = len(face_dict)
			for face_number in face_dict:
				cropped_image = None
				feature_vector = None
				if len(face_dict) > 1:
					height_padding = 0.25*(face_dict[face_number]['bottom'] - face_dict[face_number]['top'])
					width_padding = 0.25*(face_dict[face_number]['right'] - face_dict[face_number]['left'])
					cropped_image = np.array(img_array[face_dict[face_number]['top'] - int(height_padding):face_dict[face_number]['bottom'] + int(height_padding),face_dict[face_number]['left'] - int(width_padding):face_dict[face_number]['right'] + int(width_padding)])
				try:
					image_landmarks = get_landmarks(cropped_image, detector)
					feature_vector = generate_feature_vector(image_landmarks, triangle_points)
					result = clf.predict_proba(feature_vector)
					positive_probability += result[0][1]
					negative_probability += result[0][0]
					score_dict[face_number] = (result[0][1],result[0][0])
				#It may so happen that even when a face is detected, its landmarks may not be completely detected due to some obstruction on the face
				#This catches such an exception. Also, face shouldn't be considered for average either
				except Exception,e:
					print "Error in face.py:",e
					denominator -= 1
	
	
		#Populating the JSON that holds the Image Sentiment
		image_sentiment_json = {}
		if faceAbsent == 0:
			image_sentiment_json["Face"] = {}
			for face_number in score_dict:
				try:
					image_sentiment_json["Face"]["Face_"+str(face_number)] = {}
					image_sentiment_json["Face"]["Face_"+str(face_number)]["Positive"] = round(score_dict[face_number][0],3)
					image_sentiment_json["Face"]["Face_"+str(face_number)]["Negative"] = round(score_dict[face_number][1],3)
				except:
					print "Error in face.py:",e
			try: 
				image_sentiment_json["Face"]["Average"] = {}
				image_sentiment_json["Face"]["Average"]["Positive"] = round(positive_probability/denominator,3)
				image_sentiment_json["Face"]["Average"]["Negative"] = round(negative_probability/denominator,3)
			except:
				print "Error in face.py:",e
		image_sentiment_json["Tensorflow_SentiBank"] = {}
		image_sentiment_json["Tensorflow_SentiBank"]["Positive"] = positive_inception_score
		image_sentiment_json["Tensorflow_SentiBank"]["Negative"] = negative_inception_score
	
		return image_sentiment_json
	except Exception,e:
		print "Error in face.py:",e
		return {}
