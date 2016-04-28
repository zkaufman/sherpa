*************************
Binned and Unbinned grids
*************************

Sherpa supports models for both binned and unbinned data
sets. Rather than have separate models, any model can be
used for either type of data set, and the model will evaluate
either a point value - for unbinned data sets - or will
estimate the integral of the model over the bin.

This influences how the model is evaluated - since the independent
axis values for binned data seta are different to unbinned ones - and
the model values that are calculated are different. It is possible
to force a model to treat a binned data set as an unbinned one.

.. note::

   Need to document how (after checking that this is always true).

