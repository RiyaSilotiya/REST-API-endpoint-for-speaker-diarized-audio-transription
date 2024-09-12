from django.shortcuts import render
import os
from django.shortcuts import HttpResponse
from django.http import HttpResponseServerError
from django.http import JsonResponse
from transformers import pipeline
import subprocess
from django.conf import settings 
from django.conf.urls.static import static
import soundfile as sf
from pyannote.audio import Pipeline
from pydub import AudioSegment
import numpy as np
from django.contrib import messages 


from rest_framework.decorators import api_view
from rest_framework.response import Response

# Load the ASR model once when the server starts
asr_model = pipeline(model='openai/whisper-base',task='automatic-speech-recognition')

pipeline1 = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token="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")


def extract_segments(audio_file, diarization):
    audio = AudioSegment.from_wav(audio_file)
    segments = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        start_ms = turn.start * 1000
        end_ms = turn.end * 1000
        segment = audio[start_ms:end_ms]
        segments.append((segment, speaker, turn.start, turn.end))
    return segments

def transcribe_segments(segments):
    transcriptions = []
    for segment, speaker, start, end in segments:
        # Save the segment to a temporary file
        segment.export("temp_segment.wav", format="wav")

        # Transcribe the segment using Whisper
        transcription = asr_model("temp_segment.wav", return_timestamps=True , generate_kwargs={"language": "english", "task": "translate"})

        # Store the transcription with the speaker and time information
        transcriptions.append({
            "speaker": speaker,
            "start": start,
            "end": end,
            "transcription": transcription["text"]
        })

        # Remove the temporary file
        os.remove("temp_segment.wav")

    return transcriptions

@api_view(['GET','POST'])
def predicts(request):
    if request.method == 'POST' and request.FILES.get('audio_file'):

        try:
            messages.info(request, "please wait!!")
            audio_file = request.FILES['audio_file']
            upload_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            audio_file_path = os.path.join(upload_dir, audio_file.name)
            print(audio_file_path)
            with open(audio_file_path, 'wb+') as destination:
                for chunk in audio_file.chunks():
                    destination.write(chunk)

            print(f"Audio file saved at: {audio_file_path}") 

# Convert the file to WAV format using pydub
            try:
            
                audio = AudioSegment.from_file(audio_file_path)
                louder_audio = audio + 30

                louder_audio.export(audio_file_path + '.wav', format="wav")  # Append .wav extension
                converted_audio_path = audio_file_path + '.wav'
                print(f"Audio file saved at: {converted_audio_path}")
            except Exception as e:  
                print(f"Error converting to WAV: {e}")
                return HttpResponseServerError("Error processing audio file (conversion).")



            combined_annotation = pipeline1(converted_audio_path, num_speakers=2)
            # print the result
            for turn, _, speaker in combined_annotation.itertracks(yield_label=True):
                print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")

            # Extract segments based on diarization results
            extracted_segments = extract_segments(converted_audio_path, combined_annotation)
            
            transcriptions = transcribe_segments(extracted_segments)

            for t in transcriptions:
                print(f"{t['speaker']} from [{round(t['start'], 4)} - {round(t['end'], 4)}]: {t['transcription']}")
            # Perform automatic speech recognition

            result = asr_model(converted_audio_path,return_timestamps=True , generate_kwargs={"language": "english", "task": "translate"})
            
            print(f"ASR result: {result}") 

            # Clean up the temporary file
            os.remove(audio_file_path)
            os.remove(converted_audio_path)
            if os.path.exists("temp_segment.wav"): 
                os.remove("temp_segment.wav")
            
            # Pass the transcription result to the template context
            context = {
                'speaker_info': [
                    {
                        'speaker': t['speaker'],
                        'start': round(t['start'], 4),
                        'end': round(t['end'], 4),
                        'transcription': t['transcription']
                    }
                    for t in transcriptions
                ],
                'overall_transcription': result['text'] 
                
            }
                    # context = {'transcription': result}
            return Response(context)
            # return render(request, 'upload_audio.html', context)
            #return JsonResponse(context, safe=False)
        except Exception as e:
            print(f"Error processing audio file: {e}")
            return HttpResponseServerError("Internal Server Error: " + str(e))  
    elif request.method == 'GET' :
        print("you hit the get request")


    else:
        return render(request, 'upload_audio.html')



