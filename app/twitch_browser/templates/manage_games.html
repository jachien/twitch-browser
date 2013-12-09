<html>
<head>
    <title>Manage Games - Twitch Browser</title>
    <script src="/static/js/jquery-1.9.1.js"></script>
    <script src="/static/js/jquery-ui-1.10.3.custom.min.js"></script>
    <link rel="stylesheet" href="/static/css/smoothness/jquery-ui-1.10.3.custom.min.css"/>

    <style>
        body {
            font: 12px Helvetica,Arial,sans-serif;
            background-color: #dddddd;
        }
        .ui-autocomplete-loading {
            background: white url('/static/css/smoothness/images/ui-anim_basic_16x16.gif') right center no-repeat;
        }
        #game { width: 25em; }
        #games td {
            padding: 2px 16px 2px 16px;
        }
    </style>

    <!-- autocomplete js modified from http://jqueryui.com/autocomplete/#remote-jsonp -->
    <script>
        $( document ).ready(function() {
            renderGames();
        });

        $(function() {
            $( "#game" ).autocomplete({
                source: function( request, response ) {
                    $.ajax({
                        url: "https://api.twitch.tv/kraken/search/games",
                        dataType: "jsonp",
                        data: {
                            q: request.term,
                            type: "suggest"
                        },
                        success: function( data ) {
                            var games = data.games;
                            games.sort(function(a, b) {
                                return b["popularity"] - a["popularity"];
                            });
                            response($.map(games, function( item ) {
                                return {
                                    label: item.name,
                                    value: item.name
                                }
                            }));
                        }
                    });
                },
                minLength: 1,
                delay: 200,
                select: function( event, ui ) {
                    addGame(ui.item.label);
                    renderGames();
                },
                open: function() {
                    $( this ).removeClass( "ui-corner-all" ).addClass( "ui-corner-top" );
                },
                close: function() {
                    $( this ).removeClass( "ui-corner-top" ).addClass( "ui-corner-all" );
                }
            });
        });

        function writeGamesCookie(games) {
            var new_encoded_games = encodeGames(games);
            document.cookie = "games=" + new_encoded_games + "; max-age=2147483647; path=/";
        }

        function addGame(game) {
            var games = readGamesCookie();
            var found = false;
            for (var i=0; i < games.length; i++) {
                if (games[i] == game) {
                    found = true;
                }
            }
            if (!found) {
                games.push(game);
                writeGamesCookie(games);
            }
        }

        function removeGame(game) {
            var games = readGamesCookie();
            for (var i=0; i < games.length; i++) {
                if (games[i] == game) {
                    games.splice(i, 1);
                    break;
                }
            }
            writeGamesCookie(games);
        }

        function readGamesCookie() {
            var encoded_games = readEncodedGames();
            return decodeGames(encoded_games);
        }

        function readEncodedGames() {
            var nameEQ = "games=";
            var ca = document.cookie.split(';');
            for(var i=0;i < ca.length;i++) {
                var c = ca[i];
                while (c.charAt(0)==' ') c = c.substring(1,c.length);
                if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
            }

            var hardcoded_games = ["Dota 2", "StarCraft II: Heart of the Swarm", "Dark Souls"];
            writeGamesCookie(hardcoded_games);
            return encodeGames(hardcoded_games);
        }

        function decodeGames(cookieValue) {
            if (cookieValue.length == 0) {
                return [];
            }
            var games = cookieValue.split(':');
            return $.map(games, function(game) {
                return decodeURIComponent(game);
            });
        }

        function encodeGames(games) {
            games.sort(function(a, b) {
                return a.toLocaleLowerCase().localeCompare(b.toLocaleLowerCase());
            });
            var encoded_game_array = $.map(games, function(game) {
                return encodeURIComponent(game);
            });
            return encoded_game_array.join(":");
        }

        function renderGames() {
            var encoded_games = readEncodedGames();
            var games = decodeGames(encoded_games);
            $("#games").empty().append("<table>");
            if (games.length > 0) {
                for (var i=0; i < games.length; i++) {
                    $("#games").append('<tr><td>' + games[i] + '</td><td><a href="#" onclick="removeGame(\'' + games[i] + '\'); renderGames();">remove</a></td></tr>');
                }
            } else {
                $("#games").append("<tr><td>You don't have any games saved. Add some using the input box at the top!</td></tr>");
            }

            $("#games").append("</table>");
        }
    </script>
</head>
<body>
<div style="margin-bottom: 10px;"><a href="/">Browse Live Streams</a></div>
<div>
    <label for="game">Add Game: </label>
    <input id="game">
</div>
<div id="games_container">
    <h2>My Games</h2>
    <div id="games"></div>
</div>
</body>
</html>