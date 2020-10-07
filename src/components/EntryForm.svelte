<script>
    import Button from "./Button.svelte";
    import TextInput from "./TextInput.svelte";
    import {SnackBars} from "../stores";
    import {Page} from "../stores";
    import {addSnackbar} from "../utils";

    export let type;

    let username, password;

    function submitForm() {
        fetch("https://delivr.dev/api/auth/" + type, {
            method: "POST",
            credentials: "include",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                username: username,
                password: password
            })
        })
            .then(response => response.json())
            .then(data => {
                if (!data["success"]) {
                    addSnackbar(type.charAt(0).toUpperCase() + type.slice(1), data["message"], data["success"] ? "green" : "red");
                } else {
                    if (type === "login") {
                        Page.set("dashboard");
                    } else {
                        Page.set("login");
                    }
                }
            });
    }
</script>

<main>
    <div class="title">{type.charAt(0).toUpperCase() + type.slice(1)}</div>
    <div class="container">
        <div class="form-element">
            <TextInput bind:content={username} placeholder="Username"/>
        </div>

        <div class="form-element">
            <TextInput bind:content={password} password placeholder="Password"/>
        </div>

        <div class="form-element">
            <Button centered inverted onclick={() => submitForm()}>{type.charAt(0).toUpperCase() + type.slice(1)}</Button>
        </div>
    </div>
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
