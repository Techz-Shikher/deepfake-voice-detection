# 👤 User Manual

Complete step-by-step guide for using the Deepfake Voice Detection System

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Analyzing Audio Files](#analyzing-audio-files)
3. [Understanding Results](#understanding-results)
4. [Verifying Predictions](#verifying-predictions)
5. [Tracking Progress](#tracking-progress)
6. [Tips and Best Practices](#tips-and-best-practices)
7. [FAQ](#faq)
8. [Troubleshooting](#troubleshooting)

---

## Getting Started

### System Requirements

Before you start, make sure you have:
- **Computer:** Windows 10+, macOS 10.13+, or Linux
- **Memory:** At least 4GB RAM (8GB recommended)
- **Disk Space:** 1GB free space
- **Browser:** Chrome, Firefox, Safari, or Edge (recent version)
- **Audio Files:** WAV, MP3, FLAC, or OGG format

### Installation (First Time Only)

#### Step 1: Download and Prepare
1. Ensure Python 3.13+ is installed on your computer
2. Download or clone the deepfake detection system
3. Navigate to the project folder in terminal/command prompt

#### Step 2: Install Dependencies
```bash
# Run the setup script
# Windows:
setup.bat

# Mac/Linux:
bash setup.sh
```

Or manually:
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

#### Step 3: Start the Server
```bash
python api.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

#### Step 4: Open Web Interface
Open your web browser and go to:
```
http://localhost:5000
```

You should see the web interface with a file upload area.

---

## Analyzing Audio Files

### Single File Analysis

#### Method 1: Click to Upload
1. **Click** "Choose File" button
2. **Select** an audio file from your computer
3. **Wait** for analysis (usually 1-2 seconds)
4. **Review** the results

#### Method 2: Drag & Drop
1. **Locate** an audio file on your computer
2. **Drag** the file from Windows Explorer/Finder
3. **Drop** it on the upload area (it will turn blue)
4. **Wait** for analysis
5. **Review** the results

### Supported Audio Formats

✅ **WAV** (.wav) - Recommended for best quality
✅ **MP3** (.mp3) - Common format
✅ **FLAC** (.flac) - Lossless compression
✅ **OGG** (.ogg) - Open format

**Best Results:**
- Clear, clean audio
- Minimal background noise
- Duration: 1-30 seconds
- Sample rate: 16kHz or higher

### File Size Limits

| Size | Status | Notes |
|------|--------|-------|
| < 10 MB | ✅ Recommended | Fast processing |
| 10-50 MB | ✅ Acceptable | Takes longer |
| > 50 MB | ⚠️ May fail | Try splitting file |

---

## Understanding Results

### Result Display

After analysis, you'll see:

```
┌─────────────────────────────────┐
│  FILE: voice.wav                │
├─────────────────────────────────┤
│  Classification: REAL VOICE     │
│  Confidence: 95%                │
├─────────────────────────────────┤
│  Prediction Breakdown:          │
│  Real Voice:    95%  ████████   │
│  Deepfake:       5%  █          │
├─────────────────────────────────┤
│  [✅ Correct] [❌ Incorrect]    │
└─────────────────────────────────┘
```

### What Each Result Means

#### Classification
- **REAL VOICE** 🎤 - System believes this is genuine human speech
- **DEEPFAKE** 🤖 - System believes this is AI-generated or synthetic voice

#### Confidence Score
- **90-100%** ✅ Very confident prediction
- **75-90%** ⚠️ Reasonably confident
- **60-75%** ❓ Less certain, verify carefully
- **< 60%** ❗ Low confidence, likely needs expert review

#### Score Breakdown
Shows the probability for each classification:
- Higher bar = more likely
- Longer bar under "Real Voice" = more likely real
- Longer bar under "Deepfake" = more likely fake

---

## Verifying Predictions

### Why Verify Predictions?

1. **Build Better Training Data** - Helps improve the model
2. **Track Accuracy** - See how well the system performs
3. **Catch Mistakes** - Improve results over time
4. **Contribute** - Help make the system smarter

### Verification Workflow

#### Step 1: Review the Analysis
1. Listen to the audio (if possible)
2. Check the prediction
3. Decide: Is it correct or wrong?

#### Step 2: Mark Your Verdict

**If the prediction is CORRECT:**
1. Click the **✅ Correct** button
2. Your feedback is saved immediately
3. Statistics are updated automatically
4. Done!

**If the prediction is WRONG:**
1. Click the **❌ Incorrect** button
2. A form appears asking for the actual label
3. Select the correct classification:
   - 🎤 **Real Voice** - It's actually human speech
   - 🤖 **Deepfake** - It's actually AI-generated/synthetic
4. (Optional) Add a comment explaining why it's wrong
5. Click **Submit Feedback**
6. Your correction is saved

### Adding Comments

When marking incorrect predictions, you can add optional comments:

**Good comment examples:**
- "This is clearly a voice cloner"
- "The pitch is too perfect, sounds artificial"
- "Background noise is wrong"
- "Breathing pattern is too regular"
- "EQ/processing artifacts visible"

**Why add comments?**
- Helps understand what the model missed
- Provides context for improvements
- Useful for training dataset curation
- Identifies edge cases

---

## Tracking Progress

### Check Statistics

After verifying predictions, check your progress:

1. **Look for the Statistics Section** below the verification form
2. You'll see four statistics:

| Statistic | Meaning | Example |
|-----------|---------|---------|
| **Total Verified** | How many predictions you've reviewed | 25 |
| **Correct** | Predictions that were right | 23 |
| **Incorrect** | Predictions that were wrong | 2 |
| **Accuracy %** | How often the system got it right | 92% |

### Interpreting Your Statistics

```
If you see:
✅ 25 total verified
✅ Accuracy: 92%

This means:
→ You've verified 25 predictions
→ 23 were correct (92%)
→ 2 were wrong (8%)
→ System is very reliable!
```

### Improving Over Time

As you verify more predictions:
- **< 10 verified:** Building baseline accuracy
- **10-50 verified:** Getting good data coverage
- **50-100 verified:** Strong pattern emerging
- **> 100 verified:** Comprehensive testing done

---

## Tips and Best Practices

### For Best Results

#### 1. **Listen Carefully**
- Please actually listen to or review each audio file
- Don't just guess based on appearance
- Use headphones for critical analysis
- Take breaks if doing many files

#### 2. **Be Honest**
- Mark mistakes even if they're unusual cases
- Provide accurate corrections
- Help build a representative dataset

#### 3. **Describe Why**
- Add comments for completely wrong predictions
- Explain what clues indicate it's fake or real
- Help others understand the decision

#### 4. **Quality Over Quantity**
- 50 carefully-verified samples > 500 quick guesses
- Focus on difficult cases
- Mark edge cases as such

### Audio Quality Tips

**Best for Analysis:**
- Clear, medium volume
- Minimal background noise
- 3-10 seconds of continuous speech
- 16kHz+ sample rate

**Worst Case Scenarios:**
- Heavy background noise
- Very quiet audio
- Very long files (> 5 minutes)
- Compressed/low quality files

### When to Trust the System

✅ **Trust it when:**
- Confidence is 85%+
- The prediction matches your impression
- The audio is clearly one type or the other

⚠️ **Be skeptical when:**
- Confidence is 55-75%
- You're unsure what you're hearing
- Audio quality is poor
- The result doesn't match expectations

---

## FAQ

### Q: How accurate is the system?
**A:** The system was trained on synthetic data and achieves ~100% accuracy on training data. Real-world accuracy depends on:
- Audio quality
- Sample diversity
- System familiarity with that type of deepfake

By providing feedback, you help it improve!

### Q: What if I disagree with the system?
**A:** That's very valuable! Mark it as incorrect and provide feedback. Your corrections help improve the system.

### Q: How long does analysis take?
**A:** Usually 1-2 seconds per file, depending on:
- File size
- Your computer speed
- System load
- Audio sample rate

### Q: Can I analyze very long audio files?
**A:** Yes, but:
- Files > 5 min take longer
- Files > 50 MB may fail
- Best results: 3-30 seconds

Try splitting very long files into segments.

### Q: Does the system work offline?
**A:** Yes! All processing happens on your computer. No internet required.

### Q: Where is my data stored?
**A:** 
- Feedback: `data/feedback.json`
- Statistics: `data/feedback_stats.json`
- All files stay on your computer

### Q: Can I delete my feedback?
**A:** Currently, no. You can manually edit the JSON files in `data/` folder if needed.

### Q: What formats are supported?
**A:** WAV, MP3, FLAC, and OGG. Other formats will fail.

### Q: Can I use this commercially?
**A:** Check the LICENSE file for usage terms.

### Q: How do I stop the server?
**A:** In the terminal/command prompt, press `Ctrl+C`

### Q: Can I change the port number?
**A:** Yes, edit `api.py` and change the port number in the last line.

---

## Troubleshooting

### Issue: "File upload not working"

**Possible Causes:**
- Browser not compatible
- File format not supported
- File too large
- File corrupted

**Solutions:**
1. Try different browser (Chrome, Firefox)
2. Verify file format (WAV, MP3, FLAC, OGG)
3. Try smaller file (< 10 MB)
4. Try different audio file
5. Clear browser cache and reload

### Issue: "Analysis takes very long"

**Possible Causes:**
- File is large
- Computer is slow
- Server is busy

**Solutions:**
1. Try smaller file
2. Close other applications
3. Restart the server
4. Check computer RAM usage

### Issue: "API connection failed"

**Possible Causes:**
- Server not running
- Wrong port number
- Firewall blocking
- Browser issue

**Solutions:**
1. Check terminal - see "Running on http://..."?
2. Try http://localhost:5000 in browser
3. Check firewall settings
4. Try different port number
5. Restart server: `python api.py`

### Issue: "Unsupported audio format"

**Possible Causes:**
- File format not supported
- File corrupted
- Wrong file extension

**Solutions:**
1. Convert file to WAV or MP3
2. Use program: Audacity (free), FFmpeg
3. Verify file is not corrupted
4. Try a test file first

### Issue: "Feedback not being saved"

**Possible Causes:**
- File permission issues
- Disk full
- JSON file corrupted
- Server error

**Solutions:**
1. Check `/data` directory exists
2. Verify you have write permissions
3. Check free disk space
4. Restart server
5. Check browser console for errors (F12)

### Issue: "Statistics showing 0%"

**Possible Causes:**
- No feedback submitted yet
- File corrupted
- Server issue

**Solutions:**
1. Submit feedback first (mark predictions correct/incorrect)
2. Wait a moment for stats to update
3. Refresh browser (F5)
4. Restart server

### Issue: "System is slow"

**Possible Causes:**
- Computer low on RAM
- Disk is full
- Other programs using CPU

**Solutions:**
1. Close unnecessary programs
2. Check RAM usage
3. Check free disk space (need at least 1GB)
4. Restart computer
5. Use smaller audio files

---

## Performance Optimization

### Speed Up Analysis

1. **Use smaller files**
   - Extract 10-30 second clips
   - Analyze segments instead of full recordings

2. **Close unnecessary programs**
   - Free up RAM
   - Reduce system load

3. **Use better audio**
   - Clear, good quality files process faster
   - Avoid heavily compressed audio

4. **Batch processing**
   - Process multiple files at once
   - System handles them efficiently

### Storage Optimization

1. **Manage feedback files**
   - Regularly review `data/feedback.json`
   - Archive old feedback if needed
   - Keep < 100MB for best performance

2. **Clean up**
   - Remove large unused audio files
   - Keep system folder organized
   - Keep 1GB+ free disk space

---

## Accessibility

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `↑ ↓` | Navigate results |
| `Enter` | Submit form |
| `Esc` | Close dialog |
| `Tab` | Focus next element |
| `Ctrl+A` | Select all text |
| `Ctrl+C` | Copy text |

### Browser Features

- **Text Size:** Chrome menu → Settings → Zoom
- **High Contrast:** OS accessibility settings
- **Screen Reader:** All text properly labeled
- **Keyboard Navigation:** Full support

---

## Next Steps

1. ✅ **Run the system** - Follow installation steps
2. ✅ **Analyze a file** - Test with sample audio
3. ✅ **Verify results** - Mark as correct/incorrect
4. ✅ **Check statistics** - See your progress
5. 🎯 **Continue verifying** - Build up feedback dataset

For detailed information about:
- **Installation:** See [QUICK_START.md](QUICK_START.md)
- **API Usage:** See [API_REFERENCE.md](API_REFERENCE.md)
- **Advanced Topics:** See [ARCHITECTURE.md](ARCHITECTURE.md)
- **Documentation:** See [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)

---

## Need Help?

1. **Check this manual** - Search for your issue
2. **Read QUICK_START.md** - Common problems
3. **Check VERIFICATION_GUIDE.md** - Feedback system questions
4. **Review README.md** - General information

---

**Happy analyzing!** 🎵

Feel free to submit feedback on wrong predictions - every correction helps improve the system! 🚀
