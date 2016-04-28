
***************
Sherpa and CIAO
***************

The Sherpa package was developed by the Chandra X-ray Center
as a eneral purpose fitting and modeling tool, with specializations
for handling X-ray Astronomy data. It is provided as part of the
CIAO analysis package, where the code is the same as that available
from the Sherpa GitHub page, with the following modifications:

* the plotting and I/O backends use the CIAO versions, namely
  ChIPS and Crates, rather than matplotlib and astropy

* a set of customized IPython routines are provided as part of
  CIAO that automatically load Sherpa and related packages, as well
  as tweak the IPython look and feel.

* the CIAO version of Sherpa includes the optional XSPEC model
  library (``sherpa.astro.xspec``).
  
The online documentation provided for Sherpa as part of CIAO,
namely http://cxc.harvard.edu/sherpa/, can be used with the
standalone version of Sherpa, but note that the focus of this
documentation is the session-based API provided by the
``sherpa.astro.ui`` and ``sherpa.ui`` modules.
These are wrappers around the Object-Oriented
interface described in this document, and  data management
and utility routines. This API can be used with standalone Sherpa,
but is not described in this documentation.
