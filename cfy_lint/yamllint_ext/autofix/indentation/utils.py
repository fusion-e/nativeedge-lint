import re
import yaml
from io import StringIO

from cfy_lint.yamllint_ext.autofix.indentation.constants import (
    INSTRINSIC_FUNCTIONS
)


class CloudifyLoader(yaml.SafeLoader):
    def construct_mapping(self, node, deep=False):
        mapping = super(CloudifyLoader, self).construct_mapping(
            node, deep=deep)
        # Add 1 so line numbering starts at 1
        # mapping['__line__'] = node.start_mark.line + 1
        return mapping


def repr_str(dumper, data):
    if '\n' in data:
        return dumper.represent_scalar(
            u'tag:yaml.org,2002:str', data, style='>')
    return dumper.org_represent_str(data)


def represent_intrinsic_functions(dumper, data):
    for fn in INSTRINSIC_FUNCTIONS:
        if fn in data:
            return dumper.org_represent_str(
                '{{ {fn}: {val} }}'.format(fn=fn, val=data[fn]))
    return dumper.represent_dict(data)


def increase_indent(self, flow=False, indentless=False):
    indentless = indentless if not indentless else False
    self.indents.append(self.indent)
    if self.indent is None:
        if flow:
            self.indent = self.best_indent
        else:
            self.indent = 0
    elif not indentless:
        self.indent += self.best_indent


yaml.SafeDumper.org_represent_str = yaml.SafeDumper.represent_str
yaml.add_representer(str, repr_str, Dumper=yaml.SafeDumper)
yaml.add_representer(
    dict, represent_intrinsic_functions, Dumper=yaml.SafeDumper)
yaml.SafeDumper.increase_indent = increase_indent


def get_file_content(path):
    f = open(path)
    content = f.readlines()
    f.close()
    return content


def get_yaml_dict(path):
    f = open(path)
    content = yaml.load(f, CloudifyLoader)
    f.close()
    return content


def get_compare_file_content(data):
    file = StringIO()
    yaml.safe_dump(data,
                   file,
                   default_flow_style=False,
                   sort_keys=False,
                   width=float('inf'))
    file.seek(0)
    content = file.readlines()
    file.close()
    return content


def indentify_indentation_corrections(left_content, right_content):
    corrections = {}
    il = ir = 0

    def get_left(lineno):
        while True:
            left = left_content[lineno]
            if len(left.strip()) >= 1:
                break
            lineno += 1
        return lineno, left

    if not basically_equivalent_files(left_content, right_content):
        return {-1: "Bad YAML conversion."}

    while True:
        right_indent = 0
        if il >= len(left_content) or ir >= len(right_content):
            break

        il, left = get_left(il)

        right = right_content[ir]
        right_indent = compare_indentations(left, right)

        if right_indent:
            corrections.update({il + 1: right_indent})

        il += 1
        ir += 1

    return corrections


def compare_indentations(left, right):
    left_matches = re.search(r'^\s{1,}', left)
    right_matches = re.search(r'^\s{1,}', right)
    if right_matches:
        right_indent = len(right_matches.group())
        if left_matches:
            left_indent = len(left_matches.group())
        else:
            left_indent = 0
        if right_indent != left_indent:
            return {
                'original': left,
                'new': '{}{}'.format(' ' * right_indent, left.lstrip()),
            }


def filter_corrections(corrections, line_to_fix):
    new_corrections = {}
    while True:
        try:
            new_corrections.update(
                {
                    line_to_fix: corrections[line_to_fix]
                }
            )
        except KeyError:
            break
        line_to_fix += 1
    return new_corrections


def basically_equivalent_files(a, b):
    a = [lia for lia in a if len(lia.strip())]
    b = [lib for lib in b if len(lib.strip())]
    if len(a) == len(b):
        return True
    return False
