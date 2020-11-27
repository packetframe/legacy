<script>
    import Router from "svelte-spa-router";
    import Navbar from "./components/Navbar.svelte";
    import Index from "./pages/Index.svelte";
    import Login from "./pages/Login.svelte";
    import Signup from "./pages/Signup.svelte";
    import Dashboard from "./pages/Dashboard.svelte";
    import Docs from "./pages/Docs.svelte";
    import Peering from "./pages/Peering.svelte";
    import NotFound from "./pages/NotFound.svelte";
    import SnackbarGroup from "./components/SnackbarGroup.svelte";

    const routes = {
        "/": Index,
        "/login": Login,
        "/signup": Signup,
        "/dashboard": Dashboard,
        "/peering": Peering,
        "/docs": Docs,
        "*": NotFound
    }

    // // Load global theme
    // for (const [key, value] of Object.entries(DarkTheme)) {
    //     document.documentElement.style.setProperty("--" + key, value)
    // }
</script>

<main>
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
