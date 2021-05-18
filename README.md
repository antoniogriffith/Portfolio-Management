# Portfolio-Management
Robo-Advisor utilizing user preferences, risk tolerance, and varying investment approaches to produce portfolio management recommendations and advice for the user. [GitHub Repo](https://github.com/antoniogriffith/Portfolio-Management).

## Setup

Create and activate a new virtual environment:

```sh
conda create -n stockmanager-env python=3.8
conda activate stockmanager-env
```

Copy the default stock information (then customize the resulting "default_stocks.csv" file with your own portfolio stocks as desired):

```sh
cp data/default_stock.csv
```

## Installation

Install package dependencies:

```sh
pip install -r requirements.txt
```

```

Running the abbreviated portfolio management application:

```sh
python -m app.manager
```

## Testing

Running all tests:

```sh
pytest
```