<script>
    import Button from './Button.svelte'
    import TextInput from "./TextInput.svelte";
    import Dropdown from "./Dropdown.svelte";
    import {onMount} from "svelte";
    import Snackbar from "./Snackbar.svelte";

    let showAddRecord = true;

    export let zone;
    let records;

    let type, label, value;
    type = "A";

    let snackbarEnabled = false;
    let snackbarColor = "green";
    let snackbarMessage = "";
    let snackbarTitle = "";

    function toggleForm() {
        showAddRecord = !showAddRecord;
    }

    function submitForm() {
        fetch("http://localhost/api/zone/" + zone + "/add", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                type: type,
                label: label,
                value: value,
                ttl: 3600
            })
        })
            .then((response) => response.json())
            .then((data) => {
                snackbarColor = data["success"] ? "green" : "red";
                snackbarMessage = data["message"];
                snackbarEnabled = true;
            })
            .then(() => loadRecords());
    }

    function deleteRecord(index) {
        fetch("http://localhost/api/zone/" + zone + "/delete_record/" + index, {
            method: "POST"
        }).then(() => loadRecords());
    }

    function loadRecords() {
        fetch("http://localhost/api/zone/" + zone + "/records")
            .then(response => response.json())
            .then(data => {
                records = data["message"];
            });
    }

    onMount(() => loadRecords());
</script>

<main>
    <div class="header-container">
        <div>
            <h2>Records</h2>
            <span>
                <Button icon="add" inverted=true onclick={() => toggleForm()} size="1rem">Add Record</Button>
            </span>
        </div>

        {#if showAddRecord}
            <div class="record-add-container">
                <div class="record-add-element">
                    <Dropdown id="add-type" bind:content={type}>
                        <option value="A">A</option>
                        <option value="AAAA">AAAA</option>
                    </Dropdown>
                </div>

                <div class="record-add-element">
                    <TextInput placeholder="Label" id="add-label" bind:content={label}/>
                </div>

                <div class="record-add-element">
                    <TextInput placeholder="Value" id="add-value" bind:content={value}/>
                </div>

                <div class="record-add-element">
                    <Button icon="check" onclick={() => submitForm()}>Submit</Button>
                </div>
            </div>

        {/if}
    </div>

    <table class="sethjs-table">
        <tr>
            <th>Label</th>
            <th>Type</th>
            <th>TTL</th>
            <th>Value</th>
            <th></th>
        </tr>

        {#if records}
            {#each records as record, i }
                <tr>
                    <td>{record["label"]}</td>
                    <td>{record["type"]}</td>
                    <td>{record["ttl"]}</td>
                    <td>{record["value"]}</td>
                    <td style="padding-right: 0">
                        <Button color="red" icon="delete" size="1.25rem" onclick={() => {deleteRecord(i)}}/>
                    </td>
                </tr>
            {/each}
        {:else}
            <p style="padding-left: 10px">Loading...</p>
        {/if}
    </table>

    <Snackbar
            open={snackbarEnabled}
            color={snackbarColor}
            handleClose={() => {snackbarEnabled = false}}
            message={snackbarMessage}
            status={snackbarTitle}
    />
</main>

<style>
    main {
        margin: auto;
        border: 2px solid white;
        border-radius: 15px;
        padding-bottom: 10px;
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
        width: clamp(0%, 750px, 95%);
        align-content: center;
        flex-wrap: wrap;
        margin: 5px 8px 20px;
    }

    .record-add-element {
        flex-grow: 1;
        display: flex;
        flex-direction: column;
        margin: 5px;
        justify-content: center;
    }
</style>
