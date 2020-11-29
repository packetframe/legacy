---
id: security
title: Security
---

<script>
import Email from "../components/Email.svelte";
</script>

<div>

# <a href="#/docs">Docs</a> <span>/</span> Security

<img src="/static/img/main/hacker.svg">

Hackers are welcome! If you're interested in testing PacketFrame for vulns, please follow the rules below. When in doubt, ask!

Scope: Source code at https://github.com/packetframe/cdn

Security vulnerabilities should be reported to <Email/>, for general bugs feel free to file an issue at https://github.com/packetframe/cdn/issues 

Don't test in production! Download the source at https://github.com/packetframe/cdn and spin up a local instance of the CDN. If there's something you want to try on the production network, let me know first and we can work something out.

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
