---
id: caching-proxy
title: Caching Proxy
---

<div>

# <a href="#/docs">Docs</a> <span>/</span> Caching Proxy

<img src="/static/img/main/cache.svg" alt="Cache">

The PacketFrame caching proxy puts the PacketFrame network in front of your origin webserver to increase performance and security. 

Proxied records can be added though the dashboard by clicking the "Add Record" button and enabling the proxy by clicking the cloud icon.

Once a proxied record is enabled, PacketFrame will request an SSL certificate from [LetsEncrypt](https://letsencrypt.org/) and configure the proxy. Origin pulls will come from unicast source IPs of the caching network.

Backend errors (HTTP 500, 502, 503, 504) will be caught by the caching servers and a generic error page will be shown.

### ACL Configuration

Every domain that has a proxied record must have at least one user with an ACL configured. IP blocks in the ACL are permitted to send the `PURGE` HTTP request method to any route under domains that user controls to purge the cache of that object. The ACL can be configured on a per-user basis by clicking the settings gear icon in the dashboard and adding the address in CIDR notation.

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
