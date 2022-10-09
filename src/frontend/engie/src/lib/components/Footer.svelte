<script>
    const tips = [
        'A leak of one drop per second can cost $35 per year',
        'Setting your water temperature too high can cost $50 per year',
        'Keeping game consoles in ready mode can cost $23 per year',
        'A desktop left idle can cost $75 per year',
        'A laser printer left on can cost $130 per year',
        'Never let the water run while shaving or brushing teeth',
        'Never pour water down the drain when there may be another use for it—such as watering a plant or garden',
        'Wash fruits and vegetables in a basin. Use a vegetable brush',
        'Sweep driveways, sidewalks and steps rather than hosing off',
        'Use natural light whenever possible'
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