import Layout from '@theme/Layout';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import React, { useState, useEffect } from 'react';

function Home() {
    const context = useDocusaurusContext();
    const {siteConfig = {}} = context;

    const [nodes, setNodes] = useState("∞");
    const [locations, setLocations] = useState("∞");

    useEffect(() => {
        fetch("https://dash.delivr.dev/api/counters")
            .then(response => response.json())
            .then(data => {
                setNodes(data["message"]["nodes"]);
                setLocations(data["message"]["locations"]);
            })
    });

    const containerStyle = {
        margin: "auto",
        display: "flex",
        "justify-content": "center",
        "align-items": "center",
        "margin-top": "50px",
        "box-sizing": "unset",
        "flex-wrap": "wrap",
    }

    const featureBlock = {
        "display": "flex",
        "justify-content": "center",
        "align-items": "center",
        "margin-top": "85px",
        "flex-wrap": "wrap",
        "width": "50%",
        "margin-left": "auto",
        "margin-right": "auto"
    }

    const featureCaption = {
        "margin-left": "3em",
        "margin-right": "3em",
        "width": "25vw",
        "font-size": "larger"
    }

    const featureImage = {
        "width": "17vw",
    }

    return (
        <Layout
            title={`${siteConfig.title}`}
            description="The open source CDN for technology enthusiasts.">
            <header>
                <br/>
                <div style={containerStyle}>
                    <div style={{"padding-bottom": "25px"}}>
                        <div className="container" style={{"text-align": "center"}}>
                            <h1 className="hero__title">{siteConfig.title}</h1>
                            <p className="hero__subtitle">Welcome to delivr.dev, the Open Source CDN for technology enthusiasts.<br/>The platform is currently in private beta, contact <span style={{"unicode-bidi": "bidi-override", direction: "rtl"}}>ved.rviled@ofni</span> for more information!</p>
                            <a className="button button--outline button--secondary button--lg" href="https://dash.delivr.dev/">Get Started</a>
                        </div>
                    </div>

                    <div>
                        <img src="https://dash.delivr.dev/favicon-noborder.png" alt="delivr.dev" style={{"width": "350px"}}/>
                    </div>
                </div>
            </header>
            {/*HEX IS #6D2BD8*/}
            <div style={featureBlock}>
                <img style={featureImage} src="/img/main/code.svg" alt="code image"/>
                <div style={featureCaption}>
                    <h1>Built for Developers</h1>
                    <p>delivr.dev was built with developers in mind. With delivr.dev, the only thing kept private is <a href="https://delivr.dev/docs/privacy-policy">your data</a> and keys to the infrastructure. Every function of the dashboard is exposed via the <a href="https://delivr.dev/docs/api">API</a> and the entire codebase is <a href="https://github.com/natesales/delivr">open source</a>.</p>
                </div>
            </div>

            <div style={featureBlock}>
                <div style={featureCaption}>
                    <h1>Globally Distributed</h1>
                    <p>There are currently {nodes} PoPs across {locations} cities and with a presence in all 6 consumer-inhabited continents. (If you know of a datacenter in Antarctica, let me know!)</p>
                </div>
                <img style={featureImage} src="/img/main/world.svg" alt="world image"/>
            </div>

            <div style={featureBlock}>
                <img style={featureImage} src="/img/main/community.svg" alt="community image"/>
                <div style={featureCaption}>
                    <h1>Community Centric</h1>
                    <p>While the code is written by one person (<a href="https://natesales.net">me!</a>), the open source community plays a huge role in the CDN infrastructure. Special thanks to <a href="https://fosshost.org">fosshost</a> for their support and partnership in the project. Want to get involved? Feel free to send an email to <span style={{"unicode-bidi": "bidi-override", direction: "rtl"}}>ved.rviled@ofni</span> or hop in #delivr on <a href="https://freenode.net/kb/answer/chat">freenode</a> and ask away!</p>
                </div>
            </div>

            <footer style={{"text-align": "center", "margin-top": "15px"}}>
                <p>&copy; 2020 Nathan Sales.</p>
            </footer>
        </Layout>
    );
}

export default Home;
