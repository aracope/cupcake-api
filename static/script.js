$(async function () {
    const BASE_URL = "/api/cupcakes";
  
    function generateCupcakeHTML(cupcake) {
      return `
        <li data-id="${cupcake.id}">
          ${cupcake.flavor} (${cupcake.size}) - Rating: ${cupcake.rating}
          <br>
          <img src="${cupcake.image}" alt="${cupcake.flavor}" style="height: 50px;">
        </li>`;
    }
  
    async function getCupcakes() {
      const res = await axios.get(BASE_URL);
      for (let cupcake of res.data.cupcakes) {
        $("#cupcake-list").append(generateCupcakeHTML(cupcake));
      }
    }
  
    $("#cupcake-form").on("submit", async function (evt) {
      evt.preventDefault();
  
      const flavor = $("input[name='flavor']").val();
      const size = $("input[name='size']").val();
      const rating = $("input[name='rating']").val();
      const image = $("input[name='image']").val() || null;
  
      const cupcakeData = { flavor, size, rating, image };
  
      const res = await axios.post(BASE_URL, cupcakeData);
  
      $("#cupcake-list").append(generateCupcakeHTML(res.data.cupcake));
      $("#cupcake-form").trigger("reset");
    });
  
    await getCupcakes();
  });
  
  $("#search-form").on("submit", async function(evt) {
    evt.preventDefault();
    const searchTerm = $("#search-input").val();
  
    const response = await axios.get("/api/cupcakes", {
      params: { search: searchTerm }
    });
  
    $("#cupcake-list").empty();
    for (let cupcake of response.data.cupcakes) {
      $("#cupcake-list").append(makeCupcakeHTML(cupcake));
    }
  });
  