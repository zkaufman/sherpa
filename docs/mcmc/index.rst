=========================================
Markov Chain Monte Carlo and Poisson data
=========================================

Sherpa provides a
`Markov Chain Monte Carlo (MCMC)
<https://en.wikipedia.org/wiki/Markov_chain_Monte_Carlo>`_
method designed for Poisson-distributed data.
It was originally developed as the
`Bayesian Low-Count X-ray Spectral (BLoCXS)
<http://hea-www.harvard.edu/astrostat/pyblocxs/>`_
package, but has since been incorporated into Sherpa.
It is developed from the work presented in
`Analysis of Energy Spectra with Low Photon Counts
via Bayesian Posterior Simulation
<https://ui.adsabs.harvard.edu/#abs/2001ApJ...548..224V>`_
by van Dyk et al.

Unlike many MCMC implementations, idea is that have some
idea of the search surface at the optimum - i.e. the
covariance matrix - and then use that to explore this region.

Example
=======

.. note::

   This example probably needs to be simplified to reduce the run time

Simulate the data
------------------

Create a simulated data set:

.. sherpa::

   In [1]: np.random.seed(2)

   In [1]: x0low, x0high = 3000, 4000

   In [1]: x1low, x1high = 4000, 4800

   In [1]: dx = 15

   In [1]: x1, x0 = np.mgrid[x1low:x1high:dx, x0low:x0high:dx]

   # Convert to 1D arrays
   In [1]: shape = x0.shape

   In [1]: x0, x1 = x0.flatten(), x1.flatten()
   
   In [1]: from sherpa.astro.models import Beta2D

   In [1]: truth = Beta2D()

   In [1]: truth.xpos, truth.ypos = 3512, 4418

   In [1]: truth.r0, truth.alpha = 120, 2.1

   In [1]: truth.ampl = 12

   # Create the expected values
   In [1]: mexp = truth(x0, x1).reshape(shape)

   # Add in Poisson noise
   In [1]: msim = np.random.poisson(mexp)

What does the data look like?
-----------------------------

Use an arcsinh transform to view the data, based on the work of
`Lupton, Gunn & Szalay (1999)
<https://ui.adsabs.harvard.edu/#abs/1999AJ....118.1406L>`_.
   
.. sherpa::

   In [1]: plt.imshow(np.arcsinh(msim), origin='lower', cmap='viridis',
      ...:            extent=(x0low, x0high, x1low, x1high),
      ...:            interpolation='nearest', aspect='auto');

   @savefig mcmc_sim.png width=8in
   In [1]: plt.title('Simulated image');

.. sherpa::
   :suppress:

   In [1]: plt.clf()

Find the starting point for the MCMC
------------------------------------

Set up a model and use the standard Sherpa approach to find a good
starting place for the MCMC analysis:

.. sherpa::

   In [1]: from sherpa import data, stats, optmethods, fit

   In [1]: d = data.Data2D('sim', x0, x1, msim.flatten(), shape=shape)

   In [1]: mdl = Beta2D()

   In [1]: mdl.xpos, mdl.ypos = 3500, 4400

   # Use a ML statistic and Nelder-Mead algorithm
   In [1]: f = fit.Fit(d, mdl, stats.Cash(), optmethods.NelderMead())

   In [1]: res = f.fit()

   In [1]: print(res.format())

Now calculate the covariance matrix (the default):

.. sherpa::

   In [1]: f.estmethod

   In [1]: eres = f.est_errors()

   In [1]: print(eres.format())

   In [1]: cmatrix = eres.extra_output

   In [1]: pnames = [p.split('.')[1] for p in eres.parnames]

   In [1]: plt.imshow(cmatrix, interpolation='nearest', cmap='viridis');

   In [1]: plt.xticks(np.arange(5), pnames);

   In [1]: plt.yticks(np.arange(5), pnames);

   @savefig mcmc_covar_matrix.png width=8in
   In [1]: plt.colorbar();

.. sherpa::
   :suppress:

   In [1]: plt.clf()

Run the chain
-------------

Finally, run a chain (use a small number to keep the run time low
for this example):

.. sherpa::

   In [1]: from sherpa.sim import MCMC

   In [1]: mcmc = MCMC()

   In [1]: mcmc.get_sampler_name()
   
   In [1]: draws = mcmc.get_draws(f, cmatrix, niter=1000)

   In [1]: svals, accept, pvals = draws

   In [1]: pvals.shape

   In [1]: accept.sum() * 1.0 / 1000

Trace plots
-----------

.. sherpa::

   In [1]: plt.plot(pvals[0, :]);

   In [1]: plt.xlabel('Iteration');

   @savefig mcmc_trace_r0_manual.png width=8in
   In [1]: plt.ylabel('r0');

Or using the :py:mod:`sherpa.plot` module:

.. sherpa::

   In [1]: from sherpa import plot

   In [1]: tplot = plot.TracePlot()

   In [1]: tplot.prepare(svals, name='Statistic')

   @savefig mcmc_trace_r0.png width=8in
   In [1]: tplot.plot()
   
.. sherpa::
   :suppress:

   In [1]: plt.clf()

PDF of a parameter
------------------

.. sherpa::

   In [1]: pdf = plot.PDFPlot()

   In [1]: pdf.prepare(pvals[1, :], 20, False, 'xpos', name='example')

   In [1]: pdf.plot()

   # Add in the covariance estimate
   In [1]: xlo, xhi = eres.parmins[1] + eres.parvals[1], eres.parmaxes[1] + eres.parvals[1]
   
   In [1]: plt.annotate('', (xlo, 90), (xhi, 90), arrowprops={'arrowstyle': '<->'});

   @savefig mcmc_pdf_xpos.png width=8in
   In [1]: plt.plot([eres.parvals[1]], [90], 'ok');
   
.. sherpa::
   :suppress:

   In [1]: plt.clf()

CDF for a parameter
-------------------

Normalise by the actual answer to make it wasier to see how well
the results match reality:

.. sherpa::

   In [1]: cdf = plot.CDFPlot()

   In [1]: plt.subplot(2, 1, 1);
   
   In [1]: cdf.prepare(pvals[1, :] - truth.xpos.val, r'$\Delta x$')

   In [1]: cdf.plot(clearwindow=False)

   In [1]: plt.title('');
   
   In [1]: plt.subplot(2, 1, 2);

   In [1]: cdf.prepare(pvals[2, :] - truth.ypos.val, r'$\Delta y$')

   In [1]: cdf.plot(clearwindow=False)

   @savefig mcmc_cdf_xpos.png width=8in
   In [1]: plt.title('');

.. sherpa::
   :suppress:

   In [1]: plt.clf()

Scatter plot
------------

.. sherpa::

   In [1]: plt.scatter(pvals[0, :] - truth.r0.val,
      ...:             pvals[4, :] - truth.alpha.val, alpha=0.3);

   In [1]: plt.xlabel(r'$\Delta r_0$', size=18);

   @savefig mcmc_scatter_r0_alpha.png width=8in
   In [1]: plt.ylabel(r'$\Delta \alpha$', size=18);

.. sherpa::
   :suppress:

   In [1]: plt.clf()
   
This can be compared to the
:py:class:`~sherpa.plot.RegionProjection` calculation:

.. sherpa::

   In [1]: plt.scatter(pvals[0, :], pvals[4, :], alpha=0.3);

   In [1]: from sherpa.plot import RegionProjection

   In [1]: rproj = RegionProjection()

   In [1]: rproj.prepare(min=[95, 1.8], max=[150, 2.6], nloop=[21, 21])

   In [1]: rproj.calc(f, mdl.r0, mdl.alpha)

   In [1]: rproj.contour(overplot=True)

   @savefig mcmc_scatter_r0_alpha_compare.png width=8in
   In [1]: plt.xlabel(r'$r_0$'); plt.ylabel(r'$\alpha$');

.. sherpa::
   :suppress:

   In [1]: plt.clf()

Reference/API
=============

sherpa.sim Package
------------------

.. automodule:: sherpa.sim
    :members:
    :undoc-members:
    :show-inheritance:

sherpa.sim.simulate Package
---------------------------

.. automodule:: sherpa.sim.simulate
    :members:
    :undoc-members:
    :show-inheritance:

sherpa.sim.sample Package
-------------------------

.. automodule:: sherpa.sim.sample
    :members:
    :undoc-members:
    :show-inheritance:

sherpa.sim.mh Package
---------------------

.. automodule:: sherpa.sim.mh
    :members:
    :undoc-members:
    :show-inheritance:
    
