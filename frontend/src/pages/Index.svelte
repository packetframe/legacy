<script>
    import Button from "../components/Button.svelte";

    let nodes = 27;
    let locations = 22;
</script>

<main>
    <div class="wrapper">
        <header>
            <div class="containerStyle">
                <div style="width: clamp(0px, 950px, 95%)">
                    <div class="hero">
                        <img alt="PacketFrame Icon" src="/static/img/icon.png" style="width: 15rem; display: inline-block"/>
                        <h1><span class="textGradient">PacketFrame CDN</span></h1>
                        <p>Welcome to PacketFrame, the Open Source CDN for technology enthusiasts. The platform is currently in private beta, contact <span style="unicode-bidi: bidi-override; direction: rtl">moc.emarftekcap@ofni</span> for more information.</p>
                        <Button inverted onclick={() => window.location.hash = "#/dashboard"} size="1.2rem">Get Started</Button>
                    </div>
                </div>
            </div>
        </header>
        <div class="featureBlock">
            <img alt="code" class="featureImage" src="/static/img/main/code.svg"/>
            <div class="featureCaption">
                <h1>Built for Developers</h1>
                <p>PacketFrame was built with developers in mind. With the PacketFrame CDN, the only thing kept private is <a href="https://packetframe.com/docs/privacy-policy">your data</a> and keys to the infrastructure. Every function of the dashboard is exposed via the <a href="https://packetframe.com/docs/api">API</a> and the entire codebase is <a href="https://github.com/packetframe/cdn">open source</a>.</p>
            </div>
        </div>

        <div class="featureBlockReverse">
            <div class="featureCaption">
                <h1>Globally Distributed</h1>
                <p>There are currently {nodes} PoPs across {locations} cities and with a presence in all 6 consumer-inhabited continents. (If you know of a datacenter in Antarctica, let me know!)</p>
            </div>
            <img alt="world" class="featureImage" src="/static/img/main/world.svg"/>
        </div>

        <div class="featureBlock">
            <img alt="community" class="featureImage" src="/static/img/main/community.svg"/>
            <div class="featureCaption">
                <h1>Community Centric</h1>
                <p>While the code is written by one person (<a href="https://natesales.net">me!</a>), the open source community plays a huge role in the CDN infrastructure. Special thanks to <a href="https://fosshost.org">fosshost</a> for their support and partnership in the project. Want to get involved? Feel free to send an email to <span style="unicode-bidi: bidi-override; direction: rtl">moc.emarftekcap@ofni</span> or hop in #packetframe on <a href="https://freenode.net/kb/answer/chat">freenode</a> and ask away!</p>
            </div>
        </div>
    </div>
</main>

<style>
    main {
        line-height: 30px;
    }

    .featureBlock .featureBlockReverse h1 {
        font-size: 1.2em;
    }

    .containerStyle {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 50px auto auto;
        box-sizing: unset;
        flex-wrap: wrap-reverse;
    }

    .featureBlock {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 85px;
        flex-wrap: wrap;
        width: clamp(0px, 950px, 95%);
        margin-left: auto;
        margin-right: auto;
    }

    .featureBlockReverse {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 85px;
        flex-wrap: wrap-reverse;
        width: clamp(0px, 950px, 95%);
        margin-left: auto;
        margin-right: auto;
    }

    .featureCaption {
        width: clamp(0px, 500px, 95%);
        font-size: larger;
        margin-left: 30px;
        margin-right: 30px;
    }

    .featureImage {
        width: min(50%, 350px);
        margin: 5px;
    }

    .textGradient {
        background: linear-gradient(90deg, rgba(255, 164, 252, 1) 0%, rgba(148, 98, 228, 1) 52%, rgba(103, 34, 212, 1) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    a {
        color: #d000ff;
    }

    .hero {
        text-align: center;
        font-size: 1.5em;
        display: flex;
        align-items: center;
        flex-direction: column;
    }
</style>

<!--{/*HEX IS #6D2BD8*/}-->
