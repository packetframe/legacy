<script defer>
    import L from 'leaflet';
    import {onMount} from "svelte";
    import {addSnackbar} from "../utils";
    import {SnackBars} from "../stores";

    export let admin = false;

    onMount(() => {
        let mymap = L.map("netmap").setView([51.505, -0.09], 13);
        mymap.setView([50, -25], 1.5);

        let NASAGIBS_ViirsEarthAtNight2012 = L.tileLayer('https://map1.vis.earthdata.nasa.gov/wmts-webmerc/VIIRS_CityLights_2012/default/{time}/{tilematrixset}{maxZoom}/{z}/{y}/{x}.{format}', {
            attribution: 'Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System (<a href="https://earthdata.nasa.gov">ESDIS</a>) with funding provided by NASA/HQ.',
            bounds: [[-85.0511287776, -179.999999975], [85.0511287776, 179.999999975]],
            minZoom: 1,
            maxZoom: 8,
            format: 'jpg',
            time: '',
            tilematrixset: 'GoogleMapsCompatible_Level'
        });

        let CartoDB_DarkMatter = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
            subdomains: 'abcd',
            maxZoom: 19
        });

        if (document.location.toString().split("?map=")[1] === "nasa") {
            NASAGIBS_ViirsEarthAtNight2012.addTo(mymap)
        } else {
            CartoDB_DarkMatter.addTo(mymap)
        }

        fetch("https://delivr.dev/api/nodes/list", {
            credentials: "include"
        })
            .then(response => response.json())
            .then((data) => {
                const nodes = data["message"];
                for (const i in nodes) {
                    const lat = nodes[i]["geoloc"].split(", ")[0];
                    const lon = nodes[i]["geoloc"].split(", ")[1];
                    if (admin) {
                        L.marker([lat, lon])
                            .addTo(mymap)
                            .bindPopup(`
                            <b>${nodes[i]["name"]}</b>
                            <br>
                            ${nodes[i]["location"]}
                            <br>
                            ${nodes[i]["provider"]}
                            <br>
                            ${nodes[i]["datacenter"]}
                            <br>
                            <a href='#' onclick='setNode("${nodes[i]["name"]}", "on")'>Start</a>
                            <a href='#' onclick='setNode("${nodes[i]["name"]}", "off")'>Stop</a>
                        `)
                    } else {
                        L.marker([lat, lon])
                            .addTo(mymap)
                            .bindPopup(`
                            <b>${nodes[i]["name"]}</b>
                            <br>
                            ${nodes[i]["location"]}
                            <br>
                            ${nodes[i]["provider"]}
                            <br>
                            ${nodes[i]["datacenter"]}
                        `)
                    }
                }
            })
    })
</script>

<main>
    <div id="netmap"></div>
</main>

<style>
    #netmap {
        height: 400px;
        border: 2px solid white;
        border-radius: 15px;
        margin-bottom: 15px;
    }
</style>

<link crossorigin="" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css"
      integrity="sha512-xodZBNTC5n17Xt2atTPuE1HxjVMSvLVW9ocqUKLsCC5CXdbqCmblAshOMAS6/keqq/sMZMZ19scR4PsZChSR7A=="
      rel="stylesheet"/>
