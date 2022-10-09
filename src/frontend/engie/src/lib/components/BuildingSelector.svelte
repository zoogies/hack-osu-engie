<script>
	import { createEventDispatcher } from 'svelte';
    // 2022-10-08
    export let buildings;

    const dispatch = createEventDispatcher();

    let open = false;

    function choose(building) {
        dispatch('chosen', building);
        open = false;
    }
</script>

<div class="container">
    <button on:click={() => open = true} class="init-btn">Change Building</button>
    {#if open}
        <div class="buildings">
            <h1 on:click={() => open = false}><span>x</span></h1>
            {#each buildings as building}
                <p> <button on:click={() => choose(building)}> { building[0].toUpperCase() + building.substring(1) } </button> </p>
            {/each}
        </div>
    {/if}
</div>

<style>
    .container {
        justify-self: flex-end;
        height: 100%;
        display: flex;
        align-items: center;
    }

    button {
        border: none;
        background-color: #333;
        font-size: 2rem;
        padding: 10px 20px;
        color: white;
        position: relative;
        bottom: 3px;
        border-radius: 15px;
        cursor: pointer;
        transition: background .3s border-radius .3s;
        margin: 10px;
    }

    button:hover {
        background-color: #000;
        animation: CircleMain .3s forwards;
    }

    @keyframes CircleMain {
        100% {
            border-radius: 30px;
        }
    }

    .buildings {
        position: absolute;
        background-color: #ccc;
        padding: 10px 30px;
        text-align: center;
        top: 10%;
        right: 5%;
        z-index: 9999999999;
        box-shadow: 0 0 30px -4px rgba(0,0,0,0.75);
    }

    .buildings button {
        font-size: 1.2rem;
        border-radius: 2px;
        margin: 15px 0 0 0;
    }

    .buildings button:hover {
        animation: CircleBuildings .3s forwards;
    }

    @keyframes CircleBuildings {
        100% {
            border-radius: 4px;
        }
    }

    h1 {
        text-align: right;
        margin-right: 5px;
    }

    h1 span {
        color: red;
        transition: background .3s;
        cursor: pointer;
    }

    h1 span:hover {
        color: #990000;
    }
</style>