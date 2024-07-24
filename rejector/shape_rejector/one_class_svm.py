
import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import datetime


def train(X, feature_names):
    X = np.array(X)
    print('one class svm')
    # Datensatz in Trainings- und Testdaten aufteilen
    X_train, X_test = train_test_split(X, test_size=0.2, random_state=42)

    # OneClassSVM-Modell trainieren
    clf = svm.OneClassSVM(kernel='linear', nu=0.05, gamma='auto')
    print('Training one class svm model...')
    clf.fit(X_train)
    
        # Vorhersagen treffen
    y_pred_train = clf.predict(X_train)
    y_pred_test = clf.predict(X_test)
    
    # Für OneClassSVM sind die Vorhersagen +1 (Inlier) und -1 (Outlier)
    # Berechnung der Genauigkeit für das Trainings- und Testset
    accuracy_train = accuracy_score(np.ones_like(y_pred_train), y_pred_train)
    accuracy_test = accuracy_score(np.ones_like(y_pred_test), y_pred_test)

    print(f'Training Accuracy: {accuracy_train * 100:.2f}%')
    print(f'Test Accuracy: {accuracy_test * 100:.2f}%')

        
    # Generate a unique filename with a timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # Save the model
    joblib_file = f"rejector/shape_rejector/one_class_linear_svm_models/one_class_linear_svm_model_{timestamp}.joblib"
    joblib.dump(clf, joblib_file)
    
    result = ['features: '+ str(feature_names), 'classifier: '+ 'linear_svm', 'accuracy: '+ str(accuracy_test * 100) + '%', 'nu: 0.05', 'gamma: auto']

    #save model configuration to logs
    with open(f"rejector/shape_rejector/logs/one_class_linear_svm_model_{timestamp}.txt", 'w') as f:
        for item in result:
            f.write(item + '\n')
            
            
def use(X, candidate, expected_shapes)-> dict:
    
    X = np.array(X)
    
    joblib_file = 'rejector/shape_rejector/one_class_linear_svm_models/one_class_linear_svm_model_20240723_192458.joblib'
    
    loaded_clf = joblib.load(joblib_file)
     # Ensure X is a 2D array
    if X.ndim == 1:
        X = X.reshape(1, -1)
        
    predicted_label = loaded_clf.predict(X)
    # probability = loaded_clf.predict_proba(X)
    # print('predicted_label', predicted_label)
    
    if predicted_label[0] == -1:
        # print('outlier')
        return {'invalid': candidate}
    else:
        # print('inlier')
        return {'valid': {'rectangle': candidate}}
    

    