(() => {
  const deleteCategory = (event) => {
    const $category = $(event.target).closest('.category');
    const catName = $category.find('.name').html();
    const catId = $category.data('category');
    const message = `Are you sure you want to delete the ${catName} category? This can not be undone.`;

    if (!confirm(message)) { return; }

    return fetch(`/categories/${catId}/`, { method: 'DELETE' })
      .then(res => res.json())
      .then(success => {
        if (success) {
          $category.remove();
        }
      })
      .catch(console.error);
  };

  $('.delete').on('click', deleteCategory);
})();
