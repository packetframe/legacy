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
    import Banner from "./components/Banner.svelte";

    const routes = new Map();

    routes.set("/", Index)
    routes.set("/login", Login)
    routes.set("/signup", Signup)
    routes.set("/dashboard", Dashboard)
    routes.set("/community", Community)
    routes.set("/docs", Docs)
    // TODO: 404 doesn't work
    // routes.set("*", NotFound)

    // // Load global theme
    // for (const [key, value] of Object.entries(DarkTheme)) {
    //     document.documentElement.style.setProperty("--" + key, value)
    // }

    let showBanner = true;

    if (document.cookie.includes("hidebanner")) {
        showBanner = false;
    }

    document.cookie = "hidebanner=true";
</script>

<main>
    {#if showBanner}
        <Banner>Delivr.dev is now PacketFrame! Same service, same projects, just a new name and domain. 😃</Banner>
    {/if}

    <Navbar/>

    <div class="body">
        <Router {routes}/>
        <SnackbarGroup/>
    </div>

    <footer>&copy; PacketFrame 2020.</footer>
</main>

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
