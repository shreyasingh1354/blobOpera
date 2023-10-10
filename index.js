function callRunhand() {
  fetch('http://127.0.0.1:5000/run_hand')
      .then(response => {
          if (response.ok) {
              return response.text();
          } else {
              throw new Error(`HTTP Error: ${response.status}`);
          }
      })
      .then(data => {
          console.log(data); // Output the response from the Flask server
          alert(data); // Display the response as an alert
      })
      .catch(error => {
          console.error(error); // Handle any errors that occur during the request
          alert('An error occurred while executing Opera.py.');
      });
}

function callRunOpera() {
  fetch('http://127.0.0.1:5000/run_opera')
      .then(response => {
          if (response.ok) {
              return response.text();
          } else {
              throw new Error(`HTTP Error: ${response.status}`);
          }
      })
      .then(data => {
          console.log(data); // Output the response from the Flask server
          alert(data); // Display the response as an alert
      })
      .catch(error => {
          console.error(error); // Handle any errors that occur during the request
          alert('An error occurred while executing Opera.py.');
      });
}


async function  fe() {
  let response = await fetch("http://127.0.0.1:5000/");

  if (response.ok) { // if HTTP-status is 200-299
  // get the response body (the method explained below)
  let json = await response.json();
} else {
  alert("HTTP-Error: " + response.status);
}
  
}
// function playMusic() {
//     const musicFileInput = document.getElementById('musicFile');
//     const musicPlayer = document.getElementById('musicPlayer');

//     const selectedFile = musicFileInput.files[0];

//     if (selectedFile) {
//         const objectURL = URL.createObjectURL(selectedFile);
//         musicPlayer.src = objectURL;
//         musicPlayer.play();
//     } else {
//         alert('Please select a music file.');
//     }
// };