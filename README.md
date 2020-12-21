<p align="center">
  <img width="500px" src="https://packetframe.com/static/img/logo.png" alt="PacketFrame logo"/>
  <br>
  <a href="https://github.com/packetframe/cdn/blob/main/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/packetframe/cdn?style=for-the-badge"></a>
  <a href="https://packetframe.com"><img alt="Documentation" src="https://img.shields.io/badge/docs-packetframe.com-blue?style=for-the-badge"></a>
  <br>
  <a href="https://saucelabs.com"><img height="50px" alt="Documentation" src="https://opensource.saucelabs.com/images/opensauce/powered-by-saucelabs-badge-white.png?sanitize=true"></a>
</p>

## PacketFrame

The PacketFrame CDN is an open source (AGPL-3.0) anycast CDN platform, currently in beta. If you're interested in an account, send an email to the address listed on the front page of https://packetframe.com or reach out in #packetframe on freenode. 

#### Project Structure

```
.
├── backend # All code that runs server side
│   ├── acme # LetsEncrypt automation for ACME challenges
│   ├── provisioning # Ansible playbooks for node deployment
│   └── templates # Per-node config templates used by the orchestrator
└── frontend # Svelte dashboard (https://packetframe.com)
    ├── public
    │   └── static # Public static assets
    ├── scripts
    └── src
        └── components # Individual Svelte components
```
