import {fileURLToPath, URL} from 'node:url'

import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
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
            'Access-Control-Allow-Credentials': 'true'
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
            }
        }
    }
})
