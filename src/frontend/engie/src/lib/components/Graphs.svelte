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
    $: formattedDate = `${date.getFullYear()}-${twoDigits(date.getMonth() + 1)}-${twoDigits(date.getDate())}`

    let data = {};

    for (let i of stat_types)
        data[i] = {
            labels: ['Sun', 'Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat'],
            datasets: [
                {
                    values: [0, 0, 0, 0, 0, 0, 0]
                }
            ]
        }

    console.log(`http://127.0.0.1:5000/api/${building}/${formattedDate}/7`);

    $: try {
        fetch(`http://127.0.0.1:5000/api/${building}/${formattedDate}/7`)
            .then(res => res.json())
            .then(json => {
                let obj = new Object();

                for(let stat_type of stat_types)
                    obj[stat_type] = {
                        labels: ['Sun', 'Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat'],
                        datasets: [
                            {
                                values: json.map(day => day[stat_type])
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
        <Chart data={data[stat_type]} type="line" colors={['#CE0E3D']} />
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

