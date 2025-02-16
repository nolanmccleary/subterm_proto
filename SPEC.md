## Sub-Components
 1. Audio stream (system audio feed or microphone)
 2. Audio slicer (need to decide between dsp or ML-based VAD)
 3. Model handler (whispercpp for final implementation)
 4. Output handler (terminal feed)


 ## Optimization Hierarchy
 1. Model: -> whispercpp
 2. Audio slicer: -> Custom VAD/slicer implementation in cpp
 3. Audio stream: -> Custom pipewire interface
 4. Output handler: -> Way less optimization needed but a c/cpp implementation is required in order to package the whole thing as a binary 
 

 # TODO:
 1) Get full prototype for basic mic feed
 2) Design audio router architecture (this will be a pain in the ass because there is no pre-built library for speaker audio capture)