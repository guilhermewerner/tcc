// Copyright (c) 2024 Guilherme Werner
// SPDX-License-Identifier: MIT

import mineflayer from "mineflayer";
import { mineflayer as mineflayerViewer } from "prismarine-viewer";

const bot = mineflayer.createBot({
    host: 'localhost',
    port: 25565,
    username: 'Bot',
    auth: 'offline'
})

bot.once('spawn', () => {
    bot.setControlState('forward', true)
    mineflayerViewer(bot, { port: 3000, firstPerson: true })
})

bot.on('chat', (username, message) => {
    if (username === bot.username) return
    bot.chat(message)
})

bot.on('kicked', console.log)
bot.on('error', console.log)
