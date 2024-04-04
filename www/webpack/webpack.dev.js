/* eslint-disable @typescript-eslint/no-var-requires */
const { DefinePlugin } = require('webpack');
/* eslint-enable @typescript-eslint/no-var-requires */

module.exports = {
  mode: 'development',
  plugins: [
    new DefinePlugin({
      'process.env': {
        NODE_ENV: JSON.stringify('development')
      }
    })
  ],
  devtool: 'eval-source-map'
};
