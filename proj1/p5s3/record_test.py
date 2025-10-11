import sounddevice as sd
from scipy.io.wavfile import write

fs = 44100  # 샘플레이트(Hz)
seconds = 5  # 녹음할 시간(초)

print("🎙 녹음 중... 말해보세요!")
audio = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='int16')
sd.wait()  # 녹음이 끝날 때까지 대기

write("output.wav", fs, audio)  # 파일 저장
print("✅ 녹음 완료! output.wav 파일이 생성되었습니다.")
