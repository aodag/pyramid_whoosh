from zope.interface import Interface


class ISearcher(Interface):
    def search(query):
        """search for query"""


class IIndex(Interface):
    """index """
    def searcher():
        """create searcher"""

    def writer():
        """create writer"""


class IWriter(Interface):
    def add_document(document):
        """add document to index"""

    def commit():
        """commit documents"""
