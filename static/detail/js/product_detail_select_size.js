                                            $(document).ready(function () {
                                                // Инициализация Select2
                                                function initSelect2() {
                                                    $('#size_desc, #packageType, #zeston, #size_sku').select2({
                                                        placeholder: function(){
                                                            return $(this).data('placeholder');
                                                        },
                                                        allowClear: true
                                                    });
                                                }

                                                initSelect2();

                                                // Использование переменной productId, объявленной в HTML шаблоне
                                                console.log(productId);

                                                function updateZestonVisibility(data) {
                                                    console.log("updateZestonVisibility called", data);
                                                    const hasVisibleZeston = data.some(item => item.product_number != null && item.product_number !== '');
                                                    console.log("Has visible Zeston:", hasVisibleZeston);

                                                    if (hasVisibleZeston) {
                                                        $('#zeston').closest('.form-group').show();
                                                    } else {
                                                        $('#zeston').closest('.form-group').hide();
                                                    }
                                                }

                                                function updatePrice(price) {
                                                    $('#price').text(price + ' $'); // Предполагая, что у вашего элемента цены есть id="price"
                                                }

                                                function updateMainImage(imageUrl) {
                                                    $('#main-image').attr('src', imageUrl);
                                                }







                                                // Функция для обновления списка packageType на основе полученных данных
                                                function updatePackageTypeSelect(data) {
                                                    let options = data.length > 2 ? ['<option value="">-</option>'] : [];
                                                    options = options.concat(data.map(item => `<option value="${item.package_type}">${item.package_type}</option>`));

                                                    $('#packageType').empty().append(options.join('')).trigger('change').trigger('select2:updated');
                                                    $('#selected_packageType_input').val($('#packageType').val());
                                                    updateSelectionIndicator('packageType');

                                                }

                                                // Функция для обновления списка Zeston на основе полученных данных
                                                function updateZestonSelect(data) {
                                                    let options = data.length > 1 ? ['<option value="">-</option>'] : [];
                                                    options = options.concat(data.map(item => `<option value="${item.product_number}">${item.product_number}</option>`));
                                                    $('#zeston').empty().append(options.join('')).trigger('change').trigger('select2:updated');
                                                    $('#selected_zeston_input').val($('#zeston').val());
                                                    updateSelectionIndicator('zeston');
                                                }









                                                // Функция для обновления списка Size SKU на основе полученных данных
                                                function updateSizeSkuSelect(data) {

                                                    let options = data.length > 1 ? ['<option value="">-</option>'] : [];
                                                    options = options.concat(data.map(item => `<option value="${item.sku}">${item.sku}</option>`));
                                                    $('#size_sku').empty().append(options.join('')).trigger('change').trigger('select2:updated');
                                                    $('#selected_size_sku_input').val($('#size_sku').val());
                                                    updateSelectionIndicator('size_sku');

                                                }


                                                // Функция для обновления списка Size Description на основе полученных данных


                                                // Функция для обновления списка Size Description на основе полученных данных
                                                function updateSizeDescSelect(data) {
                                                    let options = data.length > 1 ? ['<option value="">-</option>'] : [];
                                                    options = options.concat(data.map(item => `<option value="${item.value}">${item.value}</option>`));

                                                    $('#size_desc').empty().append(options.join('')).trigger('change').trigger('select2:updated');
                                                    $('#selected_size_desc_input').val($('#size_desc').val());
                                                    updateSelectionIndicator('size_desc');

                                                }
                                                                                                function filterData(data, zeston, packageType) {
                                                    return data.filter(item => item.product_number === zeston && item.package_type === packageType);
                                                }



                                                // ... [Аналогичные изменения для других функций]
                                                 $('#packageType, #zeston, #size_sku, #size_desc').on('select2:select select2:unselect', function () {
                                                     updateSelectionIndicator(this.id);
                                                 });



                                                // Если значение в списке packageType изменится, выполнится этот код
                                                $('#packageType').on('select2:select', function () {
                                                    fetch(`/update_based_on_package/${productId}/${$(this).val()}/`)
                                                        .then(response => response.json())
                                                        .then(data => {
                                                            updateZestonSelect(data);
                                                            updateSizeSkuSelect(data);
                                                            updateSizeDescSelect(data);
                                                            updatePackageTypeSelect(data);

                                                        })
                                                        .catch(error => console.error('Error fetching data:', error));
                                                });

                                                $('#zeston, #packageType').on('select2:select', function () {
                                                    let selectedZeston = $('#zeston').val();
                                                    let selectedPackageType = $('#packageType').val();

                                                    if (selectedZeston) {
                                                        fetch(`/update_based_on_product_number/${productId}/${selectedZeston}/${selectedPackageType}/`)
                                                            .then(response => response.json())
                                                            .then(data => {
                                                                let filteredData = filterData(data, selectedZeston, selectedPackageType);
                                                                updateZestonSelect(filteredData, selectedZeston);
                                                                updatePackageTypeSelect(filteredData, selectedPackageType);
                                                                updateSizeSkuSelect(filteredData);
                                                                updateSizeDescSelect(filteredData);

                                                                if (data.length > 0) {
                                                                    if (data[0].image_url) {
                                                                        updateMainImage(data[0].image_url);
                                                                    }
                                                                    if (data[0].price) {
                                                                        updatePrice(data[0].price);
                                                                    }
                                                                }
                                                            })
                                                            .catch(error => console.error('Error fetching data:', error));
                                                    }
                                                });




                                                $('#size_sku').on('select2:select', function () {
                                                    fetch(`/update_based_on_sku/${productId}/${$(this).val()}/`)
                                                        .then(response => response.json())
                                                        .then(data => {
                                                            updateZestonSelect(data);
                                                            updateSizeDescSelect(data);
                                                            updateSizeSkuSelect(data);
                                                            updatePackageTypeSelect(data);
                                                            updateMainImage(data[0].image_url);

                                                        })
                                                        .catch(error => console.error('Error fetching data:', error));
                                                });

                                                $('#size_desc, #packageType').on('select2:select', function () {
                                                    let selectedSizeDesc = $('#size_desc').val();
                                                    let selectedPackageType = $('#packageType').val();

                                                    if (selectedSizeDesc && selectedPackageType) {
                                                        fetch(`/update_based_on_size_and_package/${productId}/${selectedSizeDesc}/${selectedPackageType}/`)
                                                            .then(response => response.json())
                                                            .then(data => {
                                                                updateZestonSelect(data);
                                                                updateSizeSkuSelect(data);
                                                                updateSizeDescSelect(data);
                                                                updatePackageTypeSelect(data);
                                                                if (data.length > 0) {
                                                                    if (data[0].image_url) {
                                                                        updateMainImage(data[0].image_url);
                                                                    }
                                                                    if (data[0].price) {
                                                                        updatePrice(data[0].price);
                                                                    }
                                                                }
                                                            })
                                                            .catch(error => console.error('Error fetching data:', error));
                                                    }
                                                });





                                                        function updateSelectionIndicator(selectElementId) {
                                                            let selectElement = $(`#${selectElementId}`);
                                                            let optionsCount = selectElement.children('option').length;
                                                            let indicator = selectElement.siblings('.selected-mark');

                                                            // Показываем индикатор только если остается ровно один вариант для выбора
                                                            if (optionsCount === 1) {
                                                                indicator.addClass('visible');
                                                            } else {
                                                                indicator.removeClass('visible');
                                                            }
                                                        }

                                            });