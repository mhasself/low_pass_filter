from distutils.core import setup, Extension

modname = 'npfilt'

import os
import glob
import numpy

includes = [numpy.get_include()]
library_dirs = []
libraries = []


sources = ['wrapper.c', 'lo_pass.c']

module1 = Extension('npfilt',
                    sources=sources,
                    include_dirs=includes,
                    library_dirs=library_dirs,
                    libraries=libraries,
                    extra_compile_args=['-std=c99', '-fopenmp'],
                    extra_link_args=['-fopenmp']
                )

setup(name = modname,
      version = '1.0',
      description = modname,
      ext_modules = [module1],
      )
