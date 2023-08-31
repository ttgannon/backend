// // 1
let base = "https://deckofcardsapi.com/api/deck";
// let deck1 = axios.get(`${base}/new/draw/?count=1`);
// deck1
//     .then(response => console.log(response.data.cards[0].code))

// 2

let deck2 = axios.get(`${base}/new/draw`);
let first;
deck2
    .then(response => {
        first = response.data.cards[0];
        let deckId = response.data.deck_id;
        return axios.get(`${base}/${deckId}/draw`)
    })
    .then(response => {
        let second = response.data.cards[0];
        [first, second].forEach(card => {
            console.log(`${card.value.toLowerCase()} of ${card.suit.toLowerCase()}`);
        });
    })

// 3 

document.addEventListener('DOMContentLoaded', () => {
    let button = document.getElementById('button')
    let deckId;

    let deck3 = axios.get(`${base}/new/shuffle/`)
        .then(response => {
            deckId = response.data.deck_id;
        });

    button.addEventListener('click', () => {
        let currentDeck = axios.get(`${base}/${deckId}/draw/`)
        currentDeck
            .then(response => {
                console.log(response.data);
                let cardSrc = response.data.cards[0].image;
                let cardImg = document.createElement('img');
                let cardCont = document.querySelector('p')
                cardImg.src = cardSrc;
                cardCont.appendChild(cardImg)

            })
    })
})
