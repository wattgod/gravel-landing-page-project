# TRAININGPEAKS MARKETPLACE UPDATE - ACTION PLAN
# Unbound Gravel 200 - 15 Plans

## WHAT YOU HAVE

✓ **60 tier-specific descriptions** - All variations generated and organized
✓ **15-to-60 mapping** - Clear guide showing which description goes with each plan
✓ **Alternatives documented** - Backup options for future A/B testing
✓ **GitHub instructions** - Ready to push all 60 for version control

---

## TONIGHT: UPDATE TRAININGPEAKS (75 minutes)

### Your 15 Plans → Best-Fit Descriptions

Open these files from `/Users/mattirowe/Downloads/unbound_200/`:

**AYAHUASCA (4 plans):**
1. Ayahuasca Beginner → `ayahuasca/ayahuasca_beginner.txt`
2. Ayahuasca Intermediate → `ayahuasca/ayahuasca_intermediate.txt`
3. Ayahuasca Masters → `ayahuasca/ayahuasca_beginner_masters.txt`
4. Ayahuasca Save My Race → `ayahuasca/ayahuasca_save_my_race.txt`

**FINISHER (5 plans):**
5. Finisher Beginner → `finisher/finisher_beginner.txt`
6. Finisher Intermediate → `finisher/finisher_intermediate.txt`
7. Finisher Advanced → `finisher/finisher_advanced.txt`
8. Finisher Masters → `finisher/finisher_intermediate_masters.txt`
9. Finisher Save My Race → `finisher/finisher_save_my_race.txt`

**COMPETE (4 plans):**
10. Compete Intermediate → `compete/compete_intermediate.txt`
11. Compete Advanced → `compete/compete_advanced.txt`
12. Compete Masters → `compete/compete_intermediate_masters.txt`
13. Compete Save My Race → `compete/compete_save_my_race.txt`

**PODIUM (2 plans):**
14. Podium Advanced → `podium/podium_advanced.txt`
15. Podium Advanced GOAT → `podium/podium_elite.txt`

### Update Process

For each plan (5 min × 15 = 75 min):
1. Log into TrainingPeaks marketplace
2. Find the plan listing
3. Click "Edit" on marketplace description
4. Open the corresponding `.txt` file
5. Copy entire contents
6. Paste into TrainingPeaks description field
7. Save

---

## TOMORROW: PUSH TO GITHUB (10 minutes)

```bash
# Navigate to your repo
cd /path/to/gravel-landing-page-project

# Create directory
mkdir -p marketplace_descriptions/unbound_200

# Copy all files
cp -r ~/Downloads/unbound_200/* marketplace_descriptions/unbound_200/
cp ~/Downloads/TRAININGPEAKS_DESCRIPTION_MAPPING.md marketplace_descriptions/unbound_200/

# Commit and push
git add marketplace_descriptions/
git commit -m "Add tier-specific marketplace descriptions for Unbound 200"
git push origin main
```

---

## WEEK 1: MONITOR PERFORMANCE

Track which descriptions are converting on TrainingPeaks analytics.

**If a plan underperforms:**
- Check the alternatives in `TRAININGPEAKS_DESCRIPTION_MAPPING.md`
- Swap in alternative description
- Give it 2-4 weeks
- Keep the winner

**Example:**
- Finisher Advanced not converting?
- Try `finisher_sub_12_hours.txt` (performance-specific angle)
- Or try `finisher_pr_attempt.txt` (improvement-focused angle)

---

## WEEK 2+: SCALE TO OTHER RACES

Use the same tier-specific system for:
- Belgian Waffle Ride
- Mid South
- SBT GRVL
- Crusher in the Tushar
- etc.

**Time per race:** ~2 hours
- 5 min: Copy generation script
- 3 min: Generate 60 descriptions
- 30 min: Review batch
- 60 min: Upload to TrainingPeaks
- 10 min: Push to GitHub

---

## FILES YOU HAVE

**Main descriptions folder:**
`/Users/mattirowe/Downloads/unbound_200/`
- ayahuasca/ (15 files)
- finisher/ (15 files)
- compete/ (15 files)
- podium/ (15 files)

**Documentation:**
- `TRAININGPEAKS_DESCRIPTION_MAPPING.md` - Your 15-plan mapping
- `GITHUB_PUSH_INSTRUCTIONS.md` - How to push to repo
- `GENERATION_SUMMARY.txt` - What was generated
- `SESSION_COMPLETE_STATUS.md` - Full system overview

**System source code:**
`/Users/mattirowe/Downloads/tier_variation_system/`
- All 6 phase files
- Integration system
- Production generation script

---

## QUALITY CHECK BEFORE UPDATING

**Read these 3 descriptions first:**
1. `ayahuasca/ayahuasca_beginner.txt` - Check the "wink" tone
2. `finisher/finisher_intermediate.txt` - Check the "leveling up" angle
3. `podium/podium_elite.txt` - Check the "elite athlete" voice

**If the tone matches Gravel God brand:** Proceed with all 15 updates.

**If you want adjustments:** Let me know which tier needs tweaking.

---

## SUCCESS METRICS

**Immediate (Week 1):**
- ✓ 15 descriptions updated on TrainingPeaks
- ✓ 60 descriptions backed up to GitHub
- ✓ All files version controlled

**Short-term (Month 1):**
- Conversion data on new descriptions
- A/B test results if swapping alternatives
- At least 1 more race (60 descriptions) generated

**Medium-term (Quarter 1):**
- 5+ races with tier-specific descriptions (300+ descriptions)
- Clear data on which tier-specific angles convert best
- System validated across multiple race types

---

## QUESTIONS TO CONSIDER

**After updating TrainingPeaks:**
1. Do the descriptions feel more targeted per tier?
2. Is the Ayahuasca "wink" too aggressive or just right?
3. Does Podium Elite match your "GOAT" positioning?

**If any feel off:**
- Check the alternatives in mapping document
- Or tell me which tier needs adjustment
- Can regenerate specific variations

---

## YOU'RE READY

All files are in `/Users/mattirowe/Downloads/`

**Step 1:** Update TrainingPeaks (tonight)
**Step 2:** Push to GitHub (tomorrow)
**Step 3:** Monitor performance (week 1)

The copy is better. The variation is there. Time to ship it.
