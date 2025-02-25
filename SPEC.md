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
 1) FULLY UNDERSTAND FASTER_WHISPER CODEBASE


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


## 02/24/2025

1) There has been some really interesting behaviour observed with whisper and especially faster_whisper, I will give an example of what I've been seeing because I think it's funny:

 testing for better truncation.
 
 Okay.
 
 Okay.  <-Repeats word (I think what's happening is the VAD is breaking up one word into multiple word slices where both slices map to the same output word (for example, 
 okay might get broken into oke-ayy where both oke and ayy predict an okay so okay gets said twice), this can mostly be resolved by fine-tuning the VAD threshold but it's never perfect, I think the best low-effort solution would be to set the VAD threshold dynamically based on the detected background noise present)
 
 Thank you. <-Whenver I chuckle or grunt, it thinks I am thanking it
 
 . <- I dont even know what sort of noise generates a period (my best guess is a grunt or some sort of glottal stop gets associated with a period somewhere in the attention layer but idk)
 
 testing for better truncation. <- Says what it was saying before for some reason, still need to figure this out

 Thanks for watching, and I'll see you in the next one! <- Complete hallucination, I never said this, but I may have grunted

 Thanks.    <- Chuckled again

 That's weird. <- Hey, it finally worked!


Verdict: Whisper was trained on a shitload of YouTube.

I think a lot of the issues above could be resolved by using a larger model, but I'm tryna make this this thing ghetto friendly because my T480 potato is the only thing I have right now that can rip cuda.

2) Proposed solution to the "Gracious Model Problem":
Whenver the model does not understand what I am saying, it tends to think that I am thanking it. This is especially evident in the case of grunts: for some reason, there seems to be something in the attention layer which is associating gruntiness with grattitude. An interesting and very nonrigorously determined result of this is that low intensity grunts are met with a "Thank you" while higher intensity grunts or grunts with a drawn out end are met with a "Thank you very much".
One naive way this could potentially be solved is by somehow extracting the confidence of answers given and replace them with something like *inaudible* if they are below a certain threshold. We may even be able to loosely identify these noises by things such as energy level, frequency spectrum etc, this way we could further differentiate between grunting, screeching, yodelling etc without using a larger model.

3) faster_whisper seems to have built in support for silero vad which runs on the ONNX runtime, which in theory should be a bit faster than the current torchscript (.jit) implementation I have, however I suspect that this performance boost is trivial. Aside from this, the other main speedups occur due to ctranslate being used for the model backend, and the possibility of batched inference. Upon first glance however, that batched inference seems to be for the cpu and not the gpu. Will need to look into that further. Ctranslate also isn't recognizing my gpu right now, which means that I can't run it in cuda mode. However, even in cpu mode it seems to be a bit faster than the standard whisper model, which is pretty impressive.

4) Right now it seems like pretty much every major pain point I'm dealing with comes down to not fully understanding the actual model/implementation that I'm working with, so I should probably just shut up and read the model code for a few days.