<script>
    import {Page} from "../stores.js";
</script>

<style>
    main {
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    div {
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

    .right div {
        padding-left: 5px;
        padding-right: 5px;
    }
</style>

<main>
    <div class="left">
        <img style="width: 20rem" alt="delivr.dev" on:click={() => {$Page = "index"}} src="/full.png">
    </div>
    <div class="right" style="display: flex;">
        {#if $Page === "dashboard"}
            <div class="nav-item" on:click={() => {
                        $Page = "login";
                        document.cookie = "";
                        location.hash = "";
                    }}>Logout
            </div>
        {:else}
            <div class="nav-item" on:click={() => {$Page = "signup"}}>Signup</div>
            <div class="nav-item" on:click={() => {$Page = "login"}}>Login</div>
        {/if}
    </div>
</main>