#!/bin/bash
#
# get components to build ffmpeg

. shell/utils.sh

mkdir -p build && cd build

# get faac-1.28
if [ ! -e "faac-1.28.tar.bz2" ]; then
  download http://downloads.sourceforge.net/faac/faac-1.28.tar.bz2
  if [ ! -d "faac-1.28" ]; then
    extract faac-1.28.tar.bz2
    # apply patch for faac
    cd faac-1.28
    download http://www.linuxfromscratch.org/patches/blfs/svn/faac-1.28-glibc_fixes-1.patch
    patch -Np1 -i faac-1.28-glibc_fixes-1.patch
    sed -i -e '/obj-type/d' -e '/Long Term/d' frontend/main.c
    cd ..
  fi
else
  echo "faac-1.28.tar.bz2 already exists..."
fi

# get lame-3.99.5
if [ ! -e "lame-3.99.5.tar.gz" ]; then
  download http://sourceforge.net/projects/lame/files/lame/3.99/lame-3.99.5.tar.gz
  if [ ! -d "lame-3.99.5" ]; then
    extract lame-3.99.5.tar.gz
  fi
else
  echo "lame-3.99.5.tar.gz already exists..."
fi

# get x264
if [ ! -d "x264" ]; then
  git clone git://git.videolan.org/x264.git
  cd x264 && git checkout stable && cd ..
fi

# get SDL-1.2.15
if [ ! -e "SDL-1.2.15.tar.gz" ]; then
  download https://www.libsdl.org/release/SDL-1.2.15.tar.gz
  if [ ! -d "SDL-1.2.15" ]; then
    extract SDL-1.2.15.tar.gz
  fi
else
  echo "SDL-1.2.15.tar.gz already exists..."
fi

# get ffmpeg-2.6.3
if [ ! -e "ffmpeg-2.6.3.tar.bz2" ]; then
  download http://ffmpeg.org/releases/ffmpeg-2.6.3.tar.bz2
  if [ ! -d "ffmpeg-2.6.3" ]; then
    extract ffmpeg-2.6.3.tar.bz2
  fi
else
  echo "ffmpeg-2.6.3.tar.bz2 already exists..."
fi

ln -s ../Makefile.static Makefile
