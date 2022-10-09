<script>
	import BuildingSelector from '$lib/components/BuildingSelector.svelte';
	import Graphs from '$lib/components/Graphs.svelte';
	import WeekPicker from '$lib/components/WeekPicker.svelte';
	import Footer from '$lib/components/Footer.svelte';

	const dorm_buildings = ['busch', 'baker', 'taylor', 'smith'];
	const other_buildings = ['knowlton', 'recreation', 'denny', 'library', 'enarson'];

	let mode = /*localStorage.getItem('mode') ||*/ 'other';
	let buildings = other_buildings;

	let default_dorm = /*localStorage.getItem('default_dorm') ||*/ dorm_buildings[0];
	let default_other = /*localStorage.getItem('default_other') ||*/ other_buildings[0];

	let building = other_buildings[0];
	let date = new Date('Sun Sep 25 2022 00:00:00 GMT-0400 (Eastern Daylight Time)');

	function switchBuildingType(buildingType) {
		if (mode === buildingType)
			return;

		// localStorage.setItem('mode', mode);
		mode = buildingType;
		building = buildingType === 'dorm' ? default_dorm : default_other;
		buildings = buildingType === 'dorm' ? dorm_buildings : other_buildings;
	}

	function switchBuilding($event) {
		console.log($event);

		const newBuilding = $event.detail;

		if (mode === 'dorm') {
			default_dorm = newBuilding;
			// localStorage.setItem('default_dorm', default_dorm);
		} else {
			default_other = newBuilding;
			// localStorage.setItem('default_other', default_other);
		}

		building = newBuilding;
	}

	function switchDate($event) {
		date = $event.detail;
	}

	/**
	 * api/<building>/<type>/<timestring in yyyy-mm-dd>/<length in days>
	 * api/busch/steam/2017-01-01/30
	*/
</script>

<svelte:head>
	<title>Engie Panel</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<section>
	<div class="uppermost">
		<div> { building[0].toUpperCase() + building.slice(1) } </div>
		<div class="type-selector">
			<a on:click={() => switchBuildingType('dorm')} class="{mode === 'dorm' ? 'selected' : ''}">Dorm</a> | 
			<a on:click={() => switchBuildingType('other')} class="{mode === 'other' ? 'selected' : ''}">Non-Dorm</a>
		</div>
	</div>

	<div class="controls">
		<WeekPicker on:selected={switchDate} />
		<BuildingSelector buildings={buildings} on:chosen={switchBuilding} class="right" />
	</div>
	<Graphs building={building} date={date} />

	<Footer />
</section>

<style>
	a {
		cursor: pointer;
		text-decoration: underline;
	}

	a.selected {
		font-weight: bold;
		text-decoration: none;
		cursor: default;
	}

	.uppermost {
		background-color: #333;
		/* background-color: #sB0B7BD; */
		padding: 3px;
		color: white;
		text-align: center;
		display: flex;
	}

	.type-selector {
		margin-left: auto;
	}

	.controls {
		/* background-color: #A0A0A0; */
		background-color: #CE0E3D;
		padding: 30px;
		display: flex;
		overflow: wrap;
	}
</style>
