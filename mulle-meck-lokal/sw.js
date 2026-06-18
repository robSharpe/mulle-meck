/* Service worker för Mulle Meck (PWA).
   Höj versionen för att tvinga ut en ny cache vid uppdatering. */
const VERSION = "mulle-v1";

// Appens "skal" – pre-cachas vid installation så spelet kan startas offline.
const SHELL = [
  "./",
  "./index.html",
  "./bundle.js",
  "./phaser.min.js",
  "./style.css",
  "./manifest.webmanifest",
  "./loading.png",
  "./icons/icon-192.png",
  "./icons/icon-512.png",
  "./icons/icon-180.png"
];

self.addEventListener("install", (e) => {
  e.waitUntil(
    caches.open(VERSION).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== VERSION).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET") return;

  const url = new URL(req.url);
  // Nätverk-först för skalet (html/js/css) så att rättningar slår igenom direkt;
  // cachen är reserv när man är offline.
  const isShell =
    req.mode === "navigate" ||
    url.pathname.endsWith("/") ||
    /\.(html|js|css)$/.test(url.pathname);

  if (isShell) {
    e.respondWith(
      fetch(req)
        .then((res) => {
          const copy = res.clone();
          caches.open(VERSION).then((c) => c.put(req, copy));
          return res;
        })
        .catch(() => caches.match(req).then((r) => r || caches.match("./index.html")))
    );
  } else {
    // Cache-först för tunga statiska resurser (grafik, ljud, speldata).
    e.respondWith(
      caches.match(req).then(
        (r) =>
          r ||
          fetch(req).then((res) => {
            const copy = res.clone();
            caches.open(VERSION).then((c) => c.put(req, copy));
            return res;
          })
      )
    );
  }
});
