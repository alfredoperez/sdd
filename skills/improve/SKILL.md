---
name: sdd:improve
description: "SDD — Add improvement idea to Obsidian vault tracker."
---

## User Input

```text
$ARGUMENTS
```

If `$ARGUMENTS` is empty, stop and say: "Provide an improvement idea: `/sdd:improve <description>`"

---

## Steps

### 1. Read Current File

Read the file at `/Users/alfredoperez/dev/GitHub/obsidian-vault/Current.md`.

If the file doesn't exist, stop and say: "Obsidian vault file not found at `/Users/alfredoperez/dev/GitHub/obsidian-vault/Current.md`."

---

### 2. Find the SDD Section

Look for a section starting with `## SDD` in the file.

If no `## SDD` section exists, append one at the end of the file:

```markdown

## SDD

- [ ] {improvement description from $ARGUMENTS}
```

If the section exists, append the new item after the last existing `- [ ]` item in that section:

```markdown
- [ ] {improvement description from $ARGUMENTS}
```

---

### 3. Confirm

Display:

```
Added to SDD improvements:
- [ ] {improvement description}
```
