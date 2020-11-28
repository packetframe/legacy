<script>
    import DocsHome from "../components/DocsHome.svelte";

</script>

<main>
    <DocsHome/>

    <h2>Dashboard</h2>
    The PacketFrame dashboard implements all the functionality of PacketFrame through the API. Records can be added though the dashboard by clicking the "Add Record" button. Each record type has specific required attributes which will be displayed as input fields after selecting the record type from the dropdown.

    <h2>Adding Zones</h2>
    To add a zone, log in and click the "Add Zone" button located near the top right corner of the page, and entering your domain name. PacketFrame supports reverse zones as well, which can be added by specifying the IP address block in CIDR notation.

    <h2>Record Management</h2>
    The dashboard implements all the functionality of PacketFrame through the API. Records can be added though the dashboard by clicking the "Add Record" button. Each record type has specific required attributes which will be displayed as input fields after selecting the record type from the dropdown.

    <h2>Node Pinning</h2>
    DNS records are propagated to every edge node by default. You can control which nodes have an individual record with Node Pinning. By clicking the location icon when adding a record, you can choose which nodes that the record will be served from.

    <h2>Embedded Cache Appliance</h2>
    The Edge Cache Appliance (ECA) program brings PacketFrame content as close to your users as possible by deploying an anycast node directly in your network. ECAs are designed to run in a wide variety of environments, even those behind firewalls with limited external access. Requests are evaluated on a case-by-case basis and involve specific technical and policy requirements. Depending on the scenario, ECAs are available as dedicated hardware as well as VM images. Networks that wish to have PacketFrame content with the lowest possible latency can opt to host an EOS server for the full DNS or HTTP(S) traffic. EOS are fully managed by PacketFrame and can be run on a VM or dedicated server. EOS nodes to the host network via BGP and announce routes based on instructions from the PacketFrame control plane.

</main>

<style>
    main {
        width: 75%;
        margin: auto;
    }
</style>
