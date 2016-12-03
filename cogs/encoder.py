from discord.ext import commands
from discord.opus import Encoder as OpusEncoder
from discord.voice_client import ProcessPlayer
from discord.errors import ClientException

import pickle
import threading
import os
import shlex
import subprocess
import logging
import asyncio
from threading import Event
import time
import audioop

log = logging.getLogger("red.encoder")


class AudioCacheFileConverter(commands.Converter):
    def convert(self):
        cache_path = os.path.join('data/audio/cache', self.argument)
        if not os.path.exists(cache_path):
            raise commands.BadArgument("Cache file '{}' not found.".format(
                cache_path))
        return cache_path


class EncodedCacheFile(commands.Converter):
    def convert(self):
        cache_path = os.path.join('data/audio/cache',
                                  self.argument + "-encoded")
        if not os.path.exists(cache_path):
            raise commands.BadArgument("Cache file '{}' not found.".format(
                cache_path))
        return cache_path


class EncodedSong:
    def __init__(self, filename, delay, encoded_data):
        self.filename = filename
        self.delay = delay
        self.data = encoded_data


class ShittyPlayer(threading.Thread):
    def __init__(self, esong, audio_instance, connected, player, after=None):
        super().__init__()
        self.esong = esong
        self.audio_instance = audio_instance

        self.data = self.esong.data
        self.delay = self.esong.delay

        self._end = threading.Event()
        self._resumed = threading.Event()
        self._resumed.set()  # we are not paused
        self._connected = connected
        self.after = after
        self._volume = 1.0
        self.frame_size = 16
        self.player = lambda data: player(data, encode=False)

        if after is not None and not callable(after):
            raise TypeError('Expected a callable for the "after" parameter.')

    def run(self):
        self.loops = 0
        self._start = time.time()
        while not self._end.is_set():
            # are we paused?
            if not self._resumed.is_set():
                # wait until we aren't
                self._resumed.wait()

            if not self._connected.is_set():
                self.stop()
                break

            self.loops += 1
            data = self.data.pop(0)

            if self._volume != 1.0:
                data = audioop.mul(data, 2, min(self._volume, 2.0))

            """if len(data) != self.frame_size:
                self.stop()
                break"""

            self.player(data)
            next_time = self._start + self.delay * self.loops
            delay = max(0, self.delay + (next_time - time.time()))
            time.sleep(delay)

    def stop(self):
        self._end.set()
        if self.after is not None:
            try:
                self.after()
            except:
                pass

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        self._volume = max(value, 0.0)

    def pause(self):
        self._resumed.clear()

    def resume(self):
        self.loops = 0
        self._start = time.time()
        self._resumed.set()

    def is_playing(self):
        return self._resumed.is_set() and not self.is_done()

    def is_done(self):
        return not self._connected.is_set() or self._end.is_set()


class Encoder:
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

        self.filename = None
        self.converter = None
        self.opus_data = []

        self.encoder = OpusEncoder(48000, 2)
        self.delay = self.encoder.frame_length / 1000.0
        self.encoder.frame_length = 0
        self._connected = Event()
        self._connected.set()

        self.to_encode = asyncio.Queue()
        self.encode_task = bot.loop.create_task(self.queue_encoder())

    def __unload(self):
        try:
            self.encode_task.cancel()
        except:
            pass

    def create_ffmpeg_player(self, filename, *, use_avconv=False, pipe=False,
                             options=None, before_options=None, headers=None,
                             after=None):
        """
        Stolen from Rapptz/Danny, thanks!
        """
        command = 'ffmpeg' if not use_avconv else 'avconv'
        input_name = '-' if pipe else shlex.quote(filename)
        before_args = ""
        if isinstance(headers, dict):
            for key, value in headers.items():
                before_args += "{}: {}\r\n".format(key, value)
            before_args = ' -headers ' + shlex.quote(before_args)

        if isinstance(before_options, str):
            before_args += ' ' + before_options

        cmd = command + '{} -i {} -f s16le -ar {} -ac {} -loglevel warning'
        cmd = cmd.format(before_args, input_name, self.encoder.sampling_rate,
                         self.encoder.channels)

        if isinstance(options, str):
            cmd = cmd + ' ' + options

        cmd += ' pipe:1'

        stdin = None if not pipe else filename
        args = shlex.split(cmd)
        try:
            p = subprocess.Popen(args, stdin=stdin, stdout=subprocess.PIPE)
            return ProcessPlayer(p, self, after)
        except FileNotFoundError as e:
            raise ClientException('ffmpeg/avconv was not found in your PATH'
                                  ' environment variable') from e
        except subprocess.SubprocessError as e:
            raise ClientException(
                'Popen failed: {0.__name__} {1}'.format(type(e), str(e))) \
                from e

    @commands.command()
    async def encode(self, filename: AudioCacheFileConverter):
        """Encodes a song to pickled pcm data"""
        if self.converter is not None:
            return

        self.converter = \
            self.create_ffmpeg_player(filename, after=self._reset_converter)
        self.filename = filename
        self.converter.start()
        log.debug('encoding {}'.format(filename))

    @commands.command(pass_context=True)
    async def fakeplay(self, ctx, filename: EncodedCacheFile):
        audio = self.bot.get_cog('Audio')
        with open(filename, 'rb') as f:
            esong = pickle.load(f)
        if not isinstance(esong, EncodedSong):
            await self.bot.say("Bad file")
            return
        vc = audio.voice_client(ctx.message.server)
        vc.audio_player = ShittyPlayer(esong, audio, vc._connected,
                                       vc.play_audio)
        vc.audio_player.start()

    def play_audio(self, data_frame):
        # opus_frame = self.encoder.encode(data_frame,
        #                                  self.encoder.samples_per_frame)
        # self.opus_data.append(opus_frame)
        self.to_encode.put_nowait(data_frame)

    async def queue_encoder(self):
        while True:
            pcm = await self.to_encode.get()
            opus = self.encoder.encode(pcm,
                                       self.encoder.samples_per_frame)
            self.opus_data.append(opus)

    def _reset_converter(self):
        self.save_opus_data()
        self.converter = None
        self.filename = None

    def save_opus_data(self):
        enc = EncodedSong(self.filename + "-encoded",
                          self.delay, self.opus_data)
        with open(enc.filename, 'wb') as f:
            pickle.dump(enc, f)


def setup(bot):
    bot.add_cog(Encoder(bot))
