var ErgoAnimes = {
  animeImg: function (elm) {
    'use strict';
    return function () {
      var img = elm.getElementsByTagName('img');
      if (img.length > 0) {
        img = img[0];
        if (!img.hasAttribute('src')) {
          img.src = img.dataset.src;
        }
      }
    };
  }
};


(function () {
  'use strict';
  var animes = document.querySelectorAll('.anime'),
    max = animes.length,
    i,
    anime;
  for (i = 0; i < max; i++) {
    anime = animes[i];
    anime.onmouseover = ErgoAnimes.animeImg(anime);
  }
}());
