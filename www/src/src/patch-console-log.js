const consoleLog = console.log;

console.log = (...args) => {
  if (process.env.NODE_ENV === 'production') {
    return;
  }

  if (globalThis.EPOCH_TIME === undefined) {
    consoleLog('EPOCH_TIME not set');
    globalThis.EPOCH_TIME = (new Date()).getTime();
  }

  let seconds = (new Date()).getTime() - globalThis.EPOCH_TIME;
  seconds /= 1000;

  // Round to nearest millisecond
  seconds = seconds.toFixed(3);
  consoleLog(seconds, ...args);
};
