########
# Copyright (c) 2014-2022 Cloudify Platform Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import yamllint.rules
from ..utils import update_dict_values_recursive
from yamllint.config import YamlLintConfig
from yamllint.config import (
    validate_rule_conf,
    YamlLintConfigError)

from .constants import DEFAULT_CLOUDIFY_YAMLLINT_CONFIG


class YamlLintConfigExt(YamlLintConfig):
    def __init__(self, content=None, file=None, yamllint_rules=None):
        if content:
            update_dict_values_recursive(
                DEFAULT_CLOUDIFY_YAMLLINT_CONFIG, content)
        self._yamllint_rules = yamllint_rules or yamllint.rules
        super().__init__(DEFAULT_CLOUDIFY_YAMLLINT_CONFIG, file)

    @property
    def yamllint_rules(self):
        return self._yamllint_rules

    @yamllint_rules.setter
    def yamllint_rules(self, value):
        self._yamllint_rules = value

    def enabled_rules(self, filepath):
        return [self.yamllint_rules.get(id) for id, val in self.rules.items()
                if val is not False and (
                    filepath is None or 'ignore' not in val or
                    not val['ignore'].match_file(filepath))]

    def validate(self):
        for id in self.rules:
            try:
                rule = self.yamllint_rules.get(id)
            except Exception as e:
                raise YamlLintConfigError('invalid config: %s' % e)

            self.rules[id] = validate_rule_conf(rule, self.rules[id])
