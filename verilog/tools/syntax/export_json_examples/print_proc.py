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

import sys

import anytree

import verible_verilog_syntax
import os



def main():
  if len(sys.argv) < 3:
    print(f"Usage: {sys.argv[0]} path to \'verible-verilog-syntax\' binary " +
          "VERILOG_FILE [VERILOG_FILE [...]]")
    return 1

  parser_path = sys.argv[1]
  files = sys.argv[2:]

  parser = verible_verilog_syntax.VeribleVerilogSyntax(executable=parser_path)
  procs = parser.build_proc('always_comb', files, options={"gen_tokens": True})
  parser.print_feedback(procs)

  return
  for f in procs:
    print(f'FILE: {f}')
    for p in procs[f]:
      print(f'PROCESS: {p.name}')

      print(f'Triggers :')
      for t in p.triggers:
        print(f't = {t}')
      print('Sens :')
      for s in p.sens:
        print(f't = {s}')


if __name__ == "__main__":
  sys.exit(main())
