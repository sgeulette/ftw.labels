# -*- coding: utf-8 -*-
from ftw.labels.interfaces import ILabelJar
from ftw.labels.interfaces import ILabelJarChild
from ftw.labels.interfaces import ILabelRoot
from ftw.labels.interfaces import ILabelSupport
from ftw.labels.labeling import ILabeling
from plone import api
from zope.annotation.interfaces import IAnnotations

# The migration function -------------------------------------------------------
def migrate(context):
    """This migration function:
    """
    # take all elements who provides ftw.labels.interfaces.ILabelRoot or ILabelJarChild
    portal_catalog = api.portal.get_tool('portal_catalog')
    brains = set(portal_catalog(object_provides=ILabelRoot.__identifier__) +
                 portal_catalog(object_provides=ILabelJarChild.__identifier__))
    for brain in brains:
        object = brain.getObject()
        jar = ILabelJar(object)
        for key in jar.storage.keys():
            if 'by_user' not in jar.storage[key].keys():
                # give default value if not exist
                jar.storage[key]['by_user'] = False

    # take all elements who provides ftw.labels.interfaces.IlabelSupport
    brains = portal_catalog(object_provides=ILabelSupport.__identifier__)
    # Transform PersistentList in PersistentMapping
    for brain in brains:
        object = brain.getObject()
        labeling = ILabeling(object)
        old_values = [label for label in labeling.storage]
        annotation = IAnnotations(object)
        del annotation['ftw.labels:labeling']
        labeling._storage = None
        labeling.update(old_values)

    print(brains)
# ------------------------------------------------------------------------------
