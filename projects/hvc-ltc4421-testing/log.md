# TEK0000:
12V Supp going up from 9 to 9.5 to 10.4

# TEK0001:
Same as above but with 1.5 A current limit, same behaviour

# TEK0002:
Now 1 A current limit. DCDC and Supp connected by jumper wire.

Obv wouldn't do anything because DCDC UVR is 11 V.

# TEK0003:
Trying to jump in directly at 10.4 V, same behaviour as rising up.

# TEK0004:
Trying to really get the waveform of the oscillation on rising and falling, to determine if it's a capacitor charging & discharging or not.

Supply voltage: 9.5 V

# TEK0005:
Same as above but V 12V supply = 10.3 V

# TEK0006:
Probing UVR SUPP

voltage scale is now 100 mV per divison

We have trigger on CH1, 12V out and saving CH2, UVR SUPP. This way we record UVR during the rising edge of the oscillation.

# TEK0007:
Same as above but better data.

(Actually, idk what the data for TEK0006 is, but the description of it is what we did for TEK0007)

# TEK0008:
Tigther time scale:
x time div: 500 uS

Same as TEK0006 description, UVR SUPP during rising edge of oscillation.

# TEK0009:

x time div: 100 us
-500 mV offset so our default value is centered on zero, now we're looking at noise.

Wow!

# TEK0010:

Probing power supply input (12V supp test pin on HVC) to see if it's oscillating and causing the oscillation on UVR (voltage divided from 12V Supp)

Huge oscillation still! On the input! (12V_Supp pin that the alligator is connected to)

# TEK0011:

Holding up the wire to prevent parasitic inductance, which didn't work because the wires themselves are the parasitic inductance, and holding them straighter doesn't reduce it too much.

# TEK0012:

Put oscilloscope on the terminals of the PSU itself, and saw all noise disappear! The parasitic inductance in the wire is the issue! Well, mostly disappear, it's still there! Parasitic inductance from the wires in the PSU?

# TEK0013:

Using smaller alligator wires to reduce parasitic inductance.

Looks like it didn' change, maybe a different PSU?

# TEK0014:

The waveform just as the HVC went fully on instead of oscillating.
ie. when we go from 10.3 to 10.4 V.

Except it didn't save right, try again.

# TEK0015:

Same as above.

# TEK0016:

Same as above.

Why does it start working at 10.4 V? Why not work at 9.8 V? Nothing looks different in the waveform!

# TEK0017:

Now with the PS280 DC PSU instead of the PWS2323.

Only started working at 12 V!!!! Not 10.4!

Switching back obv.

# TEK0018:

We set UVR = 8.5, UVF = 8.0 V, expecting the greater range to mean the noise is less of an issue, because the noise wouldn't reach as high (not to OV). Turns out this didn't work.

Remember to retune UVR and UVF later!

# LTSpice Note:

I'm using R = 1 ohm and C = 100 nF to backfit what the inductance could be. Then, with all values in the RLC circuit we can retune R or C to change the behaviour as we see fit.

I get a value of ~300 uH!!! Extremely high! With Chris D asked claude its guess was 143 uH, so same order.

Certainly most of this is coming from the PSU and not the wires.

Decreasing capacitance to 10 nF makes our amplitude much smaller.

Increasing R to 10 ohms makes the oscillation much more damped.

We can try replacing the capacitor with a 10 nF one.

# Next test:

Chris D just tuned UVR to 9.5 V and UVF to 7 V, huge hysteresis value, and it seemed to work very well! This matches functionality with V3, good MVP.

# TEK0019:

We replaced the 100 nF capacitor with a 10 nF one.

# TEK0020:

Redo of one above, didn't get good capture for 19.

# TEK0021:

Same replaced capacitor, now testing UVR Supp instead of 12V Supp test pin on HVC.

# TEK0022:

Again on UVR Supp but with 1 ms total instead of 2.5 ms, to overlay onto test 9.

# TEK0023:

Supp gate voltage with same setup as before, 10 nF and 1 ms total time.

# TEK0024:

12V out directly after the save above, since Gate_Supp = Out + 12

# TEK0025:

12V out with a greater time scale to see if we're going on, then off, then on again. As we saw before with 100 nF.

# TEK0026:

Trying Gate_supp again since it seems like it was too low in test 23.

# TEK0027:

Same as 26

# TEK0028:

SAme as 26
