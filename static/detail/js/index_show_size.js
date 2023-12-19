$(document).ready(function () {
    // Функция форматирования для стилизации опций
    function formatOption(option) {
        if (!option.id) {
            return option.text;
        }
        var packageType = option.element.getAttribute('data-package-type');
        var sizeValue = option.element.getAttribute('data-size-value');
        var price = option.element.getAttribute('data-price');

        return $(
            '<span style="color: blue;">' + packageType + '</span>' +
            '  / ' +
            '<span style="color: green;">' + sizeValue + '</span>' +
            '  / ' +
            '<span style="color: red;">' + price + ' $</span>)'
        );
    }

    // Используем ту же функцию для форматирования выбранного элемента
    function formatOptionSelection(option) {
        return formatOption(option);
    }

    // Инициализация Select2
    $('.size-select').select2({
        templateResult: formatOption,
        templateSelection: formatOptionSelection,
        placeholder: "Show sizes and prices",
        allowClear: true
    });

    // Функция для обновления цены
    function updatePrice(product_id, size_value) {
        let price = getPrice(product_id, size_value);
        $(`#price-${product_id}`).text(price + ' $');
    }

    // Обработчик события выбора размера
    $('.size-select').on('select2:select', function (e) {
        let selectedSize = $(this).val();
        let productId = $(this).data('product-id');
        updatePrice(productId, selectedSize);
    });
});

// Функция для получения цены
function getPrice(product_id, size_value) {
    // Здесь ваша логика для определения цены
    return 100; // Фиктивная цена
}
