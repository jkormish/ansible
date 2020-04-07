# base classes for virtualization facts
# -*- coding: utf-8 -*-
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.module_utils.facts.collector import BaseFactCollector


class Virtual:
    """
    This is a generic Virtual subclass of Facts.  This should be further
    subclassed to implement per platform.  If you subclass this,
    you should define:
    - virtualization_type
    - virtualization_role
    - container (e.g. solaris zones, freebsd jails, linux containers)

    All subclasses MUST define platform.
    """
    platform = 'Generic'

    # FIXME: remove load_on_init if we can
    def __init__(self, module, load_on_init=False):
        self.module = module

    # FIXME: just here for existing tests cases till they are updated
    def populate(self, collected_facts=None):
        return self.get_virtual_facts()

    def get_virtual_facts(self):
        return {'virtualization_type': '',
                             'virtualization_role': ''}


class VirtualCollector(BaseFactCollector):
    name = 'virtual'
    _fact_class = Virtual
    _fact_ids = set(['virtualization_type',
                     'virtualization_role'])

    def collect(self, module=None, collected_facts=None):
        collected_facts = collected_facts or {}
        if not module:
            return {}

        # Network munges cached_facts by side effect, so give it a copy
        facts_obj = self._fact_class(module)

        return facts_obj.populate(collected_facts=collected_facts)
