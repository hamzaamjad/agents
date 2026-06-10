# rough notes: shared prompt-snippets library (don't judge, brain dump)

Keep retyping the same prompt fragments into different agents — the
"summarize this PR like a changelog" one, the SQL review preamble, the
tone-guard paragraph for outreach drafts. Want one place to keep these.

Thinking: a `snippets/` folder somewhere in the agents workspace. One file
per snippet? Or one big yaml? Leaning one file per snippet, markdown with a
tiny header (title, maybe tags, date added). Easier to diff and copy-paste.

Things it needs, roughly:

- some way to list what's there quickly (a script? `ls` is probably fine to
  start, but titles live inside files, so maybe a tiny index command)
- copy a snippet to clipboard fast. pbcopy on mac. don't care about linux yet
- naming: kebab-case filenames, but titles can be whatever
- dedupe-ish: at least warn if I add a snippet whose title basically matches
  an existing one. fuzzy match is overkill, prefix match probably enough?
- versioning comes free if it lives in the repo. good.

Unclear stuff / haven't decided:

- where exactly does it live? top-level `snippets/` vs under an existing
  folder. top-level feels right but adds clutter
- do hosts (Cursor etc.) need to discover these automatically, or is this
  purely a human copy-paste library for now? probably the latter, v1
- is there a max size per snippet? some of mine are basically full briefs,
  maybe those belong elsewhere
- should the index command also grep snippet bodies, or titles only?

Not doing (at least now): templating/variables inside snippets, sharing with
other people, any kind of sync service, web UI. Plain files first.

TODO next: pick the folder location, sketch the header format, then write
maybe 5 real snippets in and see if the shape holds before any tooling.
