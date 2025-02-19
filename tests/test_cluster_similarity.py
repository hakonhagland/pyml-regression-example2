import typing

import pandas as pd

from housing_prices.cluster_similarity import ClusterSimilarity
from housing_prices.config import Config
import housing_prices.helpers as helpers
from .common import PrepareConfigDir, PrepareDataDir


class TestCreateObject:
    def test_feature_names_out(
        self,
        prepare_config_dir: PrepareConfigDir,
        prepare_data_dir: PrepareDataDir,
    ) -> None:
        prepare_data_dir(datafiles_exists=True, housing_csv=True)
        prepare_config_dir(add_config_ini=True)
        config = Config()
        housing = helpers.get_housing_data(config, download=True)
        housing = typing.cast(pd.DataFrame, housing)
        data = housing[["latitude", "longitude"]]
        num_clusters = 10
        gamma = 1.0
        cluster_similarity = ClusterSimilarity(num_clusters, gamma)
        cluster_similarity.fit_transform(data)
        # centers = cluster_similarity.kmeans_.cluster_centers_
        feature_names = cluster_similarity.get_feature_names_out()
        assert len(feature_names) == num_clusters
        assert feature_names[0] == "Cluster 0 similarity"
