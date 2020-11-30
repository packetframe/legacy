<script>
    import Button from "./Button.svelte";
    import TextInput from "./TextInput.svelte";
    import {addSnackbar} from "../utils";
    import {API} from "../stores";

    export let type;

    let username, password, message;

    function submitForm() {
        fetch($API + "auth/" + type, {
            method: "POST",
            credentials: "include",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                username: username,
                password: password,
                message: message
            })
        })
            .then(response => response.json())
            .then(data => {
                if (!data["success"]) {
                    addSnackbar(type.charAt(0).toUpperCase() + type.slice(1), data["message"], data["success"] ? "green" : "red");
                } else {
                    if (type === "login") {
                        window.location.hash = "#/dashboard";
                    } else {
                        window.location.hash = "#/login";
                    }
                }
            });
    }
</script>

<main>
    <form on:submit|preventDefault={submitForm}>
        <div class="title">{type.charAt(0).toUpperCase() + type.slice(1)}</div>
        <div class="container">
            <div class="form-element">
                <TextInput bind:content={username} placeholder="Email"/>
            </div>

            <div class="form-element">
                <TextInput bind:content={password} password placeholder="Password"/>
            </div>

            {#if type === "signup"}
                <div class="form-element">
                    <TextInput bind:content={message} placeholder="How did you hear about PacketFrame?"/>
                </div>
            {/if}

            <div class="form-element">
                <Button type="submit" centered>{type.charAt(0).toUpperCase() + type.slice(1)}</Button>
            </div>
        </div>
    </form>
</main>

<style>
    main {
        border: 2px solid white;
        border-radius: 15px;
        width: 450px;
        margin: auto;
        flex-direction: column;
    }

    .title {
        font-size: 20px;
        text-align: center;
        margin-top: 25px;
    }

    .container {
        color: #ffff;
        padding: 25px 25px 0;
        border-radius: 3px;
    }

    .form-element {
        padding-bottom: 20px;
    }
</style>
