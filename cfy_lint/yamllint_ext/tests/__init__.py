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
