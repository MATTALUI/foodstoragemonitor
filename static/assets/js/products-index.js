(() => {
  $('.delete').on('click', (event) => {
    const productId = $(event.target).closest('.product').data('product');
    const quantity = +$(event.target).closest('.product').find('.quantity').html();
    let message = " Are you sure you want to delete this product?"
    if (quantity > 0) {
      message += " This will also delete all " + quantity + " items you have in storage.";
    }
    if (!confirm(message)) { return; }

    return fetch(`/products/${productId}/`, { method: 'DELETE' })
      .then(res => res.json())
      .then(() => {
        $(event.target).closest('.product').remove();
      })
      .catch(console.error);
  });
})();
