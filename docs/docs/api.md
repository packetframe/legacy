---
id: api
title: API
---

All API routes are under `https://dash.delivr.dev/api/`

Authenticated routes require the `X-API-Key` request header to be set to your API key.

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



##### /zone/[ZONE]/add/[RECORD_TYPE]

Add a record to zone

Methods: POST

Request Body:

| POST Field | Type   | Description                                                  |
| ------ | ------ | ------------------------------------------------------------ |
| ttl    | int | Record TTL (Time To Live)                                    |
| label | string | RFC 1035 DNS label of the zone (e.g. `example.com` or `2.0.192.in-addr.arpa`) |
| type      | string | DNS record type (Supported values are A, AAAA) |
| value      | string | Value of record (IP address, name, etc) |



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
| location | string    | Location in written form (Fremont, CA) |
| management_ip | string    | Management address of the node |
