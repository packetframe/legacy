module.exports = {
  title: 'DELIVR.DEV',
  tagline: 'The open source CDN platform for technology enthusiasts.',
  url: 'https://delivr.dev/',
  baseUrl: '/',
  onBrokenLinks: 'throw',
  favicon: 'https://dash.delivr.dev/favicon.png',
  organizationName: 'natesales', // Usually your GitHub org/user name.
  projectName: 'delivr-docs', // Usually your repo name.
  themeConfig: {
    forceDarkMode: true,
    navbar: {
      title: 'DELIVR.DEV',
      logo: {
        alt: 'DELIVR.DEV',
        src: 'https://dash.delivr.dev/favicon.png',
      },
      items: [
        {
          to: 'docs/record-management',
          activeBasePath: 'docs/record-management',
          label: 'Docs',
          position: 'left',
        },
        {to: 'blog', label: 'Blog', position: 'left'},
        {
          href: 'https://dash.delivr.dev/',
          label: 'Dashboard',
          position: 'right',
        },
      ],
    },
  },
  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          // Please change this to your repo.
          editUrl:
            'https://github.com/natesales/delivr-docs/edit/main/',
        },
        blog: {
          showReadingTime: true,
          // Please change this to your repo.
          editUrl:
            'https://github.com/natesales/delivr-docs/edit/main/',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],
};
