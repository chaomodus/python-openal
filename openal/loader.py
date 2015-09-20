import os
import ctypes
import ctypes.util

libs = {}

loader = ctypes.CDLL
suffix = ".so"
infixes = ['', ]

if os.name == 'nt':
    suffix = ".dll"
    infixes = ['', '32', '64']


class LoadLibError(Exception):
    pass


def load_lib(name):
    """Try our best to load the library."""

    # memomemomemo
    if name in libs:
        return libs[name]

    lib = None

    # 1st, local
    for infix in infixes:
        try:
            lib = loader(name+infix+suffix)
        except OSError:
            continue
    if lib:
        libs[name] = lib
        return lib

    # 2nd, global
    for infix in infixes:
        try:
            pth = ctypes.util.find_library(name+infix)
            if pth:
                lib = loader(pth)
            else:
                raise OSError()
        except OSError:
            try:
                pth = ctypes.util.find_library(name+infix+suffix)
                if pth:
                    lib = loader(pth)
                else:
                    raise OSError()
            except OSError:
                continue

    if lib:
        libs[name] = lib
        return lib

    raise LoadLibError("Can't locate library.")
