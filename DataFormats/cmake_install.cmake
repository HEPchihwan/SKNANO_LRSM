# Install script for directory: /home/achihwan/SKNanoAnalyzer/DataFormats

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/data6/Users/achihwan/SKNanoAnalyzer/install/redhat")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "0")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libDataFormats.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libDataFormats.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libDataFormats.so"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/data6/Users/achihwan/SKNanoAnalyzer/DataFormats/libDataFormats.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libDataFormats.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libDataFormats.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libDataFormats.so"
         OLD_RPATH "/data6/Users/achihawn/micromamba/envs/Nano/lib:/data6/Users/achihawn/micromamba/envs/TestRoot/lib:/data6/Users/achihawn/micromamba/envs/Nano/lib/python3.12/site-packages/correctionlib/lib:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libDataFormats.so")
    endif()
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE FILE FILES
    "/data6/Users/achihwan/SKNanoAnalyzer/DataFormats/libDataFormats.rootmap"
    "/data6/Users/achihwan/SKNanoAnalyzer/DataFormats/libDataFormats_rdict.pcm"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE FILE FILES
    "/home/achihwan/SKNanoAnalyzer/DataFormats/include/Electron.h"
    "/home/achihwan/SKNanoAnalyzer/DataFormats/include/Event.h"
    "/home/achihwan/SKNanoAnalyzer/DataFormats/include/FatJet.h"
    "/home/achihwan/SKNanoAnalyzer/DataFormats/include/Gen.h"
    "/home/achihwan/SKNanoAnalyzer/DataFormats/include/GenDressedLepton.h"
    "/home/achihwan/SKNanoAnalyzer/DataFormats/include/GenIsolatedPhoton.h"
    "/home/achihwan/SKNanoAnalyzer/DataFormats/include/GenJet.h"
    "/home/achihwan/SKNanoAnalyzer/DataFormats/include/GenVisTau.h"
    "/home/achihwan/SKNanoAnalyzer/DataFormats/include/Jet.h"
    "/home/achihwan/SKNanoAnalyzer/DataFormats/include/JetTaggingParameter.h"
    "/home/achihwan/SKNanoAnalyzer/DataFormats/include/LHE.h"
    "/home/achihwan/SKNanoAnalyzer/DataFormats/include/Lepton.h"
    "/home/achihwan/SKNanoAnalyzer/DataFormats/include/Muon.h"
    "/home/achihwan/SKNanoAnalyzer/DataFormats/include/Particle.h"
    "/home/achihwan/SKNanoAnalyzer/DataFormats/include/Photon.h"
    "/home/achihwan/SKNanoAnalyzer/DataFormats/include/Tau.h"
    "/home/achihwan/SKNanoAnalyzer/DataFormats/include/TrigObj.h"
    )
endif()

