import transaction
from .interfaces import IIndex
from .dm import WhooshDataManager


def get_index(request, name):
    reg = request.registry
    return reg.getUtility(IIndex, name=name)


def get_writer(request, name):
    index = get_index(request, name)
    t = transaction.get()
    writer = index.writer()
    dm = WhooshDataManager(writer)
    t.join(dm)
    return dm


def get_searcher(request, name):
    index = get_index(request, name)
    return index.searcher()
