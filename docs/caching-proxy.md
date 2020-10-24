---
id: caching-proxy
title: Caching Proxy
---

The delivr.dev caching proxy puts the delivr.dev network in front of your origin webserver to increase performance and security. 

Proxied records can be added though the dashboard by clicking the "Add Record" button and enabling the proxy by clicking the cloud icon.

![img](../static/img/adding_proxied_record.png)

Once a proxied record is enabled, delivr.dev will request an SSL certificate from [LetsEncrypt](https://letsencrypt.org/) and configure the proxy. Origin pulls will come from unicast source IPs of the caching network.

Backend errors (HTTP 500, 502, 503, 504) will be caught by the caching servers and a generic delivr.dev error page will be shown.
