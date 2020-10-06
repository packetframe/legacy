<script>
    import Button from "./Button.svelte";
    import TextInput from "./TextInput.svelte";

    let username, password;

    function submitLogin() {
        fetch("http://localhost/api/auth/login", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                username: username,
                password: password
            })
        })
            .then(response => response.json())
            .then(data => alert(data["message"]));
    }
</script>

<main>
    <div class="title">Login</div>
    <div class="container">
        <div class="form-element">
            <TextInput placeholder="Username" bind:content={username}/>
        </div>

        <div class="form-element">
            <TextInput password placeholder="Password" bind:content={password}/>
        </div>

        <div class="form-element">
            <Button centered inverted onclick={() => submitLogin()}>Login</Button>
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
