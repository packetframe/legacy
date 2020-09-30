<script>
    import Button from './Button.svelte'
    import TextInput from "./TextInput.svelte";
    import Dropdown from "./Dropdown.svelte";
    import {onMount} from "svelte";

    let showAddRecord = true;

    let zone = document.location.toString().split('=')[1];
    let records;

    let type, label, value;
    type = "A"

    function toggleForm() {
        showAddRecord = !showAddRecord;
    }

    function submitForm() {
        fetch("http://localhost/api/zone/" + zone + "/add", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                type: type,
                label: label,
                value: value,
                ttl: 13336
            })
        }).then(data => console.log(data));
        loadRecords();
    }

    function deleteRecord(index) {
        fetch("http://localhost/api/zone/" + zone + "/delete_record/" + index, {
            method: "POST"
        })

        loadRecords();
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
                <Button icon="add" inverted=true size="1rem" onclick={() => toggleForm()}>Add Record</Button>
            </span>
        </div>

        {#if showAddRecord}
            <table class="record-add-form">
                <tr>
                    <th>Type</th>
                    <th>Label</th>
                    <th>Value</th>
                    <th></th>
                </tr>
                <tr>
                    <td>
                        <Dropdown id="add-type" bind:content={type}>
                            <option value="A">A</option>
                            <option value="AAAA">AAAA</option>
                        </Dropdown>
                    </td>
                    <td>
                        <TextInput placeholder="Label" id="add-label" bind:content={label}/>
                    </td>
                    <td>
                        <TextInput placeholder="Value" id="add-value" bind:content={value}/>
                    </td>
                    <td style="padding-left:15px">
                        <Button icon="check" onclick={() => submitForm()}>Submit</Button>
                    </td>
                </tr>
            </table>
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
                    <td style="padding-right: 0px">
                        <Button color="red" icon="delete" size="1.25rem" onclick={() => {deleteRecord(i)}}/>
                    </td>
                </tr>
            {/each}
        {:else}
            <p style="padding-left: 10px">Loading...</p>
        {/if}
    </table>
</main>

<style>
    main {
        width: 95%;
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
        margin: 10px 10px 10px 20px;
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
        margin: 0px;
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

    .record-add-form {
        margin-left: 19px;
        margin-bottom: 20px;
    }

    .record-add-form th {
        text-align: left;
        padding-bottom: 10px;
        padding-left: 3px;
    }

    option {
        width: 125px;
    }
</style>
