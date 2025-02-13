import os.path
import numpy as np
from constants import getroot
from data_loader.train_loader_session_splitter import TrainLoaderSessionSplitter
from pipeline.base_model_pipeline import BaseModelPipeline
from preprocessor.fill_na_preprocessor import FillNaPreprocessor

RESULT_PATH = 'Lisa005'

if __name__ == '__main__':
    data_loader = TrainLoaderSessionSplitter(result_path=RESULT_PATH,
                                             train_file=os.path.join(getroot(), "data/train_dataset_full.csv"),
                                             preprocessing=BaseModelPipeline(steps=[ FillNaPreprocessor()]))
    data_loader.load_data()
    X_train, X_test, y_train, y_test = data_loader.split_data()
    y_train = np.where(y_train, y_train>0, -1)
    data_loader.dump_to_pickle()
    pipeline: BaseModelPipeline = BaseModelPipeline.load_pickle('/Users/lisapolotskaia/PycharmProjects/ctr/results/Lisa004/BaseModelPipeline-20250127_184219.pkl')
    pipeline.grid_search(X_train, y_train, cv=3, )
    pipeline.dump_to_pickle()
    pipeline.dump_results()
