#!/bin/bash
set -euo pipefail

# The LDACS-GeoOpt-Simulator includes an installation script that downloads the
# required OMNeT++/INET environment, clones the simulator dependencies, and
# prepares the plotting environment.

NUM_CPUS=${NUM_CPUS:-10}
OMNET_VERSION=5.6.2
INET_VERSION=4.2.5

LOC_OMNET="https://github.com/omnetpp/omnetpp/releases/download/omnetpp-${OMNET_VERSION}/omnetpp-${OMNET_VERSION}-src-linux.tgz"
LOC_OMNET_MAC="https://github.com/omnetpp/omnetpp/releases/download/omnetpp-${OMNET_VERSION}/omnetpp-${OMNET_VERSION}-src-macosx.tgz"
LOC_INET="https://github.com/eltayebmusab/inet/archive/refs/tags/v${INET_VERSION}.tar.gz"

LOC_RADIO_REPO="https://github.com/ComNetsHH/LDACS-Abstract-Radio.git"
LOC_TDMA_REPO="https://github.com/ComNetsHH/LDACS-Abstract-TDMA-MAC.git"
LOC_GREEDY_REPO="https://github.com/ComNetsHH/LDACS-Greedy-K-Hop-Routing.git"
LOC_DIJKSTRA_REPO="https://github.com/ComNetsHH/LDACS-Dijkstra.git"
LOC_GPSR_REPO="https://github.com/ComNetsHH/LDACS-GPSR-Routing.git"
LOC_GEOOPT_REPO="https://github.com/ComNetsHH/LDACS-GeoOpt-Routing.git"

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO_DIR="${SCRIPT_DIR}"
OMNET_DIR="${REPO_DIR}/omnetpp-${OMNET_VERSION}"
WORKSPACE_DIR="${OMNET_DIR}/workspace"

clone_or_update_repo() {
    local repo_url="$1"
    local target_dir="$2"

    if [ -d "${target_dir}/.git" ]; then
        echo "Updating $(basename "${target_dir}")"
        git -C "${target_dir}" pull --ff-only || true
    elif [ -d "${target_dir}" ]; then
        echo "Using existing directory $(basename "${target_dir}")"
    else
        echo "Cloning $(basename "${target_dir}")"
        git clone "${repo_url}" "${target_dir}"
    fi
}

build_component() {
    local component_dir="$1"
    local include_flags="$2"
    local release_libs="$3"
    local debug_libs="$4"

    if [ ! -d "${component_dir}/src" ]; then
        echo "Warning: $(basename "${component_dir}") has no src/ directory yet. Skipping build."
        return 0
    fi

    cd "${component_dir}/src"
    opp_makemake -f -s --deep -O out ${include_flags} ${release_libs}
    make MODE=release -j"${NUM_CPUS}"
    # Re-create debug makefiles as well for users who want to debug later.
    opp_makemake -f -s --deep -O out ${include_flags} ${debug_libs}
    make MODE=debug -j"${NUM_CPUS}"
    cd "${WORKSPACE_DIR}"
}

echo -n "Downloading OMNeT++ "
if [ ! -d "${OMNET_DIR}" ]; then
    if [ "${1:-linux}" = "mac" ]; then
        echo "for Mac"
        wget -O "${REPO_DIR}/omnetpp-${OMNET_VERSION}-src-macosx.tgz" "${LOC_OMNET_MAC}"
        echo -e "\n\nUnpacking OMNeT++"
        tar -xvzf "${REPO_DIR}/omnetpp-${OMNET_VERSION}-src-macosx.tgz" -C "${REPO_DIR}"
        rm -f "${REPO_DIR}/omnetpp-${OMNET_VERSION}-src-macosx.tgz"
    else
        echo "for Linux"
        wget -O "${REPO_DIR}/omnetpp-${OMNET_VERSION}-src-linux.tgz" "${LOC_OMNET}"
        echo -e "\n\nUnpacking OMNeT++"
        tar -xvzf "${REPO_DIR}/omnetpp-${OMNET_VERSION}-src-linux.tgz" -C "${REPO_DIR}"
        rm -f "${REPO_DIR}/omnetpp-${OMNET_VERSION}-src-linux.tgz"
    fi
fi

echo -e "\n\nCompiling OMNeT++"
cd "${OMNET_DIR}"
export PATH="$(pwd)/bin:${PATH}"
./configure CC=gcc CXX=g++ WITH_OSG=no WITH_OSGEARTH=no WITH_QTENV=no
make -j"${NUM_CPUS}" MODE=release base

mkdir -p "${WORKSPACE_DIR}"
cd "${WORKSPACE_DIR}"

if [ ! -d "${WORKSPACE_DIR}/inet4" ]; then
    echo -e "\n\nDownloading INET"
    wget -O "${REPO_DIR}/inet-${INET_VERSION}.tar.gz" "${LOC_INET}"
    echo -e "\n\nUnpacking INET"
    tar -xvzf "${REPO_DIR}/inet-${INET_VERSION}.tar.gz" -C "${WORKSPACE_DIR}"
    rm -f "${REPO_DIR}/inet-${INET_VERSION}.tar.gz"
    mv "${WORKSPACE_DIR}/inet-${INET_VERSION}" "${WORKSPACE_DIR}/inet4"
fi

cd "${WORKSPACE_DIR}/inet4"
echo -e "\n\nCompiling INET"
make makefiles
make -j"${NUM_CPUS}" MODE=release
cd "${WORKSPACE_DIR}"

if [ ! -e "${WORKSPACE_DIR}/LDACS-GeoOpt-Simulator" ]; then
    ln -s "${REPO_DIR}" "${WORKSPACE_DIR}/LDACS-GeoOpt-Simulator"
fi

clone_or_update_repo "${LOC_RADIO_REPO}" "${WORKSPACE_DIR}/ldacs_abstract_radio"
clone_or_update_repo "${LOC_TDMA_REPO}" "${WORKSPACE_DIR}/ldacs_abstract_tdma_mac"
clone_or_update_repo "${LOC_GREEDY_REPO}" "${WORKSPACE_DIR}/ldacs_greedy_k_hop_routing"
clone_or_update_repo "${LOC_DIJKSTRA_REPO}" "${WORKSPACE_DIR}/ldacs_dijkstra_routing"
clone_or_update_repo "${LOC_GPSR_REPO}" "${WORKSPACE_DIR}/ldacs_gpsr_routing"
clone_or_update_repo "${LOC_GEOOPT_REPO}" "${WORKSPACE_DIR}/ldacs_geoopt_routing"

echo -e "\n\nCompiling LDACS Abstract Radio"
build_component "${WORKSPACE_DIR}/ldacs_abstract_radio"     "-KINET4_PROJ=../../inet4 -DINET_IMPORT -I../../inet4 -I. -I../../inet4/src"     "-L../../inet4/src -lINET"     "-L../../inet4/src -lINET_dbg"

echo -e "\n\nCompiling LDACS Abstract TDMA MAC"
build_component "${WORKSPACE_DIR}/ldacs_abstract_tdma_mac"     "-KINET4_PROJ=../../inet4 -DINET_IMPORT -I../../ldacs_abstract_radio/src -I. -I../../inet4/src"     "-L../../inet4/src -L../../ldacs_abstract_radio/out/gcc-release/src/ -lINET -lldacs_abstract_radio"     "-L../../inet4/src -L../../ldacs_abstract_radio/out/gcc-debug/src/ -lINET_dbg -lldacs_abstract_radio_dbg"

echo -e "\n\nCompiling LDACS Greedy K-Hop Routing"
build_component "${WORKSPACE_DIR}/ldacs_greedy_k_hop_routing"     "-KINET4_PROJ=../../inet4 -DINET_IMPORT -I../../inet4 -I../../ldacs_abstract_radio/src -I../../ldacs_abstract_tdma_mac/src -I. -I../../inet4/src"     "-L../../inet4/src -L../../ldacs_abstract_radio/out/gcc-release/src/ -L../../ldacs_abstract_tdma_mac/out/gcc-release/src/ -lINET -lldacs_abstract_radio -lldacs_abstract_tdma_mac"     "-L../../inet4/src -L../../ldacs_abstract_radio/out/gcc-debug/src/ -L../../ldacs_abstract_tdma_mac/out/gcc-debug/src/ -lINET_dbg -lldacs_abstract_radio_dbg -lldacs_abstract_tdma_mac_dbg"

echo -e "\n\nCompiling LDACS Dijkstra Routing"
build_component "${WORKSPACE_DIR}/ldacs_dijkstra_routing"     "-KINET4_PROJ=../../inet4 -DINET_IMPORT -I../../inet4 -I../../ldacs_abstract_radio/src -I../../ldacs_abstract_tdma_mac/src -I. -I../../inet4/src"     "-L../../inet4/src -L../../ldacs_abstract_radio/out/gcc-release/src/ -L../../ldacs_abstract_tdma_mac/out/gcc-release/src/ -lINET -lldacs_abstract_radio -lldacs_abstract_tdma_mac"     "-L../../inet4/src -L../../ldacs_abstract_radio/out/gcc-debug/src/ -L../../ldacs_abstract_tdma_mac/out/gcc-debug/src/ -lINET_dbg -lldacs_abstract_radio_dbg -lldacs_abstract_tdma_mac_dbg"

echo -e "\n\nCompiling LDACS GPSR Routing"
build_component "${WORKSPACE_DIR}/ldacs_gpsr_routing"     "-KINET4_PROJ=../../inet4 -DINET_IMPORT -I../../inet4 -I../../ldacs_abstract_radio/src -I../../ldacs_abstract_tdma_mac/src -I. -I../../inet4/src"     "-L../../inet4/src -L../../ldacs_abstract_radio/out/gcc-release/src/ -L../../ldacs_abstract_tdma_mac/out/gcc-release/src/ -lINET -lldacs_abstract_radio -lldacs_abstract_tdma_mac"     "-L../../inet4/src -L../../ldacs_abstract_radio/out/gcc-debug/src/ -L../../ldacs_abstract_tdma_mac/out/gcc-debug/src/ -lINET_dbg -lldacs_abstract_radio_dbg -lldacs_abstract_tdma_mac_dbg"

echo -e "\n\nCompiling LDACS GeoOpt Routing"
build_component "${WORKSPACE_DIR}/ldacs_geoopt_routing"     "-KINET4_PROJ=../../inet4 -DINET_IMPORT -I../../inet4 -I../../ldacs_abstract_radio/src -I../../ldacs_abstract_tdma_mac/src -I. -I../../inet4/src"     "-L../../inet4/src -L../../ldacs_abstract_radio/out/gcc-release/src/ -L../../ldacs_abstract_tdma_mac/out/gcc-release/src/ -lINET -lldacs_abstract_radio -lldacs_abstract_tdma_mac"     "-L../../inet4/src -L../../ldacs_abstract_radio/out/gcc-debug/src/ -L../../ldacs_abstract_tdma_mac/out/gcc-debug/src/ -lINET_dbg -lldacs_abstract_radio_dbg -lldacs_abstract_tdma_mac_dbg"

cd "${REPO_DIR}/scenarios/results"
echo -e "\n\nInstall python packages into local pipenv environment"
make install-python-env

echo -e "\n\nInstallation finished. Workspace root: ${WORKSPACE_DIR}"
