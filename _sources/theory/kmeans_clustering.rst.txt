The K-means clustering algorithm
================================

The :class:`sklearn.cluster.KMeans` algorithm clusters data by trying to
separate samples into :math:`n` groups of equal variance, minimizing a
criterion known as the *inertia* or *within-cluster sum-of-squares* (see below).
This algorithm requires the number of clusters to be specified. It scales well
to large numbers of samples and has been used across a large range of
application areas in many different fields.

The k-means algorithm divides a set of :math:`n` samples
:math:`\{x_1, x_2, \dots, x_n\}` into :math:`k` disjoint clusters
:math:`C_1, C_2, \dots, C_k`, each described by the mean
:math:`\mu_j` of the samples in that cluster:

.. math::

   \mu_j = \frac{1}{\lvert C_j \rvert} \sum_{x \in C_j} x.

These means are commonly called the cluster *centroids*.

The K-means objective and computational difficulty
--------------------------------------------------

The goal of the K-means algorithm is to partition :math:`n` data points into
:math:`k` clusters in such a way as to minimize the *within-cluster sum-of-squares*.
Formally, we seek to solve the following minimization problem:

.. math::

   \min_{C_1, \ldots, C_k} \sum_{j=1}^k \sum_{x \in C_j} \lVert x - \mu_j \rVert^2,

where :math:`\mu_j` is the mean (or *centroid*) of cluster :math:`C_j`. This
is equivalent to minimizing the pairwise squared deviations of the points within
each cluster. While straightforward to formulate, this problem is known to be
NP-hard in the general case. Nonetheless, efficient heuristic algorithms have
been developed that converge quickly in practice to a *local optimum*, which
is typically sufficient for many applications.

History and variants of the Lloyd algorithm
-------------------------------------------

One of the most common and conceptually simple heuristics for K-means clustering
is known as the *Lloyd algorithm*, first proposed by Stuart Lloyd in 1957 (though
not published until 1982). Essentially, it works as an iterative refinement
technique and is also sometimes referred to as the "classical" or "vanilla"
K-means algorithm.

In :class:`sklearn.cluster.KMeans`, you can choose between two algorithms:

* ``lloyd``: This is the standard implementation of Lloyd's algorithm (the default).
* ``elkan``: This is a variant that makes use of the triangle inequality and can
  be much faster for certain datasets, especially those with well-separated
  clusters.

For most users, ``lloyd`` is a sensible default. If you find that K-means is
slow on your data, it may be worth trying ``elkan``.

Outline of the Lloyd algorithm
------------------------------

The Lloyd algorithm starts with an initial set of :math:`k` means, typically
chosen by the *k-means++* method (the default in scikit-learn). We can denote
these initial means as

.. math::

   m_1^{(1)}, m_2^{(1)}, \ldots, m_k^{(1)}.

The algorithm then proceeds by alternating between two main steps:

1. **Assignment step**:

   In this step, each data point is assigned to the cluster whose current centroid
   is nearest in terms of Euclidean distance. Mathematically, for each data point
   :math:`x_i`, we find the cluster index :math:`j` such that

   .. math::

      j = \underset{1 \leq \ell \leq k}{\mathrm{argmin}} \,
      \lVert x_i - m_\ell^{(t)} \rVert^2,

   where :math:`m_\ell^{(t)}` is the centroid of cluster :math:`\ell` at iteration
   :math:`t`.

   All data points thus get *re-labeled* into the cluster with the closest centroid.

2. **Update step**:

   Once every data point has been assigned to a cluster, the centroids are
   recalculated as the mean of the points currently in that cluster. That is, for
   each cluster :math:`C_j^{(t)}`, we compute the new centroid as

   .. math::

      m_j^{(t+1)} = \frac{1}{\lvert C_j^{(t)} \rvert} \sum_{x \in C_j^{(t)}} x.

These two steps alternate until convergence, which typically means that cluster
assignments no longer change, or the changes fall below a user-specified tolerance,
or a maximum number of iterations is reached.

Although the algorithm only guarantees convergence to a local optimum, in practice,
it often yields good clusterings. The default *k-means++* initialization in
scikit-learn also helps improve the chances of reaching a better local optimum
and generally speeds up convergence.
