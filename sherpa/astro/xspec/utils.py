#
#  Copyright (C) 2017  Smithsonian Astrophysical Observatory
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
from distutils.version import LooseVersion

from . import _xspec

__all__ = ['ModelMeta', 'include_if', 'version_at_least']

XSPEC_VERSION = LooseVersion(_xspec.get_xsversion())


class ModelMeta(type):
    """
    Metaclass for xspec models. The __function__ member in xspec model classes is seamlessly
    transformed from a string representing the low level function in the sherpa xspec extension
    into a proper call, taking into account error cases (e.g. the function cannot be found in the
    xspec extension at runtime).
    """
    NOT_COMPILED_FUNCTION_MESSAGE = "Calling an xspec function that was not compiled"

    def __init__(cls, *args, **kwargs):
        if hasattr(cls, '__function__'):
            try:
                cls._calc = getattr(_xspec, cls.__function__)
            except AttributeError:
                # Error handling: the model meets the condition expressed in the decorator
                # but the low level function is not included in the xspec extension
                cls._calc = ModelMeta._not_compiled

        # The `__function__` member signals that `cls` is a model that needs the `_calc` method
        # to be generated.
        # If the class does not have the `__function__` member, the we assume the class provides
        # a `_calc` method itself, or it does not need it to begin with. This is the case for
        # some classes extending `XSModel` but that are base classes themselves,
        # like `XSAdditiveModel`, or they have a more complex `_calc` implementation, like `XSTableModel`.
        # In principle there is room for mistakes, i.e. a proper model class might be defined without
        # the `__function__` member. Tests should make sure this is not the case. `test_xspec_models`
        # is indeed such a test, because it calls all models making sure they are usable. A model without
        # the `_calc_ method or the `__function__` member would fail the test.
        # The alternative would be to include more logic to handle the error cases, but that would require
        # more tests, making this choice impractical.

        super(ModelMeta, cls).__init__(*args, **kwargs)

    @staticmethod
    def _not_compiled(*args, **kwargs):
        raise AttributeError(ModelMeta.NOT_COMPILED_FUNCTION_MESSAGE)


class include_if(object):
    """
    Generic decorator for including xspec models conditionally. It takes a boolean condition as an argument.
    If the boolean condition is not met, then the model is not included, and its function is replaced with a
    dummy function that throws an exception.

    If the model is disabled, then its class's `version_enabled` attribute is set to `False`.
    """
    DISABLED_MODEL_MESSAGE = "Model {} is disabled because of an unmet condition"

    def __init__(self, condition):
        self.condition = condition

    def __call__(self, model_class):
        if not self.condition:
            model_class.version_enabled = False
            model_class._calc = self._disabled(self.get_message(model_class))

        return model_class

    def get_message(self, model_class):
        return self.DISABLED_MODEL_MESSAGE.format(model_class.__name__)

    @staticmethod
    def _disabled(message):
        def wrapped(*args, **kwargs):
            raise AttributeError(message)

        return wrapped


class version_at_least(include_if):
    """
    Decorator which takes a version string as an argument and enables a model only if
    the xspec version detected at runtime is equal or greater than the one provided to the decorator.
    """
    DISABLED_MODEL_MESSAGE = "Model {} is disabled because XSPEC version >= {} is required"

    def __init__(self, version_string):
        self.version_string = version_string
        include_if.__init__(self, XSPEC_VERSION >= LooseVersion(version_string))

    def get_message(self, model_class):
        return self.DISABLED_MODEL_MESSAGE.format(model_class.__name__, self.version_string)
