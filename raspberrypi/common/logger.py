#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import time, asctime


class Logger:

    SHOW  = 0
    WRITE = 1
    BOTH  = 2

    def __init__(self, exec_param, file_name=None):
        self.initial_time = time()
        self.exec_param = exec_param
        self.file = open(file_name, "w") if file_name is not None and exec_param > 0 else open("/tmp/log-{}-{}-{}.T".format(*asctime().split(" ")[1:4]),"w")

    def __call__(self, *args, **kwargs):
        self.write(*args, **kwargs)

    def write(self, *args, **kwargs):
        if self.exec_param%2 == 0:
            print("[{0:.3g}] :".format(time() - self.initial_time), *args)
            for key, content in kwargs.items():
                print("  •", key, ":")
                print("      ", content)

        if self.exec_param > 0 and self.file is not None:
            self.file.write("[{0:.3g}] :".format(time() - self.initial_time))
            for arg in args: self.file.write(" {}".format(str(arg)))
            for key, content in kwargs.items():
                self.file.write("\n{} : ".format(str(key)))
                self.file.write("\t", str(content))

    def close(self):
        if self.file is not None :  self.file.close()