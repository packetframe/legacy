---
id: dashboard
title: Dashboard
---

<div>

# <a href="#/docs">Docs</a> <span>/</span> Dashboard

<img src="/static/img/main/dashboard.svg" alt="Dashboard">

<h2>Dashboard</h2>
The PacketFrame dashboard implements all the functionality of PacketFrame through the API. Records can be added though the dashboard by clicking the "Add Record" button. Each record type has specific required attributes which will be displayed as input fields after selecting the record type from the dropdown.

<h2>Adding Zones</h2>
To add a zone, log in and click the "Add Zone" button located near the top right corner of the page, and entering your domain name. PacketFrame supports reverse zones as well, which can be added by specifying the IP address block in CIDR notation.

<h2>Record Management</h2>
The dashboard implements all the functionality of PacketFrame through the API. Records can be added though the dashboard by clicking the "Add Record" button. Each record type has specific required attributes which will be displayed as input fields after selecting the record type from the dropdown.

<h2>Node Pinning</h2>
DNS records are propagated to every edge node by default. You can control which nodes have an individual record with Node Pinning. By clicking the location icon when adding a record, you can choose which nodes that the record will be served from.

</div>

<style>
    div {
        margin: auto;
        width: 50%;
    }
    
    span {
        color: #d000ff;
    }
    
    a {
        color: white;
        text-decoration: none;
    }
    
    img {
        width: 350px;
        display: block;
        margin: auto auto 40px;
    }
</style>
