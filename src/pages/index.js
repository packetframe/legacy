import React from 'react';
import clsx from 'clsx';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import useBaseUrl from '@docusaurus/useBaseUrl';
import styles from './styles.module.css';

const features = [
    // {
    //     title: 'Easy to Use',
    //     imageUrl: 'img/undraw_docusaurus_mountain.svg',
    //     description: (
    //         <>
    //             Docusaurus was designed from the ground up to be easily installed and
    //             used to get your website up and running quickly.
    //         </>
    //     ),
    // },
    // {
    //     title: 'Simple and Automatable',
    //     imageUrl: 'img/undraw_docusaurus_tree.svg',
    //     description: (
    //         <>
    //             delivr.dev can be controlled with the dashboard or API.
    //         </>
    //     ),
    // },
    // {
    //     title: 'Fully Open Source',
    //     imageUrl: 'img/undraw_docusaurus_react.svg',
    //     description: (
    //         <>
    //             delivr.dev is fully open source, including third party components such as Caddy, Varnish, and BIRD.
    //         </>
    //     ),
    // },
];

function Feature({imageUrl, title, description}) {
    const imgUrl = useBaseUrl(imageUrl);
    return (
        <div className={clsx('col col--4', styles.feature)}>
            {imgUrl && (
                <div className="text--center">
                    <img className={styles.featureImage} src={imgUrl} alt={title}/>
                </div>
            )}
            <h3>{title}</h3>
            <p>{description}</p>
        </div>
    );
}

function Home() {
    const context = useDocusaurusContext();
    const {siteConfig = {}} = context;
    return (
        <Layout
            title={`${siteConfig.title}`}
            description="Description will go into a meta tag in <head />">
            <header>
                <br/>
                {/*TODO: Center align this*/}
                <div>
                    <div className="container">
                        <h1 className="hero__title">{siteConfig.title}</h1>
                        <p className="hero__subtitle">{siteConfig.tagline}</p>
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
            <main>
                {features && features.length > 0 && (
                    <section className={styles.features}>
                        <div className="container">
                            <div className="row">
                                {features.map((props, idx) => (
                                    <Feature key={idx} {...props} />
                                ))}
                            </div>
                        </div>
                    </section>
                )}
            </main>
        </Layout>
    );
}

export default Home;
