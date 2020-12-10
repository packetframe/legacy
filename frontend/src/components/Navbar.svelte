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
        <a href="/#/dashboard">Dashboard</a>
        <a href="/#/community">Community</a>
        <a href="/#/network">Network</a>
        <a href="/#/docs">Docs</a>
        {#if $location === "/dashboard"}
            <a href="#" on:click={() => logout()}>Logout</>
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

    .right a {
        padding: 0px 0px 4px;
        margin: 0px 10px;
        border-bottom: 1px solid white;
    }

    .right a {
        transition: ease color 0.4s, ease border-bottom 0.2s, ease padding-top 0.2s;
    }

    .right a:hover {
        color: #996de0;
        border-bottom: 4px solid white;
        padding-top: 3px;
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
    }
</style>
