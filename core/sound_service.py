import os
import wave
import math
import struct
import winsound
import threading

SOUNDS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'sounds')

class SoundService:
    def __init__(self):
        self.enabled = False
        self.current_sound = 'thock'
        self.lock = threading.Lock()
        os.makedirs(SOUNDS_DIR, exist_ok=True)
        self._ensure_sound_files()

    def _generate_wav(self, filename: str, freq1: float, freq2: float, decay_rate: float, duration: float, has_click: bool = False):
        filepath = os.path.join(SOUNDS_DIR, filename)
        if os.path.exists(filepath):
            return filepath
        
        sample_rate = 44100
        n_samples = int(sample_rate * duration)
        with wave.open(filepath, 'wb') as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(sample_rate)
            frames = bytearray()
            for i in range(n_samples):
                t = i / sample_rate
                # Main body resonance
                decay = math.exp(-t * decay_rate)
                val = math.sin(2 * math.pi * freq1 * t) * decay * 0.7
                val += math.sin(2 * math.pi * freq2 * t) * math.exp(-t * (decay_rate * 1.4)) * 0.35
                
                # Sharp mechanical click snap if requested
                if has_click and t < 0.007:
                    click_decay = (1.0 - t / 0.007)
                    val += math.sin(2 * math.pi * 3200 * t) * click_decay * 0.5
                    val += math.sin(2 * math.pi * 5400 * t) * click_decay * 0.3
                
                sample = int(max(-1.0, min(1.0, val)) * 30000)
                frames.extend(struct.pack('<h', sample))
            wav.writeframes(frames)
        return filepath

    def _ensure_sound_files(self):
        # 1. Thocky (Deep wooden tactile pop)
        self._generate_wav('thock.wav', freq1=190, freq2=340, decay_rate=110, duration=0.065, has_click=True)
        # 2. Clicky (Sharp blue switch click)
        self._generate_wav('clicky.wav', freq1=820, freq2=2200, decay_rate=180, duration=0.05, has_click=True)
        # 3. Creamy (Smooth lubed linear switch bottom-out)
        self._generate_wav('creamy.wav', freq1=260, freq2=480, decay_rate=130, duration=0.055, has_click=False)
        # 4. Bubble (Satisfying soft pop)
        self._generate_wav('bubble.wav', freq1=380, freq2=620, decay_rate=95, duration=0.07, has_click=False)

    def play_key_sound(self):
        if not self.enabled or self.current_sound == 'none':
            return
        
        filepath = os.path.join(SOUNDS_DIR, f"{self.current_sound}.wav")
        if os.path.exists(filepath):
            try:
                # Play asynchronously without blocking keyboard events
                winsound.PlaySound(filepath, winsound.SND_FILENAME | winsound.SND_ASYNC)
            except Exception:
                pass

    def set_sound(self, sound_name: str):
        with self.lock:
            self.current_sound = sound_name

    def set_enabled(self, enabled: bool):
        with self.lock:
            self.enabled = enabled

sound_service = SoundService()
