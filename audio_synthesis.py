import os
from mnemonic_generation import generate_mnemonic
from dotenv import load_dotenv
from elevenlabs import ElevenLabs
from pydub import AudioSegment
import tempfile

load_dotenv()

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
BACKGROUND_BEAT_PATH = "background_beat.mp3"
OUTPUT_PATH = "mnemonic_output.mp3"

# Audio mixing settings
VOICE_VOLUME_BOOST = 6      # dB boost for voice clarity
MUSIC_VOLUME_REDUCE = -14   # dB reduction for background music
FADE_IN_DURATION = 2000     # ms
FADE_OUT_DURATION = 3000    # ms
PADDING_BEFORE = 1000       # ms silence before voice starts
PADDING_AFTER = 2000        # ms silence after voice ends


def text_to_speech(mnemonic_text: str) -> AudioSegment:
    """Convert mnemonic text to speech using ElevenLabs."""
    
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    
    print("  Generating voice with ElevenLabs...")
    
    # Generate audio
    audio_generator = client.text_to_speech.convert(
        text=mnemonic_text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",   # George — clear, natural voice
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    
    # Save to temp file and load as AudioSegment
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        for chunk in audio_generator:
            tmp.write(chunk)
        tmp_path = tmp.name
    
    voice_audio = AudioSegment.from_mp3(tmp_path)
    os.unlink(tmp_path)  # delete temp file
    
    print(f"  Voice duration: {len(voice_audio) / 1000:.1f} seconds")
    return voice_audio


def prepare_background_music(voice_duration_ms: int) -> AudioSegment:
    """Load and prepare background music to match voice duration."""
    
    print("  Loading background music...")
    
    music = AudioSegment.from_mp3(BACKGROUND_BEAT_PATH)
    
    # Total duration = padding before + voice + padding after
    total_duration = PADDING_BEFORE + voice_duration_ms + PADDING_AFTER
    
    # Loop music if shorter than needed
    while len(music) < total_duration:
        music = music + music
    
    # Trim to exact duration needed
    music = music[:total_duration]
    
    # Fade in and out
    music = music.fade_in(FADE_IN_DURATION).fade_out(FADE_OUT_DURATION)
    
    # Reduce volume so voice is clear
    music = music + MUSIC_VOLUME_REDUCE
    
    print(f"  Music duration: {len(music) / 1000:.1f} seconds")
    return music


def mix_audio(voice: AudioSegment, music: AudioSegment) -> AudioSegment:
    """Mix voice and background music together."""
    
    print("  Mixing voice and music...")
    
    # Boost voice volume for clarity
    voice = voice + VOICE_VOLUME_BOOST
    
    # Add silence padding before and after voice
    padded_voice = (
        AudioSegment.silent(duration=PADDING_BEFORE) +
        voice +
        AudioSegment.silent(duration=PADDING_AFTER)
    )
    
    # Overlay voice on top of music
    final_audio = music.overlay(padded_voice)
    
    return final_audio


def synthesize_audio(mnemonic_text: str,
                     output_path: str = OUTPUT_PATH) -> dict:
    """
    Full audio synthesis pipeline:
    1. Convert mnemonic text to speech
    2. Prepare background music
    3. Mix together
    4. Export as mp3
    """
    
    if not mnemonic_text:
        return {"audio_path": None, "error": "Empty mnemonic text"}
    
    if not ELEVENLABS_API_KEY:
        return {"audio_path": None, "error": "ELEVENLABS_API_KEY not set"}
    
    if not os.path.exists(BACKGROUND_BEAT_PATH):
        return {"audio_path": None, 
                "error": f"Background beat not found: {BACKGROUND_BEAT_PATH}"}
    
    try:
        # Step 1 — TTS
        voice = text_to_speech(mnemonic_text)
        
        # Step 2 — Background music
        music = prepare_background_music(len(voice))
        
        # Step 3 — Mix
        final_audio = mix_audio(voice, music)
        
        # Step 4 — Export
        final_audio.export(output_path, format="mp3")
        print(f"  Audio saved to: {output_path}")
        
        return {
            "audio_path": output_path,
            "duration_seconds": len(final_audio) / 1000,
            "error": None
        }
        
    except Exception as e:
        return {"audio_path": None, "error": f"Audio synthesis error: {str(e)}"}


    generation_result = generate_mnemonic(
        concept_list=sample_concepts,
        original_text=sample_text
    )

    if generation_result["error"]:
        print(f"Mnemonic generation error: {generation_result['error']}")
    else:
        mnemonic_text = generation_result["mnemonic"]

        print("\nGenerated Mnemonic:")
        print(mnemonic_text)

        print("\n" + "=" * 50)
        print("STAGE 3: AUDIO SYNTHESIS")
        print("=" * 50)

        audio_result = synthesize_audio(mnemonic_text)

        if audio_result["error"]:
            print(f"Audio synthesis error: {audio_result['error']}")
        else:
            print("\nSuccess!")
            print(f"Duration: {audio_result['duration_seconds']:.1f} seconds")
            print(f"Output file: {audio_result['audio_path']}")
        
