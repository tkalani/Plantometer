$(document).ready(function () {
	$('#humidity').circliful({
		getText: function () {
			if (this.usesTotal())
				return Math.round(this.getCurrentValue());
			else
				return this.getCurrentValue();
		},
		getInfoText: function () {
			return "Humidity in %";
		},
		'dimension': 200,
		'background-fill-color': '#fff',
		'background-radius': 85,
		'foreground-radius': 95,
		'background-width': 15,
		'background-stroke-color': '#808080',
	});
	$('#humidity').circliful('animateToValue', 0);
});
$(document).ready(function () {
	$('#temp').circliful({
		getText: function () {
			if (this.usesTotal())
				return Math.round(this.getCurrentValue());
			else
				return this.getCurrentValue();
		},
		getInfoText: function () {
			return "Temperature in C";
		},
		'dimension': 200,
		'background-fill-color': '#fff',
		'background-radius': 85,
		'foreground-radius': 95,
		'background-width': 15,
		'background-stroke-color': '#808080',
	});
	$('#temp').circliful('animateToValue', 0);
});
$(document).ready(function () {
	$('#level').circliful({
		getText: function () {
			if (this.usesTotal())
				return Math.round(this.getCurrentValue());
			else
				return this.getCurrentValue();
		},
		getInfoText: function () {
			return "Level in %";
		},
		'dimension': 200,
		'background-fill-color': '#fff',
		'background-radius': 85,
		'foreground-radius': 95,
		'background-width': 15,
		'background-stroke-color': '#808080',
	});
	$('#level').circliful('animateToValue', 0);
});

$(document).ready(function () {
	$('#soilmoist').circliful({
		getText: function () {
			if (this.usesTotal())
				return Math.round(this.getCurrentValue());
			else
				return this.getCurrentValue();
		},
		getInfoText: function () {
			return "SoilMoisture in %";
		},
		'dimension': 200,
		'background-fill-color': '#fff',
		'background-radius': 85,
		'foreground-radius': 95,
		'background-width': 15,
		'background-stroke-color': '#808080',
	});
	$('#soilmoist').circliful('animateToValue', 0);
});

let myObser = Rx.Observable.timer(0, 10000).map(() => fetch(`/sensors/dataupdate`).then(res => res.json()))
myObser.subscribe(x => x.then(data => {
	console.log(data);


	var rain = data.rain;
	document.getElementById("time").innerHTML = data.time;
	document.getElementById("date").innerHTML = data.date;
	var hcolor, humidity = data.humidity;
	if (humidity <= 30) hcolor = '#f00';
	else hcolor = '#0f0';
	var scolor, soilmoist = data.soilmoist;
	if (soilmoist <= 35) scolor = '#f00';
	else if (soilmoist <= 65) scolor = '#0f0'
	else scolor = '#f00';
	var lcolor, level = data.distance;
	if (level <= 35) lcolor = '#f00';
	else lcolor = '#0f0'

	var pcolor, pressure = (data.pressure / 101325) * 100;
	if (pressure <= 90) pcolor = '#f00';
	else pcolor = '#0f0';
	var tcolor, temp = data.temp;
	if (temp <= 20) tcolor = '#f00';
	else if (temp <= 35) tcolor = '#0f0'
	else tcolor = '#f00';
	$('#humidity').circliful('animateToValue', humidity);
	$('#humidity').circliful('setSetting', 'foreground-color', hcolor);
	$('#level').circliful('animateToValue', level);
	$('#level').circliful('setSetting', 'foreground-color', lcolor);
	$('#temp').circliful('animateToValue', temp);
	$('#temp').circliful('setSetting', 'foreground-color', tcolor);
	$('#soilmoist').circliful('animateToValue', soilmoist);
	$('#soilmoist').circliful('setSetting', 'foreground-color', scolor);

	if (rain == 0)
		document.getElementsByClassName("weather")[0].style.backgroundImage = "url(" + sunnypngurl + ")";
	else
		document.getElementsByClassName("weather")[0].style.backgroundImage = "url(" + rainypngurl + ")";


	actuator_tab(data.actuatorstatus, data.actuatorcontrol, data.actuatorlink);
}
))
function actuator_control() {
	btn = document.getElementById("actuatorcontrol").checked;
	console.log(btn,"i")
	$.ajax({
		type: "POST",
		url: link,
		dataType: 'json',
		data: { 'plant_id': pid, 'btn': btn },

		success: function (res) {
			console.log('success1');
			console.log(res.res);
			if (res.res == 'failed') {
				console.log("connection failed");
				alert("Could not connect to the actuator.");
				if (!btn)
					document.getElementById("actuatorcontrol").checked = true;
				else
					document.getElementById("actuatorcontrol").checked = false;
			}
		},
		error: function (txt, res) {
			console.log('failed1');
		},
	});
}

function actuator_tab(actuatorstatus, actuatorcontrol, actuatorlink) {

	if (actuatorstatus == 1) {
		document.getElementById("actuatorstatus").style.backgroundImage = "url(" + runningtapurl + ")";
		document.getElementById("actuatorcontrol").checked = true;
	}
	else {
		document.getElementById("actuatorstatus").style.backgroundImage = "url(" + stoppedtapurl + ")";
		document.getElementById("actuatorcontrol").checked = false;
	}

	if (actuatorlink == -1) {
		document.getElementById("block1").style.opacity = 0.3;
		document.getElementById("err1").style.display = "block";

		document.getElementById("actuatorcontrol").disabled = true;
	}
	else {
		document.getElementById("block1").style.opacity = 1;
		document.getElementById("err1").style.display = "none";

		if (actuatorcontrol == 0) {
			document.getElementById("block2").style.opacity = 0.3;
			document.getElementById("err2").style.display = "block";

			document.getElementById("actuatorcontrol").disabled = true;
		}
		else {
			document.getElementById("block2").style.opacity = 1;
			document.getElementById("err2").style.display = "none";

			document.getElementById("actuatorcontrol").disabled = false;
		}
	}
}