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
    import {APIKey} from "./stores";
    import {IsAdmin} from "./stores";

    let zones;
    let selected_zone = window.location.toString().split("zone=")[1];
    let no_zones = false;
    let showMap = false;

    function loadRecordDropdown(page) {
        fetch("http://localhost/api/nodes/list", {
            headers: {"X-API-Key": $APIKey},
        })
            .then(response => response.json())
            .then(data => {
                if (data["success"]) {
                    $IsAdmin = true;
                }
            })

        if (page === "dashboard") {
            fetch("http://localhost/api/zones/list", {
                method: "GET",
                headers: {
                    "X-API-Key": $APIKey
                },
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
</script>

<main>
    <Navbar>
        <div slot="left-side">CDN</div>
        <div class="nav-item" on:click={() => {$APIKey = ""; $Page = "login"}} slot="right-side">Logout</div>
        <div class="nav-item" on:click={() => {$Page = "signup"}} slot="right-side">Signup</div>
    </Navbar>

    <div class="body">
        {#if $Page === "dashboard"}
            <div class="header-container">
                <h1 class="header-text">CDN Dashboard</h1>

                {#if $IsAdmin}
                    <Button onclick={() => showMap = !showMap} padded={true}>Toggle Map</Button>
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

            {#if showMap && $IsAdmin}
                <NetworkMap/>
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
        CDN v2
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
