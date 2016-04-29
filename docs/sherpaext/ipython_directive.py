#
#  Copyright (C) 2015, 2016  Smithsonian Astrophysical Observatory
#
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

"""
Extend Ipython.sphinxext.ipython.ipython_directive so that it captures
the output of the sherpa logging interface.

This could be made more generic, but it's not clear what the use
cases are, so is it worth the effort?
"""

import logging

import IPython.sphinxext.ipython_directive as ipy

import sherpa


# The Sherpa logging instance
slog = logging.getLogger('sherpa')


class SherpaIPythonDirective(ipy.IPythonDirective):
    """Include the Sherpa logging output.

    Extend the ipython directive to automatically insert any
    output from the Sherpa logger into the shell output.
    To ensure consistent behavior the sherpa logging interface
    is set to the INFO level at both setup and tear down. This
    may be too restrictive.
    """

    def setup(self):
        out = ipy.IPythonDirective.setup(self)

        self._hdlr = logging.StreamHandler(stream=self.shell.cout)
        self._hdlr.setFormatter(sherpa.Formatter())
        slog.addHandler(self._hdlr)

        slog.setLevel(logging.INFO)

        return out

    def teardown(self):
        "Remove the logging handler for this session"
        slog.removeHandler(self._hdlr)
        slog.setLevel(logging.INFO)


def setup(app):

    # It seems that this works to "sub class" the ipython directive
    ipy.setup(app)
    setup.app = app

    # Sphinx v1.4.1 complains about the directive being overwritten,
    # so for now just rename it. When Sphinx 1.4.2 is out this
    # could be changed (use the warning suppression discussed at
    # https://github.com/sphinx-doc/sphinx/issues/2451)
    #
    # app.add_directive('ipython', SherpaIPythonDirective)
    app.add_directive('sherpa', SherpaIPythonDirective)
