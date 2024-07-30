
#Import scikit-learn metrics module for accuracy calculation
import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import datetime
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler



def train(X, y, feature_names):
  
    X = np.array(X)
    y = np.array(y)
    print('X', len(X), X)
    # Ensure X is 2D
    if X.ndim == 1:
        X = X.reshape(-1, 1)
    
    print('X reshaped', len(X), X)
    scaler = StandardScaler()
    scaled_x = scaler.fit_transform(X)
    
    clf = svm.SVC(kernel='linear', C=3.0)
    clf.fit(scaled_x, y)
    print('Training the model...')
    
    # Generate a unique filename with a timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save the scaler
    scaler_file = f"classifier/shape_classifier/scalers/linear_svm_scaler_{timestamp}.joblib"

    # Save the model
    joblib_file = f"classifier/shape_classifier/linear_svm_models/svm_model_{timestamp}.joblib"
    joblib.dump(scaler, scaler_file)
    joblib.dump(clf, joblib_file)
    
    result = ['features: '+ str(feature_names), 'classifier: '+ 'linear_svm', 'C: 3.0']
   
#    save model configuration to logs
    with open(f"classifier/shape_classifier/logs/linear_svm_model_{timestamp}.txt", 'w') as f:
        for item in result:
            f.write(item + '\n')
            

def use(X, candidate)-> dict:
    print('use linear svm', len(X))
    X = np.array(X)
    X = [X]
    # if X.ndim == 1:
    #     X = X.reshape(-1, 1)
   
    # get the right model
    # joblib_file = 'classifier/shape_classifier/linear_svm_models/svm_model_20240622_225934.joblib'
    
    joblib_file = 'classifier/shape_classifier/linear_svm_models/svm_model_20240729_122224.joblib'
    scaler_file = 'classifier/shape_classifier/scalers/linear_svm_scaler_20240729_122224.joblib'
    loaded_clf = joblib.load(joblib_file)
    loaded_scaler = joblib.load(scaler_file)
    print('X', len(X), X)
    scaled_X = loaded_scaler.transform(X)
    print('scaled_X', scaled_X)
        
    predicted_label = loaded_clf.predict(scaled_X)
    
   
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
    if predicted_label == 0:
        return {'valid': {'circle': candidate}}
    if predicted_label == 1:
        return {'valid': {'rectangle': candidate}}
    # else:
    #     if predicted_label[0] == 0:
    #         return {'valid': {'circle': candidate}}
    #     elif predicted_label[0] == 1:
    #         return {'valid': {'rectangle': candidate}}
        # else:
        #     return {'invalid': candidate}
    #     return {'invalid': candidate}
    # if predicted_label[0] == 0:
    #     return {'valid': {'circle': candidate}}
    # elif predicted_label[0] == 1:
    #     return {'valid': {'rectangle': candidate}}

    
