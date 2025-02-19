Stratified sampling
===================

When creating training and test splits for a machine learning model, it is important to maintain the
original distribution of key characteristics present in the data. This ensures that the test set is
representative of the full dataset, preventing biased evaluation and unrealistic performance
estimates. `Stratified sampling <https://en.wikipedia.org/wiki/Stratified_sampling>`__ is a technique
designed exactly for this purpose: it divides the data
into distinct groups (called “strata”) based on certain attributes, and then samples from each group
proportionally, preserving the overall class distribution.

An Example
----------

Imagine you have a dataset where each row represents a person. There are only two columns:

Party Vote: Which political party the person voted for—either Democrat or Republican.
Sex: The person’s sex—Male (M) or Female (F).
Suppose that in the full dataset, 55% are male and 45% are female. If you simply took a random sample
for the test set, you might accidentally end up with a subset that, for example, has a much higher
proportion of males than the original dataset. This skewed distribution could lead to a test set that
does not accurately reflect the population your model is meant to serve.

By using stratified sampling, you first separate the data into two strata: one for males and one for
females. Then, if you decide to create a 20% test set, you draw 20% from the male strata and 20% from
the female strata. This ensures that if your entire dataset is 55% male and 45% female, your test set
will also reflect those same percentages. As a result, your training and test splits more accurately
mirror the original data’s characteristics, providing a fairer and more reliable basis for model
evaluation.

Mathematical details
^^^^^^^^^^^^^^^^^^^^

Assume we have a function :math:`\mathcal{P}` that, given an array, returns a `random permutation <https://numpy.org/doc/stable/reference/random/generated/numpy.random.RandomState.permutation.html>`__ of its elements (an efficient method for generating a permutation is the `Fisher-Yates Shuffle Algorithm <https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle>`__). Here is a step-by-step guide to stratified sampling example above:

1. **Notation:**

   Let the total number of samples be :math:`N`.

   Let the fraction of the dataset we want for the test set be :math:`f`. For example, if we want 20% of the data for testing, :math:`f = 0.2`.

   The dataset consists of two strata (groups): Male (M) and Female (F).

   Let:

   .. math::
      N_M = \text{number of male samples}, \quad N_F = \text{number of female samples}

   Clearly, :math:`N = N_M + N_F`.

2. **Identify Strata:**

   From the dataset, separate the indices of male samples from the indices of female samples. Suppose:

   .. math::
      I_M = [i_1, i_2, \dots, i_{N_M}], \quad I_F = [j_1, j_2, \dots, j_{N_F}]

Applying Stratified Sampling
""""""""""""""""""""""""""""

1. **Determine the Number of Samples per Stratum for the Test Set:**

   Since we want to preserve the original ratio, we take the same fraction :math:`f` from each stratum:

   .. math::
      N_{M,\text{test}} = \lfloor f \cdot N_M \rfloor, \quad N_{F,\text{test}} = \lfloor f \cdot N_F \rfloor

   Here, :math:`\lfloor x \rfloor` denotes the floor function, which rounds :math:`x` down to the nearest integer.

2. **Randomizing Within Each Stratum:**

   Apply a random permutation :math:`\mathcal{P}` to the indices within each stratum to ensure random selection:

   .. math::
      I_M^{\text{perm}} = \mathcal{P}(I_M), \quad I_F^{\text{perm}} = \mathcal{P}(I_F)

3. **Selecting Test and Training Sets:**

   From these permuted arrays, select the first :math:`N_{M,\text{test}}` male indices and the first :math:`N_{F,\text{test}}` female indices for the test set:

   .. math::
      I_{M,\text{test}} = I_M^{\text{perm}}[1 : N_{M,\text{test}}], \quad
      I_{F,\text{test}} = I_F^{\text{perm}}[1 : N_{F,\text{test}}]

   The remaining indices in each stratum go to the training set:

   .. math::
      I_{M,\text{train}} = I_M^{\text{perm}}[N_{M,\text{test}} + 1 : N_M], \quad
      I_{F,\text{train}} = I_F^{\text{perm}}[N_{F,\text{test}} + 1 : N_F]

4. **Combine to Form the Final Sets:**

   Combine the test indices and the training indices:

   .. math::
      I_{\text{test}} = I_{M,\text{test}} \cup I_{F,\text{test}}, \quad
      I_{\text{train}} = I_{M,\text{train}} \cup I_{F,\text{train}}

   Thus, the test set maintains the same proportion of males and females as the full dataset:

   .. math::
      \frac{|I_{M,\text{test}}|}{|I_{\text{test}}|} \approx \frac{N_M}{N}, \quad
      \frac{|I_{F,\text{test}}|}{|I_{\text{test}}|} \approx \frac{N_F}{N}

Summary
"""""""

By splitting the data into strata (in this example, based on sex), and then sampling a proportionate number of elements from each stratum for the test set, we ensure that the test set’s attribute distribution reflects that of the entire dataset. The use of a random permutation ensures random selection within each stratum, and the use of flooring and indexing ensures that the appropriate number of samples from each category is chosen.
