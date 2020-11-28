<script>
    import {API} from "../stores";
    import {location} from 'svelte-spa-router'

    function logout() {
        fetch($API + "auth/logout", {
            credentials: "include",
            method: "POST"
        }).then(() => window.location = "/")
    }
</script>

<main>
    <div class="left">
        <a href="/#/"><img alt="Logo" src="/static/img/logo.png" style="width: 20rem"></a>
    </div>
    <div class="right">
        <a href="/#/community">Community</a>
        <a href="/#/docs">Docs</a>
        {#if $location === "/dashboard"}
            <div on:click={() => logout()}>Logout</div>
        {:else}
            <a href="/#/signup">Signup</a>
            <a href="/#/login">Login</a>
        {/if}
    </div>
</main>

<style>
    main {
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: space-between;
        cursor: pointer;
    }

    a {
        max-height: 100%;
        align-items: center;
        cursor: pointer;
    }

    .left {
        padding-top: 12px;
        display: flex;
        align-items: center;
    }

    .right {
        padding-right: 35px;
        display: flex;
        align-items: center;
    }

    .right a, .left a {
        color: white;
        text-decoration: none;
        padding-left: 5px;
        padding-right: 5px;
    }
</style>
