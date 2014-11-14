#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

import os
import glob
env=Environment(CPPPATH = ['..'],
                CXXFLAGS = '-W -Wall -g -Werror -Wno-unused-parameter -O2')
env.StaticLibrary('common',Glob('*.cc'))

test_env = env.Clone()
test_env.Append(LIBPATH = ['.'])
test_env.Append(LIBS = ['common',
                        'rt',
                        'pthread'])

for cc in glob.glob('test/*.cc'):
    test_env.Program(os.path.splitext(cc)[0] + '.exe', [cc])
