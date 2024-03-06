export function isDebug () {
  const isEnabled = window.location.search.includes('debug=1');
  return isEnabled;
}


export function isDev () {
  // local hosts are dev.
  const localHosts = ['localhost', '127.0.0.1', '0.0.0.0'];
  // const isEnabled = window.location.hostname.includes('localhost');
  let isEnabled = false;
  localHosts.forEach((host) => {
    if (window.location.hostname.includes(host)) {
      isEnabled = true;
    }
  });
  return isEnabled;
}

export function mapValues (t, x0, x1, y0, y1) {
  return ((t - x0) * (y1 - y0)) / (x1 - x0) + y0;
}

export function interpolate (t, x0, x1) {
  return mapValues(t, 0, 1, x0, x1);
}

export function setCssRootVar (name, value) {
  document.documentElement.style.setProperty(name, value);
}

export function isMobile () {
  const params = window.location.search;
  if (params.includes('m=1')) {
    return true;
  }
  if (params.includes('m=0')) {
    return false;
  }
  // First step.
  const is_mobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
  if (is_mobile) {
    return is_mobile;
  }
  return false;
}
