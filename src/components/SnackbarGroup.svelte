<script>
    import { SnackBars } from '../stores'
    import { onMount } from 'svelte';
    import Snackbar from './Snackbar.svelte'

    let pastNumChildren = 0;

    const checkSnackBars = () => {
        let cont = document.getElementById("SnackBarContainer");
        if (cont.childElementCount == 0 && pastNumChildren !== 0) {
            SnackBars.set({})
        }
        pastNumChildren = cont.childElementCount;
    }

    onMount(() => {
        const checker = setInterval(checkSnackBars, 2000)
        return () => {clearInterval(checker)}
    })

</script>

<div id="SnackBarContainer">
    {#each Object.keys($SnackBars) as key, i}
        <Snackbar
                status={$SnackBars[key].status}
                message={$SnackBars[key].message}
                color={$SnackBars[key].color}
                timeout={$SnackBars[key].timeout}
                grouped={true}
                id={key}
        />
    {/each}
</div>

<style>
    div {
        position: fixed;
        display: flex;
        bottom: 10px;
        left: 50%;
        transform: translatex(-50%);
        z-index: 500;
        flex-direction: column;
        overflow: hidden;
        transition: ease all 0.4s;
    }
</style>