import unittest
from pyramid import testing
from testfixtures import ShouldRaise, TempDirectory
from zope.interface.verify import verifyObject


class Testadd_schema(unittest.TestCase):
    def _makeSchema(self):
        from whoosh.fields import Schema, TEXT
        schema = Schema(title=TEXT, content=TEXT)
        return schema

    def _callFUT(self, *args, **kwargs):
        from pyramid_whoosh.directives import add_schema
        return add_schema(*args, **kwargs)

    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_whoosh')

    def tearDown(self):
        testing.tearDown()

    def test_prepare(self):
        self.assertTrue(hasattr(self.config, "add_schema"))

    def test_add_schema_no_config(self):
        from pyramid.exceptions import ConfigurationError
        schema = self._makeSchema()
        with ShouldRaise(ConfigurationError):
            self._callFUT(self.config, "dummy", schema)

    def test_add_schema(self):
        from pyramid_whoosh.interfaces import IIndex
        schema = self._makeSchema()
        with TempDirectory() as d:
            self.config.registry.settings["pyramid_whoosh.dummy.indexdir"] = d.path
            self._callFUT(self.config, "dummy", schema)
            result = self.config.registry.getUtility(IIndex, name="dummy")
            verifyObject(IIndex, result)

    def test_add_schema_introspection(self):
        from pyramid_whoosh.interfaces import IIndex
        schema = self._makeSchema()
        with TempDirectory() as d:
            self.config.registry.settings["pyramid_whoosh.dummy.indexdir"] = d.path
            self._callFUT(self.config, "dummy", schema)
            introspector = self.config.registry.introspector
            intr = introspector.get('pyramid_whoosh', 'pyramid_whoosh:dummy')
            self.assertIsNotNone(intr)
            self.assertEqual(intr.title, "whoosh search index: dummy")
            self.assertEqual(intr["indexdir"], d.path)


class Testget_writer(unittest.TestCase):
    def _callFUT(self, *args, **kwargs):
        from pyramid_whoosh.api import get_writer
        return get_writer(*args, **kwargs)

    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_whoosh')

    def tearDown(self):
        testing.tearDown()

    def test_it(self):
        from pyramid_whoosh.interfaces import IIndex
        import transaction
        request = testing.DummyRequest()

        class DummyWriter(object):
            pass
        dummy_writer = DummyWriter()
        class DummyIndex(object):
            def writer(self):
                return dummy_writer
        dummy_index = DummyIndex()
        request.registry.registerUtility(dummy_index, IIndex, name="dummy")
        result = self._callFUT(request, "dummy")
        self.assertEqual(result.writer, dummy_writer)

        t = transaction.get()
        self.assertIn(result, t._resources)


class TestIt(unittest.TestCase):
    def _makeSchema(self):
        from whoosh.fields import Schema, TEXT
        schema = Schema(title=TEXT, content=TEXT)
        return schema

    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_whoosh')

    def tearDown(self):
        testing.tearDown()

    def test_it(self):
        from pyramid_whoosh.api import get_writer, get_index
        schema = self._makeSchema()
        request = testing.DummyRequest()
        with TempDirectory() as d:
            self.config.registry.settings["pyramid_whoosh.dummy.indexdir"] = d.path
            self.config.add_schema("dummy", schema)
            writer = get_writer(request, "dummy")
            writer.add(dict(title=u"this is dummy",
                            content=u"dummy content"))
            import transaction
            transaction.commit()
            get_index(request, "dummy").close()
