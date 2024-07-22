
#Import scikit-learn metrics module for accuracy calculation
import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import datetime


def train(X, y, feature_names):
  
    X = np.array(X)
    y = np.array(y)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    class_weights = 'balanced'
    probability= True
    clf = svm.SVC(kernel='linear', class_weight=class_weights, C=3.0, probability=probability)
    print('Training the model...')
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy * 100:.2f}%')
    
    # Generate a unique filename with a timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # Save the model
    joblib_file = f"classifier/shape_classifier/linear_svm_models/svm_model_{timestamp}.joblib"
    joblib.dump(clf, joblib_file)
    
    result = ['features: '+ str(feature_names), 'classifier: '+ 'linear_svm', 'accuracy: '+ str(accuracy * 100) + '%', 'C: 3.0', 'random_state: 42', f'class_weight:{class_weights}, probability: {probability}']
   
#    save model configuration to logs
    with open(f"classifier/shape_classifier/logs/linear_svm_model_{timestamp}.txt", 'w') as f:
        for item in result:
            f.write(item + '\n')
            

def use(X, candidate)-> dict:
    X = np.array(X)
    # get the right model
    # joblib_file = 'classifier/shape_classifier/linear_svm_models/svm_model_20240622_225934.joblib'
    joblib_file = 'classifier/shape_classifier/linear_svm_models/svm_model_20240721_200012.joblib'

    # Load the model
    loaded_clf = joblib.load(joblib_file)
     # Ensure X is a 2D array
    if X.ndim == 1:
        X = X.reshape(1, -1)

    
    predicted_label = loaded_clf.predict(X)
    # get probability of label 0
    probability = loaded_clf.predict_proba(X)
    # print(f'Predicted label: {predicted_label[0]}')
    # print(f'Probability of label 0: {probability[0,0] * 100:.2f}%')
    # print(f'Probability of label 1: {probability[0,1] * 100:.2f}%')
    # # How can I check the probability of label 0 and label 1?
    # print('probability', probability)    
    # check if probability of label 0 is greater than 0.5
    
    # if probability[0,0] > probability[0,1] and probability[0,0] > 0.8:
    #     return {'valid': {'circle': candidate}}
    # elif probability[0,1] > 0.8:
    #     return {'valid': {'rectangle': candidate}}
    # else:
    #     return {'invalid': candidate}
    if probability[0,0] > probability[0,1]:
        return {'valid': {'circle': candidate}}
    elif probability[0,1] > probability[0,0]:
        return {'valid': {'rectangle': candidate}}
    else:
        if predicted_label[0] == 0:
            return {'valid': {'circle': candidate}}
        elif predicted_label[0] == 1:
            return {'valid': {'rectangle': candidate}}
        # else:
        #     return {'invalid': candidate}
    #     return {'invalid': candidate}
    # if predicted_label[0] == 0:
    #     return {'valid': {'circle': candidate}}
    # elif predicted_label[0] == 1:
    #     return {'valid': {'rectangle': candidate}}

    
