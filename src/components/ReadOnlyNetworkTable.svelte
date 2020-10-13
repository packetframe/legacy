<script>
    import {onMount} from "svelte";

    let nodes;


    function getNodes() {
        fetch("https://delivr.dev/api/nodes/list", {
            credentials: "include"
        })
            .then(response => response.json())
            .then(data => {
                nodes = data
            })
    }

    onMount(() => getNodes());
</script>

<main>
    <div class="table-wrapper">
        <table class="sethjs-table">
            <tr>
                <th>Name</th>
                <th>Datacenter</th>
                <th>Provider</th>
            </tr>

            {#if nodes}
                {#each nodes as node, i }
                    <tr>
                        <td>{node["name"]}</td>
                        <td>{node["datacenter"]}</td>
                        <td>{node["provider"]}</td>
                    </tr>
                {/each}
            {:else}
                <p style="padding-left: 10px">Loading...</p>
            {/if}
        </table>
    </div>
</main>

<style>
    main {
        margin: auto;
        border: 2px solid white;
        border-radius: 15px;
        padding-bottom: 10px;
        padding-top: 10px;
    }

    div {
        display: flex;
        justify-content: space-between;
    }

    span {
        margin: 10px;
    }

    h2 {
        margin: 15px;
    }

    :global(.sethjs-table) {
        width: 100%;
        border-collapse: collapse;
    }

    :global(.sethjs-table th) {
        padding-top: 16px;
        padding-bottom: 16px;
        padding-left: 20px;
        text-align: left;
        background-color: #202020;
        border-bottom: 1px solid #555555;
        color: white;
        margin: 0;
    }

    :global(.sethjs-table tr) {
        width: 100%;
    }

    :global(.sethjs-table tr:nth-child(odd)) {
        background-color: #111111;
    }

    :global(.sethjs-table td) {
        padding-top: 15px;
        padding-bottom: 15px;
        padding-left: 20px;
        text-align: left;
    }

    .header-container {
        flex-direction: column;
    }

    .record-add-container {
        display: flex;
        width: calc(100% - 15px);
        align-content: center;
        flex-wrap: wrap;
        margin: 5px 8px 20px;
    }

    .record-add-element {
        display: flex;
        flex-direction: column;
        margin: 5px;
        justify-content: center;
        flex: 1 1 auto;
    }

    .record-add-element-number {
        display: flex;
        flex-direction: column;
        margin: 5px;
        justify-content: center;
        flex: 0.5 0 100px;
    }

    .record-add-element-select {
        display: flex;
        flex-direction: column;
        margin: 5px;
        justify-content: center;
        width: 25%;
        flex: 0 0 content;
    }

    .table-wrapper {
        overflow-x: auto;
        width: 100%;
    }

    .flex-value {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
</style>
