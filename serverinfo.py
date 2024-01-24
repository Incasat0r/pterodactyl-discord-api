import requests
import json
import discord
from discord.ext import commands
import asyncio

client = commands.Bot(command_prefix=".", intents = discord.Intents.all())
client.remove_command(help)

hostingDomain = "" #e.x. panel.example.com or dash.example.com
api = "Bearer your api" # bearer don't need to delete 
serverId = "" #e.x. 1adaac52

headers = {
    'Accept': "application/json",
    'Content-Type': "application/json",
    'Authorization': api
}

responseServer1 = requests.get(f"https://{hostingDomain}/api/client/servers/{serverId}", headers=headers).json()
responseServer2 = requests.get(f"https://{hostingDomain}/api/client/servers/{serverId}/resources", headers=headers).json()

memoryLimit = responseServer1['attributes']['limits']['memory']
memoryUsedInBytes = responseServer2['attributes']['resources']['memory_bytes']
memoryUsedInMb = round(memoryUsedInBytes / (1024 * 1024))

cpuAbsolute = responseServer2['attributes']['resources']['cpu_absolute']
cpuLimit = responseServer1['attributes']['limits']['cpu'] 

diskInBytes = responseServer2['attributes']['resources']['disk_bytes']
diskInMb = round(diskInBytes / (1024 * 1024))
diskLimit = responseServer1['attributes']['limits']['disk']

serverOnline = responseServer2['attributes']['current_state']
suspended = responseServer2['attributes']['is_suspended']

def convertOnline(serverOnline):
    if serverOnline == 'running':
        return 'Онлайн'
    elif serverOnline == 'offline':
        return 'Офлайн'
    else:
        pass

def convertCpu(cpuAbsolute):
    int(cpuAbsolute)
    if cpuAbsolute > 1:
        return round(cpuAbsolute)
    elif cpuAbsolute < 1:
        return cpuAbsolute
    else:
        pass
    



@client.command()
async def server(ctx, param: str):
    if param == 'info':
        embed = discord.Embed(
            title = 'Информация о хосте',
            description = f'Ddk main: {convertOnline(serverOnline)}\n\n```\nПамять: {memoryUsedInMb}mb / {memoryLimit}mb\nПроцессор: {convertCpu(cpuAbsolute)}% / {cpuLimit}%\nДиск: {diskInMb}mb / {diskLimit}mb\n```'
        )
        await ctx.send(embed=embed)
    elif param == 'start':
        json = {
            'signal': 'start'
        }
        try:
            requests.post('https://{hostingDomain}/api/client/servers/{serverId}/power', json = json, headers=headers)
            await asyncio.sleep(5)
            embed = discord.Embed(
                title = 'Сервер успешно запущен 🚀',
                description = f'```\nПамять: {memoryUsedInMb}mb / {memoryLimit}mb\nПроцессор: {convertCpu(cpuAbsolute)}% / {cpuLimit}%\nДиск: {diskInMb}mb / {diskLimit}mb\n```'
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(e)
    elif param == 'stop':
        json = {
            'signal': 'kill'
        }
        try:
            print(requests.post('https://{hostingDomain}/api/client/servers/{serverId}/power', json = json, headers=headers))
            await asyncio.sleep(5)
            embed = discord.Embed(
                title = 'Сервер успешно остановлен 🛬',
                description = f'```\nПамять: {memoryUsedInMb}mb / {memoryLimit}mb\nПроцессор: {convertCpu(cpuAbsolute)}% / {cpuLimit}%\nДиск: {diskInMb}mb / {diskLimit}mb\n```'
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(e)
        
        
client.run('your discord bot token :)')