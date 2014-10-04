from pyramid.exceptions import ConfigurationError
from whoosh.index import create_in
from zope.interface import directlyProvides
from .interfaces import IIndex


discriminator = 'pyramid_whoosh'

def get_index_directory(config, name):
    conf_name = "pyramid_whoosh." + name + ".indexdir"
    if conf_name not in config.registry.settings:
        raise ConfigurationError(conf_name)

    return config.registry.settings[conf_name]


def add_schema(config, name, schema):
    indexdir = get_index_directory(config, name)
    index = create_in(indexdir, schema)
    directlyProvides(index, IIndex)
    reg = config.registry

    def register():
        reg.registerUtility(index, name=name)

    intr = config.introspectable(category_name="pyramid_whoosh",
                                 discriminator=discriminator + ":" + name,
                                 title="whoosh search index: " + name,
                                 type_name="pyramid_whoosh.interfaces.IIndex")
    intr["indexdir"] = indexdir
    config.action(discriminator + ":" + name,
                  register,
                  introspectables=(intr,))
