# -*- coding: utf-8 -*-
# ==============================================================================
# MIT License
#
# Copyright (c) 2024 Albert Moky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==============================================================================

from typing import Optional, Any

from dimsdk import Converter, BaseConverter
from dimsdk import DateTime

from dimsdk import AsymmetricAlgorithms
from dimsdk import AsymmetricKey, PrivateKey, PublicKey
from dimplugins import RSAPrivateKeyFactory, RSAPublicKeyFactory
from dimplugins import ExtensionLoader
from dimplugins import PluginLoader


class LibraryLoader:

    def __init__(self, extensions: ExtensionLoader = None, plugins: PluginLoader = None):
        super().__init__()
        self.__extensions = CommonExtensionLoader() if extensions is None else extensions
        self.__plugins = CommonPluginLoader() if plugins is None else plugins
        self.__loaded = False

    def run(self):
        if self.__loaded:
            # no need to load it again
            return
        else:
            # mark it to loaded
            self.__loaded = True
        # try to load all plugins
        self.load()

    def load(self):
        self.__extensions.load()
        self.__plugins.load()


# noinspection PyMethodMayBeStatic
class CommonExtensionLoader(ExtensionLoader):
    """ Extensions Loader """
    pass


# noinspection PyMethodMayBeStatic
class CommonPluginLoader(PluginLoader):
    """ Plugin Loader """

    # Override
    def load(self):
        Converter.converter = _SafeConverter()
        super().load()

    # protected
    def register_rsa_key_factories(self):
        """ RSA keys with created time """
        # Public Key: RSA
        rsa_pub = RSAPublicKeyFactory()
        PublicKey.set_factory(algorithm=AsymmetricAlgorithms.RSA, factory=rsa_pub)
        PublicKey.set_factory(algorithm='SHA256withRSA', factory=rsa_pub)
        PublicKey.set_factory(algorithm='RSA/ECB/PKCS1Padding', factory=rsa_pub)
        # Private Key: RSA
        rsa_pri = _RSAPrivateKeyFactory()
        PrivateKey.set_factory(algorithm=AsymmetricAlgorithms.RSA, factory=rsa_pri)
        PrivateKey.set_factory(algorithm='SHA256withRSA', factory=rsa_pri)
        PrivateKey.set_factory(algorithm='RSA/ECB/PKCS1Padding', factory=rsa_pri)


class _RSAPrivateKeyFactory(RSAPrivateKeyFactory):

    # Override
    def generate_private_key(self) -> Optional[PrivateKey]:
        pri_key = super().generate_private_key()
        pub_key = pri_key.public_key
        # set created time
        self._set_created_time(key=pri_key)
        self._set_created_time(key=pub_key)
        # OK
        return pri_key

    # noinspection PyMethodMayBeStatic
    def _set_created_time(self, key: AsymmetricKey):
        now = key.get_datetime(key='time')
        if now is None:
            now = DateTime.now()
            key.set_datetime(key='time', value=now)


class _SafeConverter(BaseConverter):

    # Override
    def get_bool(self, value: Any, default: Optional[bool]) -> Optional[bool]:
        try:
            return super().get_bool(value=value, default=default)
        except ValueError:
            return default

    # Override
    def get_int(self, value: Any, default: Optional[int]) -> Optional[int]:
        try:
            return super().get_int(value=value, default=default)
        except ValueError:
            return default

    # Override
    def get_float(self, value: Any, default: Optional[float]) -> Optional[float]:
        try:
            return super().get_float(value=value, default=default)
        except ValueError:
            return default

    # Override
    def get_datetime(self, value: Any, default: Optional[DateTime]) -> Optional[DateTime]:
        try:
            return super().get_datetime(value=value, default=default)
        except ValueError:
            return default
