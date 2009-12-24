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
from zope import interface, component
from zope.proxy import removeAllProxies
from zope.component import queryUtility, getMultiAdapter
from zope.app.component.hooks import getSite
from zope.traversing.browser import absoluteURL
from zope.dublincore.interfaces import IDCPublishing, IDCTimes
from zope.app.container.interfaces import IObjectMovedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from zojax.catalog.interfaces import ICatalog
from zojax.content.type.interfaces import IItem, IPortalType, IDraftedContent

from zojax.cache.view import cache
from zojax.cache.tag import SiteTag
from zojax.cache.keys import Principal
from zojax.portlet.cache import PortletId, PortletModificationTag

from interfaces import IRecentlyAddedPortlet
from interfaces import IRecentlyChangedPortlet


MovedTag = SiteTag('zojax.portlets.recent:moved')
ModifiedTag = SiteTag('zojax.portlets.recent:modified')


@component.adapter(IPortalType, IObjectMovedEvent)
def addedHandler(ob, ev):
    if not IDraftedContent.providedBy(ob):
        MovedTag.update(ob)


@component.adapter(IPortalType, IObjectModifiedEvent)
def modifiedHandler(ob, ev):
    if not IDraftedContent.providedBy(ob):
        ModifiedTag.update(ob)



class RecentPortlet(object):

    items = None
    index = ''

    def update(self):
        super(RecentPortlet, self).update()

        self.site = getSite()
        catalog = queryUtility(ICatalog)

        if catalog is not None:
            if '__all__' in self.types:
                results = catalog.searchResults(
                    searchContext=(self.site,),
                    typeType={'any_of': ('Portal type',)},
                    isDraft={'any_of': (False,)},
                    sort_order='reverse', sort_on=self.index)
            else:
                results = catalog.searchResults(
                    searchContext=(self.site,),
                    sort_order='reverse', sort_on=self.index,
                    type={'any_of': self.types},
                    isDraft={'any_of': (False,)},)

            if results:
                self.items = results

    def isAvailable(self):
        if not self.items:
            return False

        return super(RecentPortlet, self).isAvailable()

    def recentItems(self):
        request = self.request

        idx = 1
        items = []
        for obj in self.items:
            item = IItem(obj, None)

            dc = IDCTimes(obj)

            try:
                url = absoluteURL(removeAllProxies(obj), request)
            except TypeError:
                continue

            yield {'title': getattr(item, 'title', obj.__name__) \
                       or obj.__name__,
                   'description': getattr(item, 'description', u''),
                   'icon': getMultiAdapter((obj, request), name='zmi_icon')(),
                   'modified': dc.modified,
                   'created': dc.created,
                   'url': '%s/'%url,
                   'item': obj}

            if idx >= self.number:
                break

            idx = idx + 1


class RecentlyAddedPortlet(RecentPortlet):
    interface.implements(IRecentlyAddedPortlet)

    index = 'created'

    @cache(PortletId(), Principal, MovedTag, PortletModificationTag)
    def updateAndRender(self):
        return super(RecentlyAddedPortlet, self).updateAndRender()


class RecentlyChangedPortlet(RecentPortlet):
    interface.implements(IRecentlyChangedPortlet)

    index = 'modified'

    @cache(PortletId(), Principal, MovedTag,ModifiedTag, PortletModificationTag)
    def updateAndRender(self):
        return super(RecentlyChangedPortlet, self).updateAndRender()
