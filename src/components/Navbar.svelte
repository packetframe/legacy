<style>
    main {
        width: 100%;
        background: #1c1c1c;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 35px;
    }
    div {
        margin: 15px;
        display: flex;
        max-height: 100%;
        align-items: center;
        cursor: pointer;
    }
</style>

<main>
    <div>
        <slot name="left-side"></slot>
    </div>
    <div>
        <slot name="right-side"></slot>
    </div>
</main>