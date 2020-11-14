---
id: api
title: API
---

All API routes are under `https://dash.delivr.dev/api/`

Authenticated routes require the `X-API-Key` request header to be set to your API key.

### Routes

| Endpoint                           | Methods | Usage                                |
| ---------------------------------- | ------- | ------------------------------------ |
| /auth/signup                       | POST    | Create an account                    |
| /auth/login                        | POST    | Get your API token                   |
| /zones/add                         | POST    | Add a zone to delivr                 |
| /zones/list                        | GET     | Get all zones under your account     |
| /zone/[ZONE]/delete                | POST    | Remove [ZONE] from delivr            |
| /zone/[ZONE]/add                   | POST    | Add a record to [ZONE]               |
| /zone/[ZONE/records                | GET     | Get records for [ZONE]               |
| /zone/[ZONE/users                  | GET     | Get users for [ZONE]                 |
| /zone/[ZONE]/delete_record/[INDEX] | POST    | Delete record at [INDEX] from [ZONE] |
| /zone/[ZONE]/export | GET   | Download RFC 1035 zone file for [ZONE] |
| /admin | GET   | Check if the authenticated user is an admin or not |
| /user/acl | GET, PUT   | Get or append to a user IP ACL |
| /user/change_password | POST   | Change a user's password |
| /counters | GET  | Get node and location counters |

### Admin Routes
| Endpoint                           | Methods | Usage                                |
| ---------------------------------- | ------- | ------------------------------------ |
| /nodes/add | POST   | Add a DNS node |
| /cache_nodes/add | POST   | Add a HTTP cache node |
| /nodes/list | GET   | Get all DNS node |
| /nodes/power | POST   | Enable or disable the node's BGP daemon |
| /stats | GET   | Get system stats counters (nodes/zones/users) |
| /users | GET   | Get all users |
| /user/[USER]/toggle | POST   | Toggle [USER]'s enabled state |

### Debug Routes
| Endpoint                           | Methods | Usage                                |
| ---------------------------------- | ------- | ------------------------------------ |
| /debug/refresh_zones | GET   | Refresh all zone registry file |
| /debug/refresh_single_zone/[ZONE] | GET   | Refresh [ZONE]'s zone file |
| /debug/refresh_all_zones | GET   | Refresh all zone files |
| /debug/clear_queue | GET   | Clear opqueue |
| /debug/queue_status | GET   | Get number of running and ready tasks |
| /debug/refresh_cache | GET   | Refresh cache's varnish and caddy configs |

### Route Specifics

##### /auth/signup

Create a zone

Methods: POST

Request Body:

| POST Field | Type   | Description |
| ---------- | ------ | ----------- |
| username   | string | Username    |
| password   | string | Password    |


##### /auth/login

Create a zone

Methods: POST
Returns: API Key

Request Body:

| POST Field | Type   | Description |
| ---------- | ------ | ----------- |
| username   | string | Username    |
| password   | string | Password    |



##### /zones/add
Create a zone

Methods: POST

Request Body:

| POST Field | Type   | Description                                                  |
| ---------- | ------ | ------------------------------------------------------------ |
| zone       | string | RFC 1035 DNS label of the zone (e.g. `example.com` or `2.0.192.in-addr.arpa`) |



##### /zones/list

Create a zone

Methods: GET



##### /zone/[ZONE]/delete

Delete a zone

Methods: POST

| URL Field | Type   | Description                                                  |
| --------- | ------ | ------------------------------------------------------------ |
| zone      | string | RFC 1035 DNS label of the zone (e.g. `example.com` or `2.0.192.in-addr.arpa`) |



##### /zone/[ZONE]/add

Add a record to zone

Methods: POST

Request Body:

| POST Field | Type   | Description                                                  |
| ------ | ------ | ------------------------------------------------------------ |
| ttl    | int | Record TTL (Time To Live)                                    |
| label | string | RFC 1035 DNS label of the zone (e.g. `example.com` or `2.0.192.in-addr.arpa`) |
| type      | string | DNS record type (Supported values are A, AAAA, MX, SRV, TXT, [PTR for reverse zones]) |
| value      | string | Value of record (IP address, name, etc) |
| {additional options}      | string|int | additional options for specific zone type |



##### /zone/[ZONE]/records

Get records

Methods: GET

| URL Field | Type   | Description                                                  |
| --------- | ------ | ------------------------------------------------------------ |
| zone      | string | RFC 1035 DNS label of the zone (e.g. `example.com` or `2.0.192.in-addr.arpa`) |



##### /zone/[ZONE]/delete_record/[INDEX]

Delete a record

Methods: POST

Request Body:

| URL Field | Type   | Description                                                  |
| --------- | ------ | ------------------------------------------------------------ |
| zone      | string | RFC 1035 DNS label of the zone (e.g. `example.com` or `2.0.192.in-addr.arpa`) |
| index     | int    | Index of the record (To retrieve records, see `/records/list`) |
