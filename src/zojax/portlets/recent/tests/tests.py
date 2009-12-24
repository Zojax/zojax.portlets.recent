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
import os
import unittest, doctest
from zope import interface, component
from zope.app.testing import setup
from zope.app.testing.functional import ZCMLLayer
from zope.app.rotterdam import Rotterdam
from zojax.content.type.interfaces import IItem
from zojax.content.type.item import PersistentItem
from zojax.content.type.container import ContentContainer
from zojax.layoutform.interfaces import ILayoutFormLayer

class IDefaultSkin(ILayoutFormLayer, Rotterdam):
    """ skin """


zojaxRecentPortlets = ZCMLLayer(
    os.path.join(os.path.split(__file__)[0], 'ftesting.zcml'),
    __name__, 'zojaxRecentPortlets', allow_teardown=True)


class IContent(IItem):
    """ """


class IFolder(IItem):
    """ folder """


class IContentType(interface.Interface):
    """ """


class Folder(ContentContainer):
    interface.implements(IFolder)


class Content(PersistentItem):
    interface.implements(IContent)


def test_suite():
    testbrowser = doctest.DocFileSuite(
        "tests.txt",
        optionflags=doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE)
    testbrowser.layer = zojaxRecentPortlets

    return unittest.TestSuite((testbrowser,))
