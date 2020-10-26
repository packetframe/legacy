<p align="center">
  <img width="250px" src="https://raw.githubusercontent.com/natesales/delivr/master/logo.png" alt=delivr.dev logo"/>
</p>


## delivr.dev

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
