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
