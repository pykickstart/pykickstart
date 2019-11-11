
# Sphinx 1.8 changed the location of versionlabels
try:
    from sphinx.domains.changeset import versionlabels
except ImportError:
    from sphinx.locale import versionlabels

# Sphinx 2.0 added a classname mapping
try:
    from sphinx.domains.changeset import versionlabel_classes
except ImportError:
    versionlabel_classes = None

from sphinx.directives.other import VersionChange

__version__ = '0.1.0'

def setup(app):
    _directive = 'versionremoved'

    if _directive not in versionlabels:
        versionlabels[_directive] = 'Removed in version %s'
        if versionlabel_classes is not None:
            versionlabel_classes[_directive] = "removed"
        app.add_directive(_directive, VersionChange)

    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
