Results
=======

Running ``housing-prices plot-histograms`` gives:

.. image:: images/histograms.png
   :alt: Histograms of the numerical features
   :width: 100%

Running ``housing-prices plot-histograms --column-name=median_income`` gives:

.. image:: images/histogram_median_income.png
   :alt: Histogram of the median income
   :width: 100%

Running ``housing-prices stratify-column median_income --bins=0,1.5,3,4.5,6,16`` gives:

.. image:: images/median_income_strat.png
   :alt: Stratified sampling of median income
   :width: 100%
