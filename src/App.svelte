<script>
    import Navbar from "./components/Navbar.svelte";
    import RecordTable from "./components/RecordTable.svelte";
    import Dropdown from "./components/Dropdown.svelte";
    import {onMount} from "svelte";
    import NetworkMap from "./components/NetworkMap.svelte";
    import Button from "./components/Button.svelte";

    let zones;
    let selected_zone = "";
    let no_zones = false;
    let showMap = false;

    onMount(() => {
        fetch("http://localhost/api/zones/list")
            .then(response => response.json())
            .then(data => {
                if (data["message"].length > 0) {
                    zones = data["message"];
                    selected_zone = data["message"][0]["zone"];
                } else {
                    no_zones = true;
                }
            });
    });
</script>

<main>
    <Navbar>
        <div slot="left-side">CDN</div>
        <div slot="right-side">Logout</div>
    </Navbar>

    <div class="body">
        <div class="header-container">
            <h1 class="header-text">CDN Dashboard</h1>

            <Button padded=true onclick={() => showMap = !showMap}>Toggle Map</Button>
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

        {#if showMap}
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

    </div>
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
</style>
