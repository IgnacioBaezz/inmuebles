document.addEventListener("DOMContentLoaded", function() {
    const regionSelect = document.getElementById("id_region");
    const communeSelect = document.getElementById("id_commune");
    const comunasPorRegion = window.comunasPorRegion;

    regionSelect.addEventListener("change", function() {
        const regionId = this.value;
        communeSelect.innerHTML = "<option value=''>Seleccione una comuna</option>";

        if (regionId && comunasPorRegion[regionId]) {
            comunasPorRegion[regionId].forEach(function(comuna) {
                const option = document.createElement("option");
                option.value = comuna.id;
                option.textContent = comuna.nombre;
                communeSelect.appendChild(option);
            });
        }
    });
});