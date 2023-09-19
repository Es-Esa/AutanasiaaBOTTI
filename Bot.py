import discord
import asyncio
import speech_recognition as sr
import os
import wave
import pyaudio
from discord.ext import commands

# DISCORD INTENT SÄÄTÖ
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.voice_states = True
intents.message_content = True

# Olio mikä käynnistää DC clientin
bot = commands.Bot(command_prefix='!', intents=intents)

# Äänitys asetuksia / täytyy poistaa jokakerta tuo audo/ muutetaan myöhemmäksi että kun whisperi käsittelee se poistaa sen.
recording = False
audio_filename = 'user_audio.wav'
p = None  # PyAudio instance

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

@bot.command()
async def apua(ctx):
    global recording, p

    # Tarkistaa onko käyttäjä voicechatissa
    if ctx.author.voice and ctx.author.voice.channel:
        # Kirjautuu käyttäjän voiceen
        voice_channel = ctx.author.voice.channel
        voice_client = await voice_channel.connect()

        # Lähettää viestin että kuunnellaan
        await ctx.send("Hei kerro huolesi, 10 sekunttia")

        # Tunnistaa puhee
        recognizer = sr.Recognizer()

        if not recording:
            # alkaa tallentamaan
            p = pyaudio.PyAudio()
            stream = p.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=44100,
                            input=True,
                            frames_per_buffer=1024)
            frames = []
            recording = True

            try:
                for _ in range(10 * 44100 // 1024):  # äänittää 10 sekunttia
                    data = stream.read(1024)
                    frames.append(data)
            except KeyboardInterrupt:
                pass
            finally:
                stream.stop_stream()
                stream.close()
                p.terminate()

                # tallentaa audion 'user_audio.wav'
                with wave.open(audio_filename, 'wb') as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
                    wf.setframerate(44100)
                    wf.writeframes(b''.join(frames))

                recording = False

        # Poistuu 10 sekunnin päästä
        await asyncio.sleep(10)  # Wait for 10 seconds
        await voice_client.disconnect()

# Tätä ei ikinä saisi pitää täälä .env siirretään myöhemmin
bot.run('MTE1MzMyMjE3ODI1NTc4MTg5OQ.G4cUp5._-ct64ACPVNnWGG7mf49bC3DrGkFjF5dSwtg3o')