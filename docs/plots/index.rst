*************
Visualisation
*************

Overview
========

Sherpa has support for different plot backends, at present limited
to matplotlib and Crates. Interactive visualizations of images is
provided by DS9 - an Astronomical image viewer - if installed.

There is limited support for visualizing two-dimensional data sets
with matplotlib.

.. note::

   The `sherpa.plot` module also includes error-estimation
   routines, such as the `IntervalProjection` class. This is mixing
   analysis with visualization, which may not be ideal.

Reference/API
=============

.. note::
   
   If the
   `DS9 <http://ds9.si.edu/site/Home.html>`_ image viewer is installed,
   image data can be viewed using the classes in the
   ``sherpa.image`` module.

.. automodapi:: sherpa.plot
.. automodapi:: sherpa.image




