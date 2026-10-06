# Phishing URL Detection

## Project Title
**Evaluating the Effectiveness of Lightweight Machine Learning Models for Real-Time Phishing URL Detection**

## Project Goal
This project investigates whether lightweight and interpretable machine-learning models can detect phishing URLs with performance comparable to more computationally expensive deep-learning approaches while requiring fewer computational resources.

The lightweight models planned for comparison include:
- Logistic Regression
- Decision Tree
- Random Forest
- Gradient Boosting

A deep-learning baseline such as an LSTM is planned for the later stage of the project.

## Current Progress Through Week 7
Completed or in progress:
- Defined the research question and system architecture
- Built a lexical URL feature-extraction prototype
- Prepared a larger preprocessing workflow
- Added duplicate and invalid-record handling
- Integrated lexical feature extraction with the preprocessing pipeline
- Added reproducible train/validation/test splitting
- Added initial Logistic Regression and Decision Tree baseline training
- Added a common evaluation script for accuracy, precision, recall, F1 score, ROC-AUC, confusion matrices, inference time, and model size

## Week 7 Experimental Results

The preprocessing pipeline was successfully run on the PhiUSIIL phishing URL dataset.
### Dataset Processing Summary

After cleaning and removing duplicate URLs, the dataset contained:

- **235,370 usable URLs**
- **164,759 training samples**
- **35,305 validation samples**
- **35,306 test samples**
- **57.3% legitimate URLs**
- **42.7% phishing URLs**

The project uses the following label convention:

- `0 = legitimate`
- `1 = phishing`

### Validation Results

| Model | Accuracy | Precision | Recall | F1 Score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 99.29% | 99.95% | 98.39% | 99.16% | 99.61% |
| Decision Tree | 99.48% | 99.87% | 98.93% | 99.39% | 99.66% |

### Held-Out Test Results

| Model | Accuracy | Precision | Recall | F1 Score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 99.41% | 99.94% | 98.67% | 99.30% | 99.67% |
| Decision Tree | 99.54% | 99.77% | 99.14% | 99.45% | 99.66% |

### Efficiency Comparison

| Model | Model Size | Approx. Inference Time per URL |
|---|---:|---:|
| Logistic Regression | 1,391 bytes | 0.000000036 sec |
| Decision Tree | 48,073 bytes | 0.000000068 sec |

The Decision Tree achieved slightly higher overall accuracy, recall, and F1 score, while Logistic Regression was substantially smaller and achieved slightly higher precision and ROC-AUC.

This demonstrates the main accuracy-versus-efficiency trade-off being investigated in the project. The Decision Tree provides a small improvement in overall classification performance, while Logistic Regression provides very strong phishing URL detection with a much smaller model footprint.

On the held-out test set, Logistic Regression produced 200 false negatives, while the Decision Tree produced 130 false negatives.

## Repository Structure

```text
phishing-url-detection/
├── src/
│   ├── feature_extraction.py
│   ├── preprocess_data.py
│   ├── train_baselines.py
│   └── evaluate_models.py
├── data/
│   └── demo_urls.csv
├── outputs/
│   └── demo_features.csv
├── requirements.txt
└── README.md
```

## Lexical Features
The current lightweight feature set includes:
- URL length
- Hostname length
- Number of dots
- Number of hyphens
- Number of question marks
- Number of equal signs
- Number of digits
- Number of special characters
- HTTPS usage
- IP-address usage
- Known URL-shortener usage

## Running the Week 7 Pipeline

Install dependencies:

```bash
pip install -r requirements.txt
```

Preprocess a labeled CSV dataset:

```bash
python src/preprocess_data.py \
  --input data/urls.csv \
  --url-column url \
  --label-column label
```

Train the initial baselines:

```bash
python src/train_baselines.py
```

Evaluate the saved models on the held-out test set:

```bash
python src/evaluate_models.py
```

## Important Note
The current Logistic Regression and Decision Tree models are baseline implementations. Final experimental conclusions should only be made after the dataset has been finalized and all selected models have been evaluated consistently on held-out data.

## Next Steps
1. Finalize and verify the cleaned dataset.
2. Complete baseline evaluation.
3. Train Random Forest and Gradient Boosting models.
4. Perform controlled hyperparameter tuning.
5. Implement the LSTM deep-learning baseline.
6. Compare predictive performance and efficiency.
7. Run the resource-constrained experiment.
8. Prepare final tables, graphs, and conclusions.
