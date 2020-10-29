<script>
    import {onMount} from "svelte";
    import Button from "./Button.svelte";
    import {addSnackbar} from '../utils'

    let users;

    function getUsers() {
        fetch("https://dash.delivr.dev/api/users", {
            credentials: "include"
        })
            .then(response => response.json())
            .then(data => {
                users = data["message"]
            })
    }

    onMount(() => getUsers());

    function toggleState(user) {
        fetch("https://dash.delivr.dev/api/user/" + user + "/toggle", {
            credentials: "include"
        })
            .then(response => response.json())
            .then((data) => {
                addSnackbar("user_toggle", data["message"], data["success"] ? "green" : "red")
                getUsers()
            })
    }
</script>

<main>
    <div class="table-wrapper">
        <table class="sethjs-table">
            <tr>
                <th>Email</th>
                <th></th>
                <th></th>
            </tr>

            {#if users}
                {#each users as user, i }
                    <tr>
                        <td>{user["username"]}</td>
                        <td>
                            {#if user["enabled"]}
                                <Button icon="check_circle" onclick={() => toggleState(user["username"])}>Enabled</Button>
                            {:else}
                                <Button icon="not_interested" onclick={() => toggleState(user["username"])}>Disabled</Button>
                            {/if}
                        </td>

                        <td>
                            {#if user["admin"]}
                                <Button disabled icon="verified_user">Admin</Button>
                            {/if}
                        </td>
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
        border: 2px solid white;
        border-radius: 15px;
        padding-top: 10px;
        padding-bottom: 10px;
        margin: 15px auto;
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

    .table-wrapper {
        overflow-x: auto;
        width: 100%;
    }
</style>
