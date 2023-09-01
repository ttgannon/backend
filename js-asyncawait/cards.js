//1
let BASE_URL = 'https://deckofcardsapi.com/api/deck'

async function get_deck() {
    let newDeck = await axios.get(`${BASE_URL}/new/draw/?count=1`);
    console.log(`${newDeck.data.cards[0].value} of ${newDeck.data.cards[0].suit}`)
}

get_deck();

//2

async function pullCards() {
    let newDeck = await axios.get(`${BASE_URL}/new/draw?count=1`);
    let currentDeck = newDeck.data.deck_id;
    let card1 = await axios.get(`${BASE_URL}/${currentDeck}/draw/?count=1`);
    let card2 = await axios.get(`${BASE_URL}/${currentDeck}/draw/?count=1`);
    console.log(`${card1.data.cards[0].value} of ${card1.data.cards[0].suit}, ${card2.data.cards[0].value} of ${card2.data.cards[0].suit}`);
}

pullCards();

// 3 

let currentDeck; 

async function drawCard() {
    if (!currentDeck) {
        let newDeck = await axios.get(`${BASE_URL}/new/draw?count=1`);
        currentDeck = newDeck.data.deck_id;
    }
    
    let card = await axios.get(`${BASE_URL}/${currentDeck}/draw?count=1`)
    let img = document.createElement('img');
    console.log(card.data);
    img.src = card.data.cards[0].image;
    document.body.appendChild(img);
}

document.addEventListener('DOMContentLoaded', async function() {
    let button = document.createElement("button");
    button.innerHTML = "Get a card";
    document.body.appendChild(button);
    button.addEventListener("click", drawCard);
})