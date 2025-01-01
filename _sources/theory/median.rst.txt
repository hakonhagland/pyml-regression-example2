Median
======

The median is a core measure of central tendency that splits a sorted dataset into two equal parts. To determine the median, first arrange all observations in ascending order. If the number of observations :math:`n` is odd, the median is simply the middle value. For example, in :math:`\{3, 1, 9, 7, 2\}`, sorting yields :math:`\{1, 2, 3, 7, 9\}`, and the median is :math:`3`. If :math:`n` is even, the median is the average of the two central values. For instance, in :math:`\{4, 8, 6, 2\}`, sorting gives :math:`\{2, 4, 6, 8\}`, and the median is :math:`(4 + 6)/2 = 5`.

Mathematically, if :math:`x_1 \le x_2 \le \dots \le x_n` are the sorted data:

.. math::

    \text{Median} = \begin{cases} x_{\frac{n+1}{2}}, & \text{if } n \text{ is odd}, \ \frac{x_{\frac{n}{2}} + x_{\frac{n}{2}+1}}{2}, & \text{if } n \text{ is even}. \end{cases}

Because the median resists the influence of extreme values, it is especially helpful when analyzing skewed datasets.
