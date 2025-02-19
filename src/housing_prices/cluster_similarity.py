import numpy as np
import pandas as pd

import sklearn.cluster  # type: ignore
import sklearn.metrics.pairwise  # type: ignore
from numpy.typing import NDArray

from sklearn.base import BaseEstimator, TransformerMixin  # type: ignore


class ClusterSimilarity(BaseEstimator, TransformerMixin):  # type: ignore
    def __init__(
        self, n_clusters: int = 10, gamma: float = 1.0, random_state: int = 42
    ):
        self.n_clusters = n_clusters
        self.gamma = gamma
        self.random_state = random_state

    def fit(self, X, y=None, sample_weight=None):  # type: ignore
        self.kmeans_ = sklearn.cluster.KMeans(
            self.n_clusters, n_init=10, random_state=self.random_state
        )
        # This will set self.kmeans_.cluster_centers_ to an m x n array, where m is the number
        # of clusters and n is the number of features in X
        self.kmeans_.fit(X, sample_weight=sample_weight)
        return self  # always return self!

    def transform(self, X):  # type: ignore
        # If X is an m x n array, and self.kmeans_.cluster_centers_ is an p x n array,
        # the result Y will be an m x p array. For example, if X contain two features,
        # each with 20640 samples (so X is 20640 x 2), and self.kmeans_.cluster_centers_ is
        # 10 x 2 (10 cluster in 2D space), then Y will be 20640 x 10. And Y[i, j] will be
        # the similarity between sample i in X and cluster j.
        return sklearn.metrics.pairwise.rbf_kernel(
            X, self.kmeans_.cluster_centers_, gamma=self.gamma
        )

    def get_feature_names_out(self, names=None) -> list[str]:  # type: ignore
        return [f"Cluster {i} similarity" for i in range(self.n_clusters)]


def transform(
    housing: pd.DataFrame, num_clusters: int, gamma: float
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Transform the housing data using the specified number of clusters and gamma value."""
    # Perform clustering
    cluster_similarity = ClusterSimilarity(n_clusters=num_clusters, gamma=gamma)
    data = housing[["latitude", "longitude"]]
    similarity = cluster_similarity.fit_transform(data)
    centers = cluster_similarity.kmeans_.cluster_centers_
    return similarity, centers
