from sklearn.model_selection import KFold, StratifiedKFold, ParameterGrid
from sklearn.metrics import accuracy_score
from sklearn.base import clone
import numpy as np
import pandas as pd
from util import calculate_disparate_impact, calculate_statistical_parity_difference

class BiasAwareGridSearchCV:
    def __init__(self, estimator, param_grid, df, outcome_column, protected_attribute, privileged_value, unprivileged_value, cv=5):
        """
        Initializes the BiasAwareGridSearchCV object.

        Args:
            estimator: The machine learning estimator to use.
            param_grid: Dictionary with parameters names as keys and lists of parameter settings to try as values.
            df: DataFrame containing the training data.
            outcome_column: Name of the target column in df.
            protected_attribute: Name of the column representing the protected attribute.
            privileged_value: The value in the protected attribute column that represents the privileged group.
            unprivileged_value: The value in the protected attribute column that represents the unprivileged group.
            cv: Number of folds to use for cross-validation.
        """
        self.estimator = estimator
        self.param_grid = param_grid
        self.df = df
        self.outcome_column = outcome_column
        self.protected_attribute = protected_attribute
        self.privileged_value = privileged_value
        self.unprivileged_value = unprivileged_value
        self.cv = cv
        self.results_ = []

    def fit(self, X_train, y_train):
        """
        Runs the grid search with cross-validation over the specified parameter grid, evaluating models for accuracy and bias.

        Args:
            X_train: DataFrame containing the features from the training data.
            y_train: Series or array-like containing the target variable from the training data.
        """
        kf = KFold(n_splits=self.cv)
        for params in ParameterGrid(self.param_grid):
            accuracies = []
            biases = []

            for train_index, val_index in kf.split(X_train):
                X_train_fold, X_val_fold = X_train.iloc[train_index], X_train.iloc[val_index]
                y_train_fold, y_val_fold = y_train.iloc[train_index], y_train.iloc[val_index]

                model = clone(self.estimator)
                model.set_params(**params)
                model.fit(X_train_fold, y_train_fold)
                preds = model.predict(X_val_fold)

                accuracy = accuracy_score(y_val_fold, preds)
                accuracies.append(accuracy)
                
                # Extract protected attribute for bias calculation
                protected_attr_val = X_val_fold[self.protected_attribute]
                temp_df = pd.DataFrame({self.outcome_column: y_val_fold, self.protected_attribute: protected_attr_val})
                temp_df[self.outcome_column + '_pred'] = preds
                bias = calculate_disparate_impact(temp_df, self.outcome_column + '_pred', self.protected_attribute, self.privileged_value, self.unprivileged_value)
                biases.append(bias)

            avg_accuracy = np.mean(accuracies)
            avg_bias = np.mean(biases)

            self.results_.append({
                'params': params,
                'accuracy': avg_accuracy,
                'bias': avg_bias
            })


    def select_highest_accuracy_model(self):
        """
        Selects and retrains the model with the highest accuracy from the grid search results.

        Returns:
            The model with the highest accuracy.
        """
        best_params = max(self.results_, key=lambda x: x['accuracy'])['params']
        return self._retrain_model(best_params)

    def select_least_biased_model(self):
        """
        Selects and retrains the model with the least bias from the grid search results.

        Returns:
            The model with the least bias.
        """
        best_params = min(self.results_, key=lambda x: x['bias'])['params']
        return self._retrain_model(best_params)

    def select_balanced_model(self, threshold):
        """
        Selects and retrains the model with the least bias among the top 'threshold' models with the highest accuracy.

        Args:
            threshold: The number of top models to consider based on accuracy.
        Returns:
            The model with the least bias among the top models based on accuracy.
        """
        top_accurate_models = sorted(self.results_, key=lambda x: x['accuracy'], reverse=True)[:threshold]
        best_params = min(top_accurate_models, key=lambda x: x['bias'])['params']
        return self._retrain_model(best_params)

    def _retrain_model(self, params):
        """
        Retrains the model using the given parameters on the full dataset.

        Args:
            params: The parameters to use for the model.
        Returns:
            The retrained model.
        """
        model = clone(self.estimator)
        model.set_params(**params)
        model.fit(self.df.drop(columns=[self.outcome_column]), self.df[self.outcome_column])
        return model

    def find_optimum_model(self, margin):
        pass
