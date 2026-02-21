const API_URL = "http://127.0.0.1:8000";

document.addEventListener("DOMContentLoaded", () => {
  loadVehicles();
});

async function loadVehicles() {
  const res = await fetch(`${API_URL}/vehicles`);
  const vehicles = await res.json();

  const table = document.getElementById("vehicleTable");
  table.innerHTML = "";

  vehicles.forEach(vehicle => {
    table.innerHTML += `
      <tr class="border-t">
        <td class="px-6 py-4">${vehicle.id}</td>
        <td class="px-6 py-4">${vehicle.name}</td>
        <td class="px-6 py-4">${vehicle.plate}</td>
        <td class="px-6 py-4">${vehicle.max_weight}</td>
        <td class="px-6 py-4">${vehicle.buy_price}</td>
      </tr>
    `;
  });
}

async function addVehicle() {
  const name = prompt("Name");
  const plate = prompt("Plate");
  const max_weight = prompt("Max Weight");
  const buy_price = prompt("Buy Price");

  const url = `${API_URL}/vehicles?name=${name}&plate=${plate}&max_weight=${max_weight}&buy_price=${buy_price}`;

  await fetch(url, {
    method: "POST"
  });

  loadVehicles();
  table.innerHTML += `
  <tr class="border-t">
    <td class="px-6 py-4">${v.id}</td>
    <td class="px-6 py-4 font-medium">${v.name}</td>
    <td class="px-6 py-4">${v.plate}</td>
    <td class="px-6 py-4">${v.max_weight}</td>
    <td class="px-6 py-4">${v.buy_price}</td>
    <td class="px-6 py-4">
      <button onclick="deleteVehicle(${v.id})"
        class="text-red-600">Delete</button>
    </td>
  </tr>
`;
async function deleteVehicle(id) {
  await fetch(`${API_URL}/vehicles/${id}`, {
    method: "DELETE"
  });
  loadVehicles();
}
}
