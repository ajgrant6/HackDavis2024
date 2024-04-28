const Dotenv = require('dotenv-webpack');

module.exports = {
  // other webpack configuration...
  plugins: [
    new Dotenv()
  ]
};