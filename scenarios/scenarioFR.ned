//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
//
// You should have received a copy of the GNU Lesser General Public License
// along with this program.  If not, see http://www.gnu.org/licenses/.
//

package simulation.scenarios;

import inet.networklayer.configurator.ipv4.Ipv4NetworkConfigurator;
import inet.node.inet.ManetRouter;
import inet.physicallayer.contract.packetlevel.IRadioMedium;
import ldacs_abstract_tdma.scheduler.AbstractLdacsTdmaScheduler;
import ldacs_scenario_manager.LdacsScenarioManager;
import inet.node.ethernet.EtherSwitch;
import ned.DatarateChannel;
import ldacs_abstract_radio.LdacsAbstractRadio;

// import dspr.Dspr;
// import dspr.NodeManager;

network scenarioFR
{
    parameters:
        int numAircrafts = default(0);
        int numGroundStations = default(1);
        @statistic[sumBeaconMsg](source=count(beacon); record=count);
        @statistic[sumPacketSent](source=count(packetSent); record=count);
        @statistic[sumAppPacketSent](source=count(appPacketSent); record=count);

        @display("bgb=10000000,10000000;bgl=2");
        @figure[title](type=label; pos=0,-1; anchor=sw; color=darkblue);
    submodules:
        scenarioManager: LdacsScenarioManager;
        scheduler: AbstractLdacsTdmaScheduler {
            parameters:
                @display("p=100,400;is=s");
        }

        radioMedium: <default("UnitDiskRadioMedium")> like IRadioMedium {
            @display("p=580,275");
        }

        configurator: Ipv4NetworkConfigurator {
            parameters:
                @display("p=100,100;is=s");
        }

        aircraft[numAircrafts]: ManetRouter {
            @display("i=aircraft");
        }

        groundStation[numGroundStations]: ManetRouter {
            parameters:
                @display("i=device/receiverdish_vl");
        }

        // nodeManager: NodeManager;
}

network scenarioFR_forwarding extends scenarioFR
{
    types:
        channel Eth1G extends DatarateChannel
        {
            parameters:
                datarate = 1Gbps;
                delay = 1.5ms;
                ber = 0;
        }
    submodules:
        switchGS: EtherSwitch {
            parameters:
                @display("p=1150000,380000");
            gates:
                ethg[372];
        }
    connections allowunconnected:
        for i=0..numAircrafts-1 {
            aircraft[i].ethg++ <--> Eth1G <--> switchGS.ethg++ ;
        }
        groundStation[0].ethg++ <--> Eth1G <--> switchGS.ethg++ ;
}
