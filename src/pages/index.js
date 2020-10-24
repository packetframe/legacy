import React from 'react';
import clsx from 'clsx';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import useBaseUrl from '@docusaurus/useBaseUrl';
import styles from './styles.module.css';

function Home() {
    const context = useDocusaurusContext();
    const {siteConfig = {}} = context;
    return (
        <Layout
            title={`${siteConfig.title}`}
            description="Description will go into a meta tag in <head />">
            <header>
                <br/>
                <div style={{textAlign: "center"}}>
                    <div className="container">
                        <h1 className="hero__title">{siteConfig.title}</h1>
                        {/*<p className="hero__subtitle">{siteConfig.tagline}</p>*/}
                        <p className="hero__subtitle">DELIVR.DEV is currently in private beta. Contact {atob("aW5mb0BkZWxpdnIuZGV2Cg==")} for more information.</p>
                        <div className={styles.buttons}>
                            <Link
                                className={clsx(
                                    'button button--outline button--secondary button--lg',
                                    styles.getStarted,
                                )}
                                to={useBaseUrl('https://dash.delivr.dev/')}>
                                Get Started
                            </Link>
                        </div>
                    </div>
                </div>
            </header>
        </Layout>
    );
}

export default Home;
