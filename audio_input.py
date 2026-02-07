import sys
import types

# Provide distutils.version.LooseVersion for SpeechRecognition on Python 3.12+
try:
    from distutils.version import LooseVersion  # type: ignore
except Exception:
    try:
        import setuptools._distutils as _distutils  # type: ignore
        sys.modules.setdefault("distutils", _distutils)
        sys.modules.setdefault("distutils.version", _distutils.version)
    except Exception:
        try:
            from packaging import version as _pkg_version  # type: ignore

            class LooseVersion:  # minimal shim
                def __init__(self, v):
                    self._v = str(v)

                def _parsed(self):
                    return _pkg_version.parse(self._v)

                def __lt__(self, other):
                    return self._parsed() < _pkg_version.parse(str(other))

                def __le__(self, other):
                    return self._parsed() <= _pkg_version.parse(str(other))

                def __gt__(self, other):
                    return self._parsed() > _pkg_version.parse(str(other))

                def __ge__(self, other):
                    return self._parsed() >= _pkg_version.parse(str(other))

                def __eq__(self, other):
                    return self._parsed() == _pkg_version.parse(str(other))

                def __repr__(self):
                    return f"LooseVersion({self._v!r})"

            _distutils_mod = types.ModuleType("distutils")
            _distutils_ver_mod = types.ModuleType("distutils.version")
            _distutils_ver_mod.LooseVersion = LooseVersion
            _distutils_mod.version = _distutils_ver_mod
            sys.modules.setdefault("distutils", _distutils_mod)
            sys.modules.setdefault("distutils.version", _distutils_ver_mod)
        except Exception:
            pass

import speech_recognition as sr
import threading
import queue
from config import Config

class AudioInput:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.audio_queue = queue.Queue()
        self.is_listening = False
        
        # Ajustation le bruit ambiant
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
    
    def start_listening(self, callback):
        """Démarre l'écoute en continu"""
        self.is_listening = True
        self.callback = callback
        
        def listen_loop():
            while self.is_listening:
                try:
                    with self.microphone as source:
                        audio = self.recognizer.listen(
                            source, 
                            timeout=2,
                            phrase_time_limit=Config.MAX_RECORDING_SECONDS
                        )
                    
                    # Transcription dans un thread séparé
                    threading.Thread(
                        target=self._process_audio,
                        args=(audio,),
                        daemon=True
                    ).start()
                    
                except sr.WaitTimeoutError:
                    continue
                except Exception as e:
                    print(f"Erreur écoute: {e}")
        
        threading.Thread(target=listen_loop, daemon=True).start()
    
    def _process_audio(self, audio):
        """Transcrit l'audio en texte"""
        try:
            text = self.recognizer.recognize_google(audio, language="fr-FR")
            if text and len(text.strip()) > 1:
                self.callback(text.strip())
        except sr.UnknownValueError:
            pass  # Silence et parole incompréhensible
        except sr.RequestError as e:
            print(f"Erreur API reconnaissance: {e}")
        except Exception as e:
            print(f"Erreur transcription: {e}")
    
    def stop_listening(self):
        """Arrête l'écoute"""
        self.is_listening = False
