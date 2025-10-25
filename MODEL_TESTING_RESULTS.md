# Model Testing Results

## Summary

All regional models have been trained and tested. Here are the results:

## ✅ Successful Models

### 1. **Northeast** - Best Overall Performance
- **Test R²**: 0.116
- **Test RMSE**: 5.82
- **Test MAE**: 3.15
- **Training Samples**: 217,032
- **Test Samples**: 54,259
- **Top Features**:
  - Wind Direction: 0.098
  - Visibility: 0.083
  - Ceiling: 0.079
  - Ceiling/Visibility Ratio: 0.077
  - Sea Level Pressure: 0.070

### 2. **PacificCoast**
- **Test R²**: 0.053
- **Test RMSE**: 5.66
- **Test MAE**: 2.99
- **Training Samples**: 322,096
- **Test Samples**: 80,525
- **Top Features**:
  - Dewpoint: 0.093
  - Relative Humidity: 0.089
  - Ceiling: 0.088
  - Sea Level Pressure: 0.086
  - Visibility: 0.082

### 3. **RockyMountains**
- **Test R²**: 0.103
- **Test RMSE**: 6.34
- **Test MAE**: 3.69
- **Training Samples**: 297,089
- **Test Samples**: 74,273
- **Top Features**:
  - Relative Humidity: 0.321
  - Humidity: 0.176
  - Ceiling: 0.059
  - Wind Direction: 0.051
  - Is Night: 0.045

### 4. **Southeast** - Best R² Score
- **Test R²**: 0.298 ⭐ (Best)
- **Test RMSE**: 7.94
- **Test MAE**: 4.20
- **Training Samples**: 334,068
- **Test Samples**: 83,518
- **Top Features**:
  - Visibility: 0.368 (Most Important!)
  - Wind Direction: 0.094
  - Temperature: 0.067
  - Humidity: 0.066
  - Sea Level Pressure: 0.055

## ❌ Failed Model

### **CentralPlains**
- **Status**: Failed
- **Reason**: No combined records (0 samples)
- **Issue**: Airport codes MCI, OMA, DSM, STL, TUL, ICT may not match weather data

## Key Insights

1. **Southeast has the best R²** (0.298) - Weather explains nearly 30% of delays
2. **Visibility is critical** for Southeast (importance: 0.368)
3. **Humidity is key** for RockyMountains (combined importance: 0.497)
4. **Wind features matter** for Northeast
5. **CentralPlains needs investigation** - Airport codes may need updating

## Model Files Created

All successful models are saved in `models/zones/`:
- `Northeast_model.pkl`
- `PacificCoast_model.pkl`
- `RockyMountains_model.pkl`
- `Southeast_model.pkl`
- Plus corresponding `.pkl` scalers and `.txt` feature lists

## Recommendations

1. **Fix CentralPlains**: Check airport codes and weather data mapping
2. **Use Southeast model** for best predictions (R² = 0.298)
3. **Consider visibility** as the most critical weather factor
4. **Regional models are distinct** - each zone has different important features

## Next Steps

1. Investigate CentralPlains data mismatch
2. Test models with `interactive_test.py`
3. Use individual training scripts for fine-tuning
4. Consider retraining with different hyperparameters
