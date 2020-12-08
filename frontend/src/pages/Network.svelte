<script>
    import {onMount} from "svelte";

    let globe = new ENCOM.Globe(window.innerWidth, window.innerHeight - (document.getElementsByTagName("main")[0].clientTop + document.getElementsByTagName("main")[0].clientHeight), {
        font: "sans-serif",
        data: [],
        tiles: grid.tiles,
        baseColor: "#dd00ff",
        markerColor: "#8e44ad",
        pinColor: "#aacfd1",
        satelliteColor: "#aacfd1",
        scale: 0.9,
        dayLength: 14000,
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
    })

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
                for (const name in data["message"]) {
                    const lat = parseFloat(data["message"][name].split(", ")[0]);
                    const lon = parseFloat(data["message"][name].split(", ")[1]);
                    globe.addPin(lat, lon, "");
                    globe.addMarker(lat, lon, name, false);
//                    globe.addSatellite(lat, lon, 0, {coreColor: "#ffffff", numWaves: 3});
                    console.log("Added " + name + " " + lat + ", " + lon);
                }
            })
    }

    window.addEventListener('resize', () => {
        let height = window.innerHeight - (document.getElementsByTagName("main")[0].clientTop + document.getElementsByTagName("main")[0].clientHeight);
        globe.camera.aspect = window.innerWidth / height;
        globe.camera.updateProjectionMatrix();
        globe.renderer.setSize(window.innerWidth, height);
    });
</script>


<style>
    main {
        margin: 0;
    }
</style>


<main>
    <div id="globe"></div>
</main>
