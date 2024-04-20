import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split, KFold
from skopt import BayesSearchCV
from skopt.space import Real, Categorical
from basic_pipeline_functions import PipelineBasic

data_all = pd.read_csv('../data/data.csv')

train, test = train_test_split(data_all, test_size=0.2, random_state=42)

X_train = train.drop(['CREDIT_SCORE', 'DEFAULT'], axis=1)
y_train = train['DEFAULT']

X_test = test.drop(['CREDIT_SCORE', 'DEFAULT'], axis=1)
y_test = test['DEFAULT']

GB_pipeline = Pipeline([
    ('basic_pipeline', PipelineBasic),
    ('pca', PCA()),
    ('classifier', GradientBoostingClassifier(random_state=42))
])

param_space = {
    'pca__n_components': Categorical([23,20,21]),
    'classifier__learning_rate': Real(0.01, 1.0, 'log-uniform'),
    'classifier__n_estimators': Categorical([19, 16, 17]),
    'classifier__max_depth': Categorical([3, 4]),
    'classifier__min_samples_split': Real(0.01, 1.0, 'uniform'),
    'classifier__min_samples_leaf': Real(0.01, 0.5, 'uniform'),
    'classifier__subsample': Real(0.5, 1.0, 'uniform')
}

bayes_search = BayesSearchCV(
    GB_pipeline,
    param_space,
    cv=KFold(n_splits=5, shuffle=True, random_state=42),
    n_iter=100,
    scoring='accuracy',
    random_state=42,
    n_jobs=-1
)

bayes_search.fit(X_train, y_train)

print("Best parameters on cross-validation:", bayes_search.best_params_)
"""
Best parameters on cross-validation: OrderedDict([('classifier__learning_rate', 0.1560845443004789), ('classifier__max_depth', 3), ('classifier__min_samples_leaf', 0.05810811531025969), ('classifier__min_samples_split', 0.40538798008071514), ('classifier__n_estimators', 17), ('classifier__subsample', 0.5), ('pca__n_components', 21)])
"""
