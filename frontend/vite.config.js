import {fileURLToPath, URL} from 'node:url'

import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
    plugins: [vue()],
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url))
        }
    },
    server: {
        host: true,
        cors: true,
        headers: {
            //allow all origins
            //'Access-Control-Allow-Origin': 'http://10.23.42.128:8000, http://10.23.42.168:8000',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token, Authorization, Accept,charset,boundary,Content-Length',
            'Access-Control-Allow-Credentials': 'true',
            'Content-Security-Policy': 'default-src \'self\';'
                + ' script-src \'self\' \'wasm-unsafe-eval\';'
                + ' style-src \'self\' \'unsafe-inline\';'
                + ' connect-src * data:', // TODO: change * to https://* for production
        },
        proxy: {
            '^/api/': {
                target: "http://127.0.0.1:8000/",
            },
            '^/auth/': {
                target: "http://127.0.0.1:8000/",
            },
            '^/admin/': {
                target: "http://127.0.0.1:8000/",
            },
            '^/docs/': {
                target: "http://127.0.0.1:8000/",
            },
            '^/static/': {
                target: "http://127.0.0.1:8000/",
            },
            '^/wiki/': {
                target: "http://127.0.0.1:8080/",
                rewrite: (path) => path.replace(/^\/wiki/, ''),
            },
            '^/livereload/': {
                target: "http://127.0.0.1:8080/",
            }
        }
    },
    test: {
        include: ['src/tests/**/*.js'],
        globals: true,
        environment: "jsdom"
    }
})
