const CACHE_NAME = 'mwesh-v2';
const ASSETS = [
  '/',
  '/index.html',
  '/styles.css',
  '/app.js',
  '/manifest.json',
  '/favicon-192x192.png',
  '/favicon-512x512.png',
  '/logo-full-512.png'
];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE_NAME).then(c => c.addAll(ASSETS)).then(()=>self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k=>k!==CACHE_NAME).map(k=>caches.delete(k)))) .then(()=>self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  // API and generated images always network-first
  if (url.pathname.startsWith('/api/') || url.pathname.startsWith('/generated_images/')) {
    e.respondWith(fetch(e.request).catch(()=>caches.match(e.request)));
    return;
  }
  e.respondWith(caches.match(e.request).then(cached => cached || fetch(e.request).then(resp => {
    return caches.open(CACHE_NAME).then(c => { c.put(e.request, resp.clone()); return resp; });
  }).catch(()=>caches.match('/index.html'))));
});
