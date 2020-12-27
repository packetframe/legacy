<script>
    import Router from "svelte-spa-router";
    import Navbar from "./components/Navbar.svelte";
    import Index from "./pages/Index.svelte";
    import Login from "./pages/Login.svelte";
    import Signup from "./pages/Signup.svelte";
    import Dashboard from "./pages/Dashboard.svelte";
    import Docs from "./pages/Docs.svelte";
    import Community from "./pages/Community.svelte";
    import NotFound from "./pages/NotFound.svelte";
    import SnackbarGroup from "./components/SnackbarGroup.svelte";
    import MDPWrapper from "rollup-plugin-mdsvex-pages/src/components/MDPWrapper.svelte";
    const routes = new Map();

    routes.set("/", Index);
    routes.set("/login", Login);
    routes.set("/signup", Signup);
    routes.set("/dashboard", Dashboard);
    routes.set("/community", Community);
    routes.set("/docs", Docs);
    // TODO: 404 doesn't work
    // routes.set("*", NotFound)

    // // Load global theme
    // for (const [key, value] of Object.entries(DarkTheme)) {
    //     document.documentElement.style.setProperty("--" + key, value)
    // }

    //
    // if (document.cookie.includes("hidebanner")) {
    //     showBanner = false;
    // }
    //
    // document.cookie = "hidebanner=true";
</script>

<style>
    :global(::selection) {
        background: #d000ff;
    }

    :global(::-moz-selection) {
        background: #d000ff;
    }

    footer {
        margin-top: 20px;
        margin-bottom: 15px;
        text-align: center;
    }
</style>

<main>
    <Navbar/>

    <MDPWrapper navbar={false} styles={{
        'sidebar-border': '1px solid white', 
        'sidebar-margin-top': '0px', 
        'background-color': 'black', 
        'text-color': 'white',
        'sidebar-active': '#996de0',
        'sidebar-hover': '#996de0',
        }}>

    <div class="body">
        <Router {routes}/>
        <SnackbarGroup/>
    </div>

    <footer>&copy; PacketFrame 2020.</footer>
    </MDPWrapper>


</main>
