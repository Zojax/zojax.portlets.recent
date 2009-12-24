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
from zope import interface, schema
from zope.i18nmessageid import MessageFactory

_ = MessageFactory(u'zojax.portlets.recent')


class IRecentPortlet(interface.Interface):
    """ recent portlet """

    number = schema.Int(
        title = _(u'Number of items'),
        description = _(u'Number of items to display'),
        default = 7,
        required = True)

    types = schema.List(
        title = _(u'Portal types'),
        description = _('Portal types to list in portlet.'),
        value_type = schema.Choice(
            vocabulary='zojax.portlets.recent-portaltypes'),
        default = ['__all__'],
        required = True)


class IRecentlyAddedPortlet(IRecentPortlet):
    """ recently added content portlet """


class IRecentlyChangedPortlet(IRecentPortlet):
    """ recently changed content portlet """
