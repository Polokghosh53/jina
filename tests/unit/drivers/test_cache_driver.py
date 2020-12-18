import os
from pathlib import Path
from typing import Any

import numpy as np
import pytest

from jina import DocumentSet
from jina.drivers.cache import BaseCacheDriver, CONTENT_HASH_KEY, ID_KEY
from jina.executors import BaseExecutor
from jina.executors.indexers.cache import DocIDCache
from jina.proto import jina_pb2
from jina.types.document import uid, Document, UniqueId
from tests import random_docs


class MockCacheDriver(BaseCacheDriver):

    @property
    def exec_fn(self):
        return self._exec_fn

    def on_hit(self, req_doc: 'jina_pb2.DocumentProto', hit_result: Any) -> None:
        raise NotImplementedError

    @property
    def docs(self):
        return DocumentSet(list(random_docs(10)))


def test_cache_driver_twice(tmpdir):
    docs = DocumentSet(list(random_docs(10)))
    driver = MockCacheDriver()
    # FIXME DocIdCache doesn't use tmpdir, it saves in curdir
    with DocIDCache(tmpdir) as executor:
        assert not executor.handler_mutex
        driver.attach(executor=executor, pea=None)
        driver._traverse_apply(docs)

        with pytest.raises(NotImplementedError):
            # duplicate docs
            driver._traverse_apply(docs)

        # new docs
        docs = list(random_docs(10, start_id=100))
        driver._traverse_apply(docs)
        filename = executor.save_abspath

        # check persistence
        executor.save()
        assert Path(filename).exists()


def test_cache_driver_tmpfile():
    docs = list(random_docs(10, embedding=False))
    print(f'test_cache_driver_tmpfile')
    executor = None
    driver = None
    driver = MockCacheDriver(field=ID_KEY)
    with DocIDCache() as executor:
        assert not executor.handler_mutex
        driver.attach(executor=executor, pea=None)

        # FIXME seems somehow the executor is loading the store from the previous run
        executor.store = {}
        print(executor.store)
        driver._traverse_apply(docs)

        with pytest.raises(NotImplementedError):
            # duplicate docs
            driver._traverse_apply(docs)

        # new docs
        docs = list(random_docs(10, start_id=100, embedding=False))
        driver._traverse_apply(docs)

    assert Path(executor.index_abspath).exists()


def test_cache_driver_from_file(tmp_path):
    filename = tmp_path / 'test-tmp.bin'
    docs = list(random_docs(10, embedding=False))
    with open(filename, 'wb') as fp:
        fp.write(np.array([int(d.id) for d in docs], dtype=np.int64).tobytes())

    driver = MockCacheDriver(field=CONTENT_HASH_KEY)
    with DocIDCache(filename) as executor:
        assert not executor.handler_mutex
        driver.attach(executor=executor, pea=None)

        with pytest.raises(NotImplementedError):
            # duplicate docs
            driver._traverse_apply(docs)

        # new docs
        docs = list(random_docs(10, start_id=100))
        driver._traverse_apply(docs)
        # check persistence
        assert Path(filename).exists()


class MockBaseCacheDriver(BaseCacheDriver):

    @property
    def exec_fn(self):
        return self._exec_fn

    def on_hit(self, req_doc: 'jina_pb2.DocumentProto', hit_result: Any) -> None:
        raise NotImplementedError


def test_cache_content_driver_same_content(tmpdir):
    doc1 = Document(id=1)
    doc1.text = 'blabla'
    doc1.update_content_hash()
    docs1 = DocumentSet([doc1])

    doc2 = Document(id=2)
    doc2.text = 'blabla'
    doc2.update_content_hash()
    docs2 = DocumentSet([doc2])
    assert doc1.content_hash == doc2.content_hash

    driver = MockBaseCacheDriver(field=CONTENT_HASH_KEY)
    filename = None

    with DocIDCache(tmpdir) as executor:
        driver.attach(executor=executor, pea=None)
        driver._traverse_apply(docs1)

        with pytest.raises(NotImplementedError):
            driver._traverse_apply(docs2)

        assert executor.size == 1
        executor.save()
        filename = executor.save_abspath

    # update
    old_hash = doc1.content_hash
    new_string = 'blabla-new'
    doc1.text = new_string
    doc1.update_content_hash()
    with BaseExecutor.load(filename) as executor:
        executor.update([UniqueId(1)], [doc1.content_hash])
        executor.save()

    with BaseExecutor.load(filename) as executor:
        assert executor.query(doc1.content_hash) is True
        assert executor.query(old_hash) is None

    # delete
    with BaseExecutor.load(filename) as executor:
        executor.delete([UniqueId(doc1.id)])
        executor.save()

    with BaseExecutor.load(filename) as executor:
        assert executor.query(doc1.content_hash) is None


def test_cache_content_driver_same_id(tmp_path):
    filename = tmp_path / 'docidcache.bin'
    doc1 = Document(id=1)
    doc1.text = 'blabla'
    doc1.update_content_hash()
    docs1 = DocumentSet([doc1])

    doc2 = Document(id=1)
    doc2.text = 'blabla2'
    doc2.update_content_hash()
    docs2 = DocumentSet([doc2])

    driver = MockBaseCacheDriver(field=CONTENT_HASH_KEY)

    with DocIDCache(filename, field=CONTENT_HASH_KEY) as executor:
        driver.attach(executor=executor, pea=None)
        driver._traverse_apply(docs1)
        driver._traverse_apply(docs2)
        assert executor.size == 2
