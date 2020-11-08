<script>
    import TextInput from "./TextInput.svelte";
    import Button from "./Button.svelte";
    import {onMount} from "svelte";
    import {addSnackbar} from "../utils";

    let acl;

    function loadAcl() {
        fetch("https://dash.delivr.dev/api/user/acl", {
            credentials: "include"
        })
            .then(response => response.json())
            .then(data => {
                addSnackbar("get_acl", data["message"], data["success"] ? "green" : "red")
                if (data["success"]) {
                    acl = data["message"]
                }
            })
    }

    function appendAcl() {
        fetch("https://dash.delivr.dev/api/user/acl", {
            credentials: "include",
            method: "PUT"
        })
            .then(response => response.json())
            .then(data => {
                addSnackbar("append_acl", data["message"], data["success"] ? "green" : "red")
                loadAcl();
            })
    }

    onMount(() => loadAcl());
</script>

<main>
    <div class="flex-item">
        <h2>User Settings <span style="font-weight: lighter; font-size: 0.75em">for nate@delivr.dev</span></h2>

        <div class="container">
            <TextInput password placeholder="Password" tbpadded/>
            <TextInput password placeholder="Repeat Password" tbpadded/>
            <Button icon="check" inverted tbpadded>Submit</Button>
        </div>
    </div>

    <div class="flex-item">
        <h2>ACL Settings</h2>
        <div class="container">
            {#if acl}
                <ul>
                    {#each acl as rule, i }
                        <li>{rule}</li>
                    {/each}
                </ul>
            {:else}
                <p>Loading...</p>
            {/if}

            <TextInput password placeholder="Add ACL rule (CIDR notation)" tbpadded/>
            <Button icon="check" inverted tbpadded onclick="appendAcl()">Submit</Button>
        </div>
    </div>
</main>

<style>
    main {
        border: 2px solid white;
        border-radius: 15px;
        padding-bottom: 10px;
        margin-bottom: 15px;
        display: flex;
    }

    .flex-item {
        width: 40%;
        margin-right: 20px;
        margin-left: 15px;
        padding-bottom: 25px;
    }

    .container {
        display: flex;
        flex-direction: column;
        flex-wrap: wrap;
    }
</style>
