##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from zope import interface
from zope.component import getUtilitiesFor
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zope.i18nmessageid import MessageFactory

from zojax.content.type.interfaces import IPortalType

_ = MessageFactory(u'zojax.portlets.recent')


class PortletTypesVocabulary(object):
    interface.implements(IVocabularyFactory)

    def __call__(self, context):
        pt = []

        for name, ct in getUtilitiesFor(IPortalType, context=context):
            pt.append((ct.title, name))

        pt.sort()

        return SimpleVocabulary(
            [SimpleTerm('__all__', '__all__', _('All portal types'))] +
            [SimpleTerm(name, name, title) for title, name in pt])
        

def spaceModesVocabulary(context):
    return SimpleVocabulary((
        SimpleTerm(1, '1', _(u'All spaces')),
        SimpleTerm(2, '2', _(u'Current space')),
        SimpleTerm(3, '3', _(u"Current space and subspaces")),
        ))

