/* eslint-disable @typescript-eslint/no-var-requires */
const path = require('path');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CopyPlugin = require('copy-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');
const LazyLoadWebpackPlugin = require('lazyload-webpack-plugin');
const ForkTsCheckerWebpackPlugin = require('fork-ts-checker-webpack-plugin');
/* eslint-enable @typescript-eslint/no-var-requires */

function copyFile (filename) {
  return {
    from: path.resolve(__dirname, '..', 'src', filename),
    to: path.resolve(__dirname, '..', 'dist', filename),
    toType: 'file'
  };
}

function copyDir (dirname) {
  return {
    from: path.resolve(__dirname, '..', 'src', dirname),
    to: path.resolve(__dirname, '..', 'dist', dirname),
    toType: 'dir'
  };
}

module.exports = {
  entry: path.resolve(__dirname, '..', './src/index.ts'),
  devtool: 'source-map',
  module: {
    rules: [
      {
        test: /\.ts$/,
        use: [{
          loader: 'ts-loader',
          options: {
            onlyCompileBundledFiles: true
          }
        }]
      },
      {
        test: /\.frag.html$/i,
        exclude: /node_modules/,
        loader: 'html-loader',
        options: {
          // Disables attributes processing
          sources: false
        }
      },
      {
        test: /\.(css)$/,
        exclude: /node_modules/,
        use: ['style-loader', 'css-loader', 'postcss-loader']
      },
      {
        test: /\.css$/,
        include: /node_modules/,
        use: ['style-loader', 'css-loader']
      },
      {
        test: /\.(scss)$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          'sass-loader'
        ],
        include: /node_modules/,
      },
      {
        test: /\.scss$/,
        exclude: /node_modules/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          'sass-loader'
        ]
      },
      {
        test: /\.(png|svg|jpg|jpeg|gif|webp)$/i,
        exclude: /node_modules/,
        use: {
          loader: 'file-loader'
        }
        // type: 'asset/resource',
      }
    ]
  },
  resolve: {
    extensions: ['*', '.ts', '.js']
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: 'main.css' // Name of the output CSS file
    }),
    new CopyPlugin({
      patterns: [
        // Every folder or file at the root directory needs to be EXPLICITLY listed here.
        copyFile('sitemap.xml'),
        copyFile('manifest.json'),
        copyFile('favicon.ico'),
        copyFile('service-worker.js'),
        copyFile('google_workbox_6.1.5-sw.js'),
        copyFile('index.css'),
        copyFile('robots.txt'),
        copyDir('assets'),
      ],
      options: {
        concurrency: 100
      }
    }),
    new CleanWebpackPlugin(),
    new HtmlWebpackPlugin({
      title: 'Hello Webpack bundled JavaScript Project',
      // scriptLoading: 'blocking',
      template: path.resolve(__dirname, '..', './src/index.html'),
      inlineSourceMap: '.js$'
    }),
    new LazyLoadWebpackPlugin({}),
    new ForkTsCheckerWebpackPlugin()
  ],
  output: {
    path: path.resolve(__dirname, '..', './dist'),
    filename: 'bundle.js'
  },
  optimization: {
    minimizer: [
      new CssMinimizerPlugin()
    ]
  },

  stats: {
    errorDetails: true
  },

  devServer: {
    static: path.resolve(__dirname, '..', './dist'),
    historyApiFallback: true // Needed by react-router for webpack.
  },

  experiments: {
    topLevelAwait: true
  },

  watchOptions: {
    // for some systems, watching many files can result in a lot of CPU or memory usage
    // https://webpack.js.org/configuration/watch/#watchoptionsignored
    // don't use this pattern, if you have a monorepo with linked packages
    ignored: /node_modules/
  }
};
