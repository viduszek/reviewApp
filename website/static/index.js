function deleteMovie(movID) {
  fetch("/delete-movie", {
    method: 'POST',
    body: JSON.stringify({ movID: movID }),
  }).then((_res) => {
    window.location.href = "/my-profile";
  });
}

function deleteToWatch(movID) {
  fetch("/delete-to-watch", {
    method: 'POST',
    body: JSON.stringify({ movID: movID }),
  }).then((_res) => {
    window.location.href = "/my-profile";
  });
}