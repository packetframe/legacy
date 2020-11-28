<script>
    import ButtonBar from "../components/ButtonBar.svelte";
    import Button from "../components/Button.svelte";
    import UserTable from "../components/UserTable.svelte";
    import Settings from "../components/Settings.svelte";
    import RecordTable from "../components/RecordTable.svelte";
    import {API, IsAdmin} from "../stores";
    import {addSnackbar, log} from "../utils";
    import Dropdown from "../components/Dropdown.svelte";
    import NetworkTable from "../components/NetworkTable.svelte";
    import NetworkMap from "../components/NetworkMap.svelte";
    import {onMount} from "svelte";

    let zones;
    let selected_zone;
    let no_zones = false;
    let showAdmin = false;
    let showUserTable = false;
    let showSettings = false;

    function loadRecordDropdown() {
        log("Checking for admin...")
        fetch($API + "admin", {
            credentials: "include"
        })
            .then(response => response.json())
            .then(data => {
                if (data["success"]) {
                    $IsAdmin = true;
                    log("Logged in as admin")
                }
            })
            .catch(result => alert(result))

        log("Querying zone list...")
        fetch($API + "zones/list", {
            method: "GET",
            credentials: "include"
        })
            .then(response => response.json())
            .then(data => {
                if (data["success"]) {
                    if (data["message"].length > 0) {
                        zones = data["message"];
                        selected_zone = zones[0]["zone"];
                    } else {
                        no_zones = true;
                    }
                } else {
                    window.location.hash = "#/login";
                }
            });
    }

    onMount(() => {
        loadRecordDropdown()
    })

    function refreshAllZones() {
        fetch($API + "debug/refresh_all_zones", {
            method: "GET",
            credentials: "include"
        })
            .then(response => response.json())
            .then(data => {
                addSnackbar("refresh_all_zones", data["message"], data["success"] ? "green" : "red")
            });
    }

    function clearQueue() {
        fetch($API + "debug/clear_queue", {
            method: "GET",
            credentials: "include"
        })
            .then(response => response.json())
            .then(data => {
                addSnackbar("clear_queue", data["message"], data["success"] ? "green" : "red")
            });
    }

    function showQueueStats() {
        fetch($API + "debug/queue_stats", {
            method: "GET",
            credentials: "include"
        })
            .then(response => response.json())
            .then(data => {
                addSnackbar("queue_stats", "success", data["success"] ? "green" : "red")
                alert("Pending: " + data["message"]["current_ready"] + "\nRunning: " + data["message"]["current_reserved"])
            });
    }

    function showSystemStats() {
        fetch($API + "stats", {
            method: "GET",
            credentials: "include"
        })
            .then(response => response.json())
            .then(data => {
                addSnackbar("stats", "success", data["success"] ? "green" : "red")
                alert("Nodes: " + data["message"]["nodes"] + "\nZones: " + data["message"]["zones"] + "\nUsers: " + data["message"]["users"] + "\nLocations: " + data["message"]["locations"])
            });
    }

    function refreshCache() {
        fetch($API + "debug/refresh_cache", {
            method: "GET",
            credentials: "include"
        })
            .then(response => response.json())
            .then(data => {
                addSnackbar("refresh_cache", data["message"], data["success"] ? "green" : "red")
            });
    }

    function addZone() {
        const zone = prompt("What domain do you want to add?")
        if (!(zone == "" || zone == null)) {
            fetch($API + "zones/add", {
            method: "POST",
            credentials: "include",
            body: JSON.stringify({
                zone: zone
            }),
            headers: {
                "Content-Type": "application/json"
            }
        })
            .then(response => response.json())
            .then(data => {
                addSnackbar("add_zone", data["message"], data["success"] ? "green" : "red")
                loadRecordDropdown("dashboard");
            });
        }
    }

    function addNode() {
        fetch($API + "nodes/add", {
            method: "POST",
            credentials: "include",
            body: JSON.stringify({
                name: prompt("Name"),
                provider: prompt("Provider"),
                datacenter: prompt("Datacenter"),
                geoloc: prompt("Geoloc"),
                location: prompt("Location"),
                management_ip: prompt("Management IP")
            }),
            headers: {
                "Content-Type": "application/json"
            }
        })
            .then(response => response.json())
            .then(data => {
                addSnackbar("add_node", data["message"], data["success"] ? "green" : "red")
            });
    }

    function updateCollector() {
        fetch($API + "debug/update_collector", {
            method: "GET",
            credentials: "include"
        })
            .then(response => response.json())
            .then(data => {
                addSnackbar("update_collector", data["message"], data["success"] ? "green" : "red")
            });
    }
</script>

<main>
    <div class="header-container">
        <h1 class="header-text">Dashboard</h1>

        {#if $IsAdmin}
            <Button onclick={() => showAdmin = !showAdmin}>Toggle Admin Tools</Button>
        {/if}

        <Button icon="settings" onclick={() => {showSettings = !showSettings}} padded={true} size="1.25rem"/>
        <Button onclick={() => addZone()} rpadded>Add Zone</Button>

        {#if zones}
            <Dropdown bind:content={selected_zone} large>
                {#each zones as zone}
                    <option value="{zone['zone']}">{zone['zone']}</option>
                {/each}
            </Dropdown>
        {:else}
            {#if no_zones}
                <p style="padding-left: 10px">No zones</p>
            {:else}
                <p style="padding-left: 10px">Loading...</p>
            {/if}
        {/if}
    </div>

    {#if showAdmin && $IsAdmin}
        <div class="admin-container">
            <div class="admin-map">
                <NetworkMap admin/>
            </div>
            <div class="admin-table">
                <NetworkTable admin/>
            </div>
        </div>

        {#if showUserTable}
            <UserTable/>
        {/if}

        <ButtonBar>
            <Button padded onclick={() => refreshAllZones()}>Refresh all zones</Button>
            <Button padded onclick={() => clearQueue()}>Clear queue</Button>
            <Button padded onclick={() => refreshCache()}>Refresh cache</Button>
            <Button padded onclick={() => showQueueStats()}>Queue Stats</Button>
            <Button padded onclick={() => addNode()}>Add Node</Button>
            <Button padded onclick={() => {showUserTable = !showUserTable}}>Toggle user table</Button>
            <Button padded onclick={() => showSystemStats()}>System Stats</Button>
            <Button padded onclick={() => updateCollector()}>Update Collector</Button>
        </ButtonBar>
    {/if}

    {#if showSettings}
        <Settings/>
    {/if}

    {#if selected_zone !== ""}
        <RecordTable zone={selected_zone}/>
    {:else}
        {#if no_zones}
            <p style="padding-left: 10px">No zones</p>
        {:else}
            <p style="padding-left: 10px">Loading...</p>
        {/if}
    {/if}
</main>


<style>
    main {
        height: 100%;
        width: clamp(70%, 300px, 100%);
        margin: auto;
        background: black;
    }

    .header-container {
        display: flex;
        flex-direction: row;
        align-items: center;
        width: 100%;
        flex-wrap: wrap;
    }

    .header-text {
        flex-grow: 1;
    }

    div img {
        width: 300px;
    }

    .admin-container {
        display: flex;
        height: 400px;
        margin-bottom: 20px;
    }

    .admin-table {
        width: 60%;
        height: 100%;
    }

    .admin-map {
        width: 40%;
        margin-right: 20px;
        max-height: 400px;
    }

    select {
        background: url(/static/img/arrow.png) 96% / 15% no-repeat #000;
    }
</style>
