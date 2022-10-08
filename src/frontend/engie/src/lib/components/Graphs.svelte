<script>
    import Chart from 'svelte-frappe-charts';
    import { onMount } from 'svelte/internal';
    export let building;
    export let date;

    const stat_types = ['steam', 'electricity', 'chilled-water', 'hot-water', 'total-consumption', 'natural-gas'];

    const twoDigits = num => num.toLocaleString('en-US', {
        minimumIntegerDigits: 2,
        useGrouping: false
    });

    const formattedDate = `${date.getFullYear()}-${twoDigits(date.getMonth())}-${twoDigits(date.getDate())}`;

    let data = stat_types.map(stat_type => {
        let obj = new Object();

        obj[stat_type] = {
            labels: ['Sun', 'Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat'],
            datasets: [
                {
                    values: [0, 0, 0, 0, 0, 0, 0]
                }
            ]
        };

        return obj;
    });

    console.log(data);

    console.log(`http://127.0.0.1:5000/api/${building}/${formattedDate}/7`);

    /*onMount(async () => {
        const res = await fetch(`http://127.0.0.1:5000/api/${building}/${formattedDate}/7`);
        const json = await res.json();

        let obj = new Object();

        for(let stat_type of stat_types)
            obj[stat_type] = {
                labels: ['Sun', 'Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat'],
                datasets: [
                    {
                        values: res.map(day => day[stat_type])
                    }
                ]
            };

        data = obj;
    });*/
</script>

<div class="container">
    {#each stat_types as stat_type}
    <div class="graph">
        <h1>{stat_type[0].toUpperCase() + stat_type.substring(1)}</h1>
        <p>{data[stat_type].datasets[0].values.join(', ')}</p>
        <Chart data={data[stat_type]} type="line" />
    </div>
    {/each}
</div>

<style>
    .container {
        display: inline-block;
    }

    .graph {
        width: 33.333%;
        display: inline-block;
    }

    h1 {
        text-align: center;
        margin-top: 10px;
    }

    @media screen and (max-width: 650px) {
        .graph {
            width: 50%;
        }
    }
</style>

