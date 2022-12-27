(async () => {
  // Functionality for resetting the LED from the UI
  const resetLED = (event) => {
    event.preventDefault();

    const host = window.location.host;
    // We can just fire and forget these. If you're resetting the user feedback
    // will come when they see the LED on the Machine turn off. Also, we send
    // it to both protocols because the servers for both are still separated.
    fetch(`https://${host}/cron/reset/`, { method: 'POST' });
    fetch(`http://${host}/cron/reset/`, { method: 'POST' });
  };

  // Functionality for running a quick LED test
  const testLED = (event) => {
    event.preventDefault();
    fetch(`/cron/test/`, { method: 'POST' });
  }

  document.querySelector('#clear-led').addEventListener('click', resetLED);
  document.querySelector('#test-led').addEventListener('click', testLED);
})();

(async () => {
  let deferredPrompt = null;

  // Register the Service Worker and Prepare PWA Schtuff.
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', function () {
      navigator.serviceWorker.register('/service-worker.js');
    });
  }

  window.addEventListener('beforeinstallprompt', function (deferredPrompt) {
    const installButton = document.createElement('a');
    installButton.innerHTML = 'Install App';
    installButton.href = ""
    installButton.addEventListener('click', function(e) {
      e.preventDefault();
      deferredPrompt.prompt();
      console.log('clicked');
    })
    document.querySelector('footer div').appendChild(installButton);
  });
})();
0