
******************
What is to be fit?
******************

The Sherpa :py:class:`~sherpa.data.Data` class is used to
carry around the data to be fit: this includes the independent
axis (or axes), the dependent axis (the data), and any
necessary metadata. Although the design of Sherpa supports
multiple-dimensional data sets, the current classes only
support one- and two-dimensional data sets.

Overview
========

The following modules are assumed to have been imported:

.. sherpa::

   In [1]: import numpy as np

   In [1]: import matplotlib.pyplot as plt

   In [1]: from sherpa import data

   In [1]: from sherpa.stats import LeastSq

   In [1]: from sherpa.optmethods import LevMar

Names
-----

The first argument to any of the Data classes is the name
of the data set. This is used for display purposes only,
and can be useful to identify which data set is in use.
It is stored in the ``name`` attribute of the object, and
can be changed at any time.

The independent axis
--------------------

The independent axis - or axes - of a data set define the
grid over which the model is to be evaluated. It is referred
to as ``x``, ``x0``, ``x1``, ... depending on the dimensionality
of the data (for
:ref:`binned datasets <data_binned>` there are ``lo``
and ``hi`` variants).

Although dense multi-dimensional data sets can be stored as
arrays with dimensionality greater than one, the internal
representation used by Sherpa is often a flattened - i.e.
one-dimensional - version.

The dependent axis
------------------

This refers to the data being fit, and is referred to as ``y``.

.. _data_unbinned:
   
Unbinned data
+++++++++++++

Unbinned data sets - defined by classes which do not end in
the name ``Int`` - represent point values; that is, the the data
value is the value at the coordinates given by the independent
axis.
Examples of unbinned data classes are
:py:class:`~sherpa.data.Data1D` and :py:class:`~sherpa.data.Data2D`.

.. sherpa::

   In [1]: np.random.seed(0)

   In [1]: x = np.arange(20, 40, 0.5)

   In [1]: y = x**2 + np.random.normal(0, 10, size=x.size)

   In [1]: d1 = data.Data1D('test', x, y)

   In [1]: print(d1)
   
.. _data_binned:
   
Binned data
+++++++++++

Binned data sets represent values that are defined over a range,
such as a histogram.
The integrated model classes end in ``Int``: examples are
:py:class:`~sherpa.data.Data1DInt`
and :py:class:`~sherpa.data.Data2DInt`.

It can be a useful optimisation to treat a binned data set as
an unbinned one, since it avoids having to estimate the integral
of the model over each bin. It depends in part on how the bin
size compares to the scale over which the model changes.

.. sherpa::

   In [1]: z = np.random.gamma(20, scale=0.5, size=1000)

   In [1]: (y, edges) = np.histogram(z)

   In [1]: d2 = data.Data1DInt('gamma', edges[:-1], edges[1:], y)

   In [1]: print(d2)

   @savefig data_data2d.png width=8in
   In [1]: plt.bar(d2.xlo, d2.y, d2.xhi - d2.xlo);

.. sherpa::
   :suppress:

   In [1]: plt.clf()

Errors
------

There is support for both statistical and systematic
errors by either using the ``staterror`` and ``syserror``
parameters when creating the data object, or by changing the
:py:attr:`~sherpa.data.Data.staterror` and
:py:attr:`~sherpa.data.Data.syserror` attributes of the object.

.. _data_filter:

Filtering data
--------------

Sherpa supports filtering data sets; that is, temporarily removing
parts of the data (perhaps because there are problems, or to help
restrict parameter values).

The :py:attr:`~sherpa.data.BaseData.mask` attribute indicates
whether a filter has been applied: if it returns ``True`` then
no filter is set, otherwise it is a bool array
where ``False`` values indicate those elements that are to be
ignored. The :py:meth:`~sherpa.data.BaseData.ignore` and
:py:meth:`~sherpa.data.BaseData.notice` methods are used to
define the ranges to exclude or include. For example, the following
hides those values where the independent axis values are between
21.2 and 22.8:

.. sherpa::

   In [1]: d1.ignore(21.2, 22.8)

   In [1]: d1.x[np.invert(d1.mask)]

After this, a fit to the data will ignore these values, as shown
below, where the number of degrees of freedom of the first fit,
which uses the filtered data, is three less than the fit to the
full data set (the call to
:py:meth:`~sherpa.data.BaseData.notice` removes the filter since
no arguments were given):

.. sherpa::

   In [1]: from sherpa.models import Polynom1D

   In [1]: mdl = Polynom1D()

   In [1]: mdl.c2.thaw()

   In [1]: from sherpa.fit import Fit
   
   In [1]: fit = Fit(d1, mdl, stat=LeastSq(), method=LevMar())

   In [1]: res1 = fit.fit()

   In [1]: d1.notice()

   In [1]: res2 = fit.fit()

   In [1]: print("Degrees of freedom: {} vs {}".format(res1.dof, res2.dof))
   
.. note::
   
   It's a bit confusing since not always clear where a given
   attribute or method is defined. There's also get_filter/get_filter_expr
   to deal with. Also filter/apply_filter.

.. _data_visualize:

Visualizing a data set
----------------------

The data objects contain several methods which can be used to
visualize the data, but do not provide any direct plotting
or display capabilities. The
:py:meth:`~sherpa.data.Data.to_plot` and
:py:meth:`~sherpa.data.Data.to_contour` methods are used for
one- and two-dimensional data sets respectively.
For a one-dimensional data set, ``to_plot()`` returns a
tuple containing::

    xval, yval, error (statistical), error (systematic), x label, y label

which respects any :ref:`data filtering <data_filter>` applied
to the data set.
For :ref:`binned data sets <data_binned>` the X values refer
to the middle of each bin.

.. sherpa::

   In [1]: pdata = d1.to_plot()

   In [1]: plt.plot(pdata[0], pdata[1]);

   In [1]: plt.xlabel(pdata[4]);

   @savefig data_to_plot.png width=8in
   In [1]: plt.ylabel(pdata[5]);
   
.. sherpa::
   :suppress:

   In [1]: plt.clf()
   
Evaluating a model
------------------

The :py:meth:`~sherpa.data.Data.eval_model` and
:py:meth:`~sherpa.data.Data.eval_model_to_fit`
methods can be used
to evaluate a model on the grid defined by the data set. The
first version uses the full grid, whereas the second respects
any :ref:`filtering <data_filter>` applied to the data.

.. sherpa::

   In [1]: d1.notice(22, 25)
   
   In [1]: y1 = d1.eval_model(mdl)

   In [1]: y2 = d1.eval_model_to_fit(mdl)

   In [1]: x2 = d1.x[d1.mask]
   
   In [1]: plt.plot(d1.x, d1.y, 'ko', label='Data');

   In [1]: plt.plot(d1.x, y1, '--', label='Model (all points)');

   In [1]: plt.plot(x2, y2, linewidth=2, label='Model (filtered)');

   @savefig data_eval_model.png width=8in
   In [1]: plt.legend(loc=2);
   
.. sherpa::
   :suppress:

   In [1]: plt.clf()
   
Reference/API
=============

.. note::

   There are a bunch of methods that seem out of place;
   e.g. Data1D has get_x0 even though it's not ND!

.. note::

   There is no check that an attribute such as ``staterror``
   has the correct length when set.
   
sherpa.data Package
-------------------

.. automodule:: sherpa.data
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: sherpa.data.DataND       
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: sherpa.data.BaseData       
    :members:
    :undoc-members:
    :show-inheritance:
       
sherpa.astro.data Package
-------------------------

.. automodule:: sherpa.astro.data
    :members:
    :undoc-members:
    :show-inheritance:

