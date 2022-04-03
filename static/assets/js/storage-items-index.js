(() => {
  let selectedModalCategories = [];
  let selectedItemSet = null;
  const modal = new bootstrap.Modal(document.getElementById('category-modal'));
  const managerMap = {
    increment: num => ++num,
    decrement: num => --num,
  };

  const changeItemSet = type => event => {
    const $button = $(event.target);
    const $itemSet = $button.closest('.itemset');
    const itemSetId = $itemSet.data('itemset');
    const reqPath = `/storage-items/${itemSetId}/${type}/`;
    fetch(reqPath, {
      method: 'POST'
    })
    .then(res => res.json())
    .then(success => {
      const previousValue = +$itemSet.find('.quantity').html();
      const nextValue = managerMap[type](previousValue);
      $itemSet.find('.quantity').html(nextValue);
    })
    .catch(console.error);
  };

  const deleteItemSet = event => {
    if (!confirm("This will permanantly remove this item. Are you sure?")) { return; }
    const $button = $(event.target);
    const $itemSet = $button.closest('.itemset');
    const itemSetId = $itemSet.data('itemset');
    fetch(`/storage-items/${itemSetId}/`, {
      method: 'DELETE'
    })
    .then(res => res.json())
    .then(() => window.location.reload())
    .catch(console.error);
  };

  const closeModal = () => {
    selectedModalCategories = [];
    selectedItemSet = null;
    $('#category-manager').val(selectedModalCategories);
    modal.hide();
  }

  const openModal = event => {
    selectedItemSet = $(event.target).closest('.itemset').data('itemset');
    selectedModalCategories = Array.from($(event.target)
      .closest('.itemset')
      .find('.categories')
      .children())
      .map(ele => $(ele).data('category'));
    $('#category-manager').val(selectedModalCategories);
    modal.show();
  }

  const saveCategories = event => {
    return fetch(`/storage-items/${selectedItemSet}/set-categories/`, {
      method: 'POST',
      body: JSON.stringify({
        categories: $('#category-manager').val(),
      }),
    })
    .then(res => res.json())
    .then(categories => {
      const catCont = $(`.itemset[data-itemset="${selectedItemSet}"]`).find('.categories');
      catCont.empty();
      categories.forEach(cat => {
        catCont.append(`<span class="badge category" style="background-color: ${cat.bg_hex}; color: ${cat.text_hex}" data-category="${cat.id}">${cat.name}</span>`);
      });
      closeModal();
    })
    .catch(console.error);
  }


  $('.increment').on('click', changeItemSet('increment'));
  $('.decrement').on('click', changeItemSet('decrement'));
  $('.delete').on('click', deleteItemSet);
  $('.manage-categories').on('click', openModal);
  $('.close-modal').on('click', closeModal);
  $('.save-categories').on('click', saveCategories);
})();
