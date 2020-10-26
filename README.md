<p align="center">
  <img width="250px" src="https://raw.githubusercontent.com/natesales/delivr/main/logo.png" alt="delivr.dev logo"/>
  <br>
  <a href="https://github.com/natesales/delivr/blob/main/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/natesales/delivr?style=for-the-badge"></a>
  <a href="https://delivr.dev/docs/record-management"><img alt="Documentation" src="https://img.shields.io/badge/docs-delivr.dev-blue?style=for-the-badge"></a>
</p>


## delivr.dev

delivr.dev is an open source CDN platform, currently in beta.

#### Installation
Set up Caddy
```bash
# Download and install
rm /etc/caddy/Caddyfile
ln -s /home/nate/delivr/Caddyfile /etc/caddy/Caddyfile
caddy reload -config /etc/caddy/Caddyfile

# Link services
ln -s /home/nate/delivr/delivr-api.service /etc/systemd/system/delivr-api.service
ln -s /home/nate/delivr/delivr-orchestrator.service /etc/systemd/system/delivr-orchestrator.service
```

#### Project Structure
```
.
├── backend # All code that runs server side
│   ├── acme # LetsEncrypt automation for ACME challenges
│   ├── provisioning # Ansible playbooks for node deployment
│   └── templates # Per-node config templates used by the orchestrator
├── docs # https://delivr.dev/ site, powered by Docusaurus
│   ├── blog # Blog posts
│   ├── docs # Doc pages
│   ├── src
│   │   ├── css
│   │   └── pages
│   └── static # Static assets
│       └── img
└── frontend # Svelte dashboard (https://dash.delivr.dev)
    ├── public # Public static assets
    │   ├── build
    │   └── img
    ├── scripts
    └── src
        └── components # Individual Svelte components
```