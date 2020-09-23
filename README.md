# cdn-v2

#### API Documentation


##### /zones/add
Create a zone

Methods: POST

Request Body:

| Field | Type   | Description                                                  |
| ----- | ------ | ------------------------------------------------------------ |
| zone  | string | RFC 1035 DNS label of the zone (e.g. `example.com` or `2.0.192.in-addr.arpa`) |



##### /zones/delete

Delete a zone

Methods: POST

Request Body:

| Field | Type   | Description                                                  |
| ----- | ------ | ------------------------------------------------------------ |
| zone  | string | RFC 1035 DNS label of the zone (e.g. `example.com` or `2.0.192.in-addr.arpa`) |



##### /records/add

Add  a record

Methods: POST

Request Body:

| Field  | Type   | Description                                                  |
| ------ | ------ | ------------------------------------------------------------ |
| zone   | string | RFC 1035 DNS label of the zone (e.g. `example.com` or `2.0.192.in-addr.arpa`) |
| domain | string | Zone key (domain) (e.g. `1.2.0.192.in-addr.arpa.` or `www.example.com.`) |
| ttl    | string | Record TTL (Time To Live)                                    |
| type   | string | `A`, `AAAA`, `CNAME`, `PTR`                                  |
| value  | string | Record value in RFC 1035 format (e.g. `192.0.2.1` or `example.com.`) |



##### /records/list

Get records

Methods: GET

Request Body:

| Field | Type   | Description                                                  |
| ----- | ------ | ------------------------------------------------------------ |
| zone  | string | RFC 1035 DNS label of the zone (e.g. `example.com` or `2.0.192.in-addr.arpa`) |



##### /records/delete

Delete a record

Methods: POST

Request Body:

| Field | Type   | Description                                                  |
| ----- | ------ | ------------------------------------------------------------ |
| zone  | string | RFC 1035 DNS label of the zone (e.g. `example.com` or `2.0.192.in-addr.arpa`) |
| index | int    | Index of the record (To retrieve records, see `/records/list`) |



##### /nodes/list

List nodes

Methods: GET

Request Body: None


##### /nodes/delete

Add  a node

Methods: POST

Request Body:

| Field | Type   | Description                                                  |
| ----- | ------ | ------------------------------------------------------------ |
| name  | string | Unique name of the node (FMT-US) |
| provider | string    | Host datacenter |
| geoloc | string    | Lat,Lon of datacenter |
| pubkey | string    | WireGuard public key of node |
| location | string    | Location in written form (Fremont, CA) |
| management_ip | string    | VPN-Internal address of node |
| ipv4 | string    | OOB IPv4 Address |
| ipv6 | string    | OOB IPv6 Address |
