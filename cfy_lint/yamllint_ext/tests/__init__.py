import os
import io
from .. import generators


def get_buffer(file_path='resources/blueprint.yaml', read=False):
    pp = os.path.join(os.path.dirname(__file__), file_path)
    return io.open(pp, newline='')


def get_gen(file_path='resources/blueprint.yaml',
            gen=generators.node_generator):
    buffer = get_buffer(file_path)
    return gen(buffer)


def get_file_obj(content):
    return io.StringIO(content, newline='')


def get_loader(yaml_content):
    buffer = get_file_obj(yaml_content)
    return generators.SafeLineLoader(buffer)


def get_gen_as_list(callable, payload):
    while True:
        try:
            if isinstance(payload, dict):
                return list(
                    callable(
                        **payload
                    )
                )
            else:
                return list(
                    callable(
                        payload
                    )
                )

        except (StopIteration, AttributeError):
            break
