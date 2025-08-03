self.addEventListener('install', function(event) {
  console.log('Service Worker installing...');
  event.waitUntil(
    caches.open('cloudie-cache').then(function(cache) {
      return cache.addAll([
        '/',
        '/index.html',
        '/script.js',
        '/service-worker.js',
        '/manifest.json',
        '/icon.png' // Make sure to add your icon or images if needed
      ]);
    })
  );
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request).then(function(response) {
      return response || fetch(event.request);
    })
  );
});
