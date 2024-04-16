# Copyright © 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

import yaml
import yamllint.rules
from ne_lint.yamllint_ext.utils import update_dict_values
from yamllint.config import YamlLintConfig
from yamllint.config import (
    validate_rule_conf,
    YamlLintConfigError)

from ne_lint.yamllint_ext.config.constants import \
    DEFAULT_YAMLLINT_CONFIG


class YamlLintConfigExt(YamlLintConfig):
    def __init__(self, content=None, file=None, yamllint_rules=None):
        default_config = DEFAULT_YAMLLINT_CONFIG
        if content:
            updated_dict = update_dict_values(
                DEFAULT_YAMLLINT_CONFIG, content)
            default_config = yaml.dump(updated_dict)
        self._yamllint_rules = yamllint_rules or yamllint.rules
        super().__init__(default_config, file)

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
