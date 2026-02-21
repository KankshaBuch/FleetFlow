/* Initialize Storage */

function initializeStorage() {
  if (!localStorage.getItem("vehicles")) {
    localStorage.setItem("vehicles", JSON.stringify([]));
  }
  if (!localStorage.getItem("drivers")) {
    localStorage.setItem("drivers", JSON.stringify([]));
  }
  if (!localStorage.getItem("trips")) {
    localStorage.setItem("trips", JSON.stringify([]));
  }
  if (!localStorage.getItem("expenses")) {
    localStorage.setItem("expenses", JSON.stringify([]));
  }
}

initializeStorage();

/* Generic Helpers */

function getData(key) {
  return JSON.parse(localStorage.getItem(key)) || [];
}

function saveData(key, data) {
  localStorage.setItem(key, JSON.stringify(data));
}