const CACHE_NAME = 'gestaofrotas-cache-v2'; // Mude a versão do cache!
const urlsToCache = [
  '/static/img/icons/apple-touch-icon-180x180.png',
  '/static/img/icons/apple-touch-icon-152x152.png',
  '/static/img/icons/apple-touch-icon-144x144.png',
  '/static/img/icons/apple-touch-icon-120x120.png',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('Cache opened');
        return cache.addAll(urlsToCache);
      })
  );
});

// Estratégia "Network first, then cache"
self.addEventListener('fetch', (event) => {
  // Ignora requisições que não são GET
  if (event.request.method !== 'GET') {
    return;
  }

  event.respondWith(
    caches.open(CACHE_NAME).then((cache) => {
      // 1. Tenta buscar da rede primeiro
      return fetch(event.request)
        .then((networkResponse) => {
          // Se a resposta for boa, armazena no cache para uso offline futuro
          if (networkResponse && networkResponse.status === 200) {
            cache.put(event.request, networkResponse.clone());
          }
          // Retorna a resposta fresca da rede
          return networkResponse;
        })
        .catch(() => {
          // 2. Se a rede falhar, busca no cache como fallback
          return cache.match(event.request);
        });
    })
  );
});

// Limpa caches antigos quando um novo service worker é ativado
self.addEventListener('activate', (event) => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});