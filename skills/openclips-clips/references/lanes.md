# The clips lanes, as last recorded

Recorded from the live catalogue on 2026-09-11 (pin `9e85097`). This is a map for choosing, not the database: ids, durations, languages and inputs move when the catalogue's upstream pin moves, and `openclips:clips_catalog` wins on every disagreement.

| Kind of film | Id at time of writing | Duration then | Reads a language | Casts creators | Notes then |
|---|---|---|---|---|---|
| One talking creator, phone-shot | `ugc-15` | 15 or 30 | yes | one | some formats take a second reference image |
| Same film per language | `ugc-multilang-30` | 20 or 30 | one per submit | one | billed per language |
| Presenter plus app screens | `saas-30` | 10 to 30 | yes | one | product URL required; resolution priced here |
| Two people talking | `two-voice-15` | 15 or 30 | locked to English | two | the only lane that reads a `saas` flag |
| Short cinematic commercial | `cin-10` | locked at 10 | locked to English | none, ignored | some formats burn a hook and call to action in verbatim |
| Premium cinematic commercial | `cin-15` | 15 or 30 | locked to English | none, ignored | |
| Narrated paper collage | `paper-collage-40` | 20, 30 or 40 | locked to English | one, as narrator | formatless; product or category, never both; a category run still needs a brand in the workspace |

Two traps the table cannot show:

- A field the lane ignores is accepted, dropped and billed. Only the catalogue's `ignored` bucket tells you which fields those are.
- The catalogue's `durationMenu` is what the workspace can be billed for, and its default is what an omitted duration is quoted at. A lane with a `null` menu cannot be priced and should not be offered.
