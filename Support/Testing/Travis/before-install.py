#!/usr/bin/env python
##
## Copyright (c) 2014-present, Facebook, Inc.
## All rights reserved.
##
## This source code is licensed under the University of Illinois/NCSA Open
## Source License found in the LICENSE file in the root directory of this
## source tree. An additional grant of patent rights can be found in the
## PATENTS file in the same directory.
##

import os
import sys
from subprocess import check_call

host = os.uname()[0]
target = os.getenv('TARGET')

if host == 'Darwin':
    check_call('brew update', shell=True)
elif host == 'Linux':
    repositories = []
    keys = []

    def add_toolchain_test_repo():
        repositories.append('ppa:ubuntu-toolchain-r/test')

    def add_llvm_repo():
        add_toolchain_test_repo()
        keys.append('http://llvm.org/apt/llvm-snapshot.gpg.key')
        repositories.append('deb http://llvm.org/apt/trusty/ llvm-toolchain-trusty-3.8 main')

    if target in [ 'Style', 'Registers' ]:
        add_llvm_repo()
    elif target in [ 'Linux-X86', 'Linux-X86_64', 'Tizen-X86' ]:
        add_toolchain_test_repo()

    if os.getenv('CLANG') != None or os.getenv('LLDB_TESTS') != None:
        add_llvm_repo()

    for r in repositories:
        check_call('sudo add-apt-repository -y "%s"' % r, shell=True)

    for k in keys:
        check_call('wget -O - "%s" | sudo apt-key add -' % k, shell=True)

    check_call('sudo apt-get update', shell=True)
