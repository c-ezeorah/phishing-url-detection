# Evidence of Progress — What to Show in the Video

Use this repository as the visual evidence portion of the 2–5 minute presentation.

## 1. Show the README
Point to:
- the research goal,
- the list of planned models,
- the evaluation metrics,
- and the Mermaid system-design diagram.

Suggested narration:
> "This is the project structure I created for the implementation phase. The diagram shows the planned pipeline from URL data, through preprocessing and feature extraction, into the lightweight models and LSTM baseline, followed by a common evaluation module."

## 2. Show `src/feature_extraction.py`
Scroll through the function `extract_lexical_features()`.

Point out that the current prototype extracts:
- URL length,
- hostname length,
- number of dots,
- hyphens,
- @ symbols,
- question marks,
- equal signs,
- digits,
- special characters,
- HTTPS usage,
- IP-address usage,
- and known URL-shortener usage.

Suggested narration:
> "I also implemented the first part of the preprocessing pipeline: a lexical feature extractor. These features are lightweight because they can be computed directly from the URL without loading the website."

## 3. Show `data/demo_urls.csv`
Explain that this is only a small synthetic/example dataset used to test the feature-extraction code.

Do **not** call this the real PhishTank/UCI dataset.

## 4. Show `outputs/demo_features.csv`
This is reproducible evidence that the feature extractor runs and produces structured numeric features.

Suggested narration:
> "This output confirms that the prototype is converting raw URLs into numeric features that can later be passed into the machine-learning models."

## 5. Be precise about what is not done yet
Say:
> "These are not model-training results yet. Dataset collection, model training, hyperparameter tuning, and benchmarking are the next steps."

That keeps the progress report accurate while still showing concrete technical work.
