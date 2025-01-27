import pandas as pd
from preprocessor.base_prepocessor import BasePreprocessor
import random
from sklearn.base import TransformerMixin
import numpy as np

class Undersampler(BasePreprocessor, TransformerMixin):
    """
    the preprocessor that keeps all is_click=1 rows and samples is_click=0
    """
    def __init__(self, sample_number=None, return_splited=False,target_column = 'is_click', positive_value=1, negative_value=0, random_state=42):
        super().__init__()
        self.preprocessor_name = 'UnderSampler'
        self.target_column = target_column
        self.sample_number = sample_number
        self.return_splited = return_splited
        self.df = pd.DataFrame()
        self.positive_value = positive_value
        self.negative_value = negative_value
        self.random_state = random_state

    def fit(self, X: pd.DataFrame, y: np.array = None):
        self.df = X.copy(deep=True)
        if y is not None:
            self.df[self.target_column] = y
        return self

    def transform(self, X: pd.DataFrame=None, y=None):
        if self.target_column is None:
            self.target_column = self.df.columns[-1]
        only_1 = self.df.loc[self.df[self.target_column]==self.positive_value]
        if self.sample_number is not None:
            only_0 = self.df.loc[self.df[self.target_column] == self.negative_value]
            if isinstance(self.sample_number, int):
                only_0 = only_0.sample(frac=1, random_state = self.random_state).head(self.sample_number)
            elif isinstance(self.sample_number, float):
                only_0 = only_0.sample(frac=self.sample_number,  random_state = self.random_state)
        else:
            available_0s = self.df.loc[self.df[self.target_column]==self.negative_value]
            available_length = min(len(only_1), available_0s.shape[0])
            only_0 = pd.DataFrame(available_0s.sample(frac=1,random_state = self.random_state).head(available_length))
        transformed_df = pd.concat([only_1, only_0])
        transformed_df = transformed_df.sample(frac=1)
        if self.return_splited:
            return transformed_df[[column for column in transformed_df.columns if column!= self.target_column]], transformed_df[self.target_column]
        else:
            return transformed_df