<script>
    import {fade} from 'svelte/transition';

    let shown = true;
</script>

<main>
    {#if shown}
        <div transition:fade>
            <span></span>
            <p><slot/></p>
            <span on:click={() => shown=false} class="material-icons">close</span>
        </div>
    {/if}
</main>

<style>
    div {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: auto;
        background-color: green;
        text-align: center;
    }

    span {
        margin: 20px;
        cursor: pointer;
    }
</style>
