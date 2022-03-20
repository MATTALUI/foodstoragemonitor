(() => {
  const toggleSpinner = (event) => {
    $('.loader').toggleClass('d-flex').toggleClass('d-none');
    $('form').closest('.row').toggleClass('d-none');
  };

  const saveCategory = (event, options={}) => {
    console.log('cats');
    toggleSpinner();
    const data = {
      name: $('input[name="name"]').val(),
    };
    // const data = Array
    //   .from(document.querySelectorAll('.item_set'))
    //   .map(ele => ({
    //     product_name: $(ele).find('.product_name').val(),
    //     expiration: $(ele).find('.expiration').val(),
    //     quantity: $(ele).find('.quantity').val(),
    //     description: $(ele).find('.description').val(),
    //   }));

    fetch('/categories/', {
      method: 'POST',
      body: JSON.stringify(data),
    })
    .then(res => res.json())
    .then(success => {
      setTimeout(() => {
        // Why timeout? I created this beautiful spinner; you're going to look at it!
        window.location.href = '/categories/';
      }, 1000);
    })
    .catch(console.error);

  };

  const preventDefaultAndHandle = handler => event => {
    event.preventDefault();
    handler(event);
  };

  $('.saveCategoryButton').on('click', preventDefaultAndHandle(saveCategory));
})();
