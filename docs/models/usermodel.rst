**********************
Writing your own model
**********************

A model class can be created to fit any function, or interface with
external code.

.. note::

   There should be some description of what needs to be done, as well
   as examples.
   
A one-dimensional model
=======================

An example is the
`AstroPy trapezoidal model <http://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.Trapezoid1D.html>`_,
which has four parameters: the amplitude of the central region, the center
and width of this region, and the slope. The following model class,
which was not written for efficiancy or robustness, implements this
interface:

.. literalinclude:: ../code/trap.py

This can be used in the same manner as the ``Gauss1D`` model
in the :ref:`quick guide to Sherpa<quick-gauss1d>`.

.. ipython::

    In [1]: import numpy as np

    In [2]: import matplotlib.pyplot as plt

    In [1]: np.random.seed(0)

    In [2]: x = np.linspace(-5., 5., 200)

    In [3]: ampl_true = 3

    In [4]: pos_true = 1.3

    In [5]: sigma_true = 0.8

    In [6]: err_true = 0.2

    In [3]: y = ampl_true * np.exp(-0.5 * (x - pos_true)**2 / sigma_true**2)

    In [4]: y += np.random.normal(0., err_true, x.shape)

    In [1]: from sherpa.data import Data1D

    In [2]: d = Data1D('example', x, y)

    In [1]: from trap import Trap1D

    In [2]: t = Trap1D()

    In [3]: print(t)

    In [1]: from sherpa.fit import Fit
    
    In [1]: from sherpa.stats import LeastSq
    
    In [1]: from sherpa.optmethods import LevMar
    
    In [4]: tfit = Fit(d, t, stat=LeastSq(), method=LevMar())

    In [5]: tres = tfit.fit()

    In [6]: if not tres.succeeded: print(tres.message)

    In [7]: plt.plot(d.x, d.y, 'ko');

    In [8]: # plt.plot(d.x, g(d.x), linewidth=2, label='Gaussian');

    In [9]: plt.plot(d.x, t(d.x), linewidth=2, label='Trapezoid');

    @savefig data1d_trap_fit.png width=8in
    In [10]: plt.legend(loc=2);

.. note::

   This needs to be cleaned up to separate out unnescessary code,
   perhaps just hiding the setup code (and it would be nice if
   this could be shared with the setup).

A two-dimensional model
=======================

The two-dimensional case is similar to the one-dimensional case,
with the major difference being the number of independent axes to
deal with. In the following example the model is assumed to only be
applied to non-integrated data sets, as it simplifies the implementation
of the ``calc`` method.

It also shows one way of embedding models from a different system,
in this case the
`two-dimemensional polynomial model 
<http://docs.astropy.org/en/stable/api/astropy.modeling.polynomial.Polynomial2D.html>`_
from the AstroPy package.

.. literalinclude:: ../code/poly.py

And now repeating the 2D fit:

.. ipython::
   
    In [1]: np.random.seed(0)

    In [2]: y2, x2 = np.mgrid[:128, :128]

    In [3]: z = 2. * x2 ** 2 - 0.5 * y2 ** 2 + 1.5 * x2 * y2 - 1.

    In [4]: z += np.random.normal(0., 0.1, z.shape) * 50000.

    In [1]: from sherpa.data import Data2D

    In [2]: x0axis = x2.ravel()

    In [2]: x1axis = y2.ravel()

    In [2]: d2 = Data2D('img', x0axis, x1axis, z.ravel(), shape=(128,128))

    In [1]: from poly import WrapPoly2D
    
    In [1]: wp2 = WrapPoly2D('wp2')

    In [1]: wp2.c1_0.frozen = True

    In [1]: wp2.c0_1.frozen = True

    In [1]: f2 = Fit(d2, wp2, stat=LeastSq(), method=LevMar())

    In [2]: res2 = f2.fit()

    In [3]: if not res2.succeeded: print(res2.message)

    In [4]: print(res2)

    In [5]: print(wp2)
    
.. note::

   Hmmm, this looks similar to the Sherpa results. In particular
   the 0,0 value is -80 not 1. Aha, is it a normalization at
   (0,0) vs (1,1) sort of thing?
