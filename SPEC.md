# Sub-Components
 1. Audio stream (system audio feed or microphone)
 2. Audio slicer (need to decide between dsp or ML-based VAD)
 3. Model handler (whispercpp for final implementation)
 4. Output handler (terminal feed)


 # Optimization Hierarchy
 1. Model: -> whispercpp
 2. Audio slicer: -> Custom VAD/slicer implementation in cpp
 3. Audio stream: -> Custom pipewire interface
 4. Output handler: -> Way less optimization needed but a c/cpp implementation is required in order to package the whole thing as a binary -> NOT TRUE, USE PYINSTALLER/NUITKA
 

 # TODO:
 1) Clean up code and remove un-necessary objects -> DONE
 2) Better list flattening -> Current method actually works well
 3) Optimize all python code / redundant operation check
 4) Figure out whisper context optimization -> NEED TO IMPLEMENT DYNAMIC CONTEXT LENGTH, <-NOT WORTH IT FOR NOW, SHOULD BE DONE AT SOME POINT THO
 5) Refine display logic
 6) Move to whispercpp -> REDACTED: MOVE TO FASTER_WHISPER; DONE 
 7) Thread safety fixes
 8) Get a MacOS/Metal port running so I don't have to write all this on my shitbox thinkpad (RIP my suicidal XPS)

 69) Design audio router architecture (this will be a pain in the ass because there is no pre-built library for speaker audio capture)


# Current state of afairs:

## 02/21/2025:

The first two lines I am speaking normally while taking a brief break in the middle to let the model catch up. There are small misses but the overall translation quality is decent. However, when I start freestyling, the model has a stroke:

Transcript: ["The threshold filtering actually seems to work really well when it's used in conjunction with the VAD.", "Wow, it's even recognizing that that's pretty good. This is way better than I was expecting.", 'ew hook! WOAH! WOAH! WOAH! WOAH! WOAH! WOAH! WOAH! WOAH! WOAH! WOAH! WOAH! WOAH!']


So far two things have been ascertained: 

1) A much faster Whisper model should be used

2) Whisper turns into a Choomah when it is overwhelmed



## 02/22/2025:

1) Sinusoidal positional encoding is cool, should write about it at some point.

2) Whispercpp needs to be modified to support variable size context windows like in the Python library otherwise there will be like 29.434 seconds of zero-buffering slowing it down each transcription cycle. I think this modification could be substantial enough to justify releasing it as its own fork.



## 02/23/2025:

1) I should start writing these while not sleep-deprived because it's obvious now that the Python library also zero-pads the input, it just does so with the spectrogram buffer converted from the variably-sized array passed to it. This means that based on testing so far, a mostly zeroed context window requires significantly less compute than a full context one, however it's still obviously not ideal. As I learn more about this, it also seems like these changes need to be made at the model architecture level which could be very painful and probably require re-training. It seems like there is an existing technique called varied-size attention window (VSA) that is already used in image transformers, but its main use case is to increase accuracy and it actually increases the overall compute cost of the system. Since our concern is speed not accuracy, I don't think this is applicable in its current form. I think this would be a cool research project actually. Additionally, whispercpp tiny.en seems to be fast enough in its current form for most practical use-cases so I think that this should be another project for another time as there is still opportunity to build a really high-performing system as-is.

2) There's a model called faster-whisper that might be faster than whispercpp. Overall it might be easier to use faster-whisper and then package the whole thing as a binary via pyinstaller/Nuitka, then figure out model improvements afterwards. Current performance is already satisfactory as long as spazzing on the mic does not occur.

3) I've intentionally used a really shitty computer for testing so far such that the effects of optimization decisions are viscerally felt. There is a greater than 0% chance that this thing runs way faster on a modern system to the extent that a larger model can be used such that both the transcription quality and speed improves.
