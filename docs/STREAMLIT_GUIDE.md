# 🎨 Streamlit Dashboard Guide
## Interactive Web Interface for Personalized Tutor Agent

---

## 📌 What is Streamlit?

Streamlit is a Python framework that quickly turns data scripts into shareable web apps. No HTML, CSS, or JavaScript needed!

**For this project**, Streamlit provides:
- ✅ Interactive web dashboard
- ✅ Real-time data visualization
- ✅ Quiz interface
- ✅ Analytics and metrics
- ✅ System information display

---

## 🚀 Quick Start

### Install Streamlit
```bash
pip install streamlit==1.28.0
```

### Verify Installation
```bash
streamlit --version
# Should show: Streamlit, version 1.28.0
```

### Run the App
```bash
cd PersonalizedTutorAgent
streamlit run app.py
```

### Access Dashboard
- **Automatic**: Browser opens at `http://localhost:8501`
- **Manual**: Go to `http://localhost:8501` in your browser

---

## 📊 Dashboard Tabs Explained

### 1. 📊 Dashboard Tab
**Purpose**: Overview of the entire system

**What you'll see:**
- System status and initialization logs
- Key metrics:
  - Number of students in dataset
  - Total learning interactions
  - Number of concepts covered
  - Questions in database
  - DKT model accuracy (%)
  - Average student mastery level
- System initialization checklist

**How to use:**
- Verify all components are initialized
- Check DKT accuracy
- Monitor overall system health

---

### 2. 📝 Interactive Quiz Tab
**Purpose**: Take adaptive quizzes with difficulty adjustment

**Features:**
- Select student ID
- Display quiz questions
- Show answer options
- Difficulty adapts based on performance
- Score tracking

**How to use:**
1. Select a student (1-5)
2. Read the question
3. Select your answer
4. Submit and see result
5. Move to next question
6. Watch difficulty adjust based on your score

**Example:**
- Easy question (Difficulty 1): Basic algebra
- Medium question (Difficulty 2): Expanding expressions
- Hard question (Difficulty 3): Complex factoring

---

### 3. 🛤️ Learning Path Tab
**Purpose**: View personalized learning sequences

**What it shows:**
- Customized learning path for each student
- Prerequisite concepts
- Recommended study sequence
- Concept dependencies

**How to use:**
1. Select a student ID
2. View their learning path
3. See which concepts they should study next
4. Understand why certain order is recommended

**Example Flow:**
- Student 1 → Algebra basics → Geometry → Calculus

---

### 4. 📈 Analytics Tab
**Purpose**: Deep dive into performance metrics

**Visualizations:**
- Student performance trends
- Concept mastery heatmap
- Learning curves
- Time spent analysis
- Accuracy by concept
- Interactive charts

**How to use:**
1. View various performance metrics
2. Identify weak areas
3. Track improvement over time
4. Compare students

---

### 5. ℹ️ System Info Tab
**Purpose**: Technical information

**Information displayed:**
- Project description
- Key features
- Module documentation
- System architecture
- Dependencies

---

## 🎮 Sidebar Navigation

### Left Sidebar
- **Tutor Agent** title
- **Radio buttons** to switch between tabs
- Always visible during app usage

### Right Sidebar Options
- **Refresh** button (circular arrow, top right)
  - Reloads all data and visualizations
- **Menu** button (≡, top right)
  - App settings
  - View code
  - Keyboard shortcuts
  - About Streamlit

---

## ⚙️ Running Streamlit

### Basic Command
```bash
streamlit run app.py
```

### Custom Port (if 8501 is busy)
```bash
streamlit run app.py --server.port 8502
# Access at: http://localhost:8502
```

### Custom Host (for network access)
```bash
streamlit run app.py --server.address 0.0.0.0
```

### Disable Analytics (if desired)
```bash
streamlit run app.py --logger.level=error
```

---

## 🔧 Troubleshooting

### Issue: "Streamlit not found"
```bash
# Solution: Install streamlit
pip install streamlit==1.28.0

# Verify installation
streamlit --version
```

### Issue: Browser doesn't open automatically
1. Check terminal output for URL
2. Copy URL (format: `http://localhost:8501`)
3. Paste into browser address bar
4. Press Enter

### Issue: Port 8501 already in use
```bash
# Check what's using port 8501 (Windows)
netstat -ano | findstr :8501

# Use different port
streamlit run app.py --server.port 8502
```

### Issue: Dashboard shows "No data available"
**Solution:**
1. Stop Streamlit: `Ctrl + C`
2. Run pipeline: `python run_pipeline.py`
3. Restart Streamlit: `streamlit run app.py`

### Issue: Module not found errors
```bash
# Make sure virtual environment is active
# Windows:
.\venv\Scripts\Activate.ps1

# Mac/Linux:
source venv/bin/activate

# Then reinstall dependencies
pip install -r requirements.txt
```

### Issue: Dashboard is slow/freezing
**Solutions:**
- Close other browser tabs
- Close other applications
- Restart Streamlit
- Check internet connection
- Clear browser cache: `Ctrl + Shift + Delete`

### Issue: "Cannot connect to localhost:8501"
```bash
# Check if Streamlit is still running
# Should see something like:
#   "Collecting usage statistics..."
#   "You can now view your Streamlit app..."

# If not running, start it:
streamlit run app.py

# Wait 5-10 seconds for it to fully initialize
```

---

## 🎨 Dashboard Features

### Data Refresh
- Click the circular **refresh button** (top right)
- Re-reads data from CSV files
- Updates all visualizations

### Interactive Charts
- Hover over charts to see values
- Click legend items to toggle series
- Zoom and pan with mouse
- Download chart as PNG

### Student Selection
- Most tabs have dropdown to select student
- Filters data for specific student
- Updates all visualizations for that student

### Quiz Features
- Auto-saves quiz responses
- Calculates difficulty dynamically
- Shows immediate feedback
- Tracks score

---

## 💡 Tips & Tricks

### Keyboard Shortcuts
- **R**: Refresh app
- **C**: Clear cache
- **Ctrl+K**: Command palette (settings)

### For Better Performance
1. Keep only 1 browser tab open
2. Use Chrome, Firefox, or Edge (not IE)
3. Close unnecessary background apps
4. Ensure stable internet connection

### For Development
- Edit `app.py` and save
- Dashboard auto-reloads (with notification)
- No need to restart Streamlit

### Debugging
- Open browser console: `F12`
- Check terminal output for errors
- Look for red error boxes in dashboard

---

## 📱 Responsive Design

The dashboard works on:
- **Desktop** (1920x1080 and up) - Full view
- **Laptop** (1366x768) - Adjusted layout
- **Tablet** (iPad, 768x1024) - Responsive grid
- **Mobile** (Smartphone) - Vertical stacking

Sidebar collapses on smaller screens for more space.

---

## 🌐 Network Access

### Local Only (Default)
```bash
streamlit run app.py
# Access only from: http://localhost:8501
```

### From Other Computers
```bash
streamlit run app.py --server.address 0.0.0.0
# Access from: http://<your-computer-ip>:8501
# Example: http://192.168.1.100:8501
```

⚠️ **Note**: Not recommended for production. For security, only use on trusted networks.

---

## 🔒 Security Notes

### For Development/Testing:
- Streamlit is single-user by default
- No authentication required
- Fine for local use

### For Production:
- Add user authentication
- Use reverse proxy (nginx)
- Enable HTTPS
- Implement access controls
- See Streamlit deployment guides

---

## 📈 Performance Metrics

### Typical Dashboard Performance
- **Load time**: 3-5 seconds
- **Quiz submission**: <1 second
- **Chart rendering**: <2 seconds
- **Tab switching**: <1 second

### System Requirements
- **RAM**: 512 MB minimum (1 GB recommended)
- **CPU**: Dual-core
- **Internet**: Not required after initialization

---

## 🔄 Restarting Streamlit

### Normal Restart
```bash
# In terminal:
Ctrl + C

# Answer: y (or just press Enter)

# Then restart:
streamlit run app.py
```

### Hard Restart (Clear cache)
```bash
Ctrl + C
# Clear browser cache: Ctrl + Shift + Delete
streamlit run app.py
```

### Full Reset
```bash
# Stop Streamlit
Ctrl + C

# Regenerate data
python run_pipeline.py

# Restart app
streamlit run app.py
```

---

## 📚 Next Steps

1. **Explore Dashboard**: Try all 5 tabs
2. **Take Quiz**: Test adaptive difficulty
3. **View Analytics**: Check performance metrics
4. **Read Code**: Look at `app.py` source
5. **Modify**: Customize dashboard for your needs

---

## 🆘 Getting Help

### If Something Goes Wrong:
1. Check [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md#troubleshooting)
2. Verify all dependencies installed: `pip list`
3. Ensure virtual environment active: `(venv)` in prompt
4. Check port availability
5. Restart computer if issues persist

### Common Commands
| Task | Command |
|------|---------|
| Start dashboard | `streamlit run app.py` |
| Use different port | `streamlit run app.py --server.port 8502` |
| Show version | `streamlit --version` |
| Install | `pip install streamlit==1.28.0` |
| Upgrade | `pip install --upgrade streamlit` |

---

## 📞 Support Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [GitHub Issues](https://github.com/streamlit/streamlit/issues)
- [Streamlit Community](https://discuss.streamlit.io/)

---

**Happy Exploring!** 🎓
