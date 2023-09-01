//1 
let BASE_URL = "http://numbersapi.com";

async function get_number() {
    let number_facts = await axios.get(`${BASE_URL}/3?json`);
    console.log(number_facts.data.text); 
}

get_number();

//2
async function get_numbers() {
    let number_facts = await axios.get(`${BASE_URL}/1..3?json`);
    for (let i = 1; i < 4; i++) {
        let paragraph = document.createElement('p');
        paragraph.innerHTML = number_facts.data[i];
        document.body.appendChild(paragraph);
    }
}

get_numbers()

// 3 
async function get_fav_facts() {
    let number_list = await Promise.all([
        axios.get(`${BASE_URL}/3?json`),
        axios.get(`${BASE_URL}/3?json`),
        axios.get(`${BASE_URL}/3?json`),
        axios.get(`${BASE_URL}/3?json`)
    ]);
    for (let fact of number_list) {
        let listItem = document.createElement('li');
        listItem.innerHTML = fact.data.text;
        document.body.appendChild(listItem);
    }
}

get_fav_facts();