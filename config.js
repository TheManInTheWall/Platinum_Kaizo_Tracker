// ─────────────────────────────────────────────────────────────────
// PERSONAL CONFIG — your own settings, kept separate from the app
// logic and the trainer list so they never get lost or overwritten
// when the tracker itself gets edited.
//
// Edit the values below. Nothing else in this file needs to change.
// ─────────────────────────────────────────────────────────────────

// ── GitHub sync (Push to GitHub button, save.json auto-sync) ──────
const GH_OWNER='themaninthewall';       // your GitHub username
const GH_REPO='Platinum_Kaizo_Tracker'; // your repo name
const GH_FILE='save.json';              // filename in the repo

// ── Team tab — external Google Sheet someone else maintains ───────
const TEAM_SHEET_ID='1UVjtaEREAyYAMTPwyuNTrvlbESYtsWy956Cqj-guWPE';
const TEAM_SHEET_GID='825940800';        // gid of "Full List" tab
const TEAM_SHEET_GID_FALLEN='59463193';  // gid of "Fallen" tab
const TEAM_CREDIT = '/u/OpticalPlays'; // ← put their actual name/handle here

// Catch Log tab: how often (in minutes) to auto-check the sheet for newly
// added Pokémon while that tab is open. Set to 0 to disable auto-polling
// entirely (manual "Check now" still works).
const TEAM_AUTOLOG_INTERVAL_MIN=5;


// Combine specific Pokémon together in the Stats tab (Obtained/Died/Method
// breakdown, Trades, Natures) — e.g. treat a baby form and its evolution as
// one entry. Left-hand name gets folded INTO the right-hand name.
// Example: { "Azurill": "Azurill/Azumarill", "Azumarill": "Azurill/Azumarill" }
const SPECIES_ALIASES={
   "Azurill": "Azurill/Azumarill/Marill",
   "Azumarill": "Azurill/Azumarill/Marill",
  "Marill": "Azurill/Azumarill/Marill",

  "Prinplup": "Piplup",
  "Piplup": "Piplup",
  "Empoleon": "Piplup",

  "Grotle": "Turtwig",
  "Turtwig": "Turtwig",
  "Torterra": "Turtwig",

  "Monferno": "Chimchar",
  "Chimchar": "Chimchar",
  "Infernape": "Chimchar",

  "Spinarak": "Ariados",
  "Ariados": "Ariados"
};
// Pure DISPLAY layer on top of the above — the real/combined species name is
// still used for matching, tallying, and searching everywhere; only the text
// shown to you gets swapped for the nickname. Key by the name SPECIES_ALIASES
// resolves TO (the canonical/combined form), not the raw sheet spelling.
// Matching is case-insensitive, same as SPECIES_ALIASES.
const SPECIES_NICKNAMES={
  "Ariados": "Webarak Obama Der Spinnenpräsident",
};
