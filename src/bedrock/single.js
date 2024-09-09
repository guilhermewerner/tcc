// Copyright (c) 2024 Guilherme Werner
// SPDX-License-Identifier: MIT

import bedrock  from "bedrock-protocol";

const bot = bedrock .createClient({
    host: 'localhost',
    port: 19132,
    username: 'Bot',
    version: '1.20.0',
    offline: true,
})

bot.once('spawn', () => {
    //bot.setControlState('forward', true)
})

bot.on('chat', (username, message) => {
    if (username === bot.username) return
    bot.chat(message)
})

bot.on('kicked', console.log)
bot.on('error', console.log)
