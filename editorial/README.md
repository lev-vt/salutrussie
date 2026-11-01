# SalutRussie — ChatGPT editorial workspace

Status: DRAFT ONLY. This directory is not part of the public site.

## Ownership
- ChatGPT editorial team: work only on `editorial/guides/**` on branch `editorial/chatgpt-guides`.
- Codex development team: owns site generator, HTML/CSS/JS, tests and deployment. It reviews and imports approved draft content from the editorial branch into its own development branch.
- The `main` branch and deployed site are not automatically modified.

## Required editorial outputs per guide
- `article.md`: complete Russian practical guide.
- `source_audit.md`: legal claims, official sources, provisions, effective dates, unresolved questions.
- `seo.json`: title, meta description, slug, user intent, FAQs and related links.
- `visual_brief.md`: diagrams/illustrations/interactivity brief; no decorative invented stock content.
- `editorial_qa.md`: independent review, corrections, approval status.
For the 2027 income guide, also provide `calculator_spec.md` and `calculator_tests.json` with legally verified logic. Do not invent regional numeric parameters.

## Editorial standards
- Prioritize 5 exceptional, current and practical guides; extend only when quality warrants it. Do not force 10.
- Check each material legal statement using current primary law, official publications and effective dates. Mark future-effective and disputed rules.
- Write comprehensible, actionable guides with tables, examples, FAQ and useful visuals. Optimize for SEO and AI retrieval without keyword stuffing or unsupported guarantees.
- Compare with existing site pages to prevent duplicates/cannibalization.
- Preserve the approved Claude design, approved copy and business positioning; do not create or edit public site files from the editorial branch.
- Russian first; FR/EN localization deferred.
- Never include Telegram member names, message IDs, verbatim private conversations, client files, secrets or other personal data in GitHub, including editorial notes or source archives.

## Handoff
- ChatGPT commits reviewed content to this branch with useful version history, without merging or force-pushing.
- Every guide starts as `draft`; editorial completion does not equal legal/publication approval.
- Codex first inventories any local unsynced work, checks conflicts, then imports approved files, performs code/UX/QA tests and publishes only with owner approval.
- Baseline tag: `baseline-pre-ai-ru-v3.2`. Do not delete or rewrite it.
