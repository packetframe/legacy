<script>
    import {API} from "../stores";
    import {location} from 'svelte-spa-router'

    function logout() {
        fetch($API + "auth/logout", {
            credentials: "include",
            method: "POST"
        }).then(() => window.location = "/")
    }

    let screenWidth;
    let menuOpen = false;

    $: if (screenWidth > 820 && menuOpen) {
        menuChange();
    }

    const menuChange = () => {
            menuOpen = !menuOpen;
            if (menuOpen && screenWidth <= 820) {
                document.body.style.setProperty('height', '100vh');
                document.body.style.setProperty('overflow', 'hidden');
            } else {
                document.body.style.removeProperty('height');
                document.body.style.removeProperty('overflow');
            }
    }

</script>

<svelte:window bind:innerWidth={screenWidth} />

<main class:open={menuOpen} class:condensed={screenWidth <= 820}>
    <div class="condensed-container" class:condensed={screenWidth <= 820}>
        <div class="left">
            <a href="/#/"><img alt="Logo" src="/static/img/logo.png" style="width: min(20rem, calc(100% - 50px));"></a>
        </div>
        {#if screenWidth <= 820}
            <span class="material-icons right" on:click={menuChange}>
                {menuOpen ? 'close' : 'menu'}
            </span>
        {/if}
    </div>
    <div class="right" class:condensed={screenWidth <= 820} class:open={menuOpen}>
        <a on:click={menuChange} href="/#/dashboard">Dashboard</a>
        <a on:click={menuChange} href="/#/community">Community</a>
        <a on:click={menuChange} href="/#/docs">Docs</a>
        {#if $location === "/dashboard"}
            <a href="#" on:click={() => logout()}>Logout</a>
        {:else}
            <a on:click={menuChange} href="/#/signup">Signup</a>
            <a on:click={menuChange} href="/#/login">Login</a>
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
        position: relative;
        top: 0;
        left: 0;
    }

    main.open.condensed {
        flex-direction: column;
        height: 100vh;
    }

    a {
        max-height: 100%;
        align-items: center;
        cursor: pointer;
    }

    .right.condensed {
        display: none;
        width: 100%;
        height: 0px;
        position: relative;
        top: 0;
        left: 0;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        background-color: black;
        z-index: 2000;
        padding-right: 0px;
    }

    .right.condensed.open {
        display: flex;
        height: 100%;
    }

    .right.condensed a {
        font-size: large;
        width: min(90%, 400px);
        text-align: center;
        padding: 20px 0px;
        border-bottom: 1px solid white;
    }

    .right.condensed a:hover {
        border-bottom: 1px solid #996de0;
        padding: 20px 0px;
        border-collapse: collapse;
    }

    .condensed-container {
        display: flex;
        justify-content: space-between;
    }

    .condensed-container.condensed {
        width: 100%;
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
