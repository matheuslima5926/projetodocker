const proxy = [
    {
      context: '/api',
      target: 'http://ws-docker:8086',
      pathRewrite: {'^/api' : ''}
    }
  ];
  module.exports = proxy;