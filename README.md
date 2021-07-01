# Ignis - FE14 Randomizer
Ignis is a simple randomizer for FE14 and the successor to the original Fire Emblem Fates Randomizer.

Compared to the original, Ignis has several advantages:
* Easier to use. Give it an extracted RomFS and somewhere to put the outputs and Ignis will figure out the rest. No copying files out of the ROM, compressing/decompressing, etc.
* New features. Randomize chest and village items, configurable stat randomization, and better join order randomization.
* More thorough. Route-specific stats, proper handling of weapon exp, etc.
* More stable. FE14 hacking's come a long way since 2016.

## Usage
1. Assuming you have a ROM of the game (*.3ds, *.cxi, *.cia, etc), you need to extract the RomFS from the game. End result of this step is a folder containing the game files, **not** romfs.bin. Extracting files from your game ROM is outside of the scope of this readme, but you can use one of the methods/tools listed below:
    * Right click on Fates from Citra's game menu and select "Dump RomFS"
    * DotNet3dsToolkit: [https://github.com/evandixon/DotNet3dsToolkit](https://github.com/evandixon/DotNet3dsToolkit)
    * Ninfs: [https://github.com/ihaveamac/ninfs](https://github.com/ihaveamac/ninfs)
    * (Command Line) CTRTool: [https://github.com/3DSGuy/Project_CTR/releases/tag/ctrtool-v0.7](https://github.com/3DSGuy/Project_CTR/releases/tag/ctrtool-v0.7)
 2. Create a directory for the outputs (can either put your mods like Gay Fates in there or leave it empty). This is where your randomized files will go.
 3. Open Ignis and select your extracted romfs folder (step 1) and output folder (step 2).
 4. Select the ROM language.
    * For Japanese versions of the game, this must be Japanese.
    * For NA versions of the game, this must be EnglishNA.
    * For EU versions of the game, anything but Japanese or EnglishNA. If you want English text, you **must** select EnglishEU, **not** EnglishNA.
 5. Select whatever options you want and click randomize.
 6. You will get a popup when the randomizer is done. Copy the outputs to either your mods folder (Citra) or layered fs folder (Luma) and start the game.
    
## Building
The build process is identical to [Paragon](https://github.com/thane98/paragon).

Ignis requires Rust and Python 3.8.x. You will also need to install the python packages listed in `requirements.txt`. More on this below. If you want to build a standalone executable, you should also install PyInstaller.

1. Install the virtualenv package for Python. This is used to create an environment for building.
2. If you have not already done so, create a virtual environment for the project by running `virtualenv venv` in the root directory of the project. This should produce a folder named "venv".
3. Enter the virtual environment by running the appropriate command for your operating system. In Windows Powershell, for example, the command is "./venv/Scripts/activate.ps1".
4. Install the required python packages. You can do this conveniently by running `pip install -r requirements.txt` from the root directory of the project.
5. To build the Rust backend, run `maturin develop --release` from the root directory of the project. This will produce a "target" folder and a "pyd" file in the ignis folder.
6. If the install succeeds, you can run the main script with the command `python ignis/ui/main.py`.

## Credits
- DeathChaos, TildeHat, Moonling, and RainThunder for research and reverse engineering that made Paragon and Ignis possible.
- @SinsofSloth and @muhmuhten for contributions to Paragon which handles most of the low-level details for Ignis.

## License
Unless explicitly stated in a file, this project is licensed under the GNU General Public License 3.0.
