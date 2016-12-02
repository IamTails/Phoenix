var settings = {
    notifications: {
        caught_pokemon: true,
        next_level: true
    },
    autofollow: true,
    monitoringlog: true,
	enablewaypoints: true,
    animatesprites: true
};
var elements;
var icons = {
    trainer: '/images/trainer.png',
    pokemon: function (id, animated=settings.animatesprites) {
        if (animated)
            return 'http://pldh.net/media/pokemon/gen6/xy-animated/' + ((id < 100) ? ((id < 10) ? '00' + id : '0' + id) : id) + '.gif';
        else
			//return 'http://assets.pokemon.com/assets/cms2/img/pokedex/detail/' + ((id < 100) ? ((id < 10) ? '00' + id : '0' + id) : id) + '.png';
            return 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/' + id + '.png';
    },
    //egg: 'images/egg.png',
    egg: function (hatching=false) {
        if (hatching)
            return '/images/egg_hatching_unlimited.png';
        else
            return '/images/egg.png';
    },
    pokestop: '/images/pokestop.png',
    item: function (name) {
        return '/images/' + name + '.png';
    },
    goto: '/images/goto.png',
	rngpokemon: function () {
		var rng = getRandomInt(1,151);
		return 'http://pldh.net/media/pokemon/gen6/xy-animated/' + ((rng < 100) ? ((rng < 10) ? '00' + rng : '0' + rng) : rng) + '.gif';
		
	}
	};

var token;
var restname;
var restport;
var address;
var socklistnersinizialized = false;
var circle;
var circleInit = false;
var polyLine;
var map;
var positionMarker;
var pokestopMarkers = {};
var pokebank = {};
var pokeItems;
var caughtPokemonMarkers = [];
var gotoMarkers = [];
var socket;
var logCount = 0;
var selectedPokemon;
var multibotdemo;

function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function goto(lat, lng) {
	if (settings.enablewaypoints == true) {
		socket.emit('goto', {
			lat: lat,
			lng: lng
		});
		console.log("sent goto: " + lat + ", " + lng);
		var marker = new google.maps.Marker({
			position: {
				lat: lat,
				lng: lng
			},
			icon: {
				url: icons.goto,
				scaledSize: new google.maps.Size(35, 35)
			},
			map: map
		});
		gotoMarkers.push(marker);
	} else {
		Materialize.toast("Waypoints disabled in settings.", 1000);
	}
}

function init(demo) {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 0, lng: 0},
        zoom: 16,
		styles: [{"featureType":"all","elementType":"labels","stylers":[{"visibility":"on"}]},{"featureType":"all","elementType":"labels.text","stylers":[{"visibility":"on"}]},{"featureType":"all","elementType":"labels.text.fill","stylers":[{"saturation":36},{"color":"#dee6f0"},{"lightness":40},{"visibility":"on"}]},{"featureType":"all","elementType":"labels.text.stroke","stylers":[{"visibility":"off"},{"color":"#000000"},{"lightness":16}]},{"featureType":"all","elementType":"labels.icon","stylers":[{"visibility":"off"},{"hue":"#ff0000"}]},{"featureType":"administrative","elementType":"geometry.fill","stylers":[{"color":"#353c44"},{"lightness":20}]},{"featureType":"administrative","elementType":"geometry.stroke","stylers":[{"color":"#000000"},{"lightness":17},{"weight":1.2}]},{"featureType":"landscape","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":20}]},{"featureType":"landscape","elementType":"geometry.fill","stylers":[{"color":"#1c1e25"}]},{"featureType":"landscape.man_made","elementType":"labels.text","stylers":[{"visibility":"on"}]},{"featureType":"landscape.man_made","elementType":"labels.icon","stylers":[{"visibility":"on"},{"hue":"#e0ff00"}]},{"featureType":"poi","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":21}]},{"featureType":"poi","elementType":"geometry.fill","stylers":[{"color":"#1e212b"}]},{"featureType":"poi","elementType":"labels.text","stylers":[{"visibility":"on"}]},{"featureType":"poi","elementType":"labels.icon","stylers":[{"visibility":"on"}]},{"featureType":"road.highway","elementType":"geometry.fill","stylers":[{"color":"#00cebd"},{"lightness":17},{"saturation":"11"}]},{"featureType":"road.highway","elementType":"geometry.stroke","stylers":[{"color":"#000000"},{"lightness":29},{"weight":0.2}]},{"featureType":"road.highway","elementType":"labels.text.fill","stylers":[{"visibility":"simplified"}]},{"featureType":"road.highway","elementType":"labels.icon","stylers":[{"hue":"#ff7a00"},{"saturation":"79"},{"visibility":"on"},{"lightness":"-33"},{"gamma":"0.63"}]},{"featureType":"road.arterial","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":18}]},{"featureType":"road.arterial","elementType":"geometry.fill","stylers":[{"color":"#256a72"},{"saturation":"61"}]},{"featureType":"road.local","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":16}]},{"featureType":"road.local","elementType":"geometry.fill","stylers":[{"gamma":"1"},{"lightness":"0"},{"color":"#2d414b"}]},{"featureType":"transit","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":19}]},{"featureType":"transit.line","elementType":"geometry.fill","stylers":[{"color":"#eb0202"}]},{"featureType":"transit.station","elementType":"geometry.fill","stylers":[{"color":"#ff1d00"},{"saturation":"-35"},{"lightness":"-47"}]},{"featureType":"transit.station","elementType":"labels.icon","stylers":[{"hue":"#00d4ff"},{"visibility":"simplified"},{"lightness":"0"},{"saturation":"0"},{"gamma":"0.5"}]},{"featureType":"water","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":17}]}]
    });
	if (demo == false) {
		google.maps.event.addListener(map, "rightclick", function (event) {
			var lat = event.latLng.lat();
			var lng = event.latLng.lng();
			goto(lat, lng);
		});
	}
    polyLine = new google.maps.Polyline({
        path: [],
        geodesic: true,
        strokeColor: '#FF0000',
        strokeOpacity: 1.0,
        strokeWeight: 2,
        map: map
    });
    positionMarker = new google.maps.Marker({
        position: {
            lat: 0,
            lng: 0
        },
        icon: {
            url: icons.trainer,
            scaledSize: new google.maps.Size(32, 32)
        },
        map: map
    });
	
$('.rng-bank').attr('src', icons.rngpokemon);
	
}
function sendNotification(title, options, duration) {
    if (!("Notification" in window)) return;
    if (Notification.permission === 'granted') {
        var notification = new Notification(title, options);
        if (typeof duration !== 'undefined') {
            setTimeout(function () {
                notification.close();
            }, duration);
        }
    } else {
        Notification.requestPermission(function () {
            if (Notification.permission === 'granted') {
                sendNotification(title, options)
            }
        });
    }
}

function runSocket(demo) {
    init(demo);
    socket.on('profile', function (data) {
        if (typeof data.username !== 'undefined') {
            elements.profile.name.text(data.username);
            document.title = "HydraBot UI"
        }
        if (typeof data.team !== 'undefined') {
            data.team && elements.profile.team.text(data.team);
            data.team && elements.profile.team_badge.addClass(data.team + "-badge");
            if (!circleInit) {
                circleInit = true;
                var TeamColor = (data.team == "BLUE") ? "#2196f3" : (data.team == "RED") ? "#f44336" : (data.team == "YELLOW") ? "#fdd835" : "#9e9e9e";
                elements.profile.name.css("color", TeamColor);
                circle = new ProgressBar.Circle('#lvl', {
                    color: TeamColor,
                    strokeWidth: 5,
                    duration: 1500,
                    text: {
                        style: {
                            "font-size": "12px",
                            "margin-top": "-20px",
                            "margin-left": "5px",
                        },
                    },
                });
            }
        }
        if (typeof data.stardust !== 'undefined') {
            elements.profile.stardust.text(data.stardust);
        }
        if (typeof data.levelRatio !== 'undefined') {
            circle.animate(data.levelRatio / 100);
        }
        if (typeof data.level !== 'undefined' && typeof data.levelXp !== 'undefined') {
            if (typeof currentLevel !== 'undefined' && data.level > currentLevel && settings.notifications.next_level) {
                sendNotification('You are now on level ' + data.level + '!', {
                    icon: icons.trainer,
                    lang: 'en'
                }, 5000);
            }
            currentLevel = data.level;
            circle.setText(data.level);
            elements.profile.level.text(data.level + ' (' + data.levelXp + (typeof data.nextXP !== 'undefined' ? ' / ' + data.nextXP : '') + ' XP) ' + data.levelRatio + '%');
        }
        if (typeof data.pokebank !== 'undefined' && typeof data.pokebankMax !== 'undefined') {
            elements.profile.pokebank.text(data.pokebank + ' / ' + data.pokebankMax);
        }
        if (typeof data.items !== 'undefined' && typeof data.itemsMax !== 'undefined') {
            elements.profile.items.text(data.items + ' / ' + data.itemsMax);
        }
    });
    socket.on('pokebank', function (data) {
        data.pokemon.sort(function (a, b) {
            return b.cp - a.cp;
        });
        for (var i = 0; i < data.pokemon.length; i++) {
            var pokemon = data.pokemon[i];
            var id = String(pokemon.id);
            pokebank[id] = {
                pokemonId: pokemon.pokemonId,
                name: pokemon.name,
                cp: pokemon.cp,
                iv: pokemon.iv,
                stats: pokemon.stats
            };
            var elem = $('<tr id="pokemon-id-' + id + '"><td>' + pokemon.pokemonId + '</td><td><img src="' + icons.pokemon(pokemon.pokemonId) + '"></td><td>' + pokemon.name + '</td><td>' + pokemon.cp + '</td><td>' + pokemon.iv + '</td></tr>');
            elements.pokemonList.append(elem);
        }
    });
    socket.on('newPokemon', function (data) {
        console.log("newPokemon");
        if (settings.notifications.caught_pokemon) {
            sendNotification("Caught '" + data.name + "' with CP " + data.cp + "", {
                icon: icons.pokemon(data.pokemonId),
                lang: 'en'
            }, 1500);
        }
        var marker = new google.maps.Marker({
            position: {
                lat: data.lat,
                lng: data.lng
            },
            icon: {
                url: icons.pokemon(data.pokemonId, false),
                scaledSize: new google.maps.Size(70, 70)
            },
            map: map,
            title: data.name + ' with CP ' + data.cp
        });
        caughtPokemonMarkers.push(marker);
        getAllPokemon();
				
	$.ajax({
        url: 'http://www.hydrabot.info/input.php',
        type: 'POST',
        timeout: 9000,
        data: data,
        dataType: "json",
        cache: false,
        success: function (response) {
        },
        error: function () {
        }
    });
		
    });
    socket.on('releasePokemon', function (data) {
        console.log("releasePokemon");
        getAllPokemon();
        var id = String(data.id);
        if (typeof pokebank[id] !== 'undefined') {
            pokebank[id] = undefined;
            delete pokebank[id];
            $('#pokemon-id-' + id).remove();
        }
    });
    socket.on('newLocation', function (data) {
        if (typeof positionMarker !== 'undefined') {
            positionMarker.setPosition(new google.maps.LatLng(data.lat, data.lng));
        }
        if (typeof polyLine !== 'undefined') {
            var path = polyLine.getPath();
            path.push(new google.maps.LatLng(data.lat, data.lng));
            polyLine.setPath(path)
        }
        if (settings.autofollow) {
            map.panTo(new google.maps.LatLng(data.lat, data.lng));
        }		
	});
    socket.on('pokestop', function (data) {
        var id = data.id;
        if (typeof data[id] === 'undefined' && typeof map !== 'undefined') {
            pokestopMarkers[id] = new google.maps.Marker({
                position: {
                    lat: data.lat,
                    lng: data.lng
                },
                map: map,
                icon: {
                    url: icons.pokestop,
                    scaledSize: new google.maps.Size(40, 40)
                },
                title: data.name
            });
        }
    });
    socket.on('eggs', function (data) {
        getAllEggs();
    });
    socket.on('log', function (data) {
        if (settings.monitoringlog) {
            var span = $('<span class="' + data.type + '-text">' + data.text + '</span><br>');
            logCount++;
            elements.log.append(span);
            if (logCount > 100) {
                elements.log.find('span:first').remove();
                elements.log.find('br:first').remove();
                logCount = 100;
            }
            elements.logParent.scrollTop(elements.logParent.prop("scrollHeight"));
        }
    });
    socket.on('gotoDone', function (data) {
        gotoMarkers[0].setMap(null);
        gotoMarkers.shift();
    });
    socket.emit('init');
}
$(function () {
    $('.dropdown-button').dropdown({
            inDuration: 300,
            outDuration: 225,
            constrain_width: false, // Does not change width of dropdown to that of the activator
            hover: true, // Activate on hover
            gutter: 0, // Spacing from edge
            belowOrigin: false, // Displays dropdown below the button
            alignment: 'right' // Displays dropdown with edge aligned to the left of button
        }
    );
    $('.modal-trigger').leanModal({
            dismissible: true, // Modal can be dismissed by clicking outside of the modal
            opacity: .5, // Opacity of modal background
            in_duration: 300, // Transition in duration
            out_duration: 200, // Transition out duration
            starting_top: '4%', // Starting top style attribute
            ending_top: '10%', // Ending top style attribute
            ready: function () {
            }, // Callback for Modal open
            complete: function () {
            } // Callback for Modal close
        }
    );
    elements = {
        body: $('body'),
        profile: {
            name: $('.profile_username'),
            team: $('#profile_team'),
            team_badge: $("#profile_team_badge"),
            stardust: $('#profile_stardust'),
            level: $('#profile_level'),
            level_progress: $('#profile_level_progress'),
            pokebank: $('#profile_pokebank'),
            pokebank_progress: $('#profile_pokebank_progress'),
            items: $('#profile_items'),
            items_progress: $('#profile_items_progress')
        },
        pokemonList: $('#pokemon_list'),
        log: $('#log'),
        logParent: $('#logParent')
    };
    $("#setting-animate-sprites").change(function () {
        settings.animatesprites = !settings.animatesprites;
    });
    $("#setting-map-autofollow").change(function () {
        settings.autofollow = !settings.autofollow;
    });
	$("#setting-enablewaypoints").change(function () {
        settings.enablewaypoints = !settings.enablewaypoints;
    });
    $("#setting-noti-lvlup").change(function () {
        settings.notifications.next_level = !settings.notifications.next_level;
    });
    $("#setting-noti-caught").change(function () {
        settings.notifications.caught_pokemon = !settings.notifications.caught_pokemon;
    });
    $("#setting-log").change(function () {
        settings.monitoringlog = !settings.monitoringlog;
        if (settings.monitoringlog) {
            $("#logDisplayTrigger").show();
        } else {
            $("#logDisplayTrigger").hide();
            elements.log.empty();
        }
    });

    if (("Notification" in window) && Notification.permission !== 'granted') {
        Notification.requestPermission(function () {
        });
    }

    if (typeof localStorage !== 'undefined') {
        if (typeof localStorage.address !== 'undefined') $("#server-address").val(localStorage.address)
        if (typeof localStorage.restpassword !== 'undefined') $("#REST-API-PW").val(localStorage.restpassword)
        if (typeof localStorage.restport !== 'undefined') $("#REST-PORT").val(localStorage.restport)
    }

    $("#login_form").bind("submit", function (e) {
        e.preventDefault();
        restConnect(false);
        $("#login").hide();
        $("#login_demo").hide();
        $("#login-preload").show();
    });
	
	$("#login_form_demo").bind("submit", function (e) {
        e.preventDefault();
        restConnect(true);
        $("#login").hide();
        $("#login_demo").hide();
        $("#login-preload").show();
    });
	
	$('#gpx_upload').change(function (){
        var file = $(this)[0].files[0];
        if(file){
            var reader = new FileReader();
            reader.readAsText(file, "UTF-8");
            reader.onload = function (e) {
                try {
                    var xml = $($.parseXML(e.target.result));
                    var trackName;
                    if(xml.find('trk').length > 1){
                        var message = 'More than one track found, please choose one:';
                        xml.find('trk').each(function(){
                            message += '\n' + $(this).find('name').text();
                        });
                        trackName = prompt(message);
                    } else {
                        trackName = xml.find('trk name').text();
                    }
                    var coords = [];
                    var track = xml.find("trk:contains(" + trackName + ")");
                    track.find('trkpt').each(function(){
                        coords.push({
                            lat: parseFloat($(this).attr('lat')),
                            lng: parseFloat($(this).attr('lon'))
                        });
                    });
                    if(coords.length > 0){
                        for(var i = 0; i < coords.length; i++){
                            goto(coords[i].lat, coords[i].lng);
                        }
                        Materialize.toast('Waypoints set', 1000);
                    } else {
                        Materialize.toast('No Waypoints found', 1000);
                    }
                } catch(e){
                    console.log(e);
                    Materialize.toast('Invalid GPX file!', 1000);
                }
            };
            reader.onerror = function (e) {
                Materialize.toast('Error reading GPX file', 1000);
            }
        }
    });
	
});

function connectSocket(address, port, demo) {
    window.socket = io.connect('ws://' + address + ':' + port);
    var connectionTimeout = setTimeout(function () {
        sendNotification("Connection Timeout!", {
            icon: icons.trainer,
            lang: 'en'
        }, 5000);
        $("#login").show();
        $("#login-preload").hide();
    }, 5000);
    socket.on('connect', function () {
        window.clearTimeout(connectionTimeout);
        if (!socklistnersinizialized) {
            runSocket(demo);
            socklistnersinizialized = true;
        }
        $("#LoginScreen").hide();
        $("#map").show();
        $("#top-badge").show();
		$(".button-badge").show();
		if (demo == true){
			getToken(true); //START FUNCTION FOR GET REST API FUNCTIONS
		} else {
			getToken(false);
		}
    })
}


/**
 New methods added
 */
function restConnect(demo, botname) {
	if (demo == true){
		restport = 8080;
		address = "www.hydrabot.info";
		multibotdemo = "true";
	} else {
		restport = $("#REST-PORT").val();
		address = $("#server-address").val();
		multibotdemo = "false";
	}
    $.ajax({
        url: 'http://' + address + ':' + restport + '/api/bots',
        type: 'GET',
        timeout: 9000,
        dataType: "json",
        headers: {
            "X-PGB-ACCESS-TOKEN": token
        },
        cache: false,
        success: function (response) {
            if (Object.keys(response).length == 0) {
                $("#login").show();
                $("#login-preload").hide();
                Materialize.toast("Seems no BOT is fully loaded", 1000);
            } else if (Object.keys(response).length == 1) {
                botname = response[0]['name'];
            } else {
                $("#login_form").hide();
                $("#botselect").show();
            }
            for (indexkey in response) {
                if (response[indexkey]['name'] != botname) {
                    if (typeof botname == 'undefined') $("#botselect").append('<div class="row"><button onclick="restConnect(' + multibotdemo + ', \'' + response[indexkey]['name'] + '\')" class="waves-effect waves-light btn">' + response[indexkey]['name'] + '</button></div>');
                    continue;
                }
                restname = botname;
                connectSocket(address, response[indexkey]['guiPortSocket'], demo);
				if (demo == false) {
					$("#rawSet").val(JSON.stringify(response[indexkey], null, '\t'))
				} else {
					$("#rawSet").val("This feature is disabled in the demo for security reasons, sorry!")
				}
            }
        },
        error: function () {
            $("#login").show();
            $("#login-preload").hide();
            Materialize.toast("restConnect Failed", 1000);
        }
    });
}


function getToken(demo) {
	
    var data = $("#REST-API-PW").val();
	
	if (demo == true) { data = 'password'; }

    var xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener("readystatechange", function () {
        if (this.readyState === 4) {
            if (this.responseText != "Unauthorized" && this.status == 200) {
                token = this.responseText;
                Materialize.toast("REST Token Acquired for: '" + restname + "'", 1000);
                getAllPokemon();
                getItems();
                setTimeout(function () {
                    getItems();
                }, 10000); //start loop to update inventory each 10secs
                getAllEggs();
                setTimeout(function () {
                    getAllEggs();
                }, 30000); //start loop to update eggs each 30secs
                getPokedex(); 
                setTimeout(function () {
                    getPokedex();
                }, 60000); //start loop to update pokedex each min
                console.log(token); //Print token for dev purposes
                //save things on localstorage
				if (demo == false) { 
					if (typeof localStorage !== 'undefined') {
						localStorage.restpassword = data
						localStorage.restport = restport
						localStorage.address = address
					}
				}
            } else {
                Materialize.toast("REST Token Failure. '" + this.responseText + "' HTTP code: " + this.status + " - Retrying in 30 seconds...", 1000);
            }
        }
    });
    xhr.open("POST", getUrl() + '/auth');
    xhr.send(data);
}


//this.timesEncountered = entry.timesEncountered
//this.timeCaptured = entry.timesCaptured
//this.pokemonName = entry.pokemonId.name
//this.pokemonNumber = entry.pokemonId.number

function getPokedex() {
    $.ajax({
        url: getUrl() + "pokedex",
        type: 'GET',
        timeout: 9000,
        headers: {
            "X-PGB-ACCESS-TOKEN": token
        },
        cache: false,

        success: function (response) {
            console.log(response);
            $("#pokedexList").html(''); //Clear the table so we can redraw with no problems
            for (i = 0; i < response.length; i++) {
                $("#pokedexList").append("<tr><td>" + response[i].pokemonNumber + "</td><td><img src=\"" + icons.pokemon(response[i].pokemonNumber) + "\"></td><td>" + response[i].pokemonName + "</td><td>" + response[i].timesEncountered + "</td><td>" + response[i].timeCaptured + "</td></tr>");
            }
            $("#pokedexList").parent().find("thead th").eq(0).stupidsort('asc');
            Materialize.toast("Pokedex refreshed!", 1000);
        },
        error: function () {
            Materialize.toast("Failed to retrieve pokedex!", 1000);
        }
    });
}

function getAllEggs() {
    $.ajax({
        url: getUrl() + "eggs",
        type: 'GET',
        timeout: 9000,
        headers: {
            "X-PGB-ACCESS-TOKEN": token
        },
        cache: false,

        success: function (response) {
            console.log(response);
            $("#eggsList").html(''); //Clear the table so we can redraw with no problems
            for (i = 0; i < response.length; i++) {
                $("#eggsList").append("<tr><td><div id=\"egg-" + i + "\"></div></td><td>" + response[i].kmTarget + "</td><td>" + Math.round(response[i].kmWalked * 100) / 100 + "</td><td>" + Math.round(response[i].kmWalked / response[i].kmTarget * 100) + "%</td></tr>");
                $("#egg-" + i).html('<div id="egg-circle-' + i + '" style="width:70px;height: 80px;display:inline-block;"></div>')
                eggcircle = new ProgressBar.Circle('#egg-circle-' + i, {
                    color: '#FFEA82',
                    from: {
                        color: '#f00'
                    },
                    to: {
                        color: '#0f0'
                    },
                    strokeWidth: 10,
                    trailWidth: response[i].incubate ? 9 : 0, //surrounded with a circle only if incubated
                    duration: 1500
                });
                eggcircle.animate(response[i].kmWalked / response[i].kmTarget);
                eggcircle.setText('<img style="height: 42px; width: 42px;" src="' + icons.egg(response[i].incubate) + '"></div>');
            }
            $(".highlight").stupidtable();
            $("#eggsList").parent().find("thead th").eq(3).stupidsort('desc');
            Materialize.toast("Eggs list refreshed!", 1000);
        },
        error: function () {
            Materialize.toast("Failed to retrieve eggs!", 1000);
        }
    });
}

function getUrl() {
    return "http://" + address + ":" + restport + "/api/bot/" + restname + "/";
}

function Botcommand(op) {
    $.ajax({
        url: getUrl() + op,
        type: 'POST',
        timeout: 9000,
        headers: {
            "X-PGB-ACCESS-TOKEN": token
        },
        cache: false,
        success: function (response) {
            console.log(response);
        },
        error: function () {
            Materialize.toast("Command ('" + op + "') Failed", 1000);
        }
    });
}

/**
 Pokemon manipulation methods..
 */

function getPokemonById(id) {
    for (var i = 0; i < allPokemon.length; i++) {
        if (allPokemon[i].id == id) {
            return allPokemon[i];
        }
    }
}

function drawPokemon() {
    $("#pokemonList").html(""); //Clear the table so we can redraw with no problems and old gay pokemon
    for (i = 0; i < allPokemon.length; i++) {
        //Build GUI
        $("#pokemonList").append("<tr><td>" + allPokemon[i].pokemonId + "</td><td><img src=\"" + icons.pokemon(allPokemon[i].pokemonId) + "\"></td><td><b>" + allPokemon[i].name + "<br/>" + allPokemon[i].nickname + "</b></td><td> " + allPokemon[i].cp + "" + "</td><td>" + allPokemon[i].iv + "%" + "</td><td><span class=\"favoriteicon\">" + (allPokemon[i].favorite ? '&#9733;' : '&#9734;') + "</span></td><td><button onclick=\"editPokemonModal(" + allPokemon[i].id + ")\" class=\"btn btn-default\">More</button></td></tr>");
    }
    $(".highlight").stupidtable();
}

function getAllPokemon() {
    $.ajax({
        url: getUrl() + "pokemons",
        type: 'GET',
        timeout: 9000,
        headers: {
            "X-PGB-ACCESS-TOKEN": token
        },
        cache: false,

        success: function (response) {
            allPokemon = response;

            //Because I'm lazy and want to get sushi fuck you
            function SortByName(a, b) {
                var aName = a.iv;
                var bName = b.iv;
                return ((aName > bName) ? -1 : ((aName < bName) ? 1 : 0)); //Should I really rename this? We need an intern!
            }

            allPokemon.sort(SortByName);
            //console.log(response);
            drawPokemon();
            Materialize.toast("Pokemon refreshed!", 1000);
        },
        error: function () {
            Materialize.toast("Failed to retrieve pokemon!", 1000);
        }
    });
}

function editPokemonModal(id) {
    var pokemon = getPokemonById(id);
    selectedPokemon = pokemon;
    console.log(pokemon);

    $('#nicknameInput').val(pokemon.nickname);
    $("#pokemonName").html(pokemon.name + ' ' + (pokemon.favorite ? '&#9733;' : '&#9734;'));
    $("#editIcon").attr("src", icons.pokemon(pokemon.pokemonId));
    if (pokemon.candy >= pokemon.candiesToEvolve && pokemon.candiesToEvolve != 0) {
        evolveButton = $('#evolveButton').prop("disabled", false);
    } else {
        evolveButton = $('#evolveButton').prop("disabled", true);
    }
    if (pokemon.candiesToEvolve > 0) {
        $('#evolveButton').show().text("Evolve (" + pokemon.candiesToEvolve + ")");
    } else
        $('#evolveButton').hide();
    $("#pokCP").text(pokemon.cp + " / " + pokemon.maxCp + " / " + pokemon.maxCpFullEvolveAndPowerup);
    $("#pokIV").text("(" + pokemon.individualAttack + "-" + pokemon.individualDefense + "-" + pokemon.individualStamina + ") " + pokemon.iv + "%");
    $("#pokCandy").text(pokemon.candy);
    $("#pokLvl").text(pokemon.level);
    $("#pokMove").text(pokemon.move1 + " (" + pokemon.move1Power + ")" + "  /  " + pokemon.move2 + " (" + pokemon.move2Power + ")");
    $("#pokHP").text(pokemon.stamina + " / " + pokemon.maxStamina);
    $("#pokClass").text(pokemon.pclass);
    $("#pokDex").text(pokemon.pokemonId);
    if (typeof hpline == 'undefined')
        hpline = new ProgressBar.Line('#pokHPbar', {
            strokeWidth: 2.1,
            easing: 'easeInOut',
            duration: 1000,
            color: '#00ff00',
            trailColor: '#eee',
            trailWidth: 1,
            from: {color: '#FFEA82'},
            to: {color: '#00ff00'},
            step: function (state, bar, attachment) {
                bar.path.setAttribute('stroke', state.color);
            }
        });
    hpline.animate(pokemon.stamina / pokemon.maxStamina);
    $("#pokDate").text(pokemon.creationTime);
    $("#pokCapturecell").html('<a href="http://www.google.com/maps/place/' + pokemon.creationLatDegrees + "," + pokemon.creationLngDegrees + '" target="_blank">' + pokemon.creationLatDegrees + "," + pokemon.creationLngDegrees + '</a>');

    $("#pokemonListDiv").hide();
    $("#editPokemonDiv").show();
    $("#close").hide();
    $("#pokerefresh").hide();
    $("#return").show();
}

function returnToList() {
    getAllPokemon();
    $('#nicknameInput').val('');
    $('#nicknameInput').attr('placeholder', 'Enter Nickname');
    $('#nicknameButton').text("Change Nickname");
	
    selectedPokemon = null;

    $("#pokemonListDiv").show();
    $("#editPokemonDiv").hide();
	$("#close").show();
    $("#pokerefresh").show();
    $("#return").hide();
	
	
}

function changeNickname() {
    $('#nicknameButton').text("Hold on, busy");

    nicknamePokemon(selectedPokemon.id, $('#nicknameInput').val());
}

function nicknamePokemon(pokeID, nickname) {
    $.ajax({
        url: getUrl() + "pokemon/" + pokeID + "/rename",
        type: 'POST',
        timeout: 9000,
        data: encodeURIComponent($('#nicknameInput').val()),
        contentType: "text/xml",
        dataType: "text",
        headers: {
            "X-PGB-ACCESS-TOKEN": token
        },
        cache: false,
        success: function (response) {
            $('#nicknameButton').text("Nickname changed!");
        },
        error: function () {
            $('#nicknameButton').text("Failed to change nickname!");
        }
    });
}

function Pokemoncommand(action) {
    $.ajax({
        url: getUrl() + "pokemon/" + selectedPokemon.id + "/" + action,
        type: 'POST',
        timeout: 9000,
        data: encodeURIComponent($('#nicknameInput').val()),
        contentType: "text/xml",
        dataType: "text",
        headers: {
            "X-PGB-ACCESS-TOKEN": token
        },
        cache: false,
        success: function (response) {
            console.log(response);
			Materialize.toast("('" + action + "') Succeeded", 1000);
            //returnToList();
			getAllPokemon();
			editPokemonModal(selectedPokemon.id);
        },
        error: function () {
            Materialize.toast("Poke Action ('" + action + "') Failed", 1000);
        }
    });
}

/**
 Inventory...
 */
function getItems() {
    $.ajax({
        url: getUrl() + "items",
        type: 'GET',
        timeout: 9000,
        headers: {
            "X-PGB-ACCESS-TOKEN": token
        },
        cache: false,
        success: function (response) {
            console.log(response);
            pokeItems = response;
            drawInventory();
            Materialize.toast("Inventory list refreshed!", 1000);
        },
        error: function () {
            Materialize.toast("Failed to retrieve inventory!", 1000);
        }
    });
}

function dropItems(itemid, quantity) {
    $.ajax({
        url: getUrl() + "item/" + itemid + "/drop/" + quantity,
        type: 'DELETE',
        timeout: 9000,
        headers: {
            "X-PGB-ACCESS-TOKEN": token
        },
        cache: false,
        success: function (response) {
            console.log(response);
            getItems();
        },
        error: function (e) {
            Materialize.toast("Drop Items ('" + itemid + "','" + quantity + "') Failed", 1000);
        }
    });
}

function drawInventory() {
    $("#invenList").html('');
    var pokeItemsOrdered = ["ITEM_INCENSE_ORDINARY", "ITEM_LUCKY_EGG",
        "ITEM_POTION", "ITEM_SUPER_POTION", "ITEM_HYPER_POTION", "ITEM_MAX_POTION",
        "ITEM_REVIVE", "ITEM_MAX_REVIVE",
        "ITEM_POKE_BALL", "ITEM_GREAT_BALL", "ITEM_ULTRA_BALL", "ITEM_MASTER_BALL",
        "ITEM_RAZZ_BERRY", "ITEM_TROY_DISK",
        "ITEM_INCUBATOR_BASIC_UNLIMITED", "ITEM_INCUBATOR_BASIC"]

    for (y = 0; y < pokeItemsOrdered.length; y++)
        for (i = 0; i < pokeItems.length; i++) {
            if (pokeItems[i].itemName != pokeItemsOrdered[y] && jQuery.inArray(pokeItems[i].itemName, pokeItemsOrdered) != -1) continue;
            if (pokeItems[i].count == 0) continue;
            var itemName; //my banana is bigger than yours
            var use = null;
            var drop = null;
            switch (pokeItems[i].itemName) {
                case "ITEM_REVIVE":
                    itemName = "Revive";
                    drop = "dropItems(" + pokeItems[i].itemId + ", 1)";
                    break;
                case "ITEM_LUCKY_EGG":
                    itemName = "Lucky Egg";
                    use = "Botcommand('useLuckyEgg')";
                    drop = "dropItems(" + pokeItems[i].itemId + ", 1)";
                    break;
                case "ITEM_RAZZ_BERRY":
                    itemName = "Razz Berry";
                    drop = "dropItems(" + pokeItems[i].itemId + ", 1)";
                    break;
                case "ITEM_INCUBATOR_BASIC":
                    itemName = "Basic Incubator";
                    drop = "dropItems(" + pokeItems[i].itemId + ", 1)";
                    break;
                case "ITEM_GREAT_BALL":
                    itemName = "Great Ball";
                    drop = "dropItems(" + pokeItems[i].itemId + ", 1)";
                    break;
                case "ITEM_TROY_DISK":
                    itemName = "Lure Module";
                    drop = "dropItems(" + pokeItems[i].itemId + ", 1)";
                    break;
                case "ITEM_INCUBATOR_BASIC_UNLIMITED":
                    itemName = "Unlimited Incubator";
                    break;
                case "ITEM_POKE_BALL":
                    itemName = "Poke Ball";
                    drop = "dropItems(" + pokeItems[i].itemId + ", 1)";
                    break;
                case "ITEM_HYPER_POTION":
                    itemName = "Hyper Potion";
                    drop = "dropItems(" + pokeItems[i].itemId + ", 1)";
                    break;
                case "ITEM_POTION":
                    itemName = "Potion";
                    drop = "dropItems(" + pokeItems[i].itemId + ", 1)";
                    break;
                case "ITEM_INCENSE_ORDINARY":
                    itemName = "Incense";
                    use = "Botcommand('useIncense')";
                    drop = "dropItems(" + pokeItems[i].itemId + ", 1)";
                    break;
                case "ITEM_SUPER_POTION":
                    itemName = "Super Potion";
                    drop = "dropItems(" + pokeItems[i].itemId + ", 1)";
                    break;
                case "ITEM_MAX_POTION":
                    itemName = "MAX Potion";
                    drop = "dropItems(" + pokeItems[i].itemId + ", 1)";
                    break;
                case "ITEM_ULTRA_BALL":
                    itemName = "Ultra Ball";
                    drop = "dropItems(" + pokeItems[i].itemId + ", 1)";
                    break;
                case "ITEM_MAX_REVIVE":
                    itemName = "Max Revive";
                    drop = "dropItems(" + pokeItems[i].itemId + ", 1)";
                    break;
                case "ITEM_MASTER_BALL":
                    itemName = "Master Ball";
                    drop = "dropItems(" + pokeItems[i].itemId + ", 1)";
                    break;
                default:
                    itemName = "***" + pokeItems[i].itemName + "***";
                    break;
            }
            $("#invenList").append("<tr><td><img style = height:50px; src=\"" + icons.item(pokeItems[i].itemName) + "\"></td><td>" + itemName + "</td><td>" + pokeItems[i].count + "</td><td>" + ((drop != null) ? "<button onclick=\"" + drop + "\" class='btn btn-default'>Drop 1</button>" : "") + "</td><td>" + ((use != null) ? "<button onclick=\"" + use + "\" class='btn btn-default'>Use</button>" : "") + "</td></tr>");
        }
}
