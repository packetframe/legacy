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
    import {SnackBars} from "./stores"
    import ButtonBar from "./components/ButtonBar.svelte";
    import TextInput from "./components/TextInput.svelte";
    import {addSnackbar} from "./utils"

    let zones;
    let selected_zone = window.location.toString().split("zone=")[1];
    let no_zones = false;
    let showAdmin = false;
    let showMap = true;

    function loadRecordDropdown(page) {
        fetch("https://delivr.dev/api/nodes/list", {
            credentials: "include"
        })
            .then(response => response.json())
            .then(data => {
                if (data["success"]) {
                    $IsAdmin = true;
                }
            })

        if (page === "dashboard") {
            fetch("https://delivr.dev/api/zones/list", {
                method: "GET",
                credentials: "include"
            })
                .then(response => response.json())
                .then(data => {
                    if (data["message"].length > 0) {
                        zones = data["message"];

                        if (selected_zone === undefined) {
                            selected_zone = data["message"][0]["zone"];
                        }
                    } else {
                        no_zones = true;
                    }
                });
        }
    }

    $: loadRecordDropdown($Page)

    function refreshZoneRegistry() {
        fetch("https://delivr.dev/api/debug/refresh_zones", {
            method: "GET",
            credentials: "include"
        })
            .then(response => response.json())
            .then(data => {
                addSnackbar("refresh_zone_registry", data["message"], data["success"] ? "green" : "red")
            });
    }

    function refreshAllZones() {
        fetch("https://delivr.dev/api/debug/refresh_all_zones", {
            method: "GET",
            credentials: "include"
        })
            .then(response => response.json())
            .then(data => {
                addSnackbar("refresh_all_zones", data["message"], data["success"] ? "green" : "red")
            });
    }

    function refreshSingleZone() {
        fetch("https://delivr.dev/api/debug/refresh_single_zone/" + prompt("Which zone do you want to refresh?"), {
            method: "GET",
            credentials: "include"
        })
            .then(response => response.json())
            .then(data => {
                addSnackbar("refresh_single_zone", data["message"], data["success"] ? "green" : "red")
            });
    }

    function clearQueue() {
        fetch("https://delivr.dev/api/debug/clear_queue", {
            method: "GET",
            credentials: "include"
        })
            .then(response => response.json())
            .then(data => {
                addSnackbar("clear_queue", data["message"], data["success"] ? "green" : "red")
            });
    }
</script>

<main>
    {#if $Page === "login"}
        <Navbar>
            <div slot="left-side" on:click={() => {$Page = "dashboard"}}>delivr.dev</div>
            <div class="nav-item" on:click={() => {$Page = "signup"}} slot="right-side">Signup</div>
        </Navbar>
    {:else}
        <Navbar>
            <div slot="left-side" on:click={() => {$Page = "dashboard"}}>delivr.dev</div>
            <div class="nav-item" on:click={() => {$Page = "login"}} slot="right-side">Login</div>
        </Navbar>
    {/if}

    <div class="body">
        {#if $Page === "dashboard"}
            <div class="header-container">
                <h1 class="header-text">CDN Dashboard</h1>

                {#if $IsAdmin}
                    <Button onclick={() => showAdmin = !showAdmin} padded={true}>Toggle Admin Tools</Button>
                {/if}

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
                {#if showMap}
                    <NetworkMap/>
                {/if}

                <ButtonBar>
                    <Button padded onclick={() => refreshZoneRegistry()}>Refresh zone registry</Button>
                    <Button padded onclick={() => refreshAllZones()}>Refresh all zones</Button>
                    <Button padded onclick={() => clearQueue()}>Clear queue</Button>
                    <Button padded onclick={() => refreshSingleZone()}>Refresh single zone</Button>
                    <Button padded onclick={() => {showMap = !showMap}}>Toggle map</Button>
                </ButtonBar>
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
</style>
