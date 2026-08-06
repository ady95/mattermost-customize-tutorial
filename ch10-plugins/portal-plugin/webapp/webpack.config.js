// 10-4절: 번들 설정의 핵심 — react를 externals로 (본체 웹앱의 React 인스턴스 사용)
module.exports = {
    entry: './src/index.tsx',
    module: {
        rules: [{test: /\.tsx?$/, use: 'ts-loader', exclude: /node_modules/}],
    },
    resolve: {extensions: ['.ts', '.tsx', '.js']},
    externals: {
        react: 'React',
        'react-dom': 'ReactDOM',
    },
    output: {filename: 'main.js', path: __dirname + '/dist'},
};
