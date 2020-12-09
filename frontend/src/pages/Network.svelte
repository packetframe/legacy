<script>
    import {onMount} from "svelte";

    let globe = new ENCOM.Globe(window.innerWidth, window.innerHeight - (document.getElementsByTagName("main")[0].clientTop + document.getElementsByTagName("main")[0].clientHeight), {
        font: "Segoe UI",
        data: [],
        tiles: grid.tiles,
        baseColor: "#dd00ff",
        markerColor: "#8e44ad",
        pinColor: "#aacfd1",
        satelliteColor: "#aacfd1",
        scale: 0.9,
        dayLength: 28000,
        introLinesDuration: 2000,
        maxPins: 100,
        maxMarkers: 100,
        viewAngle: 0.75
    });

    onMount(() => {
        document.getElementById("globe").prepend(globe.domElement);

        setTimeout(() => {
            initGlobe();
        }, 100);
    });

    function onWindowResize(){
        globe.camera.aspect = window.innerWidth / window.innerHeight;
        globe.camera.updateProjectionMatrix();
        globe.renderer.setSize(window.innerWidth, window.innerHeight);
    }

    window.addEventListener( 'resize', onWindowResize, false );

    function animate() {
        if (globe) globe.tick();
        requestAnimationFrame(animate);
    }

    function initGlobe() {
        globe.init();
        animate();

        fetch("https://packetframe.com/api/nodes/geoloc")
            .then(response => response.json())
            .then(data => {
                nodes = data["message"];
                for (const name in data["message"]) {
                const lat = parseFloat(data["message"][name].split(", ")[0]);
                const lon = parseFloat(data["message"][name].split(", ")[1]);

                if (name.length <= 3) {
                    let altitude = 1.1 + .2 * Math.random();
                    globe.addPin(lat, lon, "", altitude + .1);
                    globe.addMarker(lat, lon, name, altitude, false);
                }
                // console.log("Added " + name + " " + lat + ", " + lon);
                }
            })
    }
</script>


<style>
    * {
        margin: 0;
    }

    #globe {
        z-index: -5;
    }

    .overlay {
        position: absolute;
        left: 35px;
        top: 170px;
    }
    
    h1 {
        text-decoration: underline;
    }

    p {
        margin-top: 15px;
    }
</style>


<main>
    <div id="globe"></div>
    <div class="overlay">
        <h1>PacketFrame Network</h1>
        <p>PacketFrame uses <a href="https://natesales.net/network">AS34553</a> for network operations. All AS34553 PoPs have CDN presence and direct peering is available at most locations.</p>
    </div>
</main>
