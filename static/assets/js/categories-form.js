(() => {
  const toggleSpinner = (event) => {
    $('.loader').toggleClass('d-flex').toggleClass('d-none');
    $('form').closest('.row').toggleClass('d-none');
  };

  const saveCategory = (event, options={}) => {
    toggleSpinner();
    const data = {
      id: $('input[name="id"]').val(),
      name: $('input[name="name"]').val(),
      bg_hex: $('input[name="bg_hex"]').val(),
      text_hex: $('input[name="text_hex"]').val(),
    };

    fetch(`/categories/${!!data.id ? `${data.id}/`: ''}`, {
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

  const displayChipPreview = () => {
    $('#chip-preview').empty();
    const name = $('input[name="name"]').val();
    const bg = $('input[name="bg_hex"]').val();
    const text = $('input[name="text_hex"]').val();
    if (!name || !bg || !text) { return; }
    $('#chip-preview').append(`<span class="badge" style="background-color: ${bg}; color: ${text}">${name}</span>`);
  }

  const preventDefaultAndHandle = handler => event => {
    event.preventDefault();
    handler(event);
  };

  $('.saveCategoryButton').on('click', preventDefaultAndHandle(saveCategory));
  $('form').on('change', preventDefaultAndHandle(displayChipPreview));
  displayChipPreview();
})();
