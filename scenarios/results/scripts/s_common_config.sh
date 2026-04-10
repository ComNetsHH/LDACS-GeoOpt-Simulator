#!/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
RESULTS_DIR=$(cd "${SCRIPT_DIR}/.." && pwd)
SCENARIOS_DIR=$(cd "${RESULTS_DIR}/.." && pwd)
WORKSPACE_ROOT=$(cd "${RESULTS_DIR}/../../omnetpp-5.6.2/workspace" && pwd)

NUM_CPUS=${NUM_CPUS:-4}
MEM_PER_CPU=${MEM_PER_CPU:-1G}
INI_FILE_FR_EF="${SCENARIOS_DIR}/scenarioFR_equipage_fraction.ini"

INET_PROJ="${WORKSPACE_ROOT}/inet4"
LDACS_ABSTRACT_RADIO_PROJ="${WORKSPACE_ROOT}/ldacs_abstract_radio"
LDACS_ABSTRACT_TDMA_PROJ="${WORKSPACE_ROOT}/ldacs_abstract_tdma_mac"
DSPR_PROJ="${WORKSPACE_ROOT}/ldacs_dijkstra_routing"
GPSR_PROJ="${WORKSPACE_ROOT}/ldacs_gpsr_routing"
GREEDY_PROJ="${WORKSPACE_ROOT}/ldacs_greedy_k_hop_routing"
GEOOPT_PROJ="${WORKSPACE_ROOT}/ldacs_geoopt_routing"

SIM_BINARY_GREEDY_RELEASE="${GREEDY_PROJ}/out/gcc-release/src/ldacs_greedy_k_hop_routing"
SIM_BINARY_GPSR_RELEASE="${GPSR_PROJ}/out/gcc-release/src/ldacs_gpsr_routing"
SIM_BINARY_DSPR_RELEASE="${DSPR_PROJ}/out/gcc-release/src/ldacs_dijkstra_routing"
SIM_BINARY_OPTIMIZEDGREEDY_RELEASE="${GEOOPT_PROJ}/out/gcc-release/src/ldacs_geoopt_routing"

INCL_GREEDY="-n ${SCENARIOS_DIR}:./:${INET_PROJ}/src:${LDACS_ABSTRACT_RADIO_PROJ}/src:${LDACS_ABSTRACT_TDMA_PROJ}/src:${GREEDY_PROJ}/src"
INCL_GPSR="-n ${SCENARIOS_DIR}:./:${INET_PROJ}/src:${LDACS_ABSTRACT_RADIO_PROJ}/src:${LDACS_ABSTRACT_TDMA_PROJ}/src:${GPSR_PROJ}/src"
INCL_DSPR="-n ${SCENARIOS_DIR}:./:${INET_PROJ}/src:${LDACS_ABSTRACT_RADIO_PROJ}/src:${LDACS_ABSTRACT_TDMA_PROJ}/src:${DSPR_PROJ}/src"
INCL_OPTIMIZEDGREEDY="-n ${SCENARIOS_DIR}:./:${INET_PROJ}/src:${LDACS_ABSTRACT_RADIO_PROJ}/src:${LDACS_ABSTRACT_TDMA_PROJ}/src:${GEOOPT_PROJ}/src"

GREEDY1_CONFIG="greedy-forwarding-1hop"
GPSR_CONFIG="gpsr-forwarding"
DSPR_CONFIG="dijkstra"
OPTIMIZEDGREEDY_CONFIG="optimized-greedy"

set_dijkstra_imports() {
    local mode="$1"
    if [ "$mode" = "enable" ]; then
        sed -i '/^\/\/ import dspr.Dspr;/s|^\/\/ ||' "${SCENARIOS_DIR}/scenarioFR.ned"
        sed -i '/^\/\/ import dspr.NodeManager;/s|^\/\/ ||' "${SCENARIOS_DIR}/scenarioFR.ned"
        sed -i 's|^        // nodeManager: NodeManager;|        nodeManager: NodeManager;|' "${SCENARIOS_DIR}/scenarioFR.ned"
    else
        sed -i 's|^import dspr.Dspr;|// import dspr.Dspr;|' "${SCENARIOS_DIR}/scenarioFR.ned"
        sed -i 's|^import dspr.NodeManager;|// import dspr.NodeManager;|' "${SCENARIOS_DIR}/scenarioFR.ned"
        sed -i 's|^        nodeManager: NodeManager;|        // nodeManager: NodeManager;|' "${SCENARIOS_DIR}/scenarioFR.ned"
    fi
}
