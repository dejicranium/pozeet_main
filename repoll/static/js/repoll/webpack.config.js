var path = require("path");
var webpack = require("webpack");

module.exports = {
  entry: {
    main: "./src/main.js",
    
    /** 
    view_poll: "./src/view_poll.js",
  
    view_opinion: './src/view_opinion.js',
    
    view_conversation: "./src/view_conversation.js",
    
    show_opinion_metrics: './src/show_opinion_metrics.js',
    show_poll_metrics: './src/show_poll_metrics.js',
    show_category_posts: './src/show_category_posts.js',
    polls_voted_in: './src/polls_voted_in.js',
    opinions_voted_in: './src/opinions_voted_in.js',
    trending: './src/trending.js',
    view_comment: "./src/view_comment.js",
    notifications: "./src/notifications.js",
    users_modal: './src/users_modal.js',
    profile: './src/profile.js',
    /**
    sample: './src/sample.js',
    
    **/
  },

  output: {
    path: path.resolve(__dirname, "./dist"),
    publicPath: "/dist/",
    filename: "[name]_build.js"
  },

  module: {
    rules: [
      {
        test: /\.css$/,
        use: ["vue-style-loader", "css-loader"]
      },
      {
        test: /\.vue$/,
        loader: "vue-loader",
        options: {
          loaders: {}
          // other vue-loader options go here
        }
      },
      {
        test: /\.js$/,
        loader: "babel-loader",
        exclude: /node_modules/
      },
      {
        test: /\.(png|jpg|gif|svg)$/,
        loader: "file-loader",
        options: {
          name: "[name].[ext]?[hash]"
        }
      }
    ]
  },

  resolve: {
    alias: {
      vue$: "vue/dist/vue.esm.js"
    },
    extensions: ["*", ".js", ".vue", ".json"]
  },

  devServer: {
    historyApiFallback: true,
    noInfo: true,
    overlay: true
  },

  performance: {
    hints: false
  },

  devtool: "#eval-source-map"
};

if (process.env.NODE_ENV === "production") {
  module.exports.devtool = "#source-map";
  // http://vue-loader.vuejs.org/en/workflow/production.html
  module.exports.plugins = (module.exports.plugins || []).concat([
    new webpack.DefinePlugin({
      "process.env": {
        NODE_ENV: '"production"'
      }
    }),
    new webpack.optimize.UglifyJsPlugin({
      sourceMap: true,
      compress: {
        warnings: false
      }
    }),
    new webpack.LoaderOptionsPlugin({
      minimize: true
    })
  ]);
}
