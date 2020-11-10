<script>
    import Navbar from "./components/Navbar.svelte";
    import RecordTable from "./components/RecordTable.svelte";
    import Dropdown from "./components/Dropdown.svelte";
    import {onMount} from "svelte";
    import NetworkMap from "./components/NetworkMap.svelte";
    import Button from "./components/Button.svelte";
    import EntryForm from "./components/EntryForm.svelte";
    import SnackbarGroup from "./components/SnackbarGroup.svelte";
    import {Page} from "./stores";
    import {IsAdmin} from "./stores";
    import {SnackBars} from "./stores";
    import ButtonBar from "./components/ButtonBar.svelte";
    import TextInput from "./components/TextInput.svelte";
    import {addSnackbar} from "./utils"
    import NetworkTable from "./components/NetworkTable.svelte";
    import UserTable from "./components/UserTable.svelte";
    import Settings from "./components/Settings.svelte";

    let zones;
    let selected_zone = window.location.toString().split("zone=")[1];
    let no_zones = false;
    let showAdmin = false;
    let showUserTable = false;
    let showSettings = false;

    onMount(() => {
        fetch("https://dash.delivr.dev/api/authenticated", {
            credentials: "include"
        })
            .then(response => response.json())
            .then(data => {
                if (data["message"]) { // If you are authenticated
                    $Page = "dashboard";
                }
            })
    })

    function loadRecordDropdown(page) {
        fetch("https://dash.delivr.dev/api/admin", {
            credentials: "include"
        })
            .then(response => response.json())
            .then(data => {
                if (data["success"]) {
                    $IsAdmin = true;
                }
            })

        if (page === "dashboard") {
            fetch("https://dash.delivr.dev/api/zones/list", {
                method: "GET",
                credentials: "include"
            })
                .then(response => response.json())
                .then(data => {
                    if (data["message"].length > 0) {
                        zones = data["message"];

                        if (location.hash.length < 2) {
                            location.hash = zones[0]["zone"];
                        }

                        selected_zone = location.hash.replace("#", "");
                    } else {
                        no_zones = true;
                    }
                });
        }
    }

    $: loadRecordDropdown($Page)

    function refreshZoneRegistry() {
        fetch("https://dash.delivr.dev/api/debug/refresh_zones", {
            method: "GET",
            credentials: "include"
        })
            .then(response => response.json())
            .then(data => {
                addSnackbar("refresh_zone_registry", data["message"], data["success"] ? "green" : "red")
            });
    }

    function refreshAllZones() {
        fetch("https://dash.delivr.dev/api/debug/refresh_all_zones", {
            method: "GET",
            credentials: "include"
        })
            .then(response => response.json())
            .then(data => {
                addSnackbar("refresh_all_zones", data["message"], data["success"] ? "green" : "red")
            });
    }

    function refreshSingleZone() {
        fetch("https://dash.delivr.dev/api/debug/refresh_single_zone/" + prompt("Which zone do you want to refresh?"), {
            method: "GET",
            credentials: "include"
        })
            .then(response => response.json())
            .then(data => {
                addSnackbar("refresh_single_zone", data["message"], data["success"] ? "green" : "red")
            });
    }

    function clearQueue() {
        fetch("https://dash.delivr.dev/api/debug/clear_queue", {
            method: "GET",
            credentials: "include"
        })
            .then(response => response.json())
            .then(data => {
                addSnackbar("clear_queue", data["message"], data["success"] ? "green" : "red")
            });
    }

    function showQueueStats() {
        fetch("https://dash.delivr.dev/api/debug/queue_stats", {
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
        fetch("https://dash.delivr.dev/api/stats", {
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
        fetch("https://dash.delivr.dev/api/debug/refresh_cache", {
            method: "GET",
            credentials: "include"
        })
            .then(response => response.json())
            .then(data => {
                addSnackbar("refresh_cache", data["message"], data["success"] ? "green" : "red")
            });
    }

    function addZone() {
        fetch("https://dash.delivr.dev/api/zones/add", {
            method: "POST",
            credentials: "include",
            body: JSON.stringify({
                zone: prompt("What domain do you want to add?")
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

    function addNode() {
        fetch("https://dash.delivr.dev/api/nodes/add", {
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

    let isEnabled = false;
</script>

<main>
    {#if $Page === "login"}
        <Navbar>
            <div slot="left-side" on:click={() => {$Page = "dashboard"}}><img src="/full.png" alt="delivr.dev"></div>
            <div class="nav-item" on:click={() => {$Page = "signup"}} slot="right-side">Signup</div>
        </Navbar>
    {:else}
        {#if $Page === "signup"}
            <Navbar>
                <div slot="left-side" on:click={() => {$Page = "dashboard"}}><img src="/full.png" alt="delivr.dev"></div>
                <div class="nav-item" on:click={() => {$Page = "login"}} slot="right-side">Login</div>
            </Navbar>
        {:else}
            {#if $Page === "dashboard"}
                <Navbar>
                    <div slot="left-side" on:click={() => {$Page = "dashboard"}}><img src="/full.png" alt="delivr.dev"></div>
                    <div class="nav-item" on:click={() => {
                        $Page = "login";
                        document.cookie = "";
                    }} slot="right-side">Logout
                    </div>
                </Navbar>
            {/if}
        {/if}
    {/if}

    <div class="body">
        {#if $Page === "dashboard"}
            <div class="header-container">
                <h1 class="header-text">Dashboard</h1>

                {#if $IsAdmin}
                    <Button onclick={() => showAdmin = !showAdmin}>Toggle Admin Tools</Button>
                {/if}

                <Button onclick={() => {showSettings = !showSettings}} padded={true} icon="settings" size="1.25rem"/>
                <Button onclick={() => addZone()} rpadded>Add Zone</Button>

                {#if zones}
                    <Dropdown width="100%" bind:content={selected_zone}>
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
                    <div class="admin-map"><NetworkMap admin/></div>
                    <div class="admin-table"><NetworkTable admin/></div>
                </div>

                {#if showUserTable}
                    <UserTable/>
                {/if}

                <ButtonBar>
                    <Button padded onclick={() => refreshZoneRegistry()}>Refresh zone registry</Button>
                    <Button padded onclick={() => refreshAllZones()}>Refresh all zones</Button>
                    <Button padded onclick={() => clearQueue()}>Clear queue</Button>
                    <Button padded onclick={() => refreshSingleZone()}>Refresh single zone</Button>
                    <Button padded onclick={() => refreshCache()}>Refresh cache</Button>
                    <Button padded onclick={() => showQueueStats()}>Queue Stats</Button>
                    <Button padded onclick={() => addNode()}>Add Node</Button>
                    <Button padded onclick={() => {showUserTable = !showUserTable}}>Toggle user table</Button>
                    <Button padded onclick={() => showSystemStats()}>System Stats</Button>
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
        {:else if $Page === "login"}
            <EntryForm type="login"/>
        {:else if $Page === "signup"}
            <EntryForm type="signup"/>
        {/if}

        <SnackbarGroup/>
    </div>

    <footer>
        &copy; Nate Sales 2020.
    </footer>
</main>

<style>
    main {
        height: 100%;
        width: 100%;
        margin: auto;
        background: black;
    }

    .body {
        width: clamp(70%, 300px, 100%);
        margin: auto;
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

    footer {
        margin-top: 20px;
        margin-bottom: 15px;
        text-align: center;
    }

    .nav-item {
        padding: 2px;
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

    option:not(:checked) {
        color: black;
    }
</style>
