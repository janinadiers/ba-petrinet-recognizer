# Eine svm um zwischen shapes und no shapes zu unterscheiden

#Import scikit-learn metrics module for accuracy calculation
import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import datetime


def train(X, y, feature_names):
    X = np.array(X)
    y = np.array(y)  # Corresponding labels (1: Rectangle, 0: Circle, 2: no shape)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # besser großes C =3, da die punkte oft recht nah beieinander liegen und wir deshalb die margin klein halten wollen um Missklassifikationen zu vermeiden
    clf = svm.SVC(kernel='rbf', class_weight='balanced', C=3.0, gamma=0.5)
    print('Training the model...')
    
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy * 100:.2f}%')
    
    # Generate a unique filename with a timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # Save the model
    joblib_file = f"rejector/rbf_svm_models/rbf_svm_model_{timestamp}.joblib"
    joblib.dump(clf, joblib_file)
    
    result = ['features: '+ str(feature_names), 'rejector: '+ 'rbf_svm', 'accuracy: '+ str(accuracy * 100) + '%', 'C: 3.0', 'gamma: 0.5', 'random_state: 42', f'class_weight:balanced']

    #save model configuration to logs
    with open(f"rejector/shape_rejector/logs/rbf_svm_model_{timestamp}.txt", 'w') as f:
        for item in result:
            f.write(item + '\n')


def use(X, candidate)-> dict:
    print('use rejector rbf_svm', X)
    X = np.array(X)
    
    joblib_file = 'rejector/rbf_svm_models/rbf_svm_model_20240612_111931.joblib'
    
    loaded_clf = joblib.load(joblib_file)
     # Ensure X is a 2D array
    if X.ndim == 1:
        X = X.reshape(1, -1)
        
    predicted_label = loaded_clf.predict(X)
    
    if predicted_label[0] == 0:
        print('-----------------shape!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        return {'valid': {'circle': candidate}}
    elif predicted_label[0] == 1:
        print('-----------------no shape!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        return {'valid': {'rectangle': candidate}}
    