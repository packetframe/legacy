<script>
    import Button from './Button.svelte'

    export let title = "Table"
</script>

<main>
    <div>
        <h2>{title}</h2>
        <span>
            <slot name="header-button"></slot>
        </span>
    </div>

    <table class="sethjs-table">
        <slot></slot>
    </table>
</main>

<style>
    main {
        width: 95%;
        margin: auto;
        border: 2px solid white;
        border-radius: 15px;
        padding-bottom: 50px;
    }

    div {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    span {
        margin: 10px;
    }

    h2 {
        margin: 10px 10px 10px 20px;
    }

    :global(.sethjs-table) {
        width: 100%;
        border-collapse: collapse;
    }

    :global(.sethjs-table th) {
        padding-top: 16px;
        padding-bottom: 16px;
        padding-left: 20px;
        text-align: left;
        background-color: #202020;
        border-bottom: 1px solid #555555;
        color: white;
        margin: 0px;
    }

    :global(.sethjs-table tr) {
        width: 100%;
        width: 100%;
    }

    :global(.sethjs-table tr:nth-child(odd)) {
        background-color: #111111;
    }

    :global(.sethjs-table td) {
        padding-top: 15px;
        padding-bottom: 15px;
        padding-left: 20px;
        text-align: left;
    }
</style>
