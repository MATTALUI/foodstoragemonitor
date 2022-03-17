(() => {
  const addItemSection = (event, options={}) => {
    const nextIndex = document.querySelectorAll('.item_set').length;
    const actionButton = nextIndex === 0
      ? (`<button class="w-100 btn btn-success addItemButton">Add Another Item</button>`)
      : (`<button class="w-100 btn btn-danger removeItemButton">Remove This Item</button>`);
    const $input = $(`
      <div class="item_set row">
        <div class="col-sm-2">
          ${actionButton}
        </div>
        <div class="col-sm-8">
          <div class="row  border-bottom border-primary mb-3">
            <div class="col-sm-12">
              <div class="form-group ui-front">
                <input type="text" placeholder="Name" name="item_sets[${nextIndex}][product_name]" class="form-control product_name autocomplete" required>
              </div>
            </div>
            <div class="col-sm-6">
              <div class="form-group">
                <input type="date" placeholder="Expiration Date" name="item_sets[${nextIndex}][expiration]" class="form-control expiration" required>
              </div>
            </div>
            <div class="col-sm-6">
              <div class="form-group">
                <input type="number" placeholder="Quantity" name="item_sets[${nextIndex}][quantity]" class="form-control quantity" required min=1 step=1>
              </div>
            </div>
            <div class="col-sm-12">
              <div class="form-group">
                <textarea placeholder="Description" name="item_sets[${nextIndex}][description]" class="form-control description"></textarea>
              </div>
            </div>
          </div>
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
        product_name: $(ele).find('.product_name').val(),
        expiration: $(ele).find('.expiration').val(),
        quantity: $(ele).find('.quantity').val(),
        description: $(ele).find('.description').val(),
      }));

    fetch('/storage-items', {
      method: 'POST',
      body: JSON.stringify(data),
    })
    .then(res => res.json())
    .then(success => {
      setTimeout(() => {
        // Why timeout? I created this beautiful spinner; you're going to look at it!
        window.location.href = '/storage-items';
      }, 1000);
    })
    .catch(console.error);

  };

  const preventDefaultAndHandle = handler => event => {
    event.preventDefault();
    handler(event);
  };

  $(document).on('click', '.addItemButton', preventDefaultAndHandle(addItemSection));
  $(document).on('click', '.removeItemButton', preventDefaultAndHandle(removeItemSelection));
  $('.saveItemsButton').on('click', preventDefaultAndHandle(saveItems));
  addItemSection();
})();
