import { createClient } from '@supabase/supabase-js'
import { Telegraf } from 'telegraf'
import fetch from 'node-fetch'
import dotenv from 'dotenv'
dotenv.config()

// yah this is ai rewritten from the old python version

const supabaseUrl = "https://msfutgjgflgkckxreksp.supabase.co"
const supabaseKey = process.env.SUPABASE_KEY
const supabase = createClient(supabaseUrl, supabaseKey)
const bot = new Telegraf(process.env.BOT_TOKEN)

bot.start((ctx) => {
  ctx.reply("Hey there fellow Minecrafter! Use /help to see a list of available commands.")
})

bot.command('help', (ctx) => {
  ctx.reply(
    "Available Commands:\n" +
    "/setserver <address> - Configure server address (Artenos only)\n" +
    "/mcstatus - Get server status\n" +
    "/setcoords <x> <z> <remark> [overworld/nether] - Note coordinates\n" +
    "/getcoords - Get noted coordinates\n" +
    "/convertcoords <x> <z> [overworld/nether] - Convert coords to the other dimension\n"
  )
})

bot.command('setserver', async (ctx) => {
  const chatId = String(ctx.chat.id)
  const args = ctx.message.text.split(' ').slice(1)
  
  if (args.length === 0) {
    ctx.reply("Usage: /setserver <address>")
    return
  }

  const serverAddress = args[0]
  const data = { chat_id: chatId, server_address: serverAddress }
  
  try {
    await supabase.from("servers").upsert(data, { onConflict: ["chat_id"] })
    ctx.reply(`Server address set to ${serverAddress} for this chat.`)
  } catch (e) {
    ctx.reply(`Error: ${e.message}`)
  }
})

bot.command('mcstatus', async (ctx) => {
    const chatId = String(ctx.chat.id)
    const args = ctx.message.text.split(' ').slice(1)
    let serverAddress

    if (args.length > 0) {
        serverAddress = args[0]
    } else {
        try {
            const { data, error } = await supabase
                .from("servers")
                .select("server_address")
                .eq("chat_id", chatId)
            
            if (!data || data.length === 0) {
                ctx.reply("Server address not configured. Use /setserver <address> to set it.")
                return
            }
            serverAddress = data[0].server_address
        } catch (e) {
            ctx.reply(`Error getting server address: ${e.message}`)
            return
        }
    }

    try {
        const apiResponse = await fetch(`https://api.mcstatus.io/v2/status/java/${serverAddress}`)
        const responseData = await apiResponse.json()
        const onlineStatus = responseData.online
        
        if (!onlineStatus) {
            const responses = [
                "Server Offline 🥲",
                "Server is ded.",
                "Nope not the time yet."
            ]
            ctx.reply(responses[Math.floor(Math.random() * 3)])
        } else {
            const responses = [
                "CHAT ITS ONLINE GOGOGO!!",
                "Your life is on the line.",
                "Line up in queue."
            ]
            ctx.reply(responses[Math.floor(Math.random() * 3)])
        }
    } catch (e) {
        ctx.reply(`Error getting server status: ${e.message}`)
    }
})

bot.command('setcoords', async (ctx) => {
  const chatId = String(ctx.chat.id)
  const args = ctx.message.text.split(' ').slice(1)
  
  if (args.length < 3) {
    ctx.reply("Usage: /setcoords <x> <z> <remark> [overworld/nether]")
    return
  }

  try {
    const x = parseFloat(args[0])
    const z = parseFloat(args[1])
    let remark, dimension
    
    if (args[args.length - 1] === 'overworld' || args[args.length - 1] === 'nether') {
      remark = args.slice(2, -1).join(' ')
      dimension = args[args.length - 1]
    } else {
      remark = args.slice(2).join(' ')
      dimension = 'overworld'
    }
    
    const data = { chat_id: chatId, x, z, remark, dimension }
    
    await supabase.from("coordinates").insert(data)
    ctx.reply(`Coordinates set to (x: ${x}, z: ${z}) with remark: ${remark}`)
  } catch (e) {
    if (isNaN(parseFloat(args[0])) || isNaN(parseFloat(args[1]))) {
      ctx.reply("Invalid coordinates. Please use numbers for x and z.")
    } else {
      ctx.reply(`Error: ${e.message}`)
    }
  }
})

bot.command('getcoords', async (ctx) => {
  const chatId = String(ctx.chat.id)
  
  try {
    const { data, error } = await supabase
      .from("coordinates")
      .select("*")
      .eq("chat_id", chatId)
    
    if (!data || data.length === 0) {
      ctx.reply("No coordinates found. Use /setcoords <x> <z> <remark> to add coordinates.")
      return
    }

    const coordsList = data.map(coord => 
      `(x: ${coord.x}, z: ${coord.z}) - ${coord.remark} [${coord.dimension}]`
    ).join('\n')
    
    ctx.reply(`Stored Coordinates:\n${coordsList}`)
  } catch (e) {
    ctx.reply(`Error: ${e.message}`)
  }
})

bot.command('convertcoords', (ctx) => {
  const args = ctx.message.text.split(' ').slice(1)
  
  try {
    const x = parseFloat(args[0])
    const z = parseFloat(args[1])
    let dimension
    
    if (args[args.length - 1] === 'overworld' || args[args.length - 1] === 'nether') {
      dimension = args[args.length - 1]
    } else {
      dimension = 'overworld'
    }
    
    if (dimension === 'overworld') {
      ctx.reply(`Coordinates equivalent in the nether is x: ${x/8}, z: ${z/8}`)
    } else {
      ctx.reply(`Coordinates equivalent in the overworld is x: ${x*8}, z: ${z*8}`)
    }
  } catch (e) {
    ctx.reply(`Error: ${e.message}`)
  }
})

bot.launch()

process.once('SIGINT', () => bot.stop('SIGINT'))
process.once('SIGTERM', () => bot.stop('SIGTERM'))