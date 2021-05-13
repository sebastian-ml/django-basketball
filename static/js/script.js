const form = document.querySelector('#add-stats');
const games = form.querySelector('#id_game');
const players = form.querySelector('#id_player');
const seasons = form.querySelector('#id_year');

function getSelectedSeason(seasons) {
    if (seasons.value === 'Wszystkie') {
        return '';
    }
    return seasons.value;
}

function getTeamsFromSelectedGame(games) {
    const selectedGame = games.options[games.selectedIndex].text;
    const separatorIndex = selectedGame.indexOf('|');
    const spaceIndex = selectedGame.indexOf(' ');
    const teams = selectedGame
        .slice(spaceIndex + 1, separatorIndex - 1)
        .split(' vs ');

    return teams;
}

function filterSelect(selectNode, args) {
    const allOptions = [...selectNode.options];
    let isFirstVisibleSelected = false;

    allOptions.forEach(option => {
        option.hidden = !(option.text.split(' ').some(text => {
            return args.some(str => text.includes(str));
        }));

        // Mark first visible option as selected
        if (isFirstVisibleSelected === false) {
            if (option.hidden === false) {
                option.selected = true;
                isFirstVisibleSelected = true;
            }
        }
    });
}

function updatePlayersSelect() {
    const teams = getTeamsFromSelectedGame(games);
    filterSelect(players, teams);
}

function updateGamesSelect() {
    const season = getSelectedSeason(seasons);
    filterSelect(games, [season]);
}

games.addEventListener('change', updatePlayersSelect);

seasons.addEventListener('change', () => {
    updateGamesSelect();
    updatePlayersSelect();
});
