---
id: api
title: API
---

<div class="wrapper">
<div>

# <a href="#/docs">Docs</a> <span>/</span> API

<img src="/static/img/main/code2.svg" alt="Code">

PacketFrame's API exposes all functionality of the platform via a RESTful programmatic interface.

All API routes are under `https://packetframe.com/api/`

Authenticated routes require the `X-API-Key` request header to be set to your API key.

## Routes

| Endpoint                           | Methods  | Usage                                              |
| ---------------------------------- | -------- | -------------------------------------------------- |
| /auth/signup                       | POST     | Create an account                                  |
| /auth/login                        | POST     | Get your API token                                 |
| /zones/add                         | POST     | Add a zone                                         |
| /zones/list                        | GET      | Get all zones under your account                   |
| /zone/[ZONE]/delete                | POST     | Remove [ZONE]                                      |
| /zone/[ZONE]/add                   | POST     | Add a record to [ZONE]                             |
| /zone/[ZONE/records                | GET      | Get records for [ZONE]                             |
| /zone/[ZONE/users                  | GET      | Get users for [ZONE]                               |
| /zone/[ZONE]/delete_record/[INDEX] | POST     | Delete record at [INDEX] from [ZONE]               |
| /zone/[ZONE]/export                | GET      | Download RFC 1035 zone file for [ZONE]             |
| /admin                             | GET      | Check if the authenticated user is an admin or not |
| /user/acl                          | GET, PUT | Get or append to a user IP ACL                     |
| /user/change_password              | POST     | Change a user's password                           |
| /counters                          | GET      | Get node and location counters                     |
| /nodes/geoloc                      | GET      | Get node locations                                 |

## Admin Routes

| Endpoint            | Methods | Usage                                         |
| ------------------- | ------- | --------------------------------------------- |
| /nodes/add          | POST    | Add a DNS node                                |
| /nodes/list         | GET     | Get all DNS node                              |
| /nodes/power        | POST    | Enable or disable the node's BGP daemon       |
| /stats              | GET     | Get system stats counters (nodes/zones/users) |
| /users              | GET     | Get all users                                 |
| /user/[USER]/toggle | POST    | Toggle [USER]'s enabled state                 |

## Debug Routes

| Endpoint             | Methods | Usage                                     |
| -------------------- | ------- | ----------------------------------------- |
| /debug/refresh_zones | GET     | Refresh all zones                         |
| /debug/clear_queue   | GET     | Clear opqueue                             |
| /debug/queue_status  | GET     | Get number of running and ready tasks     |
| /debug/refresh_cache | GET     | Refresh cache's varnish and caddy configs |
| /debug/update_collector_monitoring | GET     | Update route collector and prometheus configs |

### Route Specifics

#### /auth/signup

Create a zone

Methods: POST

Request Body:

| POST Field | Type   | Description |
| ---------- | ------ | ----------- |
| username   | string | Username    |
| password   | string | Password    |

#### /auth/login

Create a zone

Methods: POST
Returns: API Key

Request Body:

| POST Field | Type   | Description |
| ---------- | ------ | ----------- |
| username   | string | Username    |
| password   | string | Password    |

#### /zones/add

Create a zone

Methods: POST

Request Body:

| POST Field | Type   | Description                                                                   |
| ---------- | ------ | ----------------------------------------------------------------------------- |
| zone       | string | RFC 1035 DNS label of the zone (e.g. `example.com` or `2.0.192.in-addr.arpa`) |

#### /zones/list

Create a zone

Methods: GET

##### /zone/[ZONE]/delete

Delete a zone

Methods: POST

| URL Field | Type   | Description                                                                   |
| --------- | ------ | ----------------------------------------------------------------------------- |
| zone      | string | RFC 1035 DNS label of the zone (e.g. `example.com` or `2.0.192.in-addr.arpa`) |

##### /zone/[ZONE]/add

Add a record to zone

Methods: POST

Request Body:

| POST Field         | Type       | Description                                                                           |
| ------------------ | ---------- | ------------------------------------------------------------------------------------- |
| ttl                | int        | Record TTL (Time To Live)                                                             |
| label              | string     | RFC 1035 DNS label of the zone (e.g. `example.com` or `2.0.192.in-addr.arpa`)         |
| type               | string     | DNS record type (Supported values are A, AAAA, MX, SRV, TXT, [PTR for reverse zones]) |
| value              | string     | Value of record (IP address, name, etc)                                               |
| additional options | string/int | additional options for specific zone type                                             |

##### /zone/[ZONE]/records

Get records

Methods: GET

| URL Field | Type   | Description                                                                   |
| --------- | ------ | ----------------------------------------------------------------------------- |
| zone      | string | RFC 1035 DNS label of the zone (e.g. `example.com` or `2.0.192.in-addr.arpa`) |


##### /zone/[ZONE]/delete_record/[INDEX]

Delete a record

Methods: POST

Request Body:

| URL Field | Type   | Description                                                                   |
| --------- | ------ | ----------------------------------------------------------------------------- |
| zone      | string | RFC 1035 DNS label of the zone (e.g. `example.com` or `2.0.192.in-addr.arpa`) |
| index     | int    | Index of the record (To retrieve records, see `/records/list`)                |

</div>
</div>

<style>
    .wrapper {
        display: flex;
        justify-content: center;
    }
    
     th {
        padding-top: 16px;
        padding-bottom: 16px;
        padding-left: 20px;
        text-align: left;
        background-color: #202020;
        border-bottom: 1px solid #555555;
        color: white;
        margin: 0;
    }
    
    tr {
        display: table-row !important;
    }
    
    tr:nth-child(odd) {
        background-color: #111111;
    }
    
    td {
        padding-top: 15px;
        padding-bottom: 15px;
        padding-left: 20px;
        text-align: left;
    }
    
    table {
        width: 100%;
        overflow-y: scroll;
        max-height: calc(100% - 20px);
        margin-top: 10px;
        border-collapse: collapse;
        border: 1px white solid;
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
