<script>
    import Navbar from "./components/Navbar.svelte";
    import RecordTable from "./components/RecordTable.svelte";

    let zone = document.location.toString().split('=')[1];
</script>

<main>
    <Navbar>
        <div slot="left-side">CDN</div>
        <div slot="right-side">Logout</div>
    </Navbar>

    <div class="body">
        {#if zone !== ""}
            <h1>Dashboard for {zone}</h1>
            <br>
            <RecordTable/>
        {:else}
            <h1>No zone specified</h1>
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
        width: 75%;
        margin: auto;
    }

    h1 {
        padding-left: 1.6vw;
    }
</style>