__author__ = 'charles'

import pepy

dll_characteristics = [
    ('IMAGE_LIBRARY_PROCESS_INIT',                     0x0001),
    ('IMAGE_LIBRARY_PROCESS_TERM',                     0x0002),
    ('IMAGE_LIBRARY_THREAD_INIT',                      0x0004),
    ('IMAGE_LIBRARY_THREAD_TERM',                      0x0008),
    ('IMAGE_DLLCHARACTERISTICS_HIGH_ENTROPY_VA',       0x0020),
    ('IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE',          0x0040),
    ('IMAGE_DLLCHARACTERISTICS_FORCE_INTEGRITY',       0x0080),
    ('IMAGE_DLLCHARACTERISTICS_NX_COMPAT',             0x0100),
    ('IMAGE_DLLCHARACTERISTICS_NO_ISOLATION',          0x0200),
    ('IMAGE_DLLCHARACTERISTICS_NO_SEH',                0x0400),
    ('IMAGE_DLLCHARACTERISTICS_NO_BIND',               0x0800),
    ('IMAGE_DLLCHARACTERISTICS_APPCONTAINER',          0x1000),
    ('IMAGE_DLLCHARACTERISTICS_WDM_DRIVER',            0x2000),
    ('IMAGE_DLLCHARACTERISTICS_GUARD_CF',              0x4000),
    ('IMAGE_DLLCHARACTERISTICS_TERMINAL_SERVER_AWARE', 0x8000) ]



class AppxExecutable:
    def __init__(self, path):
        self.path = path
        p = pepy.parse(path)
        self.dllcharacteristics = []
        for c in dll_characteristics:
            if p.dllcharacteristics & c[1]:
                self.dllcharacteristics.append(c[0])

        print('0x%x' % p.dllcharacteristics)

    def __str__(self):
        st =  'App: ' + self.path
        st += '\n\tDLL Characteristics: \n\t\t' + '\n\t\t'.join(self.dllcharacteristics)
        return st

if ( __name__ == "__main__"):
    print("in AppExecutable")
    print AppxExecutable("test/Map.exe")
