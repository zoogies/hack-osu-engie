<script>
    const tips = [
        'That a leak of one drop per second can cost $35 per year',
        'That setting your water temperature too high can cost $50 per year',
        'That keeping game consoles in ready mode can cost $23 per year',
        'That a desktop left idle can cost $75 per year',
        'That a laser printer left on can cost $130 per year',
        'That you should never let the water run while shaving or brushing teeth',
        'That you could use drain water for watering a plant or garden instead of draining',
        'That you should wash fruits and vegetables in a basin using a vegetable brush',
        'That you should sweep driveways, sidewalks and steps rather than hosing them off',
        'That you should use natural light whenever possible'
    ];

    let index = Math.floor(Math.random() * tips.length);

    function up() {
        if (index >= tips.length - 1)
            index = 0;
        else
            index++;
    }

    up();
    setInterval(up, 5000);
</script>

<footer>
    <p> <b>Did you know: </b>{ tips[index] }? </p>
</footer>

<style>
    footer {
		position: sticky;
		background-color: #A0A0A0;
		bottom: 0;
        text-align: center;
        padding: 5px;
        font-size: 1.3rem;
	}
</style>