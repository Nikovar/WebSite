const path = require('path');
const webpack = require('webpack');
const glob = require('glob');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const VueLoaderPlugin = require('vue-loader/lib/plugin');


var entries = [];


function fillEntry(entry) {
    entry = "./" + entry;
    console.log("    " + entries.length + ": " + entry);
    entries.push(entry);
}


rmDir = function(dirPath) {
    try {
        var files = fs.readdirSync(dirPath);
    } catch (e) {
        return;
    }
    if (files.length > 0)
        for (var i = 0; i < files.length; i++) {
            var filePath = dirPath + '/' + files[i];
            if (fs.statSync(filePath).isFile())
                fs.unlinkSync(filePath);
            else
                rmDir(filePath);
        }
};


console.log('Find entries');

glob.sync("front/app.jsx", {
    cwd: path.resolve(__dirname)
})
    .forEach(fillEntry);

glob.sync("front/app.js", {
    cwd: path.resolve(__dirname)
})
    .forEach(fillEntry);

var targets = [];

module.exports = targets;
console.log('-------------------------------')
console.log(entries)


entries.forEach(function(entry) {
    console.log('RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR!!!!!!!!!!!')

    targets.push({
        cache: true,
        context: path.resolve(__dirname),
        entry: entry,
        performance: {
            hints: false
        },
        output: {
            path: path.join(path.resolve(__dirname), "static", "editor"),
            filename: "app.build.js",
        },
        plugins: [
            new MiniCssExtractPlugin({
                filename: "app.build.css",
                chunkFilename: "[id].css"
            }),
            new VueLoaderPlugin(),
        ],
        module: {
            rules: [
                {
                    test: /\.vue$/,
                    exclude: /node_modules/,
                    loader: 'vue-loader'
                },
                {
                    test: /\.js$/,
                    exclude: /node_modules/,
                    use: {
                        loader: 'babel-loader'
                    }
                },
                {
                    test: /\.(sa|sc|c)ss$/,
                    use: [
                        MiniCssExtractPlugin.loader,
                        'css-loader',
                    ],
                },
            ],
        },
        resolve: {
            modules: ['node_modules', path.resolve(__dirname)],
            extensions: [
                '.js',
                '.vue',
            ],
            alias: {
                'vue$': 'vue/dist/vue.esm.js'
            }
        }
    })
});
