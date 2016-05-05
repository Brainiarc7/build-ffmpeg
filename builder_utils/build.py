#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@script : build.py
@about  :
"""
from __future__ import print_function
import os
import shutil
import multiprocessing

from config import command


class Builder:
    def __init__(self, build_dir, install_dir):
        self.build_dir_ = build_dir
        self.install_dir_ = install_dir
        self.cpu_count_ = 4 if multiprocessing.cpu_count() > 4 else multiprocessing.cpu_count()

    def build_lame(self):
        saved = os.getcwd()
        os.chdir(os.path.join(self.build_dir_, "lame-3.99.5"))
        command("./configure --prefix=%s --disable-shared --enable-static" % self.install_dir_)
        command(["make", "-j%d" % self.cpu_count_])
        command(["make", "install"])
        os.chdir(saved)

    def build_faac(self):
        saved = os.getcwd()
        os.chdir(os.path.join(self.build_dir_, "faac-1.28"))
        command("./configure --prefix=%s --disable-shared --enable-static" % self.install_dir_)
        command(["make", "-j%d" % self.cpu_count_])
        command(["make", "install"])
        os.chdir(saved)

    def build_ass(self):
        saved = os.getcwd()
        os.chdir(os.path.join(self.build_dir_, "libass"))
        command(["./autogen.sh"])
        command("./configure --prefix=%s --enable-shared=no --enable-static" % self.install_dir_)
        command(["make", "-j%d" % self.cpu_count_])
        command(["make", "install"])
        os.chdir(saved)

    def build_x264(self):
        saved = os.getcwd()
        os.chdir(os.path.join(self.build_dir_, "x264"))
        command(
            "./configure --prefix=%s --extra-cflags=\"-I%s/include\" --extra-ldflags=\"-L%s/lib\""
            " --enable-static --disable-lavf --disable-ffms --disable-opencl" % (
                self.install_dir_, self.install_dir_, self.install_dir_))
        command(["make", "-j%d" % self.cpu_count_])
        command(["make", "install"])
        os.chdir(saved)

    def build_sdl(self):
        saved = os.getcwd()
        os.chdir(os.path.join(self.build_dir_, "SDL-1.2.15"))
        command("./configure --prefix=%s --disable-shared" % self.install_dir_)
        command(["make", "-j%d" % self.cpu_count_])
        command(["make", "install"])
        os.chdir(saved)

    def build_ffmpeg(self, version):
        saved = os.getcwd()
        os.chdir(os.path.join(self.build_dir_, "ffmpeg-%s" % version))
        command(
            "sed -i -e 's|SDL_CONFIG=\"${cross_prefix}sdl-config\"|"
            "SDL_CONFIG=\"%s/bin/sdl-config\"|' ./configure" % self.install_dir_)
        shutil.copy2("configure", "configure.orig")
        os.environ['PKG_CONFIG_PATH'] = "%s/lib/pkgconfig" % self.install_dir_
        cmd = ("./configure --prefix=%s --extra-cflags=\"-I%s/include\" "
               "--extra-ldflags=\"-L%s/lib\" --enable-libfaac --enable-libmp3lame "
               "--enable-libx264 --enable-libzvbi --enable-libass --enable-gpl "
               "--enable-pthreads --enable-nonfree" % (
                  self.install_dir_, self.install_dir_, self.install_dir_))
        print(cmd)
        command(cmd)
        shutil.move("configure.orig", "configure")
        command(["make", "-j%d" % self.cpu_count_])
        command(["make", "install"])
        os.chdir(saved)

    def patch_faac(self):
        command("cp -v ../patches/faac-1.28-glibc_fixes-1.patch faac-1.28/")
        os.chdir("faac-1.28")
        command("patch -Np1 -i faac-1.28-glibc_fixes-1.patch")
        command("sed -i -e '/obj-type/d' -e '/Long Term/d' frontend/main.c")
        os.chdir("..")

    def patch_sdl(self):
        command("cp -v ../patches/libsdl-1.2.15-const-xdata32.patch SDL-1.2.15/")
        os.chdir("SDL-1.2.15")
        command("patch -Np1 -i libsdl-1.2.15-const-xdata32.patch")
        command("./autogen.sh")
        os.chdir("..")
