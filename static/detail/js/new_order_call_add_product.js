document.addEventListener("DOMContentLoaded", function() {
    const packageTypeSelect = document.getElementById("packageType");
    const zestonSelect = document.getElementById("zeston");
    const sizeSkuSelect = document.getElementById("size_sku");
    const sizeDescSelect = document.getElementById("size_desc");

    function populateSelectOptions(selectElement, options) {
        selectElement.innerHTML = options.map(opt => `<option value="${opt}">${opt}</option>`).join('');
    }

    packageTypeSelect.addEventListener("change", function() {
        fetch(`/api/update_based_on_package_call/${this.value}/`)
        .then(response => response.json())
        .then(data => {
            populateSelectOptions(zestonSelect, data.product_numbers);
            populateSelectOptions(sizeSkuSelect, data.size_skus);
            populateSelectOptions(sizeDescSelect, data.size_descs);
        });
    });

    zestonSelect.addEventListener("change", function() {
    fetch(`/api/update_based_on_product_number_call/${packageTypeSelect.value}/${this.value}/`)
    .then(response => response.json())
    .then(data => {
        populateSelectOptions(sizeSkuSelect, data.size_skus);
        populateSelectOptions(sizeDescSelect, data.size_descs);
    });
});

sizeSkuSelect.addEventListener("change", function() {
    fetch(`/api/update_based_on_sku_call/${packageTypeSelect.value}/${zestonSelect.value}/${this.value}/`)
    .then(response => response.json())
    .then(data => {
        populateSelectOptions(zestonSelect, data.product_numbers);
        populateSelectOptions(sizeSkuSelect, data.size_skus);
        populateSelectOptions(sizeDescSelect, data.size_descs);
    });
});


    sizeDescSelect.addEventListener("change", function() {
        fetch(`/api/update_based_on_size_call/${packageTypeSelect.value}/${zestonSelect.value}/${sizeSkuSelect.value}/${this.value}/`)
        .then(response => response.json())
        .then(data => {
            populateSelectOptions(zestonSelect, data.product_numbers);
            populateSelectOptions(sizeSkuSelect, data.size_skus);
            populateSelectOptions(sizeDescSelect, data.size_descs);
        });
    });
});