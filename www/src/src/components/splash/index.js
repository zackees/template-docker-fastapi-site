/* eslint-disable func-names */

// Splash screen always comes up during developement.

import html from './index.frag.html';
import './index.css';
import { isDev, isMobile } from '../../util';

const LOCAL_STORAGE_NAME = 'splashActivatedInfo';

function getData () {
  const data = localStorage.getItem(LOCAL_STORAGE_NAME);
  if (data) {
    return JSON.parse(data);
  }
  return null;
}

function setData (activatedThisSession, date) {
  const payload = JSON.stringify({
    activatedThisSession,
    date
  });
  localStorage.setItem(LOCAL_STORAGE_NAME, payload);
}

function finalize () {
  const el = document.getElementById('background-video');
  document.getElementById('splash').style.display = 'none';
  document.body.classList.remove('preload');
  document.documentElement.classList.remove('preload');
  el.pause();
}

export function splashActivatedThisSession () {
  return !!getData().activatedThisSession;
}

// Splash screen always comes up during developement.
export async function initSplash () {

  const data = getData();
  if (data === null) {
    setData(false, null);
  }

  const splashActivatedDate = getData().date;
  if (splashActivatedDate && !isDev()) {
    const maxHours = 24;
    const dateDiff = new Date().getTime() - splashActivatedDate;
    const hoursDiff = dateDiff / 1000 / 60 / 60;
    if (hoursDiff < maxHours) {
      document.body.classList.remove('preload');
      document.documentElement.classList.remove('preload');
      setData(false, data.date);
      return;
    }
  }
  setData(true, new Date().getTime());
  const $dom = document.querySelector('#splash');
  $dom.outerHTML = html;
  // html.preload, body.preload
  // add preload class to body and to html
  document.body.classList.add('preload');
  document.documentElement.classList.add('preload');
  // const vidEl = document.getElementById('background-video');

  const enabled = !isMobile();
  const $backgroundVideo = enabled ? document.getElementById('background-video') : document.getElementById('background-image');
  const listenForData = enabled ? 'loadeddata' : 'load';
  const dataTimeout = enabled ? 0 : 0;

  document.getElementById('shield-image').onload = function () {
    setTimeout(function () {
      this.style.opacity = '1';
    }.bind(this), 500);
    if (enabled) {
      const el = document.getElementById('background-video');
      el.src = 'https://techwatchproject.github.io/americanflag/small.mp4';
      // play
      el.play();
    } else {
      setTimeout(function () {
        $backgroundVideo.style.opacity = '1';
      }, 1200);
    }
  };

  if (enabled) {
    $backgroundVideo.addEventListener(listenForData, function () {
      setTimeout(function () {
        $backgroundVideo.style.opacity = '1';
      }, dataTimeout);
    });
  }

  document.getElementById('svg-header').onload = function () {
    this.style.opacity = '1';
  };

  setTimeout(function () {
    document.getElementById('splash').classList.add('hide');
  }, 4000);

  setTimeout(function () {
    finalize();
  }, 4200);

}
