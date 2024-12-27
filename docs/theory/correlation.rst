Introduction to Correlation
===========================

When studying relationships between two variables, we often want to know
if changes in one variable are associated with changes in the other.
This idea is captured by the concept of **correlation**. Correlation gives
us a way to describe how two variables move together—or fail to move together—
in a population of interest.

Imagine we consider the entire population of adults in a large country.
We focus on two variables: their height and their weight. Intuitively,
we might expect that taller individuals tend to be heavier. If we took
the time to measure every adult's height and weight (the population),
we could then look at all these data points at once. On a scatter plot,
each point would represent one person: their height on the horizontal axis
and their weight on the vertical axis. If, as we move from shorter to taller
individuals, we generally see weights increasing, we can say that there is
a **positive correlation** between height and weight in this population.

Of course, not every tall person is heavy, nor every short person light.
But what matters is the overall trend across the entire population. If
we observe this general pattern—taller often means heavier—then these two
variables are positively correlated. Conversely, if we found a situation
where increasing one variable is generally associated with a decrease in
the other (imagine the relationship between how far you travel and how
much time you have left in a fuel tank), we'd say there is a **negative
correlation**.

By starting with the entire population, we're talking about a property of
the "real world" as it exists. In practice, we rarely have the luxury
of measuring every single individual. Instead, we often work with just
a subset of the population, known as a *sample*. Later, we'll discuss
how we estimate correlation from a sample and how this relates to the
"true" correlation of the entire population.

.. note::

   In more formal terms, correlation can be expressed mathematically,
   and its value is always between -1 and 1. A value close to +1
   indicates a strong positive relationship, near -1 indicates a strong
   negative relationship, and around 0 indicates little to no linear
   relationship. We’ll introduce these formal definitions, along with
   the concept of covariance and Pearson’s correlation coefficient, after
   we’ve built a solid intuitive understanding.

Random Variables
----------------

When we study statistics, we often deal with *random variables*. A random variable
is simply a variable whose value results from some random process. For instance,
if we randomly select an adult from a population, that person's height (in cm)
can be viewed as a random variable, which we might denote :math:`X`.

- :math:`X` takes on different values depending on which individual is selected.
- Similarly, a person's weight (in kg) might be denoted :math:`Y`, and it too
  changes from person to person.

From a population perspective, you can think of :math:`X` and :math:`Y` as having
a certain distribution across all individuals. We typically focus on their
mean (average) values and other properties that describe how these variables
fluctuate.

Expectation
-----------

The *expectation* or *expected value* of a random variable (often thought of as
the *mean*) is denoted :math:`E[X]`. Conceptually, if you could measure the height
(:math:`X`) of *every* person in the population or repeat your random selection
many times, :math:`E[X]` is the long-run average of those measurements.

Mathematically, for a discrete random variable :math:`X`, the expectation is:

.. math::

   E[X] = \sum_{x} x \, P(X = x)

For a continuous random variable, it's given by an integral:

.. math::

   E[X] = \int_{-\infty}^{\infty} x \, f_X(x) \, dx

where :math:`f_X(x)` is the probability density function (PDF) of :math:`X`.

Covariance
----------

Once we understand that each of :math:`X` and :math:`Y` has an expectation,
we can measure how these two variables *co-vary*—that is, how they move together.
The **covariance** of :math:`X` and :math:`Y`, denoted :math:`\mathrm{Cov}(X, Y)`,
is defined as the expected value of the product of their deviations from their
means:

.. math::

   \mathrm{Cov}(X, Y) = E\big[(X - E[X])(Y - E[Y])\big].

Intuitively:

- If :math:`X` and :math:`Y` tend to increase and decrease together, the product
  :math:`(X - E[X])(Y - E[Y])` will often be positive, leading to a positive
  covariance.

- If one variable goes up when the other tends to go down, the product of their
  deviations will often be negative, leading to a negative covariance.

- If there's no clear pattern in how they move together, the product of their
  deviations will roughly balance out over repeated observations, and the
  covariance will be close to zero.

Connecting Covariance to Correlation
------------------------------------

While covariance tells us if two variables move together (positive covariance) or
in opposite directions (negative covariance), its numerical value depends on the
units of the original variables. For example, measuring height in centimeters vs.
meters changes the scale of the covariance. This is why **Pearson’s correlation
coefficient** becomes useful: it is the standardized version of covariance, always
ranging between -1 and +1, thus making it easier to compare relationships across
different variables and scales.

.. note::
   We'll discuss Pearson’s correlation coefficient in more detail shortly, but
   remember that it's defined as the covariance of :math:`X` and :math:`Y`, divided
   by the product of their standard deviations:

   .. math::

      \rho = \frac{\mathrm{Cov}(X, Y)}{\sqrt{\mathrm{Var}(X) \mathrm{Var}(Y)}}.

   Here, :math:`\rho` is the population correlation, and it serves as a scale-invariant
   measure of linear association between the two variables.

Pearson’s Correlation Coefficient (Population)
==============================================

Recall from the definition of *covariance* that for two random variables
:math:`X` and :math:`Y`:

.. math::

   \mathrm{Cov}(X, Y) = E\big[(X - E[X])(Y - E[Y])\big].

We can also define the *variance* of a random variable :math:`X` as:

.. math::

   \mathrm{Var}(X) = E\big[(X - E[X])^2\big].

The **population Pearson’s correlation coefficient**, denoted by
:math:`\rho(X, Y)` or simply :math:`\rho`, standardizes covariance by
dividing by the product of the variables’ standard deviations
(:math:`\sqrt{\mathrm{Var}(X)}` and :math:`\sqrt{\mathrm{Var}(Y)}`):

.. math::

   \rho(X, Y) \;=\; \frac{\mathrm{Cov}(X, Y)}
                         {\sqrt{\mathrm{Var}(X)}\;\sqrt{\mathrm{Var}(Y)}}.

Substituting the expectation-based definitions of covariance and variance,
we can write:

.. math::

   \rho(X, Y)
   \;=\; \frac{ E\big[(X - E[X])(Y - E[Y])\big] }
               { \sqrt{ E\big[(X - E[X])^2\big] } \;\sqrt{ E\big[(Y - E[Y])^2\big] } }.

Interpretation
--------------

- :math:`\rho(X, Y)` takes values in :math:`[-1, 1]`.
- A value of :math:`+1` indicates a *perfect* positive linear relationship
  between :math:`X` and :math:`Y`.
- A value of :math:`-1` indicates a *perfect* negative linear relationship.
- A value of :math:`0` indicates *no* linear relationship. (Note that
  :math:`X` and :math:`Y` could still be related in a non-linear way.)

Why Standardize Covariance?
---------------------------

Covariance by itself can be hard to compare across different variable
scales. For example, if you measure height in meters instead of centimeters,
the covariance changes numerically—even though the *underlying* relationship
has not. By dividing by the product of the standard deviations of :math:`X`
and :math:`Y`, the Pearson correlation coefficient makes the result
*dimensionless*, facilitating comparisons across different variables and
datasets.

In the next section, we’ll discuss how we estimate :math:`\rho(X, Y)` with
sample data, which is typically what we do in real-world scenarios.

Sample Correlation
==================

In practice, we often do not have access to every individual in a population.
Instead, we collect data from a *sample* of size :math:`n`. Suppose we have
paired observations:

.. math::

   \{(x_1, y_1), (x_2, y_2), \dots, (x_n, y_n)\}

where :math:`x_i` might represent the height of the :math:`i`-th individual
in your sample, and :math:`y_i` might represent their weight.

Just as we defined *population covariance* and *population correlation*
in terms of expectations, we define *sample* versions by replacing
expectations with *sample means* (averages), and by summing over the finite
set of sampled data points.

Sample Means
------------

The sample mean of the :math:`x` values is:

.. math::

   \bar{x} \;=\; \frac{1}{n} \sum_{i=1}^{n} x_i,

and similarly, the sample mean of the :math:`y` values is:

.. math::

   \bar{y} \;=\; \frac{1}{n} \sum_{i=1}^{n} y_i.

Sample Covariance
-----------------

Recall that population covariance is defined by

.. math::

   \mathrm{Cov}(X, Y)
   = E\big[ (X - E[X])(Y - E[Y]) \big].

In the sample context, we approximate the expectation :math:`E[\cdot]`
by averaging over our sampled data points. Therefore, the **sample covariance**
of :math:`x` and :math:`y`, denoted by :math:`\widehat{\mathrm{Cov}}(x, y)`, is:

.. math::

   \widehat{\mathrm{Cov}}(x, y)
   \;=\; \frac{1}{n - 1} \sum_{i=1}^{n}
         (x_i - \bar{x}) \,(y_i - \bar{y}).

Why :math:`n-1` instead of :math:`n`?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Statisticians use :math:`n-1` in the denominator to make
:math:`\widehat{\mathrm{Cov}}` (and likewise the sample variance) an
*unbiased* estimator of the true population covariance. This detail stems
from more advanced probability theory, but intuitively, using :math:`n`
would systematically *underestimate* the variability in the sample.

Sample Variances
----------------

Likewise, we approximate each variable’s variance by

.. math::

   \widehat{\mathrm{Var}}(x)
   \;=\; \frac{1}{n - 1} \sum_{i=1}^{n} (x_i - \bar{x})^2,

.. math::

   \widehat{\mathrm{Var}}(y)
   \;=\; \frac{1}{n - 1} \sum_{i=1}^{n} (y_i - \bar{y})^2.

Sample Pearson’s Correlation Coefficient
----------------------------------------

By analogy with the population correlation

.. math::

   \rho(X, Y)
   \;=\; \frac{\mathrm{Cov}(X, Y)}
               {\sqrt{\mathrm{Var}(X) \,\mathrm{Var}(Y)}},

we define the **sample correlation** coefficient, denoted by :math:`r`:

.. math::

   r
   \;=\; \frac{\widehat{\mathrm{Cov}}(x, y)}
               {\sqrt{\widehat{\mathrm{Var}}(x)} \,\sqrt{\widehat{\mathrm{Var}}(y)}}.

Substituting the definitions of sample covariance and variance, this becomes:

.. math::

   r
   \;=\; \frac{\frac{1}{n-1}\,\sum_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})}
               {\sqrt{\frac{1}{n-1}\,\sum_{i=1}^{n} (x_i - \bar{x})^2}
                \;\sqrt{\frac{1}{n-1}\,\sum_{i=1}^{n} (y_i - \bar{y})^2}}.

Notice that the factor of :math:`1/(n-1)` appears in both numerator and denominator
and effectively cancels in the fraction. Hence, you’ll often see the sample
correlation coefficient written as:

.. math::

   r
   = \frac{\sum_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})}
           {\sqrt{\sum_{i=1}^{n} (x_i - \bar{x})^2}\,
            \sqrt{\sum_{i=1}^{n} (y_i - \bar{y})^2}}.

Interpretation
--------------

1. :math:`r` always lies between -1 and +1, just like the population correlation
   :math:`\rho`.
2. A value close to +1 indicates a strong positive linear relationship; close to
   -1 indicates a strong negative linear relationship; and values near 0 suggest
   little to no *linear* relationship between :math:`x` and :math:`y` in the sample.
3. Keep in mind that this is an *estimate* based on the sample: the true population
   correlation might be slightly (or drastically) different.

In summary, the sample correlation coefficient is *conceptually the same measure*
as the population correlation—how two variables vary together, standardized by
their respective variances—but uses the sample data’s deviations from their own
means as a stand-in for the true (and often unknown) population parameter.
