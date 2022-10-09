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

    let formattedDate;
    $: formattedDate = `${date.getFullYear()}-${twoDigits(date.getMonth() + 1)}-${twoDigits(date.getDate())}`;
    

    let data = {};

    for (let i of stat_types)
        data[i] = {
            labels: ['Sun', 'Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat'],
            datasets: [
                {
                    values: [0, 0, 0, 0, 0, 0, 0]
                },
                {
                    values: [0, 0, 0, 0, 0, 0, 0]
                },         
            ]
        }

    $: try {
        fetch(`https://engie.api.zoogies.live/api/${building}/${formattedDate}/7`)
            .then(res => res.json())
            .then(async json => {
                let obj = new Object();
                let averageJSON = new Object();

                for (let stat_type of stat_types)
                    averageJSON[stat_type] = 0;

                try {
                    const average = await fetch(`http://engie.api.zoogies.live/api/average/${building}/${formattedDate}/14`);
                    averageJSON = await average.json(); 
                } catch(e) {
                    console.error(e);
                }

                for(let stat_type of stat_types)
                    obj[stat_type] = {
                        labels: ['Sun', 'Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat'],
                        datasets: [
                            {
                                values: Array(7).fill(averageJSON[stat_type]),
                                name: '2 Week Average'
                            },
                            {
                                values: json.map(day => Math.round(day[stat_type] * 1e3) / 1e3),
                                name: 'This Week'
                            }
                        ]
                    };

                data = obj;
            }).catch(console.error);
    } catch(e) {
        console.error(e);
    }
</script>

<div class="container">
    {#each stat_types as stat_type}
    <div class="graph">
        <h1>{stat_type[0].toUpperCase() + stat_type.substring(1)}</h1>
        <!-- <p>{stat_type} - {data[stat_type].datasets[0].values.join(', ')}</p> -->
        <Chart data={data[stat_type]} type="line" colors={['#B0B7BD', '#CE0E3D']} lineOptions="{{heatline: 1, hideDots: 1, regionFill: 1}}" />
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

