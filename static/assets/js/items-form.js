(() => {
  const scannerModal = new bootstrap.Modal(document.getElementById('scanner-modal'));
  let upcLookupData = null;
  let scannerEnabled = window.location.protocol == 'https:';
  let itemSetSelection = null;
  let itemSet = null;
  try {
    itemSet = JSON.parse($('meta[name="item-set-preload"]').attr('content'));
  } catch(e){}
  const editMode = !!itemSet;
  const addItemSection = (event, options={}) => {
    const itemSet = options.itemSet || {
      id: null,
      product_name: '',
      description: '',
      expiration: '',
      quantity: '',
    };
    const nextIndex = document.querySelectorAll('.item_set').length;
    const scannerButton = `
      <span class="input-group-text clickable scanner">
        <i class="fas fa-scanner"></i>
      </span>`;
    const $input = $(`
      <div class="item_set row">
        ${itemSet.id ? `<input class="id" type="hidden" name="id" value="${itemSet.id}">` : ''}
        <div class="col-sm-10">
          <div class="row  border-bottom border-primary mb-3">
            <div class="col-sm-12">
              <div class="form-group ui-front input-group">
                <input type="text" placeholder="Name" name="item_sets[${nextIndex}][product_name]" class="form-control product_name autocomplete" value="${itemSet.product_name}" required>
                ${scannerEnabled ? scannerButton : ''}
              </div>
            </div>
            <div class="col-sm-6">
              <div class="form-group">
                <input type="date" placeholder="Expiration Date" name="item_sets[${nextIndex}][expiration]" class="form-control expiration" value="${itemSet.expiration}" required>
              </div>
            </div>
            <div class="col-sm-6">
              <div class="form-group">
                <input type="number" placeholder="Quantity" name="item_sets[${nextIndex}][quantity]" class="form-control quantity" required min=1 step=1 value="${itemSet.quantity}">
              </div>
            </div>
            <div class="col-sm-12">
              <div class="form-group">
                <textarea placeholder="Description" name="item_sets[${nextIndex}][description]" class="form-control description">${itemSet.description}</textarea>
              </div>
            </div>
          </div>
        </div>
        <div class="col-sm-2">
          ${editMode ? '' : '<button class="w-100 btn btn-danger removeItemButton">Remove This Item</button>'}
        </div>
      </div>
    `);

    $(document.forms[0]).append($input);
    $('.autocomplete').autocomplete({
      source: "/products.json",
    });
  };

  const setHasError = ($ele, hasError) => {
    if (hasError) {
      $ele.addClass('is-invalid');
    } else {
      $ele.removeClass('is-invalid');
    }
  }

  const validateForm = () => {
    let valid = true; // Innocent until proven guilty!

    $('.product_name').each((i, ele) => {
      const $ele = $(ele);
      // Just has to have a value; go hog wild!
      const eleValid = !!$ele.val();
      valid = valid && eleValid;
      setHasError($ele, !eleValid);
    });

    $('.quantity').each((i, ele) => {
      const $ele = $(ele);
      // Needs value, and must be a positive number
      const eleValid = !!$ele.val() && !isNaN(+$ele.val()) && +$ele.val() > 0;
      valid = valid && eleValid;
      setHasError($ele, !eleValid);
    });

    $('.expiration').each((i, ele) => {
      const $ele = $(ele);
      // Needs value, and must be properly formatted date
      const eleValid = !!$ele.val() &&
      (
        !!$ele.val().match(/^\d{1,2}\/\d{1,2}\/\d{1,}$/) || // mm/dd/yyyy
        !!$ele.val().match(/^\d{4}-\d{2}-\d{2}$/) // yyyy-mm-dd
      );
      valid = valid && eleValid;
      setHasError($ele, !eleValid);
    });

    return valid;
  }

  const toggleSpinner = (event) => {
    $('.loader').toggleClass('d-flex').toggleClass('d-none');
    $('form').closest('.row').toggleClass('d-none');
  };

  const removeItemSelection = (event, options={}) => $(event.target).closest('.item_set').remove();

  const saveItems = (event, options={}) => {
    if (!validateForm()) {
      $('.is-invalid').first().focus();
      return;
    }
    toggleSpinner();
    const data = Array
      .from(document.querySelectorAll('.item_set'))
      .map(ele => ({
        id: $(ele).find('.id').val(),
        product_name: $(ele).find('.product_name').val(),
        product_upc: $(ele).find('.product_upc').val(), // May not even exist
        expiration: $(ele).find('.expiration').val(),
        quantity: $(ele).find('.quantity').val(),
        description: $(ele).find('.description').val(),
      }));

    fetch(`/storage-items/${editMode ? itemSet.id + '/' : ''}`, {
      method: 'POST',
      body: JSON.stringify(data),
    })
    .then(res => res.json())
    .then(success => {
      setTimeout(() => {
        // Why timeout? I created this beautiful spinner; you're going to look at it!
        window.location.href = '/storage-items/';
      }, 1000);
    })
    .catch(console.error);

  };

  const setScannerLoading = () => $('#scanner-spinner').removeClass('d-none').addClass('d-flex');
  const stopScannerLoading = () => $('#scanner-spinner').addClass('d-none').removeClass('d-flex');

  const closeScanner = event => {
    itemSetSelection = null;
    upcLookupData = null;
    Quagga.stop();
    $('#scanner-stream').empty();
    scannerModal.hide();
    setScannerLoading();
  };

  const openScanner = event => {
    itemSetSelection = $(event.target).closest('.item_set');
    scannerModal.show();
    setScannerLoading();
    setTimeout(() => {
      const quagaaConfig = {
        inputStream : {
          name : "Live",
          type : "LiveStream",
          target: document.querySelector('#scanner-stream'),
        },
        decoder : {
          readers : [
            'upc_reader',
          ]
        }
      };
      Quagga.init(quagaaConfig, err => {
        if (err) {
          console.error(err);
          scannerEnabled = false;
          $('.scanner').remove();
          return;
        }

        stopScannerLoading();
        Quagga.onDetected((data) => {
          const upc = data.codeResult.code;

          Quagga.stop()
          $('#scanner-stream').empty();
          setScannerLoading();
          fetch(`/products.json/?upc=${upc}`)
            .then(res => res.json())
            .then((productData) => {
              setTimeout(() => {
                console.log(productData);
                stopScannerLoading();
                if (productData.error) {
                  const $warning = $(`
                    <div>
                      <div>
                        <p class="h3 text-center">An error has occured. We were unable to ind information for code: ${data.codeResult.code}</p>
                      </div>
                      <div class="d-flex justify-content-center">
                        <button class="btn btn-primary retry">Retry</button>
                      </div>
                    </div>
                  `);
                  $warning.find('.retry').on('click', (_) => {
                    closeScanner(event);
                    setTimeout(() => openScanner(event), 400);

                  });
                  $('#scanner-stream').html($warning);
                } else if (productData.is_new) {
                  upcLookupData = productData;
                  const $confirm = $(`
                    <div>
                      <div>
                        <p class="h3 text-center">${productData.product.name}</p>
                        <p class="text-center">Is this correct?</p>
                      </div>
                      <div class="d-flex justify-content-between">
                        <button class="btn btn-secondary retry">No, Retry.</button>
                        <button class="btn btn-primary confirm">Yes!</button>
                      </div>
                    </div>
                  `);
                  $confirm.find('.confirm').on('click', (_) => {
                    itemSetSelection.find('.product_name').val(productData.product.name);
                    itemSetSelection.append(`<input type="hidden" class="product_upc" value="${data.codeResult.code}">`);
                    closeScanner();
                  });
                  $confirm.find('.retry').on('click', (_) => {
                    closeScanner(event);
                    setTimeout(() => openScanner(event), 400);

                  });
                  $('#scanner-stream').html($confirm);
                } else {
                  itemSetSelection.find('.product_name').val(productData.product.name);
                  closeScanner();
                }
              }, 1000);
            })
            .catch(console.error);
        });
        Quagga.start();
      });
    }, 1500);
  };

  const preventDefaultAndHandle = handler => event => {
    event.preventDefault();
    handler(event);
  };


  $(document).on('click', '.addItemButton', preventDefaultAndHandle(addItemSection));
  $(document).on('click', '.removeItemButton', preventDefaultAndHandle(removeItemSelection));
  $(document).on('click', '.scanner', preventDefaultAndHandle(openScanner));
  $('.saveItemsButton').on('click', preventDefaultAndHandle(saveItems));
  $('.close-modal').on('click', preventDefaultAndHandle(closeScanner));

  if (editMode) {
    addItemSection(null, {
      itemSet
    });
  } else {
    addItemSection();
  }
})();
