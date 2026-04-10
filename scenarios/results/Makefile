# LDACS-GeoOpt-Simulator Makefile
# This Makefile follows the structure of the original LDACS simulator repository
# and uses the OMNeT++ workspace at ../../omnetpp-5.6.2/workspace/.

install-python-env:
	pipenv install

NUM_CPUS ?= 4
WORKSPACE_ROOT := ../../omnetpp-5.6.2/workspace
INET_PROJ := $(WORKSPACE_ROOT)/inet4
LDACS_ABSTRACT_RADIO_PROJ := $(WORKSPACE_ROOT)/ldacs_abstract_radio
LDACS_ABSTRACT_TDMA_PROJ := $(WORKSPACE_ROOT)/ldacs_abstract_tdma_mac
GREEDY_PROJ := $(WORKSPACE_ROOT)/ldacs_greedy_k_hop_routing
GPSR_PROJ := $(WORKSPACE_ROOT)/ldacs_gpsr_routing
DSPR_PROJ := $(WORKSPACE_ROOT)/ldacs_dijkstra_routing
GEOOPT_PROJ := $(WORKSPACE_ROOT)/ldacs_geoopt_routing

SCENARIO_INI := ../scenarioFR_equipage_fraction.ini
SIM_OUTPUT_BASE := simresults/scenarioFR/EquipageFraction
PLOT_COMMUNICATION_RANGE ?= 100
PLOT_BEACON_INTERVAL ?= 5

SIM_BINARY_GREEDY_RELEASE := $(GREEDY_PROJ)/out/gcc-release/src/ldacs_greedy_k_hop_routing
SIM_BINARY_GPSR_RELEASE := $(GPSR_PROJ)/out/gcc-release/src/ldacs_gpsr_routing
SIM_BINARY_DIJKSTRA_RELEASE := $(DSPR_PROJ)/out/gcc-release/src/ldacs_dijkstra_routing
SIM_BINARY_GEOOPT_RELEASE := $(GEOOPT_PROJ)/out/gcc-release/src/ldacs_geoopt_routing

INCL_GREEDY := -n ../:./:$(INET_PROJ)/src:$(LDACS_ABSTRACT_RADIO_PROJ)/src:$(LDACS_ABSTRACT_TDMA_PROJ)/src:$(GREEDY_PROJ)/src
INCL_GPSR := -n ../:./:$(INET_PROJ)/src:$(LDACS_ABSTRACT_RADIO_PROJ)/src:$(LDACS_ABSTRACT_TDMA_PROJ)/src:$(GPSR_PROJ)/src
INCL_DIJKSTRA := -n ../:./:$(INET_PROJ)/src:$(LDACS_ABSTRACT_RADIO_PROJ)/src:$(LDACS_ABSTRACT_TDMA_PROJ)/src:$(DSPR_PROJ)/src
INCL_GEOOPT := -n ../:./:$(INET_PROJ)/src:$(LDACS_ABSTRACT_RADIO_PROJ)/src:$(LDACS_ABSTRACT_TDMA_PROJ)/src:$(GEOOPT_PROJ)/src

GREEDY1_CONFIG := greedy-forwarding-1hop
GPSR_CONFIG := gpsr-forwarding
DIJKSTRA_CONFIG := dijkstra
GEOOPT_CONFIG := optimized-greedy

build-release-greedy:
	cd $(WORKSPACE_ROOT); \
	echo -e "\nBuilding LDACS Abstract Radio Component in Release Mode"; \
	cd ldacs_abstract_radio/src; opp_makemake -f -s --deep -O out -KINET4_PROJ=../../inet4 -DINET_IMPORT -I../../inet4 -I. -I../../inet4/src -L../../inet4/src -lINET; make -j$(NUM_CPUS) MODE=release; cd ../..; \
	echo -e "\nBuilding LDACS Abstract TDMA Component in Release Mode"; \
	cd ldacs_abstract_tdma_mac/src; opp_makemake -f -s --deep -O out -KINET4_PROJ=../../inet4 -DINET_IMPORT -I../../ldacs_abstract_radio/src -I. -I../../inet4/src -L../../inet4/src -L../../ldacs_abstract_radio/out/gcc-release/src/ -lINET -lldacs_abstract_radio; make -j$(NUM_CPUS) MODE=release; cd ../..; \
	echo -e "\nBuilding Greedy Routing Component in Release Mode"; \
	cd ldacs_greedy_k_hop_routing/src; opp_makemake -f -s --deep -O out -KINET4_PROJ=../../inet4 -DINET_IMPORT -I../../inet4 -I../../ldacs_abstract_radio/src -I../../ldacs_abstract_tdma_mac/src -I. -I../../inet4/src -L../../inet4/src -L../../ldacs_abstract_radio/out/gcc-release/src/ -L../../ldacs_abstract_tdma_mac/out/gcc-release/src/ -lINET -lldacs_abstract_radio -lldacs_abstract_tdma_mac; make -j$(NUM_CPUS) MODE=release

build-release-gpsr:
	cd $(WORKSPACE_ROOT); \
	echo -e "\nBuilding LDACS Abstract Radio Component in Release Mode"; \
	cd ldacs_abstract_radio/src; opp_makemake -f -s --deep -O out -KINET4_PROJ=../../inet4 -DINET_IMPORT -I../../inet4 -I. -I../../inet4/src -L../../inet4/src -lINET; make -j$(NUM_CPUS) MODE=release; cd ../..; \
	echo -e "\nBuilding LDACS Abstract TDMA Component in Release Mode"; \
	cd ldacs_abstract_tdma_mac/src; opp_makemake -f -s --deep -O out -KINET4_PROJ=../../inet4 -DINET_IMPORT -I../../ldacs_abstract_radio/src -I. -I../../inet4/src -L../../inet4/src -L../../ldacs_abstract_radio/out/gcc-release/src/ -lINET -lldacs_abstract_radio; make -j$(NUM_CPUS) MODE=release; cd ../..; \
	echo -e "\nBuilding GPSR Routing Component in Release Mode"; \
	cd ldacs_gpsr_routing/src; opp_makemake -f -s --deep -O out -KINET4_PROJ=../../inet4 -DINET_IMPORT -I../../inet4 -I../../ldacs_abstract_radio/src -I../../ldacs_abstract_tdma_mac/src -I. -I../../inet4/src -L../../inet4/src -L../../ldacs_abstract_radio/out/gcc-release/src/ -L../../ldacs_abstract_tdma_mac/out/gcc-release/src/ -lINET -lldacs_abstract_radio -lldacs_abstract_tdma_mac; make -j$(NUM_CPUS) MODE=release

build-release-dijkstra:
	cd $(WORKSPACE_ROOT); \
	echo -e "\nBuilding LDACS Abstract Radio Component in Release Mode"; \
	cd ldacs_abstract_radio/src; opp_makemake -f -s --deep -O out -KINET4_PROJ=../../inet4 -DINET_IMPORT -I../../inet4 -I. -I../../inet4/src -L../../inet4/src -lINET; make -j$(NUM_CPUS) MODE=release; cd ../..; \
	echo -e "\nBuilding LDACS Abstract TDMA Component in Release Mode"; \
	cd ldacs_abstract_tdma_mac/src; opp_makemake -f -s --deep -O out -KINET4_PROJ=../../inet4 -DINET_IMPORT -I../../ldacs_abstract_radio/src -I. -I../../inet4/src -L../../inet4/src -L../../ldacs_abstract_radio/out/gcc-release/src/ -lINET -lldacs_abstract_radio; make -j$(NUM_CPUS) MODE=release; cd ../..; \
	echo -e "\nBuilding Dijkstra Routing Component in Release Mode"; \
	cd ldacs_dijkstra_routing/src; opp_makemake -f -s --deep -O out -KINET4_PROJ=../../inet4 -DINET_IMPORT -I../../inet4 -I../../ldacs_abstract_radio/src -I../../ldacs_abstract_tdma_mac/src -I. -I../../inet4/src -L../../inet4/src -L../../ldacs_abstract_radio/out/gcc-release/src/ -L../../ldacs_abstract_tdma_mac/out/gcc-release/src/ -lINET -lldacs_abstract_radio -lldacs_abstract_tdma_mac; make -j$(NUM_CPUS) MODE=release

build-release-geoopt:
	cd $(WORKSPACE_ROOT); \
	echo -e "\nBuilding LDACS Abstract Radio Component in Release Mode"; \
	cd ldacs_abstract_radio/src; opp_makemake -f -s --deep -O out -KINET4_PROJ=../../inet4 -DINET_IMPORT -I../../inet4 -I. -I../../inet4/src -L../../inet4/src -lINET; make -j$(NUM_CPUS) MODE=release; cd ../..; \
	echo -e "\nBuilding LDACS Abstract TDMA Component in Release Mode"; \
	cd ldacs_abstract_tdma_mac/src; opp_makemake -f -s --deep -O out -KINET4_PROJ=../../inet4 -DINET_IMPORT -I../../ldacs_abstract_radio/src -I. -I../../inet4/src -L../../inet4/src -L../../ldacs_abstract_radio/out/gcc-release/src/ -lINET -lldacs_abstract_radio; make -j$(NUM_CPUS) MODE=release; cd ../..; \
	echo -e "\nBuilding GeoOpt Routing Component in Release Mode"; \
	cd ldacs_geoopt_routing/src; opp_makemake -f -s --deep -O out -KINET4_PROJ=../../inet4 -DINET_IMPORT -I../../inet4 -I../../ldacs_abstract_radio/src -I../../ldacs_abstract_tdma_mac/src -I. -I../../inet4/src -L../../inet4/src -L../../ldacs_abstract_radio/out/gcc-release/src/ -L../../ldacs_abstract_tdma_mac/out/gcc-release/src/ -lINET -lldacs_abstract_radio -lldacs_abstract_tdma_mac; make -j$(NUM_CPUS) MODE=release

build-release: build-release-greedy build-release-gpsr build-release-dijkstra build-release-geoopt

build-release-hpc:
	sbatch scripts/s_build_release.sh

result-directory-hpc:
	@if [ ! -L simresults ] && [ ! -e simresults ]; then \
		ln -s /path/to/your/hpc/results/directory simresults; \
		echo "Symbolic link created to HPC simresults directory."; \
	else \
		echo "The symbolic link 'simresults' already exists or the name is used by another file."; \
	fi

uncomment-dijkstra:
	@sed -i '/^\/\/ import dspr.Dspr;/s|^\/\/ ||' ../scenarioFR.ned; \
	sed -i '/^\/\/ import dspr.NodeManager;/s|^\/\/ ||' ../scenarioFR.ned; \
	sed -i 's|^        // nodeManager: NodeManager;|        nodeManager: NodeManager;|' ../scenarioFR.ned

comment-dijkstra:
	@sed -i 's|^import dspr.Dspr;|// import dspr.Dspr;|' ../scenarioFR.ned; \
	sed -i 's|^import dspr.NodeManager;|// import dspr.NodeManager;|' ../scenarioFR.ned; \
	sed -i 's|^        nodeManager: NodeManager;|        // nodeManager: NodeManager;|' ../scenarioFR.ned

greedy-forwarding-1hop-equipageFraction-A2G:
	opp_runall -j$(NUM_CPUS) $(SIM_BINARY_GREEDY_RELEASE) $(SCENARIO_INI) -c $(GREEDY1_CONFIG) $(INCL_GREEDY)

gpsr-forwarding-equipageFraction-A2G:
	opp_runall -j$(NUM_CPUS) $(SIM_BINARY_GPSR_RELEASE) $(SCENARIO_INI) -c $(GPSR_CONFIG) $(INCL_GPSR)

optimized-greedy-equipageFraction-A2G:
	opp_runall -j$(NUM_CPUS) $(SIM_BINARY_GEOOPT_RELEASE) $(SCENARIO_INI) -c $(GEOOPT_CONFIG) $(INCL_GEOOPT)

dijkstra-equipageFraction-A2G:
	$(MAKE) uncomment-dijkstra; \
	opp_runall -j$(NUM_CPUS) $(SIM_BINARY_DIJKSTRA_RELEASE) $(SCENARIO_INI) -c $(DIJKSTRA_CONFIG) $(INCL_DIJKSTRA); \
	$(MAKE) comment-dijkstra

greedy-forwarding-1hop-equipageFraction-A2G_csv:
	cd $(SIM_OUTPUT_BASE)/$(GREEDY1_CONFIG); \
	echo -e "Generate CSV files for Greedy-1"; \
	scavetool export -f 'module(scenarioFR_forwarding.aircraft[*].app[*]) AND name("packetSent:count")' -o packet_sent_count_multiapp.csv numAircrafts\=*.sca; \
	scavetool export -f 'module(scenarioFR_forwarding.groundStation[0].app[0]) AND name("packetReceived:count")' -o packet_received_count.csv numAircrafts\=*.sca; \
	scavetool export -f 'module(scenarioFR_forwarding.aircraft[*].routing) AND name("hopCount:vector")' -o hop_count_vector.csv numAircrafts\=*.vec

gpsr-forwarding-equipageFraction-A2G_csv:
	cd $(SIM_OUTPUT_BASE)/$(GPSR_CONFIG); \
	echo -e "Generate CSV files for GPSR"; \
	scavetool export -f 'module(scenarioFR_forwarding.aircraft[*].app[*]) AND name("packetSent:count")' -o packet_sent_count_multiapp.csv numAircrafts\=*.sca; \
	scavetool export -f 'module(scenarioFR_forwarding.groundStation[0].app[0]) AND name("packetReceived:count")' -o packet_received_count.csv numAircrafts\=*.sca; \
	scavetool export -f 'module(scenarioFR_forwarding.aircraft[*].routing) AND name("hopCount:vector")' -o hop_count_vector.csv numAircrafts\=*.vec

optimized-greedy-equipageFraction-A2G_csv:
	cd $(SIM_OUTPUT_BASE)/$(GEOOPT_CONFIG); \
	echo -e "Generate CSV files for GeoOpt"; \
	scavetool export -f 'module(scenarioFR_forwarding.aircraft[*].app[*]) AND name("packetSent:count")' -o packet_sent_count_multiapp.csv numAircrafts\=*.sca; \
	scavetool export -f 'module(scenarioFR_forwarding.groundStation[0].app[0]) AND name("packetReceived:count")' -o packet_received_count.csv numAircrafts\=*.sca; \
	scavetool export -f 'module(scenarioFR_forwarding.aircraft[*].routing) AND name("hopCount:vector")' -o hop_count_vector.csv numAircrafts\=*.vec

dijkstra-equipageFraction_csv:
	cd $(SIM_OUTPUT_BASE)/$(DIJKSTRA_CONFIG); \
	echo -e "Generate CSV files for Dijkstra"; \
	scavetool export -f 'module(scenarioFR_forwarding.aircraft[*].app[*]) AND name("packetSent:count")' -o packet_sent_count_multiapp.csv numAircrafts\=*.sca; \
	scavetool export -f 'module(scenarioFR_forwarding.groundStation[0].app[0]) AND name("packetReceived:count")' -o packet_received_count.csv numAircrafts\=*.sca; \
	scavetool export -f 'module(scenarioFR_forwarding.aircraft[*].routing) AND name("hopCount:vector")' -o hop_count_vector.csv numAircrafts\=*.vec

run-paper-simulations-local: dijkstra-equipageFraction-A2G greedy-forwarding-1hop-equipageFraction-A2G gpsr-forwarding-equipageFraction-A2G optimized-greedy-equipageFraction-A2G

run-all-simulations-from-hpc-equipageFraction:
	sbatch scripts/s_scenarioFR_dspr.sh
	sbatch scripts/s_scenarioFR_greedy1.sh
	sbatch scripts/s_scenarioFR_gpsr.sh
	sbatch scripts/s_scenarioFR_optimizedGreedy_eff_m8.sh

generate-all-equipageFraction-csv: dijkstra-equipageFraction_csv greedy-forwarding-1hop-equipageFraction-A2G_csv gpsr-forwarding-equipageFraction-A2G_csv optimized-greedy-equipageFraction-A2G_csv

remove-collected-result-files:
	find ./simresults -type f ! -name "*.csv" -exec rm {} +

check-missing-runs:
	bash scripts/s_check_missing_runs.sh --path $(SIM_OUTPUT_BASE)/$(GEOOPT_CONFIG) --variables 50,100,150,200,250,300,350,400,450,500 --runs 100

plot-equipage-fraction-metrics: run-pdr-plot run-hc-plot

run-pdr-plot:
	pipenv run python3 scripts/py_scenarioFR_pdr_paper.py --r $(PLOT_COMMUNICATION_RANGE) --BI $(PLOT_BEACON_INTERVAL)

run-hc-plot:
	pipenv run python3 scripts/py_scenarioFR_hc_paper.py --r $(PLOT_COMMUNICATION_RANGE) --BI $(PLOT_BEACON_INTERVAL)
