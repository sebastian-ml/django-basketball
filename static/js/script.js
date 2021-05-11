const form = document.querySelector('#add-stats');
const games = form.querySelector('#id_game');
const players = form.querySelector('#id_player');

function getTeamsFromSelectedGame(games) {
    const selectedGame = games.options[games.selectedIndex].text;
    const separatorIndex = selectedGame.indexOf('|');
    const spaceIndex = selectedGame.indexOf(' ');
    const teams = selectedGame
        .slice(spaceIndex + 1, separatorIndex - 1)
        .split(' vs ');

    return teams;
}

function filterPlayersOptions([team1, team2], players) {
    const allPlayers = [...players.options];
    let isFirstVisibleSelected = false;

    allPlayers.forEach(player => {
        player.hidden = !(player.text.includes(team1) || player.text.includes(team2));

        // Mark first visible option as selected
        if (isFirstVisibleSelected === false) {
            if (player.hidden === false) {
                player.selected = true;
                isFirstVisibleSelected = true;
            }
        }
    });
}

games.addEventListener('change', () => {
    const teams = getTeamsFromSelectedGame(games);
    filterPlayersOptions(teams, players);
});
