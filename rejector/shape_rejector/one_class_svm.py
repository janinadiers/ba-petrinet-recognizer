
import numpy as np
from sklearn import svm
from sklearn.preprocessing import StandardScaler
import joblib
import datetime



def train(X, feature_names):
    X = np.array(X)
    # print('X', X[:25])
    if X.ndim == 1:
        X = X.reshape(-1, 1)
    
    # Create a pipeline that standardizes the data then fits the One-Class SVM
    scaler = StandardScaler()
    scaled_x = scaler.fit_transform(X)
    # print('scaled_x', scaled_x[:25])
    clf = svm.OneClassSVM(nu=0.01, kernel='linear')
    clf.fit(scaled_x)
    
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # Save the scaler
    scaler_file = f"rejector/shape_rejector/scalers/one_class_svm_scaler_{timestamp}.joblib"

    # Save the model
    joblib_file = f"rejector/shape_rejector/one_class_svm_models/one_class_svm_model_{timestamp}.joblib"
    joblib.dump(scaler, scaler_file)
    joblib.dump(clf, joblib_file)
    
    result = ['features: '+ str(feature_names), 'classifier: '+ 'one_class_svm', 'nu: 0.01', 'c: 3.0']

    #save model configuration to logs
    with open(f"rejector/shape_rejector/logs/one_class_svm_model_{timestamp}.txt", 'w') as f:
        for item in result:
            f.write(item + '\n')
    print('Model saved')      
            
def use(X, candidate, expected_shapes)-> dict:
    
    X = np.array(X)
    # print('X', X )
    if X.ndim == 1:
        X = X.reshape(-1, 1)
    # print('X reshaped', X )
    # elif X.shape[0] == 1:
    #     X = X.reshape(1, -1)
   
    joblib_file1 = 'rejector/shape_rejector/one_class_svm_models/one_class_svm_model_20240729_074949.joblib'
    scaler_file1 = 'rejector/shape_rejector/scalers/one_class_svm_scaler_20240729_074949.joblib'
    joblib_file2 = 'rejector/shape_rejector/one_class_svm_models/one_class_svm_model_20240729_074951.joblib'
    scaler_file2 = 'rejector/shape_rejector/scalers/one_class_svm_scaler_20240729_074951.joblib'
    
    loaded_clf1 = joblib.load(joblib_file1)
    loaded_scaler1 = joblib.load(scaler_file1)
    
    loaded_clf2 = joblib.load(joblib_file2)
    loaded_scaler2 = joblib.load(scaler_file2)
     
    
    
    # Scale the new data using the loaded scaler
    scaled_X1 = loaded_scaler1.transform(X)
    predicted_label1 = loaded_clf1.predict(scaled_X1)
    
    scaled_X2 = loaded_scaler2.transform(X)
    predicted_label2 = loaded_clf2.predict(scaled_X2)
    
    if predicted_label1[0] == -1 and predicted_label2[0] == -1:
        # print('outlier')
        return {'invalid': candidate}
    else:
        # print('inlier')
        return {'valid': candidate}
    

    