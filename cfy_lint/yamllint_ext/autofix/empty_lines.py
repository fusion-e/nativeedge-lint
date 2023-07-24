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

import re

from cfy_lint.yamllint_ext.utils import context
from cfy_lint.yamllint_ext.autofix.utils import filelines


def fix_empty_lines(problem):
    if problem.fix_all or problem.fix_new_lines:
        with filelines(problem.file) as lines:
            successive_blank_lines = 0
            deleted_lines = 0
            index = 0
            current_sum = 0
            keys = []
            pattern = "^ *\n"
            context['line_diff'][0] = 0
            
            #remove blanklines from start of file
            while re.match(pattern, lines[0]):
                lines.pop(0)

            while index < (len(lines)-1):
                line = lines.pop(index)

                if re.match(pattern, line):
                    successive_blank_lines -= 1
                    if successive_blank_lines <= -2:
                        continue
                else:
                    if successive_blank_lines < -1:
                        current_sum += successive_blank_lines + 1
                        context['line_diff'][index + deleted_lines] = current_sum
                                
                        deleted_lines -= successive_blank_lines + 1
                        keys.append(index)
                    successive_blank_lines = 0

                lines.insert(index, line)
                index += 1
            #remove blanklines from end of file
            while re.match(pattern, lines[-1]):
                lines.pop(-1)

            print('1context[line_diff]: {}'.format(context['line_diff']))
            print('-----------------------------------------------------')

            updated_add_label = []
            keys_diff = list(context['line_diff'].keys())
            l = context['add_label']
            print(l)
            for num in l:
                i = 0
                while num > keys_diff[i]:
                    i += 1
                
                updated_add_label.append(num + context['line_diff'][keys_diff[i-1]])


            # add 1 to dict
            for num in updated_add_label: # [9, 13, 18]
                i = 0
                while num > keys_diff[i]: #  [0, 8, 20, 24, 35, 39]
                    i += 1
                
                k = i

                while k < len(context['line_diff']):
                    context['line_diff'][keys_diff[k]] = context['line_diff'][keys_diff[k]] + 1
                    k += 1
                i = k

            # add items to dict
            print('updated_add_label: {}'.format(updated_add_label))
            print('keys_diff: {}'.format(keys_diff))
            print('2context[line_diff]: {}'.format(context['line_diff']))
            print('-----------------------------------------------------')

            i = 0
            while_condition = True
            prev_value = None
            dict_to_update = {}
            counter = 0
            print('len(updated_add_label: {}'.format(len(updated_add_label)))
                  
            for key, value in context['line_diff'].items(): # [0, 8, 20, 24, 35, 39]
                counter = 0   
                while while_condition and key > updated_add_label[i]: #  [9, 13, 17]
                    dict_to_update.update({updated_add_label[i]: prev_value + 1 + counter})
                    i += 1
                    counter += 1
                    if i >= len(updated_add_label):
                        while_condition = False
                        print(while_condition)
                    print('i:{}'.format(i))
                
                prev_value = value

                if not while_condition:
                    break

            context['line_diff'] = connect_two_sorted_dictionaries(context['line_diff'],
                                                             dict_to_update)
            
            print('3context[line_diff]: {}'.format(context['line_diff']))
            print('-----------------------------------------------------')


def connect_two_sorted_dictionaries(dict1, dict2):
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
