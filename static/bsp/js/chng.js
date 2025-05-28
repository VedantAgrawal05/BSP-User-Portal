// // let theme = "light"

// document.addEventListener("DOMContentLoaded", (event) => {
//     console.log("DOM fully loaded and parsed");
//   });
// let flag = 0;



// let themeBtnLight = document.querySelector("#theme-btn-light");
// let themeBtnDark = document.querySelector("#theme-btn-dark");
let ss_d = '/static/garage/styles_base_dark.css';
let ss_l = '/static/garage/styles_base_light.css';

// themeBtnLight.addEventListener("click", swapStyleSheet);
// themeBtnDark.addEventListener("click", swapStyleSheet);

//    //for checking if executed or not
// swapStyleSheet();

// function inits () 
// {    let theme = window.localStorage.getItem("userTheme");
//     console.log(theme);
//     if (!theme) {
//     theme = "light";    //assumes first time user
//     //   sessionStorage.setItem("userTheme", "light");
//     // window.localStorage.setItem("pageStyle", "/static/garage/styles_base_light.css");
//     window.localStorage.setItem("theme", "light");
//     }
//     flag = 1;
// }
// inits()
// window.onload = function() {
//     swapStyleSheet();
//   }

// function swapStyleSheet(){
//     if (!flag) {
//         inits();
//     } 
function setTheme()
    {        let theme = sessionStorage.getItem("userTheme");
            if (!theme) {
                theme = "light";
                console.log(sessionStorage)
            }
        //   document.getElementById('pageStyle').setAttribute('href', sheet);
        //   window.localStorage.setItem("pageStyle", sheet);
        let styleSheet = document.getElementById('pageStyle')

            if (theme === "light") {
                styleSheet.setAttribute('href', ss_l);
                // theme = "dark";
                // sessionStorage.setItem("userTheme", "dark");
                console.log("sset LIGHT");
                console.log(sessionStorage)

            }
            else {
                styleSheet.setAttribute('href', ss_d);
                // theme = "light";
            // sessionStorage.setItem("userTheme", "light");
        console.log("set DARK");
        console.log(sessionStorage)
                
            }}


            //#testing
            function abc() {
                console.log("hello"); console.log("hi")
              }
            //   undefined
            //   document.querySelector("#pageStyle").setAttribute("onload",abc()) 

// function changeTheme() {
//     console.log(theme)
//     if (theme === "light") {

//     }
// }

// let theme = sessionStorage.getItem("userTheme");
// let homeBtn = document.querySelector("#home-btn");
// let themeBtn = document.querySelector("#theme-btn");

// if (theme === "dark") {
//     homeBtn.setAttribute("src", "/static/garage/images/home-light.png");
//     themeBtn.setAttribute("src", "/static/garage/images/theme-light.png");
// }
