<script>
    import Email from "../components/Email.svelte";
</script>
<main>
    <div>
        <h1>Community</h1>
        <img alt="Together" src="/static/img/main/together.svg">
        <p>PacketFrame is fueled by the community. If you're interested in helping out or supporting the project in any way, contact <Email/></p>
    </div>

    <div class="items">
        <div class="item">
            <h3>Fosshost</h3>
            <p>The fosshost project is a non-profit organisation that exists to serve the hosting needs of the global open source community.</p>
        </div>
    </div>
</main>

<style>
    main {
        text-align: center;
        display: flex;
        justify-content: center;
        flex-direction: column;
    }

    img {
        width: 500px;
    }
</style>
