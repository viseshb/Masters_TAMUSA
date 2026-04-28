# Install script for directory: /mnt/c/Users/vises/OneDrive/Desktop/Masters_TAMUSA/Sem3/Computer Networks/LAB_3/ns-3.45/src/lr-wpan

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "default")
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
  set(CMAKE_INSTALL_SO_NO_EXE "1")
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
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libns3.45-lr-wpan-default.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libns3.45-lr-wpan-default.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libns3.45-lr-wpan-default.so"
         RPATH "/usr/local/lib:$ORIGIN/:$ORIGIN/../lib:/usr/local/lib64:$ORIGIN/:$ORIGIN/../lib64")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/mnt/c/Users/vises/OneDrive/Desktop/Masters_TAMUSA/Sem3/Computer Networks/LAB_3/ns-3.45/build/lib/libns3.45-lr-wpan-default.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libns3.45-lr-wpan-default.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libns3.45-lr-wpan-default.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libns3.45-lr-wpan-default.so"
         OLD_RPATH "/mnt/c/Users/vises/OneDrive/Desktop/Masters_TAMUSA/Sem3/Computer Networks/LAB_3/ns-3.45/build/lib:"
         NEW_RPATH "/usr/local/lib:$ORIGIN/:$ORIGIN/../lib:/usr/local/lib64:$ORIGIN/:$ORIGIN/../lib64")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libns3.45-lr-wpan-default.so")
    endif()
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/ns3" TYPE FILE FILES
    "/mnt/c/Users/vises/OneDrive/Desktop/Masters_TAMUSA/Sem3/Computer Networks/LAB_3/ns-3.45/src/lr-wpan/helper/lr-wpan-helper.h"
    "/mnt/c/Users/vises/OneDrive/Desktop/Masters_TAMUSA/Sem3/Computer Networks/LAB_3/ns-3.45/src/lr-wpan/model/lr-wpan-constants.h"
    "/mnt/c/Users/vises/OneDrive/Desktop/Masters_TAMUSA/Sem3/Computer Networks/LAB_3/ns-3.45/src/lr-wpan/model/lr-wpan-csmaca.h"
    "/mnt/c/Users/vises/OneDrive/Desktop/Masters_TAMUSA/Sem3/Computer Networks/LAB_3/ns-3.45/src/lr-wpan/model/lr-wpan-error-model.h"
    "/mnt/c/Users/vises/OneDrive/Desktop/Masters_TAMUSA/Sem3/Computer Networks/LAB_3/ns-3.45/src/lr-wpan/model/lr-wpan-fields.h"
    "/mnt/c/Users/vises/OneDrive/Desktop/Masters_TAMUSA/Sem3/Computer Networks/LAB_3/ns-3.45/src/lr-wpan/model/lr-wpan-interference-helper.h"
    "/mnt/c/Users/vises/OneDrive/Desktop/Masters_TAMUSA/Sem3/Computer Networks/LAB_3/ns-3.45/src/lr-wpan/model/lr-wpan-lqi-tag.h"
    "/mnt/c/Users/vises/OneDrive/Desktop/Masters_TAMUSA/Sem3/Computer Networks/LAB_3/ns-3.45/src/lr-wpan/model/lr-wpan-mac-header.h"
    "/mnt/c/Users/vises/OneDrive/Desktop/Masters_TAMUSA/Sem3/Computer Networks/LAB_3/ns-3.45/src/lr-wpan/model/lr-wpan-mac-pl-headers.h"
    "/mnt/c/Users/vises/OneDrive/Desktop/Masters_TAMUSA/Sem3/Computer Networks/LAB_3/ns-3.45/src/lr-wpan/model/lr-wpan-mac-trailer.h"
    "/mnt/c/Users/vises/OneDrive/Desktop/Masters_TAMUSA/Sem3/Computer Networks/LAB_3/ns-3.45/src/lr-wpan/model/lr-wpan-mac-base.h"
    "/mnt/c/Users/vises/OneDrive/Desktop/Masters_TAMUSA/Sem3/Computer Networks/LAB_3/ns-3.45/src/lr-wpan/model/lr-wpan-mac.h"
    "/mnt/c/Users/vises/OneDrive/Desktop/Masters_TAMUSA/Sem3/Computer Networks/LAB_3/ns-3.45/src/lr-wpan/model/lr-wpan-net-device.h"
    "/mnt/c/Users/vises/OneDrive/Desktop/Masters_TAMUSA/Sem3/Computer Networks/LAB_3/ns-3.45/src/lr-wpan/model/lr-wpan-phy.h"
    "/mnt/c/Users/vises/OneDrive/Desktop/Masters_TAMUSA/Sem3/Computer Networks/LAB_3/ns-3.45/src/lr-wpan/model/lr-wpan-spectrum-signal-parameters.h"
    "/mnt/c/Users/vises/OneDrive/Desktop/Masters_TAMUSA/Sem3/Computer Networks/LAB_3/ns-3.45/src/lr-wpan/model/lr-wpan-spectrum-value-helper.h"
    "/mnt/c/Users/vises/OneDrive/Desktop/Masters_TAMUSA/Sem3/Computer Networks/LAB_3/ns-3.45/build/include/ns3/lr-wpan-module.h"
    )
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/mnt/c/Users/vises/OneDrive/Desktop/Masters_TAMUSA/Sem3/Computer Networks/LAB_3/ns-3.45/cmake-cache/src/lr-wpan/examples/cmake_install.cmake")

endif()

