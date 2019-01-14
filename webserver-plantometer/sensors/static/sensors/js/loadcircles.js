		$(document).ready(function() {
			$('#humidity').circliful({
				getText : function(){
					if (this.usesTotal())
						return Math.round(this.getCurrentValue())+" %";
					else
						return this.getCurrentValue()+" %";
					},
				getInfoText : function(){
					return "Humidity in %";
				},
				"dimension" : 300
			});
		});
		$(document).ready(function() {

			$('#temp').circliful({
				getText : function(){
					if (this.usesTotal())
						return Math.round(this.getCurrentValue())+" C";
					else
						return this.getCurrentValue()+" C";
					},
				getInfoText : function(){
					return "Temperature in C";
				},
				"dimension" : 300
			});
		});
		$(document).ready(function() {

			$('#level').circliful({
				getText : function(){
					if (this.usesTotal())
						return Math.round(this.getCurrentValue())+" L";
					else
						return this.getCurrentValue()+" L";
					},
				getInfoText : function(){
					return "Level in L";
				},
				"dimension" : 300
			});
		});
		$(document).ready(function() {

			$('#pressure').circliful({
				getText : function(){
					if (this.usesTotal())
						return Math.round(this.getCurrentValue())+" Pa";
					else
						return this.getCurrentValue()+" Pa";
					},
				getInfoText : function(){
					return "Pressure in Pa";
				},
				"dimension" : 300
			});
		});
		$(document).ready(function() {

			$('#soilmoist').circliful({
				getText : function(){
					if (this.usesTotal())
						return Math.round(this.getCurrentValue())+" %";
					else
						return this.getCurrentValue()+" %";
					},
				getInfoText : function(){
					return "SoilMoisture in %";
				},
				"dimension" : 300
			});
		});
		let myObser = Rx.Observable.timer(0, 2000).map(() => fetch(`/sensors/dataupdate`).then(res => res.json()))
			myObser.subscribe(x => x.then(data => {
				$('#humidity').circliful('animateToValue',Math.round(Math.random()*100))
				$('#level').circliful('animateToValue',Math.round(Math.random()*100))
				$('#pressure').circliful('animateToValue',Math.round(Math.random()*100))
				$('#temp').circliful('animateToValue',Math.round(Math.random()*100))
				$('#soilmoist').circliful('animateToValue',Math.round(Math.random()*100))
			}
		))