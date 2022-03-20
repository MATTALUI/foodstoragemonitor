(() => {
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

  const deleteItemSet = (event) => {
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


  $('.increment').on('click', changeItemSet('increment'));
  $('.decrement').on('click', changeItemSet('decrement'));
  $('.delete').on('click', deleteItemSet);
})();
