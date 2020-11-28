import Layout from '@theme/Layout';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import React, {useEffect, useState} from 'react';

function Home() {
    const context = useDocusaurusContext();
    const {siteConfig = {}} = context;

    useEffect(() => {
        window.location = "https://dash.delivr.dev/"
        fetch("https://dash.delivr.dev/api/counters")
            .then(response => response.json())
            .then(data => {
                setNodes(data["message"]["nodes"]);
                setLocations(data["message"]["locations"]);
            })
    });

    return (
        <Layout
            title={`${siteConfig.title}`}
            description="The open source CDN for technology enthusiasts.">

            <h1>Looks like you're in the wrong place! You should be at https://dash.delivr.dev/</h1>

            <footer style={{"text-align": "center", "margin-top": "15px"}}>
                <p>&copy; 2020 Nathan Sales.</p>
            </footer>
        </Layout>
    );
}

export default Home;
