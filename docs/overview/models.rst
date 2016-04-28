
*************************
Defining and using models
*************************

The following modules are assumed to have been imported:

.. ipython::

    In [1]: import numpy as np

    In [2]: from sherpa import models

    In [3]: import matplotlib.pyplot as plt


The :mod:`sherpa.models` namespace provides a collection of one- and 
two-dimensional models as a convenience; the actual definition of
each particular model depends on its type. The optional
:mod:`sherpa.astro.xspec` module provides access to the set of
XSPEC models (this will not be discussed further here).

Models must be created before there parameter values can
be set. In this case a one-dimensional gaussian:

.. ipython::

   In [1]: g = models.Gauss1D()

   In [2]: print(g)

.. note::

   At present there is no documentation provided for the model
   classes, and the `CIAO Sherpa 
   documentation <http://cxc.harvard.edu/sherpa/ahelp/models.html>`_,
   or direct experimentation with the returned object, are needed
   to find out what the parameters are. This will be fixed.

The parameter values have a current value, as well as a valid range
(as given by the the minimum and maximum columns in the table above),
as well as a units field. The units field is a string, describing the
expected units for the parameter; there is currently *no support* for
using `astropy.units
<http://docs.astropy.org/en/stable/units/index.html>`_ to set a
parameter value.  The "Type" column refers to whether the parameter is
fixed, (``frozen``) or can be varied during a fit (``thawed``).

Models can be given a name, to help distinguish multiple versions
of the same model type. The default value is the lower-case version
of the class name.

.. ipython::

   In [1]: g.name

   In [1]: h = models.Gauss1D('other')

   In [2]: print(h)

   In [1]: h.name

The parameters can be accesed as attributes, both to read or change
the current settings. The ``val`` attribute contains the current
value, but it can be set directly (just by assigning a value to
the parameter):

.. ipython::

   In [1]: h.fwhm

   In [1]: h.pos

   In [1]: h.ampl

   In [1]: h.fwhm.val

   In [1]: h.fwhm.min

   In [1]: h.fwhm.frozen

   In [1]: h.fwhm = 15

   In [1]: print(h)

   In [1]: h.fwhm.val = 12

   In [1]: print(h)
   
.. note::

    * Linking parameters.

    * combining models (e.g. a + b as well as more complex)

Reference/API
-------------

sherpa.models.basic Package
+++++++++++++++++++++++++++

.. automodule:: sherpa.models.basic
    :members:
    :undoc-members:
    :show-inheritance:

sherpa.models.model Package
+++++++++++++++++++++++++++

.. automodule:: sherpa.models.model
    :members:
    :undoc-members:
    :show-inheritance:

sherpa.models.parameter Package
+++++++++++++++++++++++++++++++

.. automodule:: sherpa.models.parameter
    :members:
    :undoc-members:
    :show-inheritance:

sherpa.models.template Package
++++++++++++++++++++++++++++++

.. automodule:: sherpa.models.template
    :members:
    :undoc-members:
    :show-inheritance:

sherpa.astro.models Package
+++++++++++++++++++++++++++

.. automodule:: sherpa.astro.models
    :members:
    :undoc-members:
    :show-inheritance:

sherpa.astro.xspec Package
++++++++++++++++++++++++++

The models provided by the optional ``sherpa.astro.xspec``
module are not discussed here.
