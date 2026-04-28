/* ============================================================================
 *  Project: Network Performance Monitoring — FABRIC Equivalent (ns-3)
 *  Author : Visesh Bentula
 *  Modes  : 1. static     -> traditional static routing
 *            2. wireguard -> overlay link (encrypted-like tunnel)
 *            3. sshuttle  -> TCP relay simulation
 *  Output : Saves results to results/flow_<mode>.xml & results/ns3_<mode>.xml
 *            → Open the XML in NetAnim to visualize the FABRIC-style topology.
 *  ============================================================================ */

#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/ipv4-static-routing-helper.h"
#include "ns3/flow-monitor-module.h"
#include "ns3/netanim-module.h"
#include <sys/stat.h>
#include <sys/types.h>

using namespace ns3;
using namespace std;

NS_LOG_COMPONENT_DEFINE("FabricSim");

/* ------------------ Utility: Ensure results directory exists ------------------ */
void EnsureResultsFolder(const string &path)
{
    struct stat info;
    if (stat(path.c_str(), &info) != 0)
    {
        NS_LOG_UNCOND("Creating results directory...");
        mkdir(path.c_str(), 0777);
    }
    else if (!(info.st_mode & S_IFDIR))
    {
        NS_LOG_UNCOND("Warning: 'results' exists but is not a directory!");
    }
}

/* ------------------ FlowMonitor Metrics Printer ------------------ */
void PrintMetrics(Ptr<FlowMonitor> monitor, Ptr<Ipv4FlowClassifier> classifier)
{
    FlowMonitor::FlowStatsContainer stats = monitor->GetFlowStats();
    cout << "\n================= Flow Monitor Results =================\n";
    for (auto const &flow : stats)
    {
        Ipv4FlowClassifier::FiveTuple t = classifier->FindFlow(flow.first);
        cout << "Flow ID: " << flow.first
             << "  (" << t.sourceAddress << " → " << t.destinationAddress << ")\n";
        cout << "  Tx Packets: " << flow.second.txPackets << endl;
        cout << "  Rx Packets: " << flow.second.rxPackets << endl;
        cout << "  Packet Loss: " << (flow.second.txPackets - flow.second.rxPackets) << endl;

        if (flow.second.timeLastRxPacket.GetSeconds() > flow.second.timeFirstTxPacket.GetSeconds())
        {
            double throughput = (flow.second.rxBytes * 8.0 /
                                 (flow.second.timeLastRxPacket.GetSeconds() -
                                  flow.second.timeFirstTxPacket.GetSeconds())) / 1e6;
            cout << "  Throughput: " << throughput << " Mbps" << endl;
        }

        cout << "  Delay Sum: " << flow.second.delaySum.GetSeconds() << " s" << endl;
        cout << "-------------------------------------------------------\n";
    }
}

/* ------------------ Main Simulation ------------------ */
int main(int argc, char *argv[])
{
    CommandLine cmd;
    string mode = "static"; // "static", "wireguard", "sshuttle"
    cmd.AddValue("mode", "Simulation mode", mode);
    cmd.Parse(argc, argv);

    string resultsDir = "results";
    EnsureResultsFolder(resultsDir);

    Time::SetResolution(Time::NS);
    LogComponentEnable("UdpEchoClientApplication", LOG_LEVEL_INFO);
    LogComponentEnable("UdpEchoServerApplication", LOG_LEVEL_INFO);

    // --- Create 3 nodes: Node1, Node2, Node3 ---
    NodeContainer nodes;
    nodes.Create(3);

    // --- Create two point-to-point channels ---
    PointToPointHelper p2p;
    p2p.SetDeviceAttribute("DataRate", StringValue("10Mbps"));
    p2p.SetChannelAttribute("Delay", StringValue("2ms"));

    NetDeviceContainer d1 = p2p.Install(nodes.Get(0), nodes.Get(1)); // Node1-Node2
    NetDeviceContainer d2 = p2p.Install(nodes.Get(1), nodes.Get(2)); // Node2-Node3

    // --- Install TCP/IP stack ---
    InternetStackHelper stack;
    stack.Install(nodes);

    // --- Assign IP addresses ---
    Ipv4AddressHelper ip;
    ip.SetBase("192.168.1.0", "255.255.255.0");
    Ipv4InterfaceContainer i1 = ip.Assign(d1);
    ip.SetBase("192.168.2.0", "255.255.255.0");
    Ipv4InterfaceContainer i2 = ip.Assign(d2);

    // --- Enable IP forwarding on Node2 ---
    Ptr<Ipv4> ipv4 = nodes.Get(1)->GetObject<Ipv4>();
    ipv4->SetAttribute("IpForward", BooleanValue(true));

    // --- Configure static routes ---
    Ipv4StaticRoutingHelper routing;
    Ptr<Ipv4StaticRouting> r1 = routing.GetStaticRouting(nodes.Get(0)->GetObject<Ipv4>());
    Ptr<Ipv4StaticRouting> r3 = routing.GetStaticRouting(nodes.Get(2)->GetObject<Ipv4>());
    r1->AddNetworkRouteTo(Ipv4Address("192.168.2.0"), Ipv4Mask("255.255.255.0"), 1);
    r3->AddNetworkRouteTo(Ipv4Address("192.168.1.0"), Ipv4Mask("255.255.255.0"), 1);

    /* ========================= MODES ========================= */

    if (mode == "static")
    {
        NS_LOG_UNCOND("Mode: Static Routing (UDP Echo)");

        UdpEchoServerHelper echoServer(9);
        ApplicationContainer serverApps = echoServer.Install(nodes.Get(2));
        serverApps.Start(Seconds(1.0));
        serverApps.Stop(Seconds(10.0));

        UdpEchoClientHelper echoClient(i2.GetAddress(1), 9);
        echoClient.SetAttribute("MaxPackets", UintegerValue(5));
        echoClient.SetAttribute("Interval", TimeValue(Seconds(1.0)));
        echoClient.SetAttribute("PacketSize", UintegerValue(1024));
        ApplicationContainer clientApps = echoClient.Install(nodes.Get(0));
        clientApps.Start(Seconds(2.0));
        clientApps.Stop(Seconds(10.0));
    }
    else if (mode == "wireguard")
    {
        NS_LOG_UNCOND("Mode: WireGuard-style overlay (Encrypted Tunnel)");

        PointToPointHelper wg;
        wg.SetDeviceAttribute("DataRate", StringValue("20Mbps"));
        wg.SetChannelAttribute("Delay", StringValue("1ms"));
        NetDeviceContainer wgDevices = wg.Install(nodes.Get(0), nodes.Get(2));

        Ipv4AddressHelper wgIp;
        wgIp.SetBase("10.0.0.0", "255.255.255.0");
        wgIp.Assign(wgDevices);

        UdpEchoServerHelper echoServer(9);
        ApplicationContainer serverApps = echoServer.Install(nodes.Get(2));
        serverApps.Start(Seconds(1.0));
        serverApps.Stop(Seconds(10.0));

        UdpEchoClientHelper echoClient(InetSocketAddress("10.0.0.2", 9));
        echoClient.SetAttribute("MaxPackets", UintegerValue(5));
        echoClient.SetAttribute("Interval", TimeValue(Seconds(1.0)));
        echoClient.SetAttribute("PacketSize", UintegerValue(1024));
        ApplicationContainer clientApps = echoClient.Install(nodes.Get(0));
        clientApps.Start(Seconds(2.0));
        clientApps.Stop(Seconds(10.0));
    }
    else if (mode == "sshuttle")
    {
        NS_LOG_UNCOND("Mode: sshuttle-style TCP relay (Node2 as proxy)");

        uint16_t port = 5000;
        PacketSinkHelper sinkHelper("ns3::TcpSocketFactory",
                                    InetSocketAddress(Ipv4Address::GetAny(), port));
        ApplicationContainer sinkApp = sinkHelper.Install(nodes.Get(2));
        sinkApp.Start(Seconds(1.0));
        sinkApp.Stop(Seconds(15.0));

        OnOffHelper client("ns3::TcpSocketFactory",
                           InetSocketAddress(i2.GetAddress(1), port));
        client.SetConstantRate(DataRate("2Mbps"), 512);
        ApplicationContainer clientApp = client.Install(nodes.Get(0));
        clientApp.Start(Seconds(2.0));
        clientApp.Stop(Seconds(15.0));
    }

    /* ========================= VISUALIZATION ========================= */
    FlowMonitorHelper flowmon;
    Ptr<FlowMonitor> monitor = flowmon.InstallAll();

    string animFile = resultsDir + "/ns3_" + mode + ".xml";
    string flowFile = resultsDir + "/flow_" + mode + ".xml";

    AnimationInterface anim(animFile);

    // --- FABRIC-like layout (left → right) ---
    anim.SetConstantPosition(nodes.Get(0), 10, 20);  // Shore (Node1)
    anim.SetConstantPosition(nodes.Get(1), 30, 20);  // Relay (Node2)
    anim.SetConstantPosition(nodes.Get(2), 50, 20);  // Ship (Node3)

    // --- Add node descriptions and colors ---
    anim.UpdateNodeDescription(nodes.Get(0), "Node1 - Shore");
    anim.UpdateNodeDescription(nodes.Get(1), "Node2 - Relay");
    anim.UpdateNodeDescription(nodes.Get(2), "Node3 - Ship");

    anim.UpdateNodeColor(nodes.Get(0), 255, 100, 100); // Light Red
    anim.UpdateNodeColor(nodes.Get(1), 100, 255, 100); // Light Green
    anim.UpdateNodeColor(nodes.Get(2), 100, 100, 255); // Light Blue

    // Optional: annotate overlay tunnel
    if (mode == "wireguard")
        anim.UpdateLinkDescription(nodes.Get(0)->GetId(), nodes.Get(2)->GetId(),
                                   "Encrypted Overlay Tunnel (10.0.0.0/24)");
    if (mode == "sshuttle")
        anim.UpdateLinkDescription(nodes.Get(0)->GetId(), nodes.Get(2)->GetId(),
                                   "TCP Relay Path via Node2");

    Simulator::Stop(Seconds(15.0));
    Simulator::Run();

    Ptr<Ipv4FlowClassifier> classifier = DynamicCast<Ipv4FlowClassifier>(flowmon.GetClassifier());
    PrintMetrics(monitor, classifier);
    monitor->SerializeToXmlFile(flowFile, true, true);

    NS_LOG_UNCOND("Results saved to: " + flowFile);
    NS_LOG_UNCOND("Animation file saved to: " + animFile);

    Simulator::Destroy();
    return 0;
}
