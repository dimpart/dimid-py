# -*- coding: utf-8 -*-
# ==============================================================================
# MIT License
#
# Copyright (c) 2022 Albert Moky
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

from abc import ABC, abstractmethod
from typing import Optional, Union, Dict, List
from typing import Iterable

from dimsdk import PrivateKey, SignKey, DecryptKey
from dimsdk import ID, Meta, Document


class PrivateKeyDBI(ABC):
    """ PrivateKey Table """

    META = 'M'  # ID_KEY_TAG
    VISA = 'V'  # MSG_KEY_TAG

    @abstractmethod
    async def save_private_key(self, key: PrivateKey, user: ID, key_type: str = 'M') -> bool:
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.save_private_key()'
        )

    @abstractmethod
    async def private_keys_for_decryption(self, user: ID) -> List[DecryptKey]:
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.private_keys_for_decryption()'
        )

    @abstractmethod
    async def private_key_for_signature(self, user: ID) -> Optional[SignKey]:
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.private_key_for_signature()'
        )

    @abstractmethod
    async def private_key_for_visa_signature(self, user: ID) -> Optional[SignKey]:
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.private_key_for_visa_signature()'
        )

    #
    #  Conveniences
    #

    @classmethod
    def convert_decrypt_keys(cls, keys: Iterable[PrivateKey]) -> List[DecryptKey]:
        decrypt_keys = []
        for item in keys:
            if isinstance(item, DecryptKey):
                decrypt_keys.append(item)
        return decrypt_keys

    @classmethod
    def convert_private_keys(cls, keys: Iterable[DecryptKey]) -> List[PrivateKey]:
        private_keys = []
        for item in keys:
            if isinstance(item, PrivateKey):
                private_keys.append(item)
        return private_keys

    @classmethod
    def revert_private_keys(cls, keys: Iterable[PrivateKey]) -> List[Dict]:
        array = []
        for item in keys:
            key_info = item.to_dict()
            array.append(key_info)
        return array

    @classmethod
    def insert(cls, item: PrivateKey, array: List[PrivateKey]) -> Optional[List[PrivateKey]]:
        index = cls.find(item=item, array=array)
        if index == 0:
            # nothing changed
            return None
        elif index > 0:
            # move to the front
            array.pop(index)
        elif len(array) > 2:
            # keep only last three records
            array.pop()
        array.insert(0, item)
        return array

    @classmethod
    def find(cls, item: Union[DecryptKey, PrivateKey], array: List[PrivateKey]) -> int:
        index = 0
        data = item.get('data')
        for key in array:
            if key.get('data') == data:
                return index
            index += 1
        return -1


class MetaDBI(ABC):
    """ Meta Table """

    @abstractmethod
    async def save_meta(self, meta: Meta, identifier: ID) -> bool:
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.save_meta()'
        )

    @abstractmethod
    async def get_meta(self, identifier: ID) -> Optional[Meta]:
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.get_meta()'
        )


class DocumentDBI(ABC):
    """ Document Table """

    @abstractmethod
    async def save_document(self, document: Document, identifier: ID) -> bool:
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.save_document()'
        )

    @abstractmethod
    async def get_documents(self, identifier: ID) -> List[Document]:
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.get_documents()'
        )


# noinspection PyAbstractClass
class AccountDBI(PrivateKeyDBI, MetaDBI, DocumentDBI, ABC):
    """ Account Database """
    pass
