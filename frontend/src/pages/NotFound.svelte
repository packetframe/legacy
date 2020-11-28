<main>
    <h1>Error 404</h1>
    <h2>Not Found</h2>
    <div class="container">
        <div class="figure-element">
            <img alt="User" class="image" src="/static/img/laptop.png">
            <div class="text-container">
                <p>Browser</p>
                <img alt="" class="icon" src="/static/img/cross.png">
            </div>
        </div>

        <div class="figure-element">
            <img alt="PacketFrame" class="image" src="/static/img/icon.png">
            <div class="text-container">
                <p>PacketFrame</p>
                <img alt="" class="icon" src="/static/img/check.png">
            </div>
        </div>
    </div>
</main>

<style>
    .container {
        display: flex;
        justify-content: space-evenly;
        align-items: center;
        flex-wrap: wrap;
        width: 30%;
        margin: auto;
    }

    h1 {
        text-align: center;
        font-size: 3em;
    }

    h2 {
        text-align: center;
    }

    .figure-element {
        text-align: center;
        margin-top: 15px;
        font-size: 1.25em;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        flex-grow: 1;
    }

    .figure-element .image {
        width: 200px;
    }

    .icon {
        height: 50px;
        width: 50px;
    }

    .text-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        flex-grow: 1;
    }
</style>
