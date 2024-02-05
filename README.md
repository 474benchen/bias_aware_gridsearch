# bias_aware_gridsearchCV: Enhanced GridSearchCV for Bias and Accuracy Optimization

## Introduction
This repository introduces a novel variation of the `GridSearchCV` algorithm from `scikit-learn`, uniquely designed to optimize machine learning models not only for accuracy but also for fairness metrics. This project addresses the critical need for unbiased models in machine learning, especially in sensitive domains like healthcare, recidivism prediction, mortgage lending, and income-based financial decisions.

## Features
- **Enhanced GridSearch Algorithm**: Extends `sklearn`'s `GridSearchCV` to evaluate and optimize both accuracy and bias metrics simultaneously.
- **Bias Metrics Integration**: Incorporates key bias metrics like demographic parity, equalized odds, and others, ensuring models are fair and equitable.
- **Domain-Specific Applications**: Provides practical implementations in four critical domains:
  - Healthcare: Improving diagnostic fairness.
  - Recidivism: Ensuring unbiased risk assessments.
  - Mortgage: Facilitating fair lending practices.
  - Finance: Promoting equity in income-related decisions.

## Getting Started


To replicate our environment, you can choose from the following options. Regardless of which option,
in order to explore our work:

1. Clone the repository:

    ```
    git clone https://github.com/474benchen/biased_gridsearch.git
    ```

2. Navigate to the project directory:

    ```
    cd biased_gridsearch
    ```
### Option 1: Using requirements.txt

Ensure that you have pip installed before attempting this option. Instructions can be found [here](https://pip.pypa.io/en/stable/installation/).

1. Install the required packages using pip:

    ```
    pip install -r requirements.txt
    ```

2. Proceed to the next steps for data setup.

### Option 2: Reconstructing the Conda Environment

Ensure that you have conda installed before attempting this option. Distributions can be found [here](https://www.anaconda.com/download).

1. Create a conda environment from the provided environment.yml file:

    ```
    conda env create -f environment.yml
    ```

2. Activate the conda environment:

    ```
    conda activate biased_gs
    ```

3. Proceed to the next steps for data setup.

## Data Setup

For each example, data has been provided in the same directory.


## Examples
This section provides examples of how to apply the Enhanced GridSearchCV in each of the four domains. Please refer to the respective folders for detailed notebooks:

- `/healthcare_example`
- `/recidivism_example`
- `/mortgage_example`
- `/finance_example`

## Authors
- [Anika Garg](https://www.linkedin.com/in/anika-garg/)
- [Benjamin Chen](https://www.linkedin.com/in/474benjaminchen/)
- [Jayson Leach](https://www.linkedin.com/in/jayson-leach/)
- [Stephanie Chavez](https://www.linkedin.com/in/stephanie-chavez-000840223/)
