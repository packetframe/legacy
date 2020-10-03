<script defer>
    import L from 'leaflet';
    import {onMount} from "svelte";

    onMount(() => {
        let mymap = L.map("netmap").setView([51.505, -0.09], 13);

        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
            maxZoom: 18,
            id: 'mapbox/streets-v11',
            tileSize: 512,
            zoomOffset: -1
        }).addTo(mymap);
        mymap.setView([50, -25], 1.5);

        fetch("http://localhost/api/nodes/list")
            .then(response => response.json())
            .then((data) => {
                const nodes = data["message"];
                for (const i in nodes) {
                    const lat = nodes[i]["geoloc"].split(", ")[0];
                    const lon = nodes[i]["geoloc"].split(", ")[1];
                    L.marker([lat, lon])
                        .addTo(mymap)
                        .bindPopup("<b>" + nodes[i]["name"] + "</b><br>" + nodes[i]["location"] + "<br>" + nodes[i]["provider"])
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
