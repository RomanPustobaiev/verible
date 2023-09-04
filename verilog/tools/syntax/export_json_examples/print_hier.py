#!/usr/bin/env python3
# Copyright 2017-2020 The Verible Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Pretty-print Verilog Concrete Syntax Tree

Usage: print_tree.py PATH_TO_VERIBLE_VERILOG_SYNTAX \\
                     VERILOG_FILE [VERILOG_FILE [...]]

Visualizes hierarchy generated by ``verible-verilog-syntax --export_json ...``.
Values enclosed in ``[]`` are node tags. ``@(S-E)`` marks token's start (S)
and end (E) byte offsets in source code. When a token's text in source code
is not the same as its tag, the text is printed in single quotes.
"""

import sys

import anytree

import verible_verilog_syntax


def process_file_data(path: str, data: verible_verilog_syntax.SyntaxData):
  """Print tree representation to the console.

  The function uses anytree module (which is a base of a tree implementation
  used in verible_verilog_syntax) method to print syntax tree representation
  to the console.

  Args:
    path: Path to source file (used only for informational purposes)
    data: Parsing results returned by one of VeribleVerilogSyntax' parse_*
          methods.
  """
  print(f"\033[1;97;7m{path} \033[0m\n")
  if data.tree:
    for prefix, _, node in anytree.RenderTree(data.tree):
      print(f"\033[90m{prefix}\033[0m{node.to_formatted_string()}")
    print()

def print_parents(module):
    for parent in module.parents:
      print(f'{module.name} referenced in {parent.name} ({parent.fpath})')
      print_parents(parent)


def print_refs(modules, modulename):
  if modulename in modules:
    module = modules[modulename]
    print_parents(module)
  else:
    print(f'module {modulename} not found !')


def main():
  if len(sys.argv) < 3:
    print(f"Usage: {sys.argv[0]} path to \'verible-verilog-syntax\' binary " +
          "module name of interest" +
          "VERILOG_FILE [VERILOG_FILE [...]]")
    return 1

  parser_path = sys.argv[1]
  module_name = sys.argv[2]
  files = sys.argv[3:]

  parser = verible_verilog_syntax.VeribleVerilogSyntax(executable=parser_path)
  modules = parser.build_hier(files, options={"gen_tokens": True})
  print_refs(modules, module_name)


if __name__ == "__main__":
  sys.exit(main())
