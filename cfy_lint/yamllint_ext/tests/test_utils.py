
import os
import io
import yaml
from mock import Mock, call, patch

from .. import utils
from .. import generators


def get_buffer(file_path='resources/blueprint.yaml'):
    pp = os.path.join(os.path.dirname(__file__), file_path)
    return io.open(pp, newline='')


def get_gen(file_path='resources/blueprint.yaml', gen=generators.node_generator):
    buffer = get_buffer(file_path)
    return gen(buffer)


def test_process_relevant_tokens():

    class Foo(object):
        def __init__(self, keyword):
            self.prev = Mock()
            self.prev.node = Mock(value=keyword)

    @utils.process_relevant_tokens(Foo, 'foo')
    def foo(**kwargs):
        yield kwargs

    tok = Foo('foo')
    assert next(foo(token=tok)) == {'token': tok}

    try:
        tok = Foo('bar')
        next(foo(token=tok))
    except StopIteration:
        pass

    @utils.process_relevant_tokens(Foo, ['baz'])
    def baz(**kwargs):
        yield kwargs

    tok = Foo('baz')
    assert next(baz(token=tok)) == {'token': tok}

    try:
        tok = Foo('bar')
        next(baz(token=tok))
    except StopIteration:
        pass


def test_recurse_mapping():
    gen = get_gen()
    inputs = []
    previous = None
    while True:
        try:
            yaml_mapped = next(gen)
        except StopIteration:
            break
        current = utils.recurse_mapping(yaml_mapped)
        if previous == 'inputs' and isinstance(current, dict):
            inputs.extend(current.keys())
        elif previous == 'get_input' and isinstance(current, str):
            assert current in inputs
        previous = current


def test_setup_node_template():
    gen = get_gen()
    node_templates = []
    while True:
        try:
            yaml_mapped = next(gen)
        except StopIteration:
            break
        if not isinstance(yaml_mapped, yaml.nodes.MappingNode):
            continue
        if not isinstance(yaml_mapped.value, (list, tuple)):
            continue
        if not isinstance(yaml_mapped.value[0], (list, tuple)):
            continue
        if not isinstance(yaml_mapped.value[0][0], yaml.nodes.ScalarNode):
            continue
        if not yaml_mapped.value[0][0].value == 'foo_template':
            continue
        try:
            node_template = utils.setup_node_template(yaml_mapped.value[0])
        except TypeError:
            continue
        if node_template:
            node_templates.append(node_template)
        node_template = None
    assert node_templates[0].name == 'foo_template'
    assert node_templates[0].node_type == 'foo_type'


def test_update_model():
    elem_mock = Mock()
    elem_mock.line_no = 100
    elem_mock.curr = yaml.tokens.ScalarToken('node_templates', 'node_templates', 100, 200)
    elem_mock.nextnext = yaml.tokens.BlockMappingStartToken(201, 300)
    with patch('cfy_lint.yamllint_ext.utils.context') as context:
        utils.update_model(elem_mock)
    assert call.__setitem__('current_top_level', 'node_templates') in context.mock_calls


def test_assign_nested_node_template_level():
    elem_mock = Mock()
    elem_mock.line_no = 100
    elem_mock.curr = yaml.tokens.ScalarToken(
        'properties', 'properties', 100, 200)
    elem_mock.nextnext = yaml.tokens.BlockEntryToken(201, 300)
    assert utils.assign_nested_node_template_level(elem_mock) == 'properties'


def test_assign_current_top_level():
    elem_mock = Mock()
    elem_mock.line_no = 100
    elem_mock.curr = yaml.tokens.ScalarToken(
        'inputs', 'inputs', 100, 200)
    elem_mock.nextnext = yaml.tokens.BlockMappingStartToken(201, 300)
    assert utils.assign_current_top_level(elem_mock) == 'inputs'
