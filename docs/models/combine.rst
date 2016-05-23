****************
Combining models
****************

Example
=======

Following the `AstroPy modelling example
<http://docs.astropy.org/en/stable/modeling/#compound-models>`_,
but :ref:`linking the positions of the two gaussians <params-link>`.
It needs a lot of clean up.

.. sherpa::

   In [1]: import numpy as np

   In [1]: import matplotlib.pyplot as plt
   
   In [1]: from sherpa import data, models, stats, optmethods, fit, plot
   
   In [1]: np.random.seed(42)

Set up the model components:

.. sherpa::
   
   In [1]: g1 = models.Gauss1D('g1')

   In [1]: g2 = models.Gauss1D('g2')

Model components can be combined using standard mathematical
operations; for example addition:

.. sherpa::

   In [1]: mdl = g1 + g2

   In [1]: mdl

   In [1]: print(mdl)

The result of the combination is a
:py:class:`~sherpa.models.model.BinaryOpModel`, which has
:py:attr:`~sherpa.models.model.BinaryOpModel.op`,
:py:attr:`~sherpa.models.model.BinaryOpModel.lhs`,
and :py:attr:`~sherpa.models.model.BinaryOpModel.rhs`
attributes which describe the structure of the combination:

.. sherpa::

   In [1]: mdl.op

   In [1]: mdl.lhs

   In [1]: mdl.rhs

There is also a
:py:attr:`~sherpa.models.model.BinaryOpModel.parts` attribute
which contains all the elements of the model (in this case the
combination of the ``lhs`` and ``rhs`` attributes):

.. sherpa::

   In [1]: mdl.parts
   
The two components are separated by a fixed distance, which
will be "known" to the fit, so set it up as a variable:

.. sherpa::
   
   In [1]: sep = 0.5
      
The data to be fit is created from the same model, but using
different instances:

.. sherpa::

   In [1]: sim1, sim2 = models.Gauss1D(), models.Gauss1D()
   
   In [1]: mdl_sim = sim1 + sim2
   
   In [1]: sim1.ampl = 1.0

   In [1]: sim1.pos = 0.0

   In [1]: sim1.fwhm = 0.5

   In [1]: sim2.ampl = 2.5

   In [1]: sim2.pos = sep

   In [1]: sim2.fwhm = 0.25

.. sherpa::   

   In [1]: x = np.linspace(-1, 1, 200)
   
   In [1]: y = mdl_sim(x) + np.random.normal(0., 0.2, x.shape)

   In [1]: d = data.Data1D('multiple', x, y)
   
   In [1]: dplot = plot.DataPlot()

   In [1]: dplot.prepare(d)
   
   @savefig model_combine_data.png width=8in
   In [1]: dplot.plot()

.. sherpa::
   :suppress:

   In [1]: plt.clf()

Set up the starting position of the model:

.. sherpa::
   
   # Create a linked parameter
   In [1]: g2.pos = g1.pos + sep

   In [1]: g2.fwhm = 0.1

   In [1]: g1.fwhm = 0.1

   # Store the starting model
   In [1]: ystart = mdl(x)

   In [1]: mplot = plot.ModelPlot()

   In [1]: mplot.prepare(d, mdl)

   In [1]: dplot.plot()
   
   @savefig model_combine_start.png width=8in
   In [1]: mplot.plot(overplot=True)

.. sherpa::
   :suppress:

   In [1]: plt.clf()

Fit the data:
   
.. sherpa::
   
   In [1]: f = fit.Fit(d, mdl, stats.LeastSq(), optmethods.LevMar())

   In [1]: res = f.fit()
   
   In [1]: fplot = plot.FitPlot()

   # Update the model plot
   In [1]: mplot.prepare(d, mdl)

   In [1]: fplot.prepare(dplot, mplot)

   In [1]: fplot.plot()

   # Overplot the starting position
   In [1]: plt.plot(x, ystart, label='Start');
   
   @savefig model_combine.png width=8in
   In [1]: plt.legend(loc=2);

.. sherpa::
   :suppress:

   In [1]: plt.clf()

View the fit parameters:

.. sherpa::

   In [1]: print(g1)

   In [1]: print(mdl)

The ``pars`` attribute of a model (**note** not sure where
to reference this) lets you inspect all the parameters of
the model, including all its components for a composite model:
   
.. sherpa::
   
   In [1]: for par in mdl.pars:
      ...:     if par.link is None:
      ...:         print("{:10s} -> {:3f}".format(par.fullname, par.val))
      ...:     else:
      ...:         print("{:10s} -> link to {}".format(par.fullname, par.link.name))

The linked parameter is actually an instance of the
:py:class:`~sherpa.models.paramter.CompositeParameter`
class, which allows parameters to be combined in a similar
manner to models:

.. sherpa::

   In [1]: g2.pos.link

   In [1]: print(g2.pos.link)
   
The ``parts`` attribute of a composite model
lets you loop through all the component instances:

.. sherpa::
   
   In [1]: for cpt in mdl.parts:
      ...:     print(cpt)
