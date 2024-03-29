# Helios

Helios is a can-sized satellite development team participating the [Esero CanSat competition](https://esero.es/cansat/).

The Helios satellite is developed by a team of 6 people and a mentor, we're not going to disclose team members or the development location yet.

# Roadmap
The Arduino Firmware has the codename NyanSat. Versioning format: letter+number, e.g. a1, a2

Any version starting in version A, its code will primarily focus on getting a correct output on all sensor data.

Any version starting in version B, its code will focus on the correct transmission of data over radio

Any version starting with letter B or C will try to implement transmission redundancy, like error correction and acknowledgement system.

# License
Pending license

# Open-source acknowledgements
This project contains the signed binary of com0com, which is under the [GNU General Public License v2.0](https://tldrlegal.com/license/gnu-general-public-license-v2) license. Its source code and binary can be obtained via [sourceforge](https://sourceforge.net/projects/com0com/).

The binary of com0com (3.0.0.0 64 bit) included in this repository is obtained via [akeo.ie](https://pete.akeo.ie/2011/07/com0com-signed-drivers.html), its driver binary has been replaced by the one provided by Windows Update. `setupg.exe` was extracted from the installer on sourceforge.
