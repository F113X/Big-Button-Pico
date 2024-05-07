# Big-Button-Pico
LMNC Big Button remade with the Raspberry Pi Pico, with changes in code and functionality, and reprogrammed with micropython
Original build and documentation: https://www.lookmumnocomputer.com/big-button

![Big-Button-Pico](Images/big-button_orig_ref.jpeg)

**Disclaimer:**

This project will not work by replacing arduino with pico from the original schmatics as new code is written and functionality has changed.  New project files including PCB & stripboard layouts will be uploaded.

BOM has been uploaded, but the project is not tested yet so only use as reference

This is an ongoing project. Current progress does not allow fully making the project, however you could analyze the code and make the project based on that.
**Please point out problems in the code as it has not been tested yet.**


## Manual:
Inputs:
|Input name|Type|Function|
|----------|----|--------|
|Delete|Button|Delete current step|
|Clear|Button|Clear current track|
|Reset|Button|Clear all tracks|
|Fill|Switch & Jack|When from CV or switch, a second sequence will be played instead of the first one|
|Clock|Jack|Input a clock signal for sequencer|
|Trigger|Big Button|trigger and record a pattern with the big button|

Pots:
|Pot name|Function|
|--------|--------|
|Track|Select track 1-6|
|Step Length|Gate length of outputs|

Outputs:
|Output name|Function|
|-----------|--------|
|1|First track output|
|2|Second track output|
|3|Third track output|
|4|Fourth track output|
|5|Fifth track output|
|6|Sixth track output|