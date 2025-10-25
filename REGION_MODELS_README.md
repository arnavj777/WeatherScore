# Regional Model Training Files

Each region now has its own dedicated training script for easier management and customization.

## Files Created

1. **`Src/train_Northeast_model.py`** - Training for Northeast airports
2. **`Src/train_PacificCoast_model.py`** - Training for PacificCoast airports
3. **`Src/train_RockyMountains_model.py`** - Training for RockyMountains airports
4. **`Src/train_CentralPlains_model.py`** - Training for CentralPlains airports
5. **`Src/train_Southeast_model.py`** - Training for Southeast airports

## Benefits

### ✅ **Individual Control**
- Train each region independently
- Modify hyperparameters per region
- Test different configurations easily

### ✅ **Easy Customization**
- Each file lists its airports at the top
- Simple to add/remove airports from each zone
- Modify feature engineering per region if needed

### ✅ **Parallel Training**
- Train all models simultaneously (if you have resources)
- Fix issues in one region without affecting others
- Retrain only the region you modified

## Usage

### Train a Single Region

```bash
# Train just Northeast
python Src/train_Northeast_model.py

# Train just PacificCoast
python Src/train_PacificCoast_model.py

# Train just RockyMountains
python Src/train_RockyMountains_model.py

# Train just CentralPlains
python Src/train_CentralPlains_model.py

# Train just Southeast
python Src/train_Southeast_model.py
```

### Train All Regions (Sequential)

You can still use the original `train_all_zone_models_improved.py` to train all regions at once:

```bash
python Src/train_all_zone_models_improved.py
```

## Customization

### Adding Airports to a Region

Edit the corresponding file and update the airports list:

**Example - Adding LAX to PacificCoast:**

```python
# In train_PacificCoast_model.py
PACIFICCOAST_AIRPORTS = ['LAX', 'SFO', 'SEA', 'PDX', 'SAN', 'OAK', 'SJC', 'SMF', 'BUR']  # Added BUR
```

### Modifying Hyperparameters

Edit the `train_model()` function in any file:

**Example - Changing learning rate for Northeast:**

```python
# In train_Northeast_model.py
model = xgb.XGBRegressor(
    n_estimators=300,
    max_depth=8,
    learning_rate=0.03,  # Changed from 0.05
    # ... rest of parameters
)
```

## Region-Specific Airports

Each file defines its airports from the Excel file:

### Northeast (12 airports)
- JFK, LGA, EWR, BOS, BWI, PHL, IAD, BDL, BUF, ALB, PVD, PWM

### PacificCoast (8 airports)
- LAX, SFO, SEA, PDX, SAN, OAK, SJC, SMF

### RockyMountains (8 airports)
- DEN, SLC, BOI, BIL, BZN, JAC, COS, MSO

### CentralPlains (6 airports)
- MCI, OMA, DSM, STL, TUL, ICT

### Southeast (2 airports)
- ATL, MIA

## Output Files

Each script saves to:
- `models/zones/{ZoneName}_model.pkl`
- `models/zones/{ZoneName}_scaler.pkl`
- `models/zones/{ZoneName}_features.txt`

## Comparison

| Feature | Individual Files | Combined File |
|---------|-----------------|---------------|
| Train one region | ✅ Easy | ❌ Must run all |
| Customize per zone | ✅ Easy | ⚠️ Harder |
| Parallel training | ✅ Yes | ❌ No |
| Quick fixes | ✅ Yes | ⚠️ Slower |
| All at once | ❌ Run 5 times | ✅ Yes |

## Recommendations

- **Use individual files** for development, testing, and customization
- **Use combined file** for production training of all models
- **Add airports** by editing the corresponding individual file
- **Experiment** with hyperparameters in individual files first
