Ordinary Least Squares
=======================

The Ordinary Least Squares (OLS) method is a technique for estimating the unknown parameters
in a linear regression model. OLS chooses the parameters of a linear function of a set of
explanatory variables by minimizing the sum of the squares of the differences between the
observed dependent variable in the given dataset and those predicted by the linear function.
In other words, it tries to find the line (or hyperplane) that minimizes the sum of the squared
differences between the observed values and the values predicted by the linear approximation.

Example
-------

Assume you have a set of data points :math:`\{(x_1, y_1), (x_2, y_2), \dots, (x_n, y_n)\}`
and you want to find the best line that fits these points in the plane. The equation for the line is of the form:

.. math::

   y = \beta_0 + \beta_1 x

where :math:`\beta_0` is the intercept, :math:`\beta_1` is the slope of the line, :math:`x` is the independent variable, and :math:`y` is the dependent variable.

The goal of ordinary least squares (OLS) is to find the values of :math:`\beta_0` and :math:`\beta_1` that minimize the sum of the squared differences between the observed values :math:`y_i` and the values predicted by the linear approximation :math:`\hat{y}_i`.

For each data point :math:`(x_i, y_i)`, the predicted value :math:`\hat{y}_i` is given by:

.. math::

   \hat{y}_i = \beta_0 + \beta_1 x_i

The residual for each data point is the difference between the observed value and the predicted value:

.. math::

   e_i = y_i - \hat{y}_i

The ordinary least squares method minimizes the sum of the squared residuals:

.. math::
   :label: eq:ols

   S(\beta_0, \beta_1) = \min_{\beta_0, \beta_1} \sum_{i=1}^{n} e_i^2 = \min_{\beta_0, \beta_1} \sum_{i=1}^{n} (y_i - \beta_0 - \beta_1 x_i)^2

To minimize this sum, we take the partial derivatives of :math:`S` with respect to :math:`\beta_0` and :math:`\beta_1` and set them to zero:

.. math::

   \frac{\partial S}{\partial \beta_0} = -2 \sum_{i=1}^{n} (y_i - \beta_0 - \beta_1 x_i) = 0

.. math::

   \frac{\partial S}{\partial \beta_1} = -2 \sum_{i=1}^{n} x_i (y_i - \beta_0 - \beta_1 x_i) = 0


Solving these equations gives the values of :math:`\beta_0` and :math:`\beta_1` that minimize the sum of the squared residuals.

.. math::
   :label: eq:beta_1

   \beta_1 = \frac{\sum_{i=1}^n (x_i - \bar{x})(y_i - \bar{y})}{\sum_{i=1}^n (x_i - \bar{x})^2}

where :math:`\bar{x}` and :math:`\bar{y}` are the means of the independent and dependent variables,
respectively. Once we have :math:`\beta_1`, we can find :math:`\beta_0` using the formula:

.. math::
   :label: eq:beta_0

   \beta_0 = \bar{y} - \beta_1 \bar{x}

Intuitively, we can see :math:`\beta_1` as the slope of the line, and :math:`\beta_0` as the intercept.

You can imagine a cloud of data points scattered on a 2D plot.
The OLS method fits a straight line through these points such that the vertical distances
(errors) between the points and the line are as small as possible on average, and the
squared differences are minimized.

Relationship to the Normal Equations
------------------------------------

Equations :eq:`eq:beta_1` and :eq:`eq:beta_0` can be reformulated as a linear regression problem
leading to the so-called normal equations.
In linear regression, we aim to find a vector of coefficients :math:`\mathbf{w}` that
best fits the data. Given:

* :math:`\mathbf{X}`: the design matrix of shape :math:`(n, p)` where :math:`n` is the number of samples and :math:`p` is the number
  of features

* :math:`\mathbf{y}`: the target vector of shape :math:`(n,)`

* :math:`\mathbf{w}`: the vector of coefficients of shape :math:`(p,)`

Our goal is to find :math:`\mathbf{w}` that minimizes the residual sum of squares (RSS):

.. math::

   \min_w J(w) = \min_w \|Xw - y\|_2^2


Compare this equation with :eq:`eq:ols`. The two equations are equivalent with
:math:`\mathbf{X} = [1, x_1; 1, x_2; \dots; 1, x_n]` and :math:`\mathbf{y} = [y_1, y_2, \dots, y_n]`.
And the solution to the normal equations is the same as the solution to the OLS problem.

The objective function (cost function) :math:`J(w)` represents the sum of squared differences
between the observed targets and the predicted values:

.. math::

   J(w) = (Xw - y)^T (Xw - y)

The expands to:

.. math::

   J(w) = w^T X^T X w - 2 w^T X^T y + y^T y

Note that :math:`y^T y` is a constant with respect to :math:`w` and can be ignored during optimization.

To find the minimum of :math:`J(w)`, we compute its gradient with respect to :math:`w` and set it to zero:

.. math::

   \nabla_w J(w) = 2 X^T X w - 2 X^T y

Setting the gradient to zero to find the critical points:

.. math::

   2 X^T X w - 2 X^T y = 0

Simplify by dividing both sides by 2:

.. math::

   X^T X w = X^T y

This equation is known as the normal equation.

Assuming :math:`X^T X` is invertible (which requires that :math:`X` has full rank),
we can solve for :math:`w`:

.. math::

   w = (X^T X)^{-1} X^T y

This is the closed-form solution to the linear regression problem.
