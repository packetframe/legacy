<script>
    import Button from "./Button.svelte";
    import TextInput from "./TextInput.svelte";

    let username, password;
</script>

<main>
    <div class="title">Login</div>
    <div class="container">
        <div class="form-element">
            <TextInput placeholder="Username"/>
        </div>

        <div class="form-element">
            <TextInput placeholder="Password"/>
        </div>

        <div class="form-element">
            <Button inverted centered>Login</Button>
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
