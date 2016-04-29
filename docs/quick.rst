***********************************************
A quick guide to modeling and fitting in Sherpa
***********************************************

Here are some examples of using Sherpa to model and fit data.
It is based on some of the examples used in the `astropy.modelling
documentation <http://docs.astropy.org/en/stable/modeling/>`_.

Getting started
===============

The following modules are assumed to have been imported:

.. sherpa::

    In [1]: import numpy as np

    In [2]: import matplotlib.pyplot as plt

The basic process, which will be followed below, is:

* create a data object

* define the model

* select the statistics

* select the optimisation routine

* fit the data

* extract the parameter values

Although presented as a list, it is not necessarily a linear process,
in that the order can be different to that above, and various steps
can be repeated. It also does not include any visualization steps
needed to inform and validate any choices.

.. _quick-gauss1d:

Fitting a one-dimensional data set
==================================

The following data - where ``x`` is the independent axis and
``y`` the dependent one - is used in this example:

.. sherpa::

    In [1]: np.random.seed(0)

    In [2]: x = np.linspace(-5., 5., 200)

    In [3]: ampl_true = 3

    In [4]: pos_true = 1.3

    In [5]: sigma_true = 0.8

    In [6]: err_true = 0.2

    In [3]: y = ampl_true * np.exp(-0.5 * (x - pos_true)**2 / sigma_true**2)

    In [4]: y += np.random.normal(0., err_true, x.shape)

    @savefig data1d.png width=8in
    In [5]: plt.plot(x, y, 'ko');

.. sherpa::
   :suppress:

   In [1]: plt.clf()
       
Creating a data object
----------------------

This data can be stored in a Sherpa data object, where the first
argument is a label for the data (this can be useful when multiple
data sets are loaded, but has no influence on the results):

.. sherpa::

    In [1]: from sherpa.data import Data1D

    In [2]: d = Data1D('example', x, y)

    In [3]: print(d)

At this point no errors are being used in the fit, so the ``staterror``
and ``syserror`` fields are empty.

Plotting the data
-----------------

The :py:mod:`sherpa.plot` module provides a number of classes that
create pre-canned plots. For example, the
:py:class:`sherpa.plot.DataPlot` class can be used to display the data.
The steps taken are normally:

1. create the object

2. call the ``prepare()`` method with the appropriate arguments,
   in this case the data object

3. call the ``plot()`` method.

Sherpa has two plotting backends: matplotlib, which is used by
default for the standalone version, and Crates, which is used by
CIAO.
   
.. sherpa::

   In [1]: from sherpa.plot import DataPlot

   In [1]: dplot = DataPlot()

   In [1]: dplot.prepare(d)

   @savefig data1d_dataplot.png width=8in
   In [1]: dplot.plot()

.. sherpa::
   :suppress:

   In [1]: plt.clf()

In the following, plots will be created using either the
classes in ``sherpa.plot`` or directly via matplotlib.
   
Define the model
----------------

In this example a single model is used - a one-dimensional
gaussian - but more complex examples are possible: these
include :ref:`multiple components <model-combine>`,
sharing models between data sets, and
:doc:`adding user-defined models <models/usermodel>`.
A full description of the model language and capabilities is provided in
:doc:`models/index`.

.. sherpa::

    In [1]: from sherpa.models import Gauss1D

    In [2]: g = Gauss1D()

    In [3]: print(g)

It is also possible to
:ref:`restrict the range of a parameter <params-limits>`,
:ref:`toggle parameters so that they are fixed or fitted <params-freeze>`,
and :ref:`link parameters togetger <params-link>`.

The :py:class:`sherpa.plot.ModelPlot` class can be used to visualize
the model. The :py:meth:`~sherpa.plot.ModelPlot.prepare` method
takes both a data object and the model to plot:

.. sherpa::

   In [1]: from sherpa.plot import ModelPlot

   In [1]: mplot = ModelPlot()

   In [1]: mplot.prepare(d, g)

   @savefig data1d_modelplot.png width=8in
   In [1]: mplot.plot()

.. sherpa::
   :suppress:

   In [1]: plt.clf()

Select the statistics
---------------------

.. sherpa::

    In [1]: from sherpa.stats import LeastSq

    In [2]: stat = LeastSq()

    In [3]: print(stat)

Select the optimisation routine
-------------------------------

.. sherpa::

    In [1]: from sherpa.optmethods import LevMar

    In [2]: opt = LevMar()

    In [3]: print(opt)

Fit the data
------------

The :py:meth:`~sherpa.fit.Fit.fit` method returns a
:py:class:`~sherpa.fit.FitResults` instance, which
contains information on how the fit performed, such as
whether it succeeded (:py:attr:`~sherpa.fit.FitResults.succeeded`).
One useful method for interactive analysis is
:py:meth:`~sherpa.fit.FitResults.format`, which returns
a string representation of the fit results, as shown below:

.. sherpa::

   In [1]: from sherpa.fit import Fit

   In [1]: gfit = Fit(d, g, stat=stat, method=opt)

   In [1]: print(gfit)

   In [1]: gres = gfit.fit()

   In [1]: print(gres.format())
    
   In [1]: if not gres.succeeded: print(gres.message)

The :py:class:`sherpa.plot.FitPlot` class will display the data
and model. The :py:meth:`~sherpa.plot.FitPlot.prepare` method
requires data and model plot objects; in this case the previous
versions can be re-used, although the model plot needs to be
updated to reflect the changes to the model parameters:

.. sherpa::

   In [1]: from sherpa.plot import FitPlot

   In [1]: fplot = FitPlot()

   In [1]: mplot.prepare(d, g)
   
   In [1]: fplot.prepare(dplot, mplot)

   @savefig data1d_fitplot.png width=8in
   In [1]: fplot.plot()
   
.. sherpa::
   :suppress:

   In [1]: plt.clf()

As the model can be evaluated directly, this plot can also be
created manually:

.. sherpa::
   
   In [1]: plt.plot(d.x, d.y, 'ko', label='Data');

   In [1]: plt.plot(d.x, g(d.x), linewidth=2, label='Gaussian');

   @savefig data1d_gauss_fit.png width=8in
   In [1]: plt.legend(loc=2);

.. sherpa::
   :suppress:

   In [1]: plt.clf()

Extract the parameter values
----------------------------

The fit results include a large number of attributes, many of which
are not relevant here (as the fit was done with no error values).
The following relation is used to convert from the full-width
half-maximum value, used by the ``Gauss1D`` model, to the Gaussian sigma
value used to create the data: :math:`\rm{FWHM} = 2 \sqrt{2ln(2)} \sigma`.

.. sherpa::

    In [1]: print(gres)

    In [2]: conv = 2 * np.sqrt(2 * np.log(2))

    In [3]: ans = dict(zip(gres.parnames, gres.parvals))

    In [4]: print("Position ={:.2f}  truth={:.2f}".format(ans['gauss1d.pos'], pos_true))

    In [5]: print("Amplitude={:.2f}  truth={:.2f}".format(ans['gauss1d.ampl'], ampl_true))

    In [6]: print("Sigma    ={:.2f}  truth={:.2f}".format(ans['gauss1d.fwhm']/conv, sigma_true))

The model, and its parameter values, can also be queried directly, as they
have been changed by the fit:

.. sherpa::

    In [1]: print(g)

    In [2]: print(g.pos)

Including errors
================

For this example, the error on each bin is assumed to be
known:

.. sherpa::

    In [1]: dy = np.ones(x.size) * err_true

    In [1]: de = Data1D('with-errors', x, y, staterror=dy)

    In [1]: print(de)

The statistic is changed from least squares to chi-square:

.. sherpa::

    In [1]: from sherpa.stats import Chi2

    In [1]: ustat = Chi2()

    In [1]: ge = Gauss1D('gerr')

    In [1]: gefit = Fit(de, ge, stat=ustat, method=opt)

    In [1]: geres = gefit.fit()

    In [1]: print(geres.format())
    
    In [1]: if not geres.succeeded: print(geres.message)

    In [1]: print(g)

    In [1]: print(ge)

Since the error value is independent of bin, then the fit results
should be the same here. The difference is that more of the fields
in the result structure are populated: in particular the
:py:attr:`~sherpa.fit.FitResults.rstat` and
:py:attr:`~sherpa.fit.FitResults.qval` fields, which give the
reduced statistic and the probability of obtaining this statisitic value
respectively.

.. sherpa::

    In [1]: print(geres)

Error analysis
--------------

The default error estimation routine is
:py:attr:`~sherpa.estmethods.Covariance`, which will be replaced by
:py:attr:`~sherpa.estmethods.Confidence` for this example:

.. sherpa::

   In [1]: from sherpa.estmethods import Confidence

   In [1]: gefit.estmethod = Confidence()

   In [1]: print(gefit.estmethod)

Running the error analysis can take time, for particularly complex
models. The default behavior is to use all the available CPU cores
on the machine.

.. sherpa::

   In [1]: errors = gefit.est_errors()

   In [1]: print(errors.format())

The :py:class:`~sherpa.fit.ErrorEstResults` instance returned by
``est_errors`` contains the parameter values and limits:

.. sherpa::

   In [1]: print(errors)

.. note::

   It is my belief that the ``est_errors`` call above should have created
   screen output for the lower and upper bounds, which suggests that the
   sherpa directive isn't catching it as it is supposed to.

Add screen output
-----------------

**this may need to be renamed given the note in the previous section**

Since the error analysis can take a long time, it can be useful to
have some indication of what is going on, particularly in an
interactive session. Sherpa uses the standard Python logging framework
to control the screen output produced by the
:py:meth:`~sherpa.fit.Fit.est_errors` method.

.. note::

   Unfortunately I can't seem to get them working (although they are
   actually being created when the code is being run, since you can see
   them in the console output). So perhaps it is partly an issue with
   my sherpa directive, but I have issues on the command line too.

Concentrating on a parameter
----------------------------

It is possible to investigate the error surface of a single
parameter using the
:py:class:`~sherpa.plot.IntervalProjection` class. The following shows
how the error surface changes with the position of the gaussian. The
:py:meth:`~sherpa.plot.IntervalProjection.prepare` method are given
the range over which to vary the parameter (the range is chosen to
be close to the three-sigma limit from the confidence analysis above,
ahd the dotted line is added to indicate the three-sigma
limit above the best-fit for a single parameter):

.. sherpa::

   In [1]: from sherpa.plot import IntervalProjection

   In [1]: iproj = IntervalProjection()

   In [1]: iproj.prepare(min=1.23, max=1.32, nloop=41)

   In [1]: iproj.calc(gefit, ge.pos)

   In [1]: iproj.plot()

   @savefig data1d_pos_iproj.png width=8in
   In [1]: plt.hlines(geres.statval + 9, 1.23, 1.32, linestyle='dotted');

.. sherpa::
   :suppress:

   In [1]: plt.clf()

A contour plot of two parameters
--------------------------------

The :py:class:`~sherpa.plot.RegionProjection` class supports
the comparison of two parameters. The contours indicate the one,
two, and three sigma contours.

.. sherpa::

   In [1]: from sherpa.plot import RegionProjection

   In [1]: rproj = RegionProjection()

   In [1]: rproj.prepare(min=[1.2, 1.75], max=[1.35, 2.1], nloop=[21, 21])

   In [1]: rproj.calc(gefit, ge.pos, ge.fwhm)

   @savefig data1d_pos_fwhm_rproj.png width=8in
   In [1]: rproj.contour()

.. sherpa::
   :suppress:

   In [1]: plt.clf()
   
Fitting two-dimensional data
============================

.. sherpa::

    In [1]: np.random.seed(0)

    In [2]: y2, x2 = np.mgrid[:128, :128]

    In [3]: z = 2. * x2 ** 2 - 0.5 * y2 ** 2 + 1.5 * x2 * y2 - 1.

    In [4]: z += np.random.normal(0., 0.1, z.shape) * 50000.

Creating a data object
----------------------

To support irregularly-gridded data, the ND data sets require
one-dimensional coordinate arrays:

.. sherpa::

    In [1]: from sherpa.data import Data2D

    In [2]: x0axis = x2.ravel()

    In [2]: x1axis = y2.ravel()

    In [2]: d2 = Data2D('img', x0axis, x1axis, z.ravel(), shape=(128,128))

Define the model
----------------

Creating the model is the same as the one-dimensional case:

.. sherpa::

    In [1]: from sherpa.models import Polynom2D

    In [2]: p2 = Polynom2D('p2')

    In [3]: print(p2)

Control the parameters being fit
--------------------------------

To reduce the number of parameters being fit, the ``frozen`` attribute
can be set:

.. sherpa::

    In [1]: for n in ['cx1', 'cy1', 'cx2y1', 'cx1y2', 'cx2y2']:
       ...:     getattr(p2, n).frozen = True

    In [2]: print(p2)

Fit the data
------------

Fitting is no different (the same statistic and optimisation
objects used earlier could have been re-used here):

.. sherpa::

    In [1]: f2 = Fit(d2, p2, stat=LeastSq(), method=LevMar())

    In [2]: res2 = f2.fit()

    In [3]: if not res2.succeeded: print(res2.message)

    In [4]: print(res2)

    In [5]: print(p2)

.. note::

    TODO: why are all the parameters a good fit *except* for the
    ``c`` value, which is -80 rather than -1?

Display the model
-----------------

The model can be visualized by evaluating it over a grid of points
and then displaying it:

.. sherpa::

    In [1]: m2 = p2(x0axis, x1axis).reshape(128, 128)

    In [1]: def pimg(d, title):
       ...:     plt.imshow(d, origin='lower', interpolation='nearest',
       ...:                vmin=-1e4, vmax=5e4, cmap='viridis')
       ...:     plt.colorbar(orientation='horizontal',
       ...:                  ticks=[0, 20000, 40000])
       ...:     plt.title(title)

    In [2]: plt.figure(figsize=(8, 3));

    In [3]: plt.subplot(1, 3, 1);

    In [4]: pimg(z, "Data")

    In [6]: plt.subplot(1, 3, 2);

    In [7]: pimg(m2, "Model")

    In [9]: plt.subplot(1, 3, 3);

    @savefig data2d_residuals.png width=8in
    In [10]: pimg(z - m2, "Residual")

.. sherpa::
   :suppress:

   In [1]: plt.clf()


Simultaneous fits
=================

.. note::

    I need to work out how to do this
