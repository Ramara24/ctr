from data_loader.base_data_loader import BaseDataLoader


class TrainLoaderSessionSplitter(BaseDataLoader):
    """
    DataLoader with session splitting
    """

    def split_data(self, test_size=0.2, random_state=None) -> tuple:
        """
        Split data into training and test set so that older sessions go to the train and new to the test
        :param test_size: size of test
        :param random_state: ignored
        :return:
        """
        session_timestamps = self.train_data.groupby('session_id')["datetime"].min().reset_index()

        session_timestamps = session_timestamps.sort_values(by='datetime')

        train_size = int(len(session_timestamps) * (1.0 - test_size))

        train_sessions = session_timestamps['session_id'].iloc[:train_size]
        test_sessions = session_timestamps['session_id'].iloc[train_size:]

        train_df = self.train_data[self.train_data['session_id'].isin(train_sessions)].copy()
        test_df = self.train_data[self.train_data['session_id'].isin(test_sessions)].copy(0)

        train_df["day"] = train_df["datetime"].dt.day
        test_df["day"] = test_df["datetime"].dt.day
        train_df.drop(["datetime"], axis=1, inplace=True)
        test_df.drop(["datetime"], axis=1, inplace=True)

        X_train, X_test, y_train, y_test = \
            train_df.drop(columns=['is_click']), test_df.drop(columns=['is_click']), train_df[['is_click']].values.ravel(), \
            test_df[
                ['is_click']].values.ravel()
        return X_train, X_test, y_train, y_test