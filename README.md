# Disposable Email Address Scraper

Collecting, categorizing and analyzing Emails from top Free Disposable Email Address Services.

## Getting Started

### Prerequisites

Download and install dependencies

Python3 packages:
```
selenium
pydot
pandas
matplotlib
scikit-learn
scipy
matplotlib
beautifulsoup4
json
numpy
```
External dependencies:
```
ChromeWebdriver
```

### How to test
To run the thing, these are the exact steps
1) Open emailscraper.py, set fileName, run `$ python3 emailscraper.py`
2) After grabbing the data from multiple runs, we need to combine the data so modify `combine.py` according to your needs.
3) Run `$ python3 simpleClassifier.py` for classification based on profanity.
4) Run `$ python3 mlclassifier.py` for classification based on unsupervised learning and draw clusters.


## Authors

* [**Shubham Jindal**](https://github.com/sjindal94)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* [Anthony De Meulemeester](https://github.com/anthdm)
Core developer @CityOfZion. Lead engineer and architect @AcademicLabs.

