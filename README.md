💻 SmashAI

A Python UI designed to edit AI configuration files for Smash Ultimate (templates included).


⚠️ Prerequisites and ParamXML Usage

This program only handles XML files. You will need ParamXML to convert the game's .prc files.


🔄 Decoding PRC to XML

To decode the .prc into .xml (for editing):
```bash
./ParamXML.exe attack_list_param.prc -d
```

🔨 Assembling XML to PRC

To assemble the .prc from the .xml (after saving your changes):
```bash
./ParamXML.exe attack_list_param.xml -a
```


🧠 How the CPU AI Works (Observations)

The CPU AI's behavior (Level 9) is based on the following observations:

Movement: Jumps around randomly a lot (unless it's Little Mac; this must be hardcoded).

Defense: Shields or uses other defensive options if it anticipates an incoming hit (many questionable airdodges; it doesn't seem to spot dodge).

Attack: Performs an attack if it detects an opponent is "at range" and the situation is right.

💡 THIS is what this program is for: telling the AI WHICH attacks to use and in what "SITUATIONS" to use them.

(Note: Lower levels likely have a slower "processing speed," generally performing less. "Detection" hitboxes are coded elsewhere and haven't been modified.)

🎯 Available Attack Situations

The following are the situations this program edits (and the only ones found to be used by the game):

🥊 Close-Range & Kill Options

Quick attack: Fast attacks used at melee range for damage or frame trapping (Jab, quick tilts, Grab if quick enough).

Strong attack: Kill options, mainly Smash Attacks, but sometimes specials. The CPU might use these at lower percents if it thinks it can get away with a laggy attack.

💨 Spaced and Dashing Attacks

Spaced attack: Attacks used from a distance (projectiles and long-range attacks). Recommendation: Use 50% max to prevent the CPU from spamming and getting stuck on platforms.

Dashing attack: Used while the character is dashing (not just the Dash Attack). Jab becomes Dash Attack here. Great for Dash Grab or even RUN UP AND UP SMASH!

🛡️ Defensive and Edge Options

Out of Shield (OOS): Accepts only grounded options (no Nair, DK Up B). Best for Grab, Jab, Down Tilt, or quick Up B options (G&W, Cloud 🤢).

Ledge Trap (2 Frame): Used when near the ledge, on stage. Great for moves that can 2-frame or generally cover many ledge options.

Edgeguarding (Offstage): The only situation allowing for aerial moves (and only those). Used when near the ledge, in the air. Back Air (Bair) is a must, along with other moves to stuff out offstage opponents.

☁️ General Aerials

General Aerial: The most used aerial while on stage. Any time the opponent is close and the CPU is in the air. Often Nair/UpAir, but can be customized for characters with laggy or strange default aerials.

Rising Aerial: Rarely used. Good for laggy aerials that might be situationally useful (e.g., Dair or certain aerial specials).

Falling Aerial: Good for Fair, Bair, and other more spaced aerials used while falling.

⚠️ Warnings and Random Behavior

The CPU's behavior is highly random. Give it a few games; it might self-destruct nonsensically in one and play near-perfect the next.

They move around randomly and do very bad defensive options, but if they have to tech, from being launched on the stage (offtage mostly), they mostly tech, maybe like 75% of the time? Maybe more! (Pretty sure they should be able to always tech, but they are programmed to drop it on purpose, sometimes). They also are good at using the "Edgeguarding (Offstage)" to hit you while recovering, so be ready to tech!
They are kinda bad at combos, but they do a few (there are some modifiers on config files for what moves combo into what others, but I also didn't bother changing or testing much).

A few characters are kinda bad at recovery, and a few can't even use all their moves, like ZSS.
ZSS' Zair (almost) always comes out rising, even in the "Falling Aerial" situation, so I just gave up on using it (or most Zairs, for that matter).
ZSS also can't Flip Kick (as in using the kick attack during Flip Jump, down B), maybe because it's very easy to SD with it (I think it also never uses Dair offstage, Flip Kick could have been like that, but I didn't even kind a way to tell it to Flip Kick, as opposed to just Flip Jumping).

Speaking of, there's a list of special attacks that only a few characters have in special.txt, but I think the only really relevant one is Little Mac's KO Punch.
I was thinking of making it a seperate attack on the editor, I think there must be a way to detect that it is a Little Mac config file, and then enable this new option, I thought I had implemented it already, but I kinda forgot... I just manually put it at 100% for every option lol (manually, on the XML).
There's also each and every special move for Mii fighters, and the unique moves for shotos, but I mean, who cares? XD

Feel free to clone and branch this and add your own shtween, I was thinking of using pyprc to edit the PRC files directly, but then you lose the option to manually edit stuff like KO Punch and others that might not be on the UI... Also I only learned pyprc exists a few days ago, and I've been using this Python UI for months with ParamXML, and it worked just fine.
