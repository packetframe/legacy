<script>
    import TextInput from "./TextInput.svelte";
    import Button from "./Button.svelte";
    import {onMount} from "svelte";
    import {addSnackbar} from "../utils";

    let acl, address, password, password_confirm;


    function loadAcl() {
        fetch("https://dash.delivr.dev/api/user/acl", {
            credentials: "include"
        })
            .then(response => response.json())
            .then(data => {
                if (data["success"]) {
                    acl = data["message"]
                } else {
                    addSnackbar("get_acl", data["message"], data["success"] ? "green" : "red")
                }
            })
    }

    function appendAcl() {
        fetch("https://dash.delivr.dev/api/user/acl", {
            credentials: "include",
            method: "PUT",
            body: JSON.stringify({
                "address": address,
            }),
            headers: {
                "Content-Type": "application/json",
            }
        })
            .then(response => response.json())
            .then(data => {
                addSnackbar("append_acl", data["message"], data["success"] ? "green" : "red")
                loadAcl();
            })
    }

    function changePassword() {
        if (password !== password_confirm) {
            addSnackbar("change_password", "Passwords don't match", "red")
        } else {
            fetch("https://dash.delivr.dev/api/user/change_password", {
                credentials: "include",
                method: "POST",
                body: JSON.stringify({
                    "password": password,
                })
            })
                .then(response => response.json())
                .then(data => {
                    addSnackbar("change_password", data["message"], data["success"] ? "green" : "red")
                })
        }
    }

    onMount(() => loadAcl());
</script>

<main>
    <div class="flex-item">
        <h2>User Settings <span style="font-weight: lighter; font-size: 0.75em">for nate@delivr.dev</span></h2>

        <div class="container">
            <TextInput password placeholder="Password" tbpadded bind:content={password}/>
            <TextInput password placeholder="Repeat Password" tbpadded bind:content={password_confirm}/>
            <Button icon="check" inverted tbpadded onclick={() => changePassword()}>Submit</Button>
        </div>
    </div>

    <div class="flex-item">
        <h2>ACL Settings</h2>
        <div class="container">
            {#if acl && acl.length > 0}
                <ul>
                    {#each acl as rule, i }
                        <li>{rule}</li>
                    {/each}
                </ul>
            {:else}
                <p>No ACL rules defined</p>
            {/if}

            <TextInput placeholder="Add ACL rule (CIDR notation)" tbpadded bind:content={address}/>
            <Button icon="check" inverted tbpadded onclick={() => appendAcl()}>Submit</Button>
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

