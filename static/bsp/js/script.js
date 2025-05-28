let logoutButton = document.querySelector("#logout-btn");
// logoutButton.addEventListener("click", confirmLogout);

//below was used for theme

// themeBtn = document.querySelector("#theme-btn");

// themeBtn.addEventListener("click", swapStyleSheet);


//    //for checking if executed or not

//     theme = sessionStorage.getItem("userTheme");
//     console.log(theme);
//     if (!theme) {
//     theme = "light";    //assumes first time user
//     console.log(sessionStorage)

//     sessionStorage.setItem("userTheme", "light");
//     console.log(sessionStorage)
//     }

//   let header = document.querySelector("#header");
//    homeBtn = document.querySelector("#home-btn");
//   let body = document.querySelector("body");


// function swapStyleSheet(){

     
//   header.style.transitionDuration="1s";
//   homeBtn.style.transitionDuration="1s";
//   themeBtn.style.transitionDuration="1s";

//   logoutButton.style.transitionDuration="1s";
//   body.style.transitionDuration="1s";

//     let theme = sessionStorage.getItem("userTheme");


//     if (theme === "light") {
//         document.getElementById('pageStyle').setAttribute('href', ss_d);
//         body.style.color="white";
//         body.style.backgroundColor="#030E22";
//         homeBtn.setAttribute("src", "/static/garage/images/home-light.png");
//     themeBtn.setAttribute("src", "/static/garage/images/theme-light.png");

//         logoutButton.style.color = "white";
//         theme = "dark";
//         sessionStorage.setItem("userTheme", "dark");


//     }
//     else {
//         document.getElementById('pageStyle').setAttribute('href', ss_l);
//         body.style.color="black";
//         body.style.backgroundColor="#CDE6F5";
//         homeBtn.setAttribute("src", "/static/garage/images/home-dark.png");
//     themeBtn.setAttribute("src", "/static/garage/images/theme-dark.png");

//         logoutButton.style.color = "black";
//         theme = "light";
//         sessionStorage.setItem("userTheme", "light");

//     }
         

// }



//below ones are needed
// function confirmLogout() {
//   let accepted =  confirm("Are you sure you wish to logout?");
//   if (accepted) return true;
//   else return false;
// }

logoutButton.addEventListener("click", function(event) {
  let accepted = confirm("Are you sure you wish to logout?");
  if (!accepted) {
    event.preventDefault(); //  This stops the form from submitting
  }
});




function confirmDel() {
  let agree = confirm("Are you sure you wish to delete record?");
  if (agree) return true;
  else return false;
}

function enablefield(checkbox, tochange) {
  var element_name = document.getElementById(tochange);
  element_name.disabled = checkbox.checked ? false : true;
  if (!element_name.disabled) {
    element_name.removeAttribute("disabled");
    element_name.focus();
  }
}
function validateForm() {
  // Check if at least one checkbox is selected for the first form
  var checkboxes1 = document.querySelectorAll("#choice1, #choice2, #choice3");
  var atLeastOneChecked1 = Array.from(checkboxes1).some(
    (checkbox) => checkbox.checked
  );
  // Enable or disable the submit button based on checkbox selection for the first form
  var submitButton1 = document.getElementById("submitBtn1");
  submitButton1.disabled = !atLeastOneChecked1;
  // Optional: If you want to provide visual feedback to the user
  if (!atLeastOneChecked1) {
    alert("Please select at least one choice");
    return false; // Prevent form submission
  }

  return true; // Allow form submission
}

//for mod fuel rec bump form
function checkForm(formId) {
  let form = document.getElementById(formId);
  // console.dir(form);
  let choices = form.getElementsByTagName("input");
  //console.log(choices[1],choices[2],choices[3],choices[4])
  let checked = false;
  // console.dir(choices);
  for (let i = 1; i < 4; i++) {
    //simple fix as it also takes the last button as input tag
    //idk why choices are counting from 1 instead of usual 0
    if (choices[i].checked) {
      checked = true;
      break;
    }
  }

  if (!checked) {
    alert("Please select at least one of the given choices!");
    return false; // Prevent form submission
  }

  //return true; // Allow form submission
  form.submit(); //submit form
}

//for mod fuel rec form
function checkForm2(formId) {
  let form = document.getElementById(formId);
  // console.dir(form);
  // let choices = form.getElementsByTagName('input');
  let dateChange = document.querySelector("#frecdt");
  if (!dateChange.value) {
    alert("Please select date of record to change");
    return false;
  }
  let checkBoxes = form.querySelectorAll("#change_date, #change_fuel");
  let valBoxes = form.querySelectorAll("#frecdtnew, #frecvalnew");
  console.dir(checkBoxes, valBoxes);
  let checked = false;
  // console.log(checkBoxes, valBoxes);
  // console.dir(choices);
  for (let i = 0; i < 2; i++) {
    //value starting from 1 here
    if (checkBoxes[i].checked) {
      if (!valBoxes[i].value) {
        alert("Please enter the value for the selected option");
        return false;
      } else {
        checked = true;
        //console.log(valBoxes[i])
        break;
      }
    }
  }
  if (!checked) {
    alert("Please select at least one choice out of the options");
    return false; // Prevent form submission
  }

  //return true; // Allow form submission
  form.submit(); //submit form
  //console.log("succ")
}
