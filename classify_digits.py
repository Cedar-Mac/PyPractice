import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import Normalizer
from sklearn.model_selection import GridSearchCV

(x_train, y_train), _ = tf.keras.datasets.mnist.load_data(path="mnist.npz")
nrows = x_train.shape[0]
x_train = x_train.reshape(nrows, -1)
x_train, y_train = x_train[:6000], y_train[:6000]

x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size=0.3, random_state=40)
norm = Normalizer()
x_train_norm = norm.transform(x_train)
x_test_norm = norm.transform(x_test)


def fit_predict_eval(model, features_train, features_test, target_train=y_train, target_test=y_test):
    model.fit(features_train, target_train)
    preds = model.predict(features_test)
    score = round(accuracy_score(preds, target_test), 3)
    print(f'Model: {type(model).__name__}\nAccuracy: {score}\n')
    return score


def stage_four():
    models = (KNeighborsClassifier(), DecisionTreeClassifier(random_state=40),
              LogisticRegression(random_state=40, solver='liblinear'), RandomForestClassifier(random_state=40))
    norm_results = dict()
    for model in models:
        norm_results[model] = fit_predict_eval(model, features_train=x_train_norm, features_test=x_test_norm)

    sorted_norm_results = {k: v for k, v in sorted(norm_results.items(), key=lambda item: item[1], reverse=True)}

    for result in sorted_norm_results:
        print(f'Model: {type(result).__name__}\nAccuracy: {sorted_norm_results[result]}\n')

    print('The answer to the 1st question: yes')
    print('The answer to the 2nd question: KNeighborsClassifier-0.953, RandomForestClassifier-0.937')


def stage_five():
    estimator1 = KNeighborsClassifier()
    estimator2 = RandomForestClassifier(random_state=40, bootstrap=False, class_weight='balanced')
    param_grid_1 = dict(n_neighbors=[3, 4, 5], weights=['uniform', 'distance'], algorithm=['auto', 'brute'])
    param_grid_2 = dict(n_estimators=[270, 280, 290], max_features=['sqrt', 'log2'], criterion=['entropy', 'gini'])
    grid1 = GridSearchCV(estimator1, param_grid_1, scoring='accuracy', refit=True, n_jobs=-1, verbose=2).fit(x_train_norm, y_train)
    grid2 = GridSearchCV(estimator2, param_grid_2, scoring='accuracy', refit=True, n_jobs=-1, verbose=2).fit(x_train_norm, y_train)
    pred1 = grid1.best_estimator_.predict(x_test_norm)
    score1 = accuracy_score(pred1, y_test)
    pred2 = grid2.best_estimator_.predict(x_test_norm)
    score2 = accuracy_score(pred2, y_test)
    print(f'K-nearest neighbours algorithm \nbest estimator: {grid1.best_estimator_} \naccuracy: {score1}')
    print(f'Random forest algorithm \nbest estimator: {grid2.best_estimator_} \naccuracy: {score2}')


stage_five()
