# How to Track Changes in temp/

Quick reference for using `temp/` directory to track your development sessions.

## 🎯 Purpose

The `temp/` directory is for **tracking work-in-progress changes** before they're finalized and committed to git.

## 📝 Quick Start

### 1. Start a New Session

Copy the template:
```bash
cp temp/TEMPLATE_session.md temp/2026-01-10-my-work.md
```

Or create manually:
```bash
touch temp/$(date +%Y-%m-%d)-session.md
```

### 2. Track Your Changes

As you work, update your session file with:
- ✨ Files created
- ✏️ Files modified  
- 🗑️ Files deleted
- 💭 Decisions made
- ⚠️ Issues encountered
- 🎯 Next steps

### 3. End of Session

Review and finalize your session notes:
- Summarize what was accomplished
- Note any important context
- List what's needed next

### 4. When Ready to Commit

Move your finalized summary to `summary/`:
```bash
mv temp/2026-01-10-session.md summary/2026-01-10-implementation-start.md
git add summary/2026-01-10-implementation-start.md
git commit -m "Add implementation session summary"
```

## 📋 File Naming

Use descriptive, dated names:

**Good**:
- `2026-01-10-multi-agent-implementation.md`
- `2026-01-11-bug-fixes.md`
- `2026-01-12-rag-system-progress.md`

**Bad**:
- `session.md` (not specific)
- `work.md` (not dated)
- `temp123.md` (unclear purpose)

## 🗂️ Organize by Type

### Option 1: Flat Structure (Simple)
```
temp/
├── 2026-01-10-session.md
├── 2026-01-11-session.md
└── 2026-01-12-session.md
```

### Option 2: Organized by Feature (Complex)
```
temp/
├── multi-agent/
│   ├── 2026-01-10-implementation.md
│   └── 2026-01-12-testing.md
├── rag-system/
│   └── 2026-01-11-pdf-parser.md
└── bug-fixes/
    └── 2026-01-13-memory-leak.md
```

## ✅ What to Track

### Always Include
- **Date**: When work was done
- **Summary**: Brief overview
- **Files Changed**: What was modified
- **Next Steps**: What's pending

### Optionally Include
- Decisions made
- Issues encountered
- Lessons learned
- Code snippets
- References to specs

## ⏰ When to Update

### Real-time (Recommended)
Update as you work:
- Created a file? Add to session log
- Fixed a bug? Note it immediately
- Made a decision? Document why

### End of Session (Minimum)
At least update:
- What files changed
- What was accomplished
- What's next

## 🔄 Workflow

```
┌─────────────┐
│ Start Work  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Create      │
│ Session Log │
│ in temp/    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Work &      │
│ Update Log  │
│ as You Go   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ End Session │
│ Finalize    │
│ Summary     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Move to     │
│ summary/    │
│ When Ready  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Commit to   │
│ Git         │
└─────────────┘
```

## 💡 Pro Tips

1. **Use the Template**: `TEMPLATE_session.md` has all sections
2. **Link to Specs**: Reference spec sections for context
3. **Be Specific**: Detail what changed, not just that it changed
4. **Include Why**: Decisions and reasoning are important
5. **Clean Up Weekly**: Archive or delete old session logs
6. **Move When Done**: Transfer to `summary/` before committing

## ❌ Common Mistakes

### Don't
- ❌ Commit temp/ files to git (they're gitignored)
- ❌ Store permanent documentation here
- ❌ Use for final specifications
- ❌ Keep everything forever (clean up regularly)

### Do
- ✅ Use for work-in-progress tracking
- ✅ Update as you work
- ✅ Move completed summaries to `summary/`
- ✅ Clean up old files weekly

## 📊 Example Timeline

**Monday Morning**:
```bash
touch temp/2026-01-15-week-start.md
# Track: Starting multi-agent implementation
```

**Monday Throughout Day**:
```markdown
# Update temp/2026-01-15-week-start.md
- Created: src/agent_registry.py
- Modified: config.yaml
- Fixed: Bug in model loader
```

**Monday End of Day**:
```markdown
# Finalize summary
- Implemented agent registry (80% complete)
- Next: Add unit tests
```

**Tuesday** (if continuing):
```bash
# Create new session or continue in same file
```

**Week End** (if complete):
```bash
# Move to permanent summary
mv temp/2026-01-15-week-start.md summary/2026-W03-multi-agent-start.md
git add summary/2026-W03-multi-agent-start.md
git commit -m "Add multi-agent implementation summary"
```

## 🔗 Related

- **Template**: `temp/TEMPLATE_session.md`
- **Guidelines**: `temp/README.md`
- **Example**: `temp/2026-01-10-project-reorganization.md`
- **Summaries**: `summary/` (for completed work)

---

**Remember**: temp/ is your **working notebook**. Use it freely, update it often, and move completed work to `summary/` before committing! 📝
