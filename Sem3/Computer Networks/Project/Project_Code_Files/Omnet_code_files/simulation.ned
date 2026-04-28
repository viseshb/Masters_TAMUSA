package simulations;

import inet.node.inet.StandardHost;
import inet.node.inet.Router;
import inet.networklayer.configurator.ipv4.Ipv4NetworkConfigurator;

channel EthLink extends ned.DatarateChannel {
    delay = 1ms;
    datarate = 100Mbps;
}

network OmnetNetwork {
    parameters:
        @display("bgb=900,400");
    submodules:
        configurator: Ipv4NetworkConfigurator {
            @display("p=450,80");
        }
        node1: StandardHost {
            @display("p=100,200;i=device/laptop");
        }
        node2: Router {
            parameters:
                numEthInterfaces = 2;
            @display("p=450,200;i=device/router");
        }
        node3: StandardHost {
            @display("p=800,200;i=device/pc");
        }
    connections allowunconnected:
        node1.ethg++ <--> EthLink <--> node2.ethg[0];
        node2.ethg[1] <--> EthLink <--> node3.ethg++;
}
