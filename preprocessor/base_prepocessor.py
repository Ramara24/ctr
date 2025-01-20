import os
from datetime import datetime

import pandas as pd
from sklearn.base import TransformerMixin, BaseEstimator

from pickle_object import PickleObject


class BasePreprocessor(PickleObject, TransformerMixin, BaseEstimator):
    def __init__(self):
        self.X_transformed = None

    def fit(self, X: pd.DataFrame, y=None) -> 'BasePreprocessor':
        """
        Fit the preprocessor to the data.

        Args:
            X (pd.DataFrame): The input data to fit the preprocessor on.
            y (pd.Series): ignored
        """
        return self

    def transform(self, X: pd.DataFrame, y=None) -> pd.DataFrame:
        """
                Transform the input data using the fitted preprocessor.

                Args:
                    X (pd.DataFrame): The input data to transform.

                Returns:
                    pd.DataFrame: The transformed data.
                """
        pass

    def fit_transform(self, X: pd.DataFrame, y=None, **fit_params) -> pd.DataFrame:
        """
        Fit the preprocessor and transform the input data.

        Args:
            X (pd.DataFrame): The input data to fit and transform.

        Returns:
            pd.DataFrame: The transformed data.
        """
        self.fit(X)
        return self.transform(X)

    def save_transformed(self):
        if self.X_transformed is None:
            raise ValueError("No transformed data available")
        (pd.DataFrame(self.X_transformed).
         to_csv(f'{os.getenv('PROJECT_ROOT')}/results/{self.__class__.__name__}-{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv'))