<script>
    import Router from "svelte-spa-router";
    import Navbar from "./components/Navbar.svelte";
    import Index from "./pages/Index.svelte";
    import Login from "./pages/Login.svelte";
    import Signup from "./pages/Signup.svelte";
    import Dashboard from "./pages/Dashboard.svelte";
    import NotFound from "./pages/NotFound.svelte";
    import SnackbarGroup from "./components/SnackbarGroup.svelte";

    const routes = {
        "/": Index,
        "/login": Login,
        "/signup": Signup,
        "/dashboard": Dashboard,
        "*": NotFound
    }
</script>

<main>
    <Navbar/>

    <div class="body">
        <Router {routes}/>
        <SnackbarGroup/>
    </div>

    <footer>&copy; Nate Sales 2020.</footer>
</main>

<style>
    footer {
        margin-top: 20px;
        margin-bottom: 15px;
        text-align: center;
    }
</style>