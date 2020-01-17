from root import ROOT_DIR
from cffi import FFI

ffi = FFI()
ffi.cdef("int times2(int x);")


C = ffi.dlopen(ROOT_DIR + "/target/release/libderp_blue.dylib")

if __name__ == "__main__":
    print(C.times2(9))
