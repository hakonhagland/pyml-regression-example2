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

Running ``housing-prices geo-pop-scatter`` gives:

.. image:: images/geo-pop-scatter.png
   :alt: Scatter plot of population size and median house value
   :width: 100%

Running ``housing-prices scatter-plot median_house_value,median_income,total_rooms,housing_median_age``
gives:

.. image:: images/scatter-matrix.png
   :alt: Scatter matrix plot of median house value, median income, total rooms, and housing median age
   :width: 100%

Running ``housing-prices scatter-plot median_income,median_house_value`` gives:

.. image:: images/scatter-median_income-median_house_value.png
   :alt: Scatter plot of median income and median house value
   :width: 100%
