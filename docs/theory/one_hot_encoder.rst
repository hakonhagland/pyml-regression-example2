OrdinalEncoder and OneHotEncoder
================================

In scikit-learn (and other ML frameworks), both :class:`sklearn.preprocessing.OrdinalEncoder`
and :class:`sklearn.preprocessing.OneHotEncoder` transform categorical features into numeric form.
However, they do so in different ways and are suited for different use cases.

OrdinalEncoder
--------------

* **What it does:**

  Assigns each category an integer value. For example, if a feature has categories
  ``["red", "green", "blue"]``, the OrdinalEncoder might map them to ``[0, 1, 2]``.

* **Key characteristic:**

  - The encoded integers imply an **ordering** among categories (e.g. ``2 > 1 > 0``).
  - This is **not** desirable when there is no inherent ranking (e.g. colors).

* **When to use:**

  - When the feature truly has an ordinal relationship (e.g. shirt sizes: S < M < L).
  - Potentially with tree-based models, which often split on any integer threshold and are less
    sensitive to the numeric nature of categorical codes.
  - **Caution**: If the categories are nominal (like color), using OrdinalEncoder may mislead
    certain algorithms because it introduces a false numeric order.

OneHotEncoder
-------------

* **What it does:**

  Creates a binary (one-hot) column for each category. For a feature with categories
  ``["red", "green", "blue"]``, it produces three new features, e.g.:

  .. code-block:: none

      red   green   blue
      1     0       0
      0     1       0
      0     0       1

* **Key characteristic:**

  - Each category is represented by its own dimension.
  - There is no numeric ordering implied, which avoids introducing false relationships among categories.

* **When to use:**

  - Particularly suitable for models that rely on numeric magnitude or distance (e.g. linear models,
    neural networks).
  - A common default for nominal categorical variables.
  - **Trade-off**: Can lead to high-dimensionality if a feature has many categories.

Why do we need OneHotEncoder?
-----------------------------

Most machine learning models assume that numerical inputs have some sense of distance or order.
Simply encoding categories with integers (e.g. 0, 1, 2) can inadvertently imply that one
category is "greater" than another. OneHotEncoder eliminates this issue by assigning each
category its own column, set to 1 or 0.

This strategy is often crucial for:

- Models like linear/logistic regression that would otherwise treat integer-based categorical
  codes as numeric.
- Preserving the idea that each category is distinct without any rank or magnitude relationship.

Summary
-------

* **OrdinalEncoder:**

  - Good for truly ordered categorical variables (e.g. shirt sizes, ordinal ratings).
  - May be less harmful for tree-based models, which handle integer splits well.
  - Risky if there's no real numeric order.

* **OneHotEncoder:**

  - Often the safer, more generic choice for nominal (unordered) categories.
  - Avoids implying an order or distance between categories.
  - Can lead to a large number of features if the categorical variable has many possible values.
