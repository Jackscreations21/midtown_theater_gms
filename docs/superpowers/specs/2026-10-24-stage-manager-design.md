# The stage manager: calling the show, the calls, the company backstage, the booth's operators (2026-10-24)

Jack, verbatim:

> *"make a stage manger thing where i can call ther show and i can give 5 minuet and plcsses calss for the actors and make
> it so there are atcually people in the spotbooth moving the lights and think of somemore stuff for it"*
>
> *"make it so you can have it where i have to start each song or i just have to call the starts of both halfs"*

His answers (2026-10-24), binding:
- **What a GO does:** *"i just call when to start the lgihting and sound sequenses"*. His GO starts a sequence: the
  song's audio and its cues together. Inside a sequence the cues run on the clock as they do now. He does not call
  individual light cues.
- **Where:** a prompt desk in the stage-left wing of house 1.
- **The calls:** real backstage. Before the show and in the interval the company is in the dressing rooms and the green
  room. A call is answered, "places" walks them to where they start, and the show cannot GO until everyone is there.

## RULINGS

**GM: the calling modes.** A switch on the desk, `songs` or `acts`:
- `songs`: the show HOLDS at the top of every number (the clock stops at the track's start, lead-in included).
- `acts`: it holds only at the top of Act One and at the top of Act Two. Between those holds the album runs on, number
  into number, as the Show panel's Play does now.

A held show waits for GO. GO starts the held sequence: the clock runs, the audio plays from that point, and the cues
fire as they do now. The interval hold that exists today (`SHW.hold`, `track.hold`) is the act case of this one
mechanism; build both off it. With the desk not in use, the Show panel behaves exactly as it does today.

**GN: STANDBY before GO.** The desk's caller says *"Standby lights and sound, <number>"* and the operators answer
*"Standing by"*. GO is allowed without a standby, and the show report notes it. A GO is not refused for being early or
late; there is nothing to score against, since the cues inside a song are on the clock.

**GO: the desk.** It stands in house 1's prompt corner (the stage-left wall, beside the worklight switch box, facing the
stage), at deck level. It is a physical prop:
- a sloped desk top with the prompt book;
- a small monitor showing the stage. This is a live top-down plan with the bodies as dots, drawn into a canvas a few times
  a second, NOT a second 3D render;
- two cue lights (red STANDBY, green GO);
- a headset on a hook, and a paging microphone (the "God mic").

E at the desk while walking opens the CALLING PANEL and sits the walker there; E or Esc leaves. The panel is HTML,
like the Show panel. It holds:
- the mode switch;
- the state (PRESHOW · HOUSE OPEN · HALF · FIFTEEN · FIVE · PLACES · ACT ONE · INTERVAL · ACT TWO · CURTAIN);
- the next sequence;
- STANDBY and GO (keys S and Space, as well as the buttons);
- the calls;
- who has answered;
- who is at places;
- the clock;
- the headset log.

**GP: the calls and the company.** The calls are:
- *House open*, *Half hour* (35 min before), *Fifteen*, *Five*, *Places* before Act One;
- *Fifteen*, *Five*, *Places* in the interval;
- *Curtain* after the bows.

Times are not enforced. He gives each call when he wants, in any order, and the calls only move the company.
- A call goes over the God mic: the HUD shows it, and the browser's speech voice (`speechSynthesis`) speaks it, with a
  desk toggle. Each actor ANSWERS (*"Thank you five"*). The panel lists who has answered, and a little bubble rises over
  each head.
- Before PLACES, the company lives backstage. Each body has a home (dressing rooms 1–4, the green room, wardrobe) and
  idles there.
- PLACES walks every body from wherever it is, through the crossover and the two slots beside the set, to its START: its
  first waypoint of the act if that is on stage, else the wing that waypoint's entrance comes from. Each body reports
  *"at places"* when it arrives.
- **The first GO of an act is refused until every body is at places.** The panel names who is missing; an override
  button reads "GO anyway". At the interval (the end of 1-23) the company walks back to its homes, and it walks off after
  the curtain.
- The backstage walking is a separate layer over the blocking. While the SM's state is a backstage state, it decides
  each body's pose. Once the act's GO fires, the blocking owns the body again, from the place it was walked to. That
  place IS the blocking's pose at the act's top, so there is no jump.
- Routes run on a small hand-made graph of points: each room's door, the crossover, the two slots, and the wings. There
  is no pathfinding. Speed is ACT_WALK. A body does not walk through a closed door: the route opens it as the walker's E
  would, and leaves it as it found it.

**GQ: people in the booth.** Three operators, one behind each Lycian in house 1's booth, built from the same mannequin as
the company:
- Each stands at its spot with its hands on the handles. Its body yaw and arms follow the unit's pan and tilt every frame
  (from the followspot engine's aim), so you see them swing the light onto whoever it picks up.
- When the spot is dark the operator relaxes: hands off, a weight shift. They wear headsets and answer the SM's standby
  (*"Spot one standing by"*).
- A lighting operator and a sound operator sit at house 1's lighting desk position (`buildDeskPosition`). The lighting
  operator reaches for the desk on each GO.

## Proposed, built in v1 (Claude's additions to "think of some more stuff")

1. **Headset chatter.** Standbys answered by Lights, Sound and Spots 1–3. Spot operators say *"Spot two, I have
   Hamilton"* at a pick-up, as text in the panel's headset log; speaking it aloud is off by default.
2. **Cue lights** at the desk, the booth and both wings: red on STANDBY, green on GO, out after.
3. **Front of house.** A house manager on the headset:
   - *"House is open"* at HOUSE OPEN; the house lights at full and the preshow look.
   - At *"Clear to start?"* the FOH answers *"House is in, you're clear"* once places is complete.
   - A short preshow announcement. **The text is ours**: phones off, no photography, enjoy the show. No lyrics, no
     production copy. It is spoken on GO of Act One before the house goes out.
4. **The show report.** At CURTAIN, a report of:
   - the date and time of each call and each GO;
   - the run time of each act, and the length of the interval;
   - every GO without a standby, and every "GO anyway" with who was missing;
   - a notes box.
   
   It downloads as a text file, and the panel keeps the last one in localStorage.

## Proposed, NOT built (FUTURE.md, his to pick)

- An actor late to places (sometimes someone is in the WC when PLACES is called), so a hold matters.
- The audience filling the seats before HOUSE OPEN ends, as low-poly silhouettes. A frame cost to measure first.
- A show relay: the stage's sound at low level in the backstage rooms and the corridor.
- Calling individual light cues (a "calling" mode where his GO fires each cue rather than each sequence). This is
  ruled OUT for now by his answer.

## The contract between the parts (three builders)

`MIDTOWN.sm`, the desk and calling, is built by builder A. It owns the state machine, the panel, the holds, the
headset log and the report. It calls B and C only through these:

```js
MIDTOWN.company.call(kind)        // kind: 'half'|'fifteen'|'five'|'places'|'interval'|'curtain'|'home' — returns nothing;
                                  //   answers arrive as events
MIDTOWN.company.state()           // { mode: 'show'|'backstage', bodies: [{ id, label, where: 'home'|'walking'|'places'|'stage',
                                  //   answered: {five: true, …} }], atPlaces: n, of: n, missing: [ids] }
MIDTOWN.company.on(fn)            // fn({ type: 'answer'|'atPlaces'|'allPlaces', id, call, text }) — one listener list
MIDTOWN.company.act               // 1 or 2: which act's starts PLACES walks to (A sets it)
MIDTOWN.booth.say(text, who)      // C's operators' replies come back through MIDTOWN.sm.log(who, text) (A provides)
MIDTOWN.booth.standby() / .go()   // C's cue-light lamps and the lighting operator's reach
```

Builder B owns `MIDTOWN.company`, its homes, routes and walking layer, and the hook into `actPose` / `actTick`. That
hook must be a pure function of (the SM state, the call's start time, the walk clock) so that a seek in show mode is
untouched.

Builder C owns `MIDTOWN.booth`: the operators in both house 1 rooms (the booth and the desk position), and the cue-light
lamps outside the SM desk.

The SM desk's own lamps are A's.

**What must not change:** the show with no SM in use (the Show panel's Play, seek, the checks:
`show.check()`, `actors.check()`, `follow.check()`, `lx.check()` 301/313), Theatre 2, the walk's other doors, and the
frame cost with the SM idle. Each builder measures it.
