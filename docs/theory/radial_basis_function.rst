Radial Basis Functions (RBF)
============================

We can measure how *similar* two data points are by using a *kernel function*. One such kernel is the **Radial Basis Function** (RBF), sometimes also called the Gaussian kernel.

.. math::
   K(\mathbf{x}, \mathbf{y}) = \exp(-\gamma \|\mathbf{x} - \mathbf{y}\|^2)

where:

- :math:`\mathbf{x}` and :math:`\mathbf{y}` are feature vectors (points in some input space).
- :math:`\|\mathbf{x} - \mathbf{y}\|^2` is the squared Euclidean distance between :math:`\mathbf{x}` and :math:`\mathbf{y}`.
- :math:`\gamma` (gamma) is a parameter that controls how quickly the similarity measure decreases with distance.

In more intuitive terms, the RBF kernel outputs values close to 1 for two points that are very close together in the feature space, and values close to 0 for points that are far apart. This makes it a useful tool for measuring the “closeness” or “similarity” of data samples and is often used in algorithms where we want to capture complex, non-linear relationships.

Using ``sklearn.metrics.pairwise.rbf_kernel``
---------------------------------------------

The ``scikit-learn`` library provides the function :func:`sklearn.metrics.pairwise.rbf_kernel` to compute the RBF kernel (similarities) between sets of points. This function is useful when you want to compute the RBF kernel between two sets of points (e.g., two datasets) or between a set of points and a single reference point.

Basic usage:

.. code-block:: python

   from sklearn.metrics.pairwise import rbf_kernel

   # Suppose X and Y are NumPy arrays of shape (n_samples_x, n_features)
   # and (n_samples_y, n_features) respectively:
   similarity_matrix = rbf_kernel(X, Y, gamma=0.5)

Here, ``similarity_matrix`` will be a matrix where each entry ``similarity_matrix[i, j]`` is :math:`K(\mathbf{x}_i, \mathbf{y}_j)`.

Example with Pandas: Creating a New Similarity Feature
------------------------------------------------------

Let’s walk through a simple example where we have a Pandas ``DataFrame``, and we want to create a new column that measures how similar each value in one column is to a particular *reference value* (scalar) under the RBF kernel.

For instance, imagine we have a dataset with a numeric column called ``"height"``. We decide we want to create a feature that measures how similar each row’s ``height`` is to a *single* reference value (say, ``170 cm``). We can treat the reference value as a single-point array and compute the RBF similarity.

.. code-block:: python

   import pandas as pd
   import numpy as np
   from sklearn.metrics.pairwise import rbf_kernel

   # Example data
   df = pd.DataFrame({
       'height': [160, 165, 170, 175, 180, 185]
   })

   # Convert height column to a 2D array (n_samples, n_features)
   X = df[['height']].values  # shape: (6, 1)

   # We'll define a reference value (Y) as a single-point array
   reference_value = np.array([[170]])  # shape: (1, 1)

   # Choose a gamma value (this controls how quickly similarity decays with distance)
   gamma = 0.1

   # Compute RBF similarities
   # rbf_kernel(X, reference_value) returns shape: (6, 1)
   similarity_values = rbf_kernel(X, reference_value, gamma=gamma)

   # Flatten the result so it's easier to put back into the DataFrame
   df['height_similarity_to_170'] = similarity_values.flatten()

   print(df)

In this snippet:

1. We extract the ``height`` column as ``X`` (2D array).
2. We define our reference value ``Y`` as a single-row array containing ``170``.
3. We compute the RBF similarity between each row’s height and ``170`` using ``rbf_kernel``.
4. We store the result in a new column called ``height_similarity_to_170``.

So, if :math:`h_i` is the height at row :math:`i`, then each entry in our new column is:

.. math::
   \mathrm{similarity}_i = \exp\bigl(-\gamma (h_i - 170)^2\bigr)

A few notes:

- If :math:`\gamma` is large, then even relatively small differences :math:`(h_i - 170)` will cause the RBF value to drop quickly.
- If :math:`\gamma` is small, the RBF values will decay more slowly, and points farther from ``170`` will still have relatively high similarity.
