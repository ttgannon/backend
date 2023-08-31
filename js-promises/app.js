// let url = "http://numbersapi.com"
// let number = 5

// // 1
// axios.get(`${url}/${number}/trivia?json`)
//     .then(response => {
//         console.log(response.data)
// })


// // 2
// document.addEventListener('DOMContentLoaded', () => {
//     axios.get(`${url}/${number}..10/trivia?json`)
//     .then(response => {
//         for (let i = number; i <= 10; i ++) {
//             let paragraph = document.createElement('p');
//             paragraph.innerHTML = `${response.data[i]}`
//             document.body.appendChild(paragraph)
//         }
//     })
// })


// // 3
// let favNums = [1,3,5,7]
// document.addEventListener('DOMContentLoaded', () => {
//     axios.get(`${url}/${favNums}/trivia?json`)
//     .then(response => {
//         for (let item of favNums) {
//             let paragraph = document.createElement('p');
//             paragraph.innerHTML = `${response.data[item]}`
//             document.body.appendChild(paragraph)
//         }
//     })
// })

