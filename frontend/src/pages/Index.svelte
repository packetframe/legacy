<script>
    import Button from "../components/Button.svelte";
    import {onMount} from "svelte";
    import {API} from "../stores";
    import Email from "../components/Email.svelte";
    // import EmailSignupForm from "../components/EmailSignupForm.svelte";

    let nodes, locations;

    onMount(() => {
        fetch($API + "counters")
            .then(response => response.json())
            .then(data => {
                nodes = data["message"]["nodes"]
                locations = data["message"]["locations"]
            })
    })

    let screenWidth;
</script>

<svelte:window bind:innerWidth={screenWidth} />

<main>
    <div class="wrapper">
        <header>
            <div class="containerStyle">
                <div style="width: clamp(0px, 950px, 95%)">
                    <div class="hero">
                        <img alt="PacketFrame Icon" src="/static/img/icon.png" style="width: 15rem; display: inline-block"/>
<!--                        <h1><span class="textGradient">PacketFrame CDN</span></h1>-->
                        <h1>Packetframe</h1>
                        <p>Welcome to Packetframe, the Open Source CDN for technology enthusiasts. The platform is currently in private beta, contact <Email/> for more information.</p>
                        <Button inverted onclick={() => window.location.hash = "#/dashboard"} size="1.2rem">Get Started</Button>
                    </div>
                </div>
            </div>
        </header>
        <div class="featureBlock">
            <div class="featureImageWrapper">
                <img alt="code" class="featureImage" src="/static/img/main/code.svg"/>
            </div>
            <div class="featureCaption">
                <h1>Built for Developers</h1>
                <p>Packetframe was built with developers in mind. With the Packetframe CDN, the only thing kept private is <a href="https://packetframe.com/docs/privacy-policy">your data</a> and keys to the infrastructure. Everything else is open and accessible. All functionality of the platform is exposed via the <a href="https://packetframe.com/docs/api">API</a> and the entire codebase is <a href="https://github.com/packetframe/cdn">open source</a>.</p>
            </div>
        </div>

        <div class:shrink={screenWidth <= 950} style="width: clamp(0px, 950px, 95%); display: flex; height: 160px; flex-direction: column;">
            <div style="display: flex; width: 100%; height: 50%;">
                <div style="display: flex; flex-grow: 1; height: 100%;"></div>
                <div class:no-border={screenWidth <= 950} style="border-bottom: 1px solid white; border-right: 1px solid white; border-bottom-right-radius: .375rem; display: flex; flex-grow: 2; height: 100%;"></div>
                <div style="display: flex; flex-grow: 1; height: 100%;"></div>
            </div>
            <div style="display: flex; width: 100%; height: 50%;">
                <div style="display: flex; flex-grow: 1; height: 100%;"></div>
                <div class:no-border={screenWidth <= 950} style="border-top-left-radius: 0.375rem; margin-left: -.5rem; border-left: 1px solid white; border-top: 1px solid white; margin-right: 0.5rem; display: flex; flex-grow: 2; height: 100%;"></div>
                <div style="display: flex; flex-grow: 1; height: 100%;"></div>
            </div>
        </div>

        <div class="featureBlock featureBlockReverse">
            <div class="featureCaption">
                <h1>Globally Distributed</h1>
                <p>There are currently 41 PoPs across 38 cities and with a presence in all 6 consumer-inhabited continents. (If you know of a datacenter in Antarctica, let me know!)</p>
            </div>
            <div class="featureImageWrapper">
                <img alt="world" class="featureImage" src="/static/img/main/world.svg"/>
            </div>
        </div>

        <div class:shrink={screenWidth <= 950} style="width: clamp(0px, 950px, 95%); display: flex; height: 160px; flex-direction: column;">
            <div style="display: flex; width: 100%; height: 50%;">
                <div  style="display: flex; flex-grow: 1; height: 100%;"></div>
                <div class:no-border={screenWidth <= 950} style="margin-left: -.5rem; margin-right: .5rem; border-bottom: 1px solid white; border-left: 1px solid white; border-bottom-left-radius: .375rem; display: flex; flex-grow: 2; height: 100%;"></div>
                <div style="display: flex; flex-grow: 1; height: 100%;"></div>
            </div>
            <div style="display: flex; width: 100%; height: 50%;">
                <div style="display: flex; flex-grow: 1; height: 100%;"></div>
                <div class:no-border={screenWidth <= 950} style="border-top-right-radius: 0.375rem; border-right: 1px solid white; border-top: 1px solid white; display: flex; flex-grow: 2; height: 100%;"></div>
                <div style="display: flex; flex-grow: 1; height: 100%;"></div>
            </div>
        </div>

        <div class="featureBlock">
            <div class="featureImageWrapper">
                <img alt="community" class="featureImage" src="/static/img/main/community.svg"/>
            </div>
            <div class="featureCaption">
                <h1>Community Centric</h1>
                <p>While the code is written by one person (<a href="https://natesales.net">me!</a>), the open source community plays a huge role in the CDN infrastructure. Special thanks to <a href="https://fosshost.org">fosshost</a> for their support and partnership in the project. Want to get involved? Feel free to send an email to <Email/> or hop in #packetframe on <a href="https://freenode.net/kb/answer/chat">freenode</a> and ask away!</p>
            </div>
        </div>

<!--        <EmailSignupForm/>-->
    </div>
</main>

<style>
    main {
        line-height: 30px;
        padding-bottom: 30px;
    }

    header {
        margin-bottom: 80px;
    }
    
    .no-border {
        border: none !important;
    }

    .shrink {
        height: 50px !important;
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
        margin-top: 0px;
        flex-wrap: wrap;
        width: clamp(0px, 950px, 95%);
        margin-left: auto;
        margin-right: auto;
    }

    .featureBlock.featureBlockReverse {
        flex-wrap: wrap-reverse;
    }

    .featureCaption {
        width: clamp(0px, 500px, 95%);
        font-size: larger;
        margin-left: 20px;
        margin-right: 20px;
        display: inline-flex;
        flex-direction: column;
        height: auto;
        background-color: black;
        background-clip: padding-box;
        border: solid 3px transparent; 
        position: relative;
        box-sizing: border-box;
        border-radius: 0.375rem;
        flex-grow: 1;
        justify-self: start;
        padding: 0px 20px;
        justify-content: center;
    }

    .featureCaption p {
        margin-top: 0px;
    }

    .featureCaption::before {
        content: '';
        position: absolute;
        top: 0; right: 0; bottom: 0; left: 0;
        z-index: -1;
        margin: -3px; 
        border-radius: inherit;
        background: linear-gradient(90deg, rgba(153,109,224,1) 0%, rgba(255,255,255,1) 100%);
    }

    .featureImageWrapper {
        display: flex;
        flex-grow: 1;
        width: min(50%, 350px);
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
    }

    .featureImage {
        width: min(100%, 300px);
        margin: 0px;
    }

    /* .textGradient {
        background: linear-gradient(90deg, rgba(255, 164, 252, 1) 0%, rgba(148, 98, 228, 1) 52%, rgba(103, 34, 212, 1) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    } */

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
