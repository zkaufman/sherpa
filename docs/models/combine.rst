****************
Combining models
****************

Example
=======

Following the `AstroPy modelling example
<http://docs.astropy.org/en/stable/modeling/#compound-models>`_,
but :ref:`linking the positions of the two gaussians <params-link>`

.. sherpa::

   In [1]: import numpy as np

   In [1]: import matplotlib.pyplot as plt
   
   In [1]: from sherpa import data, models, stats, optmethods, fit, plot
   
   In [1]: np.random.seed(42)

   In [1]: sep = 0.5
   
   In [1]: g1 = models.Gauss1D('g1')

   In [1]: g1.ampl = 1.0

   In [1]: g1.pos = 0.0

   In [1]: g1.fwhm = 0.5

   In [1]: g2 = models.Gauss1D('g2')

   In [1]: g2.ampl = 2.5

   In [1]: g2.pos = sep

   In [1]: g2.fwhm = 0.25

   In [1]: x = np.linspace(-1, 1, 200)
   
   In [1]: y = g1(x) + g2(x) + np.random.normal(0., 0.2, x.shape)

   In [1]: d = data.Data1D('multiple', x, y)
   
   In [1]: g1 = models.Gauss1D('g1')
   
   In [1]: g2 = models.Gauss1D('g2')

   # Create a linked parameter
   In [1]: g2.pos = g1.pos + sep

   In [1]: g2.fwhm = 0.1

   In [1]: g1.fwhm = 0.1

   In [1]: mdl = g1 + g2

   # Store the starting model
   In [1]: ystart = mdl(x)
   
   In [1]: f = fit.Fit(d, mdl, stats.LeastSq(), optmethods.LevMar())

   In [1]: res = f.fit()
   
   In [1]: dplot = plot.DataPlot()

   In [1]: dplot.prepare(d)
   
   In [1]: mplot = plot.ModelPlot()

   In [1]: mplot.prepare(d, g1 + g2)

   In [1]: fplot = plot.FitPlot()

   In [1]: fplot.prepare(dplot, mplot)

   In [1]: fplot.plot()

   In [1]: plt.plot(x, ystart, label='Start');

   @savefig model_combine.png width=8in
   In [1]: plt.legend(loc=2);

.. sherpa::
   :suppress:

   In [1]: plt.clf()

.. sherpa::

   In [1]: print(g1)

   In [1]: print(mdl)

   In [1]: for par in mdl.pars:
      ...:     if par.link is None:
      ...:         print("{:10s} -> {:3f}".format(par.fullname, par.val))

   In [1]: mdl.op
   
   In [1]: for cpt in mdl.parts:
      ...:     print(cpt)
