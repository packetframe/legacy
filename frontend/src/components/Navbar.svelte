<style>
    main {
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 20px;
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
</style>

<main>
    <div class="left">
        <slot name="left-side"></slot>
    </div>
    <div class="right">
        <slot name="right-side"></slot>
    </div>
</main>