// Copyright (c) 2024 Guilherme Werner
// SPDX-License-Identifier: MIT

import { Worker } from 'worker_threads';
import path from 'path';

const numBots = 100;
const botsPerThread = 10;
const numThreads = Math.ceil(numBots / botsPerThread);

for (let i = 0; i < numThreads; i++) {
    const startBotIndex = i * botsPerThread;
    const endBotIndex = Math.min(startBotIndex + botsPerThread, numBots);

    const worker = new Worker(path.resolve('src/bedrock/bot.js'), {
        workerData: { startBotIndex, endBotIndex }
    });

    worker.on('message', (message) => {
        console.log(`Worker message: ${message}`);
    });

    worker.on('error', (error) => {
        console.error(`Worker error: ${error}`);
    });

    worker.on('exit', (code) => {
        if (code !== 0) {
            console.error(`Worker stopped with exit code ${code}`);
        }
    });
}

for (let i = 0; i < numThreads; i++) {
    const startBotIndex = i * botsPerThread;
    const endBotIndex = Math.min(startBotIndex + botsPerThread, numBots);

    const worker = new Worker(path.resolve('src/java/bot.js'), {
        workerData: { startBotIndex, endBotIndex }
    });

    worker.on('message', (message) => {
        console.log(`Worker message: ${message}`);
    });

    worker.on('error', (error) => {
        console.error(`Worker error: ${error}`);
    });

    worker.on('exit', (code) => {
        if (code !== 0) {
            console.error(`Worker stopped with exit code ${code}`);
        }
    });
}
