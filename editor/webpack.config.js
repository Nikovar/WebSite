var path = require('path');
var webpack = require('webpack');
var colors = require('colors/safe');
var glob = require("glob");
var ExtractTextPlugin = require('extract-text-webpack-plugin');
var BitBarWebpackProgressPlugin = require("bitbar-webpack-progress-plugin");
var fs = require('fs');

require('es6-promise')
    .polyfill();

var PROD = JSON.parse(process.env.NODE_ENV || '0');

var plugins = [
    new webpack.optimize.OccurrenceOrderPlugin(),
    new webpack.DefinePlugin({
        'process.env': {
            'NODE_ENV': PROD == "1" ? '"production"' : '"development"'
        }
    }),
    new BitBarWebpackProgressPlugin(),
    new webpack.NoEmitOnErrorsPlugin(),
    new webpack.NoErrorsPlugin(),
    new webpack.ProvidePlugin({
        '_': 'lodash',
        'moment': 'moment',
        '$': 'jquery',
        'jQuery': 'jquery',
        'swal': 'sweetalert2'
    }),
    function() {
        this.plugin('watch-run', function(watching, callback) {
            console.log(colors.yellow('Begin compile at ' + new Date()));
            callback();
        })
    },
    new ExtractTextPlugin({
        filename: function(getPath) {
            console.log('STYLES.CSS', getPath('styles.css'))
            return getPath('styles.css')
        },
        allChunks: true
    }),
];

var watch = true;

if (PROD) {
    watch = false;
    plugins.push(new webpack.optimize.UglifyJsPlugin({
        beautify: false,
        comments: false,
        sourceMap: true,
        compress: {
            sequences     : true,
            booleans      : true,
            loops         : true,
            unused      : true,
            warnings    : false,
            drop_console: true,
            unsafe      : true
        }
    }));
}
console.log(colors.yellow('Run building'));


module.exports = {
        cache: true,
        context: path.join(path.resolve(__dirname), "front"),
        entry: "app.js",
        output: {
            path: path.join(path.resolve(__dirname), "static", "editor"),
            filename: "app.build.js",
        },
        plugins: plugins,
        devtool: "cheap-module-source-map",
        module: {
            loaders: [{
                test: /\.(jsx|js)$/,
                exclude: /(node_modules|bower_components)/,
                loader: "babel-loader",
                options: {
                  presets: ['es2015', "stage-0", "react"]
                }
            }, {
                    test: /\.less$/,
                    loader: ExtractTextPlugin.extract([
                        {
                            loader: 'css-loader',
                            options: {
                                minimize: PROD,
                            }
                        }, {
                            loader: 'less-loader'
                        }
                    ])
            }, {
                test: /\.css$/,
                loader: ExtractTextPlugin.extract('css-loader?minimize=' + PROD)
            }, {
                test: /\.(jpe?g|png|gif|svg|eot|woff|ttf|svg|woff2)(\?\S*)?$/,
                loader: "file-loader?mimetype=image/svg+xml"
            }]
        },
        watch: watch,
        resolve: {
            modules: ['node_modules', "./front"],
            extensions: [
                '.jsx',
                '.js',
            ],
            unsafeCache: true,
        }
}
