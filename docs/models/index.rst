*************************
Defining and using models
*************************

The :mod:`sherpa.models` and :mod:`sherpa.astro.models`
namespaces provides a collection of one- and 
two-dimensional models as a convenience; the actual definition of
each particular model depends on its type. The optional
:mod:`sherpa.astro.xspec` module provides access to the set of
XSPEC models (this will not be discussed further here).

.. note::
   To get the link above probably means using
   :mod:`sherpa.models.model`, but users can get away with
   just importing ``sherpa.models`` as shown below.

Overview
========

Setup
-----

The following modules are assumed to have been imported:

.. sherpa::

    In [1]: import numpy as np

    In [1]: import matplotlib.pyplot as plt

    In [1]: from sherpa import models

Creating a model instance
-------------------------

Models must be created before there parameter values can
be set. In this case a one-dimensional gaussian:

.. sherpa::

   In [1]: g = models.Gauss1D()

   In [1]: print(g)

.. note::

   At present there is no documentation provided for the model
   classes, and the `CIAO Sherpa 
   documentation <http://cxc.harvard.edu/sherpa/ahelp/models.html>`_,
   or direct experimentation with the returned object, are needed
   to find out what the parameters are. This will be fixed.

The parameter values have a current value, a valid range
(as given by the the minimum and maximum columns in the table above),
and a units field. The units field is a string, describing the
expected units for the parameter; there is currently *no support* for
using `astropy.units
<http://docs.astropy.org/en/stable/units/index.html>`_ to set a
parameter value.  The "Type" column refers to whether the parameter is
fixed, (``frozen``) or can be varied during a fit (``thawed``),
as described below, in the :ref:`params-freeze` section.

Models can be given a name, to help distinguish multiple versions
of the same model type. The default value is the lower-case version
of the class name.

.. sherpa::

   In [1]: g.name

   In [1]: h = models.Gauss1D('other')

   In [1]: print(h)

   In [1]: h.name

The model classes are expected to derive from the
:py:class:`~sherpa.models.model.ArithmeticModel` class.
   
.. _model-combine:

Combining models
----------------

Models can be combined and shared by using the standard Python
numerical operators. For instance, a one-dimensional gaussian
plus a flat background would be represented by the following
model:

.. sherpa::

   In [1]: src1 = models.Gauss1D('src1')

   In [1]: back = models.Gauss1D('back')

   In [1]: mdl1 = src1 + back

   In [1]: print(mdl1)

Now consider fitting a second dataset where it is known that the background
is two times higher than the first: 
   
.. sherpa::

   In [1]: src2 = models.Gauss1D('src2')

   In [1]: mdl2 = src2 + 2 * back

   In [1]: print(mdl2)

The two models can then be fit separately or simultaneously. In this
example the two source models (the Gaussian component) were completely
separate, but they could have been identical - in which case
``mdl2 = src1 + 2 * back`` would have been used instead - or
:ref:`parameter linking <params-link>` could be used to constrain the
models. An example of the use of linking would be to force the two
FWHM parameters to be the same but to let the position and amplitude
values vary independently.

More information is available in the
:doc:`combining models <combine>` documentation.

.. note::

   It is possible to have models depend on the values of other models,
   which allows one model to convolve another, but this is
   currently not documented.

.. note::

    There is currently *no restriction* on combining models of different
    types. This means that there is no exception raised when combining
    a one-dimensional model with a two-dimensional one. It is only when
    the model is evaluated that an error *may* be raised.
    
Changing a parameter
--------------------

The parameters of a model - those numeric variables that control the
shape of the model, and that can be varied during a fit -
can be accesed as attributes, both to read or change
the current settings. The
:py:attr:`~sherpa.models.parameter.Parameter.val` attribute
contains the current value, but it can be set directly
(just by assigning a value to the parameter):

.. sherpa::

   In [1]: h.fwhm

   In [1]: print(h.fwhm)

   In [1]: h.fwhm.val

   In [1]: h.fwhm.min

   In [1]: h.fwhm = 15

   In [1]: print(h.fwhm)

   In [1]: h.fwhm.val = 12

   In [1]: print(h.fwhm)

.. _params-limits:

The soft and hard limits of a parameter
---------------------------------------

Each parameter has two sets of limits, which are referred to as
"soft" and "hard". The soft limits are shown when the model
is displayed, and refer to the
:py:attr:`~sherpa.models.parameter.Parameter.min`
and
:py:attr:`~sherpa.models.parameter.Parameter.max`
attributes for the parameter, whereas the hard limits are
given by the
:py:attr:`~sherpa.models.parameter.Parameter.hard_min`
and
:py:attr:`~sherpa.models.parameter.Parameter.hard_max`
(which are not displayed, and can not be changed).

.. sherpa::

   In [1]: print(h)

   In [1]: print(h.fwhm)

These limits act to bound the acceptable parameter range; this
is often because certain values are physically impossible, such
as having a negative value for the full-width-half-maxium value
of a Gaussian, but can also be used to ensure that the fit is
restricted to a meaningful part of the search space. The hard
limits are set by the model class, and represent the full
valid range of the parameter, whereas the soft limits can be
changed by the user, although they often default to the same
values as the hard limits.

Setting a parameter to a value outside its soft limits will
raise a :py:exc:`~sherpa.utils.err.ParameterErr` Exception.

During a fit the paramater values are bound by the soft limits,
and a screen message will be displayed if an attempt to move
outside this range was made. During error analysis the parameter
values are allowed outside the soft limits, as long as they remain
inside the hard limits.
   
.. _params-freeze:
   
Freezing and Thawing parameters
-------------------------------

Not all model parameters should be varied during a fit: perhaps
the data quality is not sufficient to constrain all the parameters,
it is already known, the parameter is highly correlated with
another, or perhaps the parameter value controls a behavior of the
model that should not vary during a fit (such as the interpolation
scheme to use). The :py:attr:`~sherpa.models.parameter.Parameter.frozen`
attribute controls whether a fit
should vary that parameter or not; it can be changed directly,
as shown below:

.. ipython ::

   In [1]: h.fwhm.frozen

   In [1]: h.fwhm.frozen = True

or via the :py:meth:`~sherpa.models.parameter.Parameter.freeze`
and :py:meth:`~sherpa.models.parameter.Parameter.thaw`
methods for the parameter.

.. ipython ::

   In [1]: h.fwhm.thaw()

   In [1]: h.fwhm.frozen

There are times when a model parameter should *never* be varied
during a fit. In this case the
:py:attr:`~sherpa.models.parameter.Parameter.alwaysfrozen`
attribute will be set to ``True`` (this particular
parameter is read-only).

.. _params-link:

Linking parameters
------------------

There are times when it is useful for one parameter to be
related to another: this can be equality, such as saying that
the width of two model components are the same, or a functional
form, such as saying that the position of one component is a
certain distance away from another component. This concept
is refererred to as linking parameter values. The second case
incudes the first - where the functional relationship is equality -
but it is treated separately here as it is a common operation.
Lnking parameters also reduces the number of free parameters in a fit.

The following examples use the same two model components:

.. ipython ::

   In [1]: g1 = models.Gauss1D('g1')
   
   In [1]: g2 = models.Gauss1D('g2')

Linking parameter values requires referring to the parameter, rather
than via the :py:attr:`~sherpa.models.parameter.Parameter.val` attribute.
The :py:attr:`~sherpa.models.parameter.Parameter.link` attribute
is set to the link value (and is ``None`` for parameters that are
not linked).
   
Equality
^^^^^^^^

After the following, the two gaussian components have the same
width:

.. sherpa::

   In [1]: g2.fwhm.val
   
   In [1]: g2.fwhm = g1.fwhm

   In [1]: g1.fwhm = 1024

   In [1]: g2.fwhm.val

   In [1]: g1.fwhm.link == None

   In [1]: g2.fwhm.link

When displaying the model, the value and link expression are included:

.. sherpa::

   In [1]: print(g2)
   
Functional relationship
^^^^^^^^^^^^^^^^^^^^^^^

The link can accept anything that evaluates to a value,
such as adding a constant.

.. ipython ::

    In [1]: g2.pos = g1.pos + 8234

    In [1]: g1.pos = 1200

    In [1]: g2.pos.val

The :py:class:`~sherpa.models.parameter.CompositeParameter` class
controls how parameters are combined. In this case the result
is a :py:class:`~sherpa.models.parameter.BinaryOpParameter` object.

Including another parameter
^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is possible to include other parameters in a link expression,
which can lead to further constraints on the fit. For instance,
rather than using a fixed separation, a range can be used. One
way to do this is to use a :py:class:`~sherpa.models.basic.Const1D`
model, restricting the value its one parameter can vary.

.. sherpa::

   In [1]: sep = models.Const1D('sep')

   In [1]: print(sep)
   
   In [1]: g2.fwhm = g1.fwhm + sep.c0

   In [1]: sep.c0 = 1200
   
   In [1]: sep.c0.min = 800

   In [1]: sep.c0.max = 1600

In this example, the separation of the two components is restricted
to lie in the range 800 to 1600.

In order for the optimiser to recognize that it needs to vary the
new parameter (``sep.c0``), the component *must* be included in the
model expression. As it does not contribute to the model output
directly, it should be multiplied by zero. So, for this example
the model to be fit would be given by:

.. sherpa::

   In [1]: mdl = g1 + g2 + 0 * sep

Resetting parameter values
--------------------------

Something to do with the
:py:meth:`~sherpa.models.parameter.Parameter.reset`
call and the
:py:attr:`~sherpa.models.parameter.Parameter.default_val`
attribute.

Inspecting models and parameters
--------------------------------

Models, whether a single component or composite, contain a
``pars`` attribute which is a tuple of all the parameters
for that model. This can be used to programatically query
or change the parameter values.
There are several attributes that return arrays of values
for the thawed parameters of the model expression: the most
useful is :py:attr:`~sherpa.models.model.Model.thawedpars`,
which gives the current values.

Composite models can be queried to find the individual
components using the ``parts`` attribute, which contains
a tuple of the components (these components can themselves
be composite objects).

Using `sherpa.models`
=====================

.. toctree::
   :maxdepth: 1

   integrate
   combine
   evaluation
   usermodel
   cache
      
Reference/API
=============

.. note::

   I tried to manually separate the ``sherpa.models.basic``
   models, to one-per-file, but this is manual work without
   something like the ``automodapi`` from
   <https://github.com/astropy/astropy-helpers>. There were
   also issues with the 'See Also' links not working (perhaps
   I needed to add a sphinx directive to each page to say
   what the base module was).

.. automodapi:: sherpa.models.basic
.. automodapi:: sherpa.models.model
.. automodapi:: sherpa.models.parameter
.. automodapi:: sherpa.models.template
.. automodapi:: sherpa.astro.models
.. automodapi:: sherpa.astro.optical

sherpa.astro.xspec Module
-------------------------

.. note::                
    The models provided by the optional ``sherpa.astro.xspec``
    module are not discussed here, as the build is currently
    done without XSPEC. It's not yet clear to me how to
    handle this (could mock out the XSPEC interface but
    would also lie to run code).
