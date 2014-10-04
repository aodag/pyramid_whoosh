import transaction
from zope.interface import implementer
from .interfaces import IWriter


@implementer(IWriter)
class WhooshDataManager(object):

    transaction_manager = transaction.manager

    def __init__(self, writer):
        self.writer = writer
        self.documents = []

    def close(self):
        self.writer.cancel()

    def add(self, document):
        self.documents.append(document)

    def abort(self):
        self.documents = []

    def tpc_begin(self, transaction):
        pass

    def commit(self, transaction):
        pass

    def tpc_vote(self, transaction):
        for doc in self.documents:
            self.writer.add_document(**doc)

    def tpc_abort(self, transaction):
        self.writer.cancel()

    def tpc_finish(self, transaction):
        self.writer.commit()

