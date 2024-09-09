// Copyright (c) 2024 Guilherme Werner
// SPDX-License-Identifier: MIT

import bedrock  from "bedrock-protocol";
import { parentPort, workerData } from 'worker_threads';

const { startBotIndex, endBotIndex } = workerData;
const movements = ['left', 'right'];

function getRandomMovement() {
    return movements[Math.floor(Math.random() * movements.length)];
}

for (let i = startBotIndex; i < endBotIndex; i++) {
    const bot = bedrock.createClient({
        host: 'localhost',
        port: 19132,
        username: `Bot${i}`,
        version: '1.20.0',
        offline: true,
    });

    bot.on('time2', () => {
        //const movement = getRandomMovement();
        //const action = Math.random() > 0.5;
        //bot.setControlState(movement, action);
        //bot.setControlState('forward', true);
        //bot.setControlState('sprint', true);
        //bot.setControlState('jump', true);
    });

    bot.on('chat', (username, message) => {
        if (username === bot.username) return;
        bot.chat(message);
    });

    bot.on('kicked', (reason, loggedIn) => {
        parentPort.postMessage(`Bot${i} foi expulso por: ${reason} | LoggedIn: ${loggedIn}`);
    });

    bot.on('error', (err) => {
        parentPort.postMessage(`Bot${i} encontrou um erro: ${err}`);
    });
}
