# Temporary Change Tracking

This directory tracks **temporary summaries of changes** made during development sessions.

## 🎯 Primary Purpose

Track work-in-progress changes and modifications:
- **Change summaries**: What was modified in each session
- **File change logs**: Which files were created/updated/deleted
- **Work notes**: Context and reasoning for changes
- **Session progress**: What was accomplished
- **Next steps**: What needs to be done next

## ⚠️ Important

- This directory is in `.gitignore`
- All files here are excluded from version control
- Move completed summaries to `summary/` when ready to commit
- Keep temporary change logs here until changes are finalized

## 📝 Appropriate Uses

### ✅ Good - Use temp/ for:
- **Change summaries** for current work session
- **File modification logs** (what files were changed)
- **Work-in-progress notes** and context
- **Session progress** tracking
- **Draft summaries** before moving to `summary/`
- **Experiment results** and findings
- **Temporary documentation** being developed
- **Local development notes**
- **Quick reference** for ongoing work

### ❌ Bad - Do NOT use temp/ for:
- **Final summaries** (use `summary/`)
- **Specifications** (use `specs/`)
- **Source code** (use `src/`)
- **Permanent documentation** (use `docs/`)
- **Anything that should be committed to git**

## 🗂️ Recommended Organization

```
temp/
├── sessions/                      # Daily/session change logs
│   ├── 2026-01-10-session.md    # Today's changes
│   └── 2026-01-09-session.md    # Yesterday's changes
│
├── changes/                       # Detailed change summaries
│   ├── feature-x-changes.md     # Changes for feature X
│   └── refactor-notes.md        # Refactoring notes
│
├── drafts/                        # Draft documents
│   └── new-feature-draft.md     # WIP drafts
│
└── notes/                         # Quick notes
    └── ideas.md                   # Random ideas
```

## 📋 Change Log Template

Create a file like `temp/sessions/2026-01-10-session.md`:

```markdown
# Work Session - January 10, 2026

## Summary
Brief description of what was accomplished in this session.

## Files Changed

### Created
- `path/to/new-file.py` - Description
- `another/file.md` - Description

### Modified
- `existing/file.py` - What was changed
- `config.yaml` - Added new settings

### Deleted
- `old/deprecated-file.py` - Why it was removed

## Changes Made

### Feature: Multi-Agent Support
- Implemented agent registry
- Added agent configuration loader
- Created agent routing logic

### Bug Fixes
- Fixed issue with context overflow
- Resolved memory leak in cache

### Documentation
- Updated README with new features
- Added examples to specs

## Next Steps
- [ ] Complete agent orchestration
- [ ] Write unit tests for agent registry
- [ ] Update API documentation

## Notes
Any important context, decisions made, or things to remember.
```

## 🧹 Cleanup Strategy

### When to Move Files
- **To `summary/`**: When change summary is complete and ready to commit
- **To `specs/`**: When draft specs are finalized
- **Delete**: When notes are no longer needed

### Cleanup Schedule
- **Daily**: Review session notes, move completed work
- **Weekly**: Archive old session logs
- **Before Commits**: Ensure important changes are documented in `summary/`

## 💡 Best Practices

1. **Date Everything**: `2026-01-10-feature-name.md`
2. **Session Logs**: Create one per work session
3. **Move When Done**: Transfer completed summaries to `summary/`
4. **Keep It Current**: Focus on recent work (last 7-14 days)
5. **Context Matters**: Include why, not just what

## 🔄 Migration Path

When work in temp/ is ready to be permanent:

```bash
# Draft specification → specs/
mv temp/drafts/new-feature.adoc specs/

# Summary document → summary/
mv temp/notes/feature-summary.md summary/

# Implementation code → src/
mv temp/experiments/new_module.py src/local_prompt_agent/
```

## 📋 Current Contents

This directory should remain mostly empty. If you see many old files here, it's time for cleanup!

---

**Remember**: Everything in this directory can be deleted at any time. Save important work elsewhere!
