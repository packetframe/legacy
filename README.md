# cdn-v2

#### API Documentation




##### /zone/add
Create a zone

Methods: POST

Request Body:

| POST Field | Type   | Description                                                  |
| ---------- | ------ | ------------------------------------------------------------ |
| zone       | string | RFC 1035 DNS label of the zone (e.g. `example.com` or `2.0.192.in-addr.arpa`) |



##### /zones/list

Create a zone

Methods: GET



##### /zone/<zone>/delete

Delete a zone

Methods: POST

| URL Field | Type   | Description                                                  |
| --------- | ------ | ------------------------------------------------------------ |
| zone      | string | RFC 1035 DNS label of the zone (e.g. `example.com` or `2.0.192.in-addr.arpa`) |



##### /zone/<zone>/add/<record_type>

Add a record to zone

Methods: POST

Request Body:

| POST Field | Type   | Description                                                  |
| ------ | ------ | ------------------------------------------------------------ |
| ttl    | int | Record TTL (Time To Live)                                    |
| label | string | RFC 1035 DNS label of the zone (e.g. `example.com` or `2.0.192.in-addr.arpa`) |
| type      | string | DNS record type (Supported values are A, AAAA) |
| value      | string | Value of record (IP address, name, etc) |



##### /zone/<zone>/records

Get records

Methods: GET

| URL Field | Type   | Description                                                  |
| --------- | ------ | ------------------------------------------------------------ |
| zone      | string | RFC 1035 DNS label of the zone (e.g. `example.com` or `2.0.192.in-addr.arpa`) |



##### /zone/<zone>/delete_record/<index>

Delete a record

Methods: POST

Request Body:

| URL Field | Type   | Description                                                  |
| --------- | ------ | ------------------------------------------------------------ |
| zone      | string | RFC 1035 DNS label of the zone (e.g. `example.com` or `2.0.192.in-addr.arpa`) |
| index     | int    | Index of the record (To retrieve records, see `/records/list`) |



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
