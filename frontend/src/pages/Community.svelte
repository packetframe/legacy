<script>
    import Email from "../components/Email.svelte";
</script>
<main>
    <div class="header">
        <h1>Community</h1>
        <img alt="Together" src="/static/img/main/together.svg">
        <p>PacketFrame is fueled by the community. If you're interested in helping out or supporting the project in any way, contact <Email/>. The supporters below have been instrumental in providing infrastructure or other services to the project - huge thanks to all of the amazing supporters!</p>
    </div>

<!--    TODO: Better flex spacing -->

    <div class="grid">
        <div class="item">
            <div class="item-text">
                <a href="https://fosshost.org/">Fosshost</a>
                <p>The fosshost project is a non-profit organisation that exists to serve the hosting needs of the global open source community.</p>
            </div>
        </div>

        <div class="item">
            <div class="item-text">
                <a href="https://heficed.com/">Heficed</a>
                <p>Heficed provides full-range infrastructure services. Heficed serves around 60 multi-billion industries starting from hosting to automotive or healthcare. With more than a decade of industry experience and operations globally, Heficed can meet any demand needs.</p>
            </div>
        </div>

        <div class="item">
            <div class="item-text">
                <a href="https://terrahost.no/">Terrahost</a>
                <p>Our vision is to offer solutions of high quality at an affordable price. Our services are delivered from our own datacenter in Sandefjord. In that way we can ensure high stability and safety. We work around the clock to give you the best price and service on the market.</p>
            </div>
        </div>

        <div class="item">
            <div class="item-text">
                <a href="https://hostus.us/">HostUS</a>
                <p>We offer cPanel Web Hosting, Reseller Hosting, OpenVZ VPS, KVM VPS and Managed VPS in 10 datacenter locations across 4 continents. All backed by our amazing 24/7 support team.</p>
            </div>
        </div>

        <div class="item">
            <div class="item-text">
                <a href="https://mythic-beasts.com/">Mythic Beasts</a>
                <p>Mythic Beasts is a privately owned hosting ISP with a focus on a no-nonsense service backed by excellent technical support.</p>
            </div>
        </div>

        <div class="item">
            <div class="item-text">
                <a href="https://combahton.net/">Combahton</a>
                <p>We offer highly available dedicated servers, colocation, DDoS protection and managed services
                    based on fail-safe and certified infrastructure in Germany. We are also your reliable partner for server and network management.</p>
            </div>
        </div>

        <div class="item">
            <div class="item-text">
                <a href="https:/ifog.ch/">iFog</a>
                <p>iFog GmbH offers IT services. This includes Web Hosting, vServers, IXP Access as well as IP Transit and LIR Services.</p>
            </div>
        </div>

        <div class="item">
            <div class="item-text">
                <a href="https://vps66.cloud/">VPS66</a>
                <p>Virtual Private Servers and Colocation in the ♥ of Frankfurt am Main, Germany.</p>
            </div>
        </div>

        <div class="item">
            <div class="item-text">
                <a href="https://spartanhost.org/">SpartanHost</a>
                <p>The main goal of the company has always been to provide the best possible service and product at a price that is good value for money. We will continue to strive to meet this goal in the future as we expand our services and locations.</p>
            </div>
        </div>

        <div class="item">
            <div class="item-text">
                <a href="https://garanntor.com">Garanntor</a>
                <p>Garanntor is a privately owned company hosting and infrastructure-as-a-service company. Since our founding in 2016, Garanntor has continually innovated new ways to deliver on our mission: Making it Easy So You Can Focus on Growing Your Business. Based in Lagos, Nigeria. we pride ourselves in providing high quality services and support for each and every one of our clients.</p>
            </div>
        </div>

        <div class="item">
            <div class="item-text">
                <a href="https://xenspec.com/">XenSpec</a>
                <p>Chicago based VPS and Web Hosting provider. Offering custom infrastructure solutions with exceptional support</p>
            </div>
        </div>

        <div class="item">
            <div class="item-text">
                <a href="https://www.hivane.net">Hivane</a>
                <p>Hivane offers DNS / MX / WWW services to non-for-profit projects. Check out https://www.hivane.net/ for more information.</p>
            </div>
        </div>

        <div class="item">
            <div class="item-text">
                <a href="https://misaka.io/">Misaka Network</a>
                <p>Superb cloud infrastructure with low latency. All our services are carefully designed to provide high performance, reliable and scalable at a reasonably price.</p>
            </div>
        </div>
    </div>
</main>

<style>
    main {
        display: flex;
        justify-content: center;
        flex-direction: column;
    }

    .header {
        text-align: center;
    }

    img {
        width: 500px;
    }

    .grid {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
    }


    .item {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 85px;
        flex-wrap: wrap;
        width: clamp(0px, 950px, 95%);
        margin-left: auto;
        margin-right: auto;
    }

    .item img {
        width: min(50%, 350px);
        margin: 5px;
    }

    .item-text {
        width: clamp(0px, 500px, 95%);
        font-size: larger;
        margin-left: 30px;
        margin-right: 30px;
    }

    .item-text a {
        color: white;
        font-size: 1.3em;
    }

    p {
        width: clamp(0px, 500px, 95%);
    }

    .header {
        display: flex;
        align-items: center;
        flex-direction: column;
    }
</style>
