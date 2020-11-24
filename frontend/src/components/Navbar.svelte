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
        <a href="/"><img alt="delivr.dev" src="/full.png" style="width: 20rem"></a>
    </div>
    <div class="right" style="display: flex;">
        {#if $location === "/dashboard"}
            <div on:click={() => logout()}>Logout</div>
        {:else}
            <a class="nav-item" href="/#/signup">Signup</a>
            <a class="nav-item" href="/#/login">Login</a>
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
    }

    .right {
        padding-right: 35px;
    }

    .right a {
        color: white;
        text-decoration: none;
        padding-left: 5px;
        padding-right: 5px;
    }
</style>
