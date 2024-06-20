# Eine svm um zwischen shapes und no shapes zu unterscheiden

#Import scikit-learn metrics module for accuracy calculation
import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import datetime
import matplotlib.pyplot as plt


def train(X, feature_names):
    X = np.array(X)
    
    # Datensatz in Trainings- und Testdaten aufteilen
    X_train, X_test = train_test_split(X, test_size=0.2, random_state=42)

    # OneClassSVM-Modell trainieren
    clf = svm.OneClassSVM(kernel='rbf', nu=0.05, gamma='auto')
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
    joblib_file = f"rejector/shape_rejector/one_class_rbf_svm_models/one_class_rbf_svm_model_{timestamp}.joblib"
    joblib.dump(clf, joblib_file)
    
    result = ['features: '+ str(feature_names), 'rejector: '+ 'rbf_svm', 'accuracy: '+ str(accuracy_test * 100) + '%', 'nu: 0.1', 'gamma: 0.5', 'random_state: 42']

    #save model configuration to logs
    with open(f"rejector/shape_rejector/logs/one_class_rbf_svm_model_{timestamp}.txt", 'w') as f:
        for item in result:
            f.write(item + '\n')


def use(X, candidate)-> dict:
    X = np.array(X)
    print('use one class svm')
    joblib_file = 'rejector/shape_rejector/one_class_rbf_svm_models/one_class_rbf_svm_model_20240618_140811.joblib'
    
    loaded_clf = joblib.load(joblib_file)
     # Ensure X is a 2D array
    if X.ndim == 1:
        X = X.reshape(1, -1)
        
    predicted_label = loaded_clf.predict(X)
    # probability = loaded_clf.predict_proba(X)
    # print('predicted_label', predicted_label)
    
    if predicted_label[0] == -1:
        # print('no shape')
        # print('-----------------no shape!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        return {'invalid': candidate}
    else:
         # print('-----------------shape!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        return {'valid': candidate}
    
def plot_decision_boundary(clf, X):
    decision_function_values = clf.decision_function(X)
    
    # Create a grid to plot the decision boundary
    xx, yy = np.meshgrid(np.linspace(X[:, 0].min() - 1, X[:, 0].max() + 1, 500),
                        np.linspace(X[:, 1].min() - 1, X[:, 1].max() + 1, 500))

    # Get the decision function values for the grid
    Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    # Plot the decision boundary and margins
    plt.contourf(xx, yy, Z, levels=np.linspace(Z.min(), 0, 7), cmap=plt.cm.PuBu)
    plt.contourf(xx, yy, Z, levels=[0, Z.max()], colors='orange')
    plt.scatter(X[:, 0], X[:, 1], c=y, edgecolors='k', linewidth=1, marker='o')
    plt.contour(xx, yy, Z, levels=[0], linewidths=2, colors='k')
    plt.show()
    