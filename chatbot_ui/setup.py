from distutils.core import setup, Extension
setup(name='trial', version='1.0',  \
      ext_modules=[Extension('trial', ['openfacemodule.cpp'])])
