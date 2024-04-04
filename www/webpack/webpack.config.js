/* eslint-disable @typescript-eslint/no-var-requires */
const { merge } = require('webpack-merge');
const commonConfig = require('./webpack.common.js');
/* eslint-enable @typescript-eslint/no-var-requires */

const getAddons = (addonsArgs) => {
  const addons = Array.isArray(addonsArgs)
    ? addonsArgs
    : [addonsArgs];

  return addons
    .filter(Boolean)
    .map((name) => require(`./addons/webpack.${name}.js`));
};

module.exports = ({ env, addon }) => {
  // eslint-disable-next-line @typescript-eslint/no-var-requires
  const envConfig = require(`./webpack.${env}.js`);

  return merge(commonConfig, envConfig, ...getAddons(addon));
};
