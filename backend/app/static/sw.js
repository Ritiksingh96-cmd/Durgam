// DURGAM Service Worker for Offline PWA Support & Cache Resilience
const CACHE_NAME = 'durgam-static-v1';
const ASSETS_TO_CACHE = [
  '/static/index.html',
  '/static/citizen.html',
  '/static/bank.html',
  '/static/police.html',
  '/static/telecom.html',
  '/static/fiu.html',
  '/static/judiciary.html',
  '/static/login.html',
  '/static/academy.html',
  '/static/style.css',
  '/static/app.js',
  '/static/images/ashok_stambh.jpg'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(ASSETS_TO_CACHE);
    })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    }).catch(() => {
      return caches.match('/static/index.html');
    })
  );
});
