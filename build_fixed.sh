#!/bin/bash

# Ensure we're in the right conda environment
eval "$(micromamba shell hook -s bash)"
micromamba activate TestRoot

# Set environment variables
export SKNANO_HOME="/data6/Users/achihwan/SKNanoAnalyzer"
export SKNANO_BUILDDIR="$SKNANO_HOME/build/redhat"
export SKNANO_INSTALLDIR="$SKNANO_HOME/install/redhat"
export BOOST_ROOT="$CONDA_PREFIX"

# Clean and create build directory
rm -rf "$SKNANO_BUILDDIR"
mkdir -p "$SKNANO_BUILDDIR"
cd "$SKNANO_BUILDDIR"

# Configure with CMake
echo "Building in: $(pwd)"
echo "CONDA_PREFIX: $CONDA_PREFIX"

cmake \
  -DCMAKE_INSTALL_PREFIX="$SKNANO_INSTALLDIR" \
  -Dcorrectionlib_DIR="$CONDA_PREFIX/lib/python3.11/site-packages/correctionlib/cmake" \
  -DCMAKE_PREFIX_PATH="$SKNANO_HOME/external/libtorch;$CONDA_PREFIX" \
  -DCMAKE_BUILD_TYPE=Release \
  -DBOOST_ROOT="$CONDA_PREFIX" \
  "$SKNANO_HOME"

if [ $? -eq 0 ]; then
    echo "CMake configuration successful. Building..."
    make -j6
    if [ $? -eq 0 ]; then
        echo "Build successful. Installing..."
        make install
    fi
else
    echo "CMake configuration failed!"
fi