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

from cfy_lint.yamllint_ext.utils import context
from contextlib import contextmanager


@contextmanager
def filelines(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    yield lines
    with open(filename, 'w') as file:
        file.writelines(lines)


def is_list(line):
    if line.lstrip().startswith('-'):
        return True


def get_eol(line):
    """Gets the end of a line."""
    stripped = line.rstrip()
    eol = ''
    for i in range(0, len(line)):
        try:
            assert stripped[i] == line[i]
        except IndexError:
            if line[i] != ' ':
                eol += line[i]
    return stripped, eol


# Creating a dictionary that connects two changes that happen in empty_lined and add_label.
def build_diff_lines():
    print('context[add_label]: {}'.format(context['add_label']))
    print('context[line_diff]: {}'.format(context['line_diff']))

    if context['add_label'] and not context['line_diff']:
        context['line_diff'][0] = 0
        count = 1
        for i in context['add_label']:
            context['line_diff'].update({i: count})
            count += 1

    elif context['add_label'] and context['line_diff']:
        print('3')
        keys_diff = list(context['line_diff'].keys())
        len_keys_diff = len(keys_diff)
        print('keys_diff: {}'.format(keys_diff))
        if context['add_label'][0] < keys_diff[-1]:
            for num in context['add_label']:
                i = 0
                print('num: {}'.format(num))

                while i >= len_keys_diff and num > keys_diff[i]: 
                    i += 1

                k = i
                while k < len(context['line_diff']):
                    context['line_diff'][keys_diff[k]] = context['line_diff'][keys_diff[k]] + 1
                    k += 1
                i = k

        # Creating a dict_to_update with the addition of items from add_label
        # Then connecting it with the line_diff dictionary
        print('keys_diff: {}'.format(keys_diff))
        print('2context[line_diff]: {}'.format(context['line_diff']))
        print('-----------------------------------------------------')

        i = 0
        while_condition = True
        prev_value = None
        dict_to_update = {}
        counter = 0
        for key, value in context['line_diff'].items(): 
            counter = 0   
            while while_condition and key > context['add_label'][i]: 
                dict_to_update.update(
                    {context['add_label'][i] + 1: prev_value + 1 + counter})
                i += 1
                counter += 1
                if i >= len(context['add_label']):
                    while_condition = False
            
            prev_value = value
            if not while_condition:
                break
        context['line_diff'] = connect_two_sorted_dicts(context['line_diff'],
                                                        dict_to_update)
        
        print('3context[line_diff]: {}'.format(context['line_diff']))
        print('-----------------------------------------------------')


def connect_two_sorted_dicts(dict1, dict2):
    result_dict = {}
    keys1 = iter(dict1)
    keys2 = iter(dict2)
    key1 = next(keys1, None)
    key2 = next(keys2, None)

    while key1 is not None or key2 is not None:
        if key2 is None or (key1 is not None and key1 < key2):
            result_dict[key1] = dict1[key1]
            key1 = next(keys1, None)
        else:
            result_dict[key2] = dict2[key2]
            key2 = next(keys2, None)
    
    return result_dict
