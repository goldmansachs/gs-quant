# GS Quant

**GS Quant** is a Python toolkit for quantitative finance, created on top of one of the world’s most powerful risk transfer platforms. Designed to accelerate development of quantitative trading strategies and risk management solutions, crafted over 25 years of experience navigating global markets.

It is created and maintained by quantitative developers (quants) at Goldman Sachs to enable the development of trading strategies and analysis of derivative products. GS Quant can be used to facilitate derivative structuring, trading, and risk management, or as a set of statistical packages for data analytics applications.

In order to access the APIs you will need a client id and secret.  These are available to institutional clients of Goldman Sachs.  Please speak to your sales coverage or Marquee Sales for further information. 

Please refer to [Goldman Sachs Developer](https://developer.gs.com/docs/gsquant/) for additional information.

## Requirements

* Python 3.8 or greater
* Access to PIP package manager
* Client ID and secret for API access (for institutional clients)

## Installation

```
pip install gs-quant
```

## Development Setup
* 1. Clone the Repository
```
git clone https://github.com/your-organization/gs-quant.git
cd gs-quant
```

* 2. Create a Virtual Environment
```
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```

* 3. Install Dependencies
```
pip install -r requirements.txt
```

* 4. Install GS Quant Locally
```
pip install -e .
```

## Building the Project
If the project requires a build step, describe it here. For example:

```
# Example build command
python setup.py build
```

## Running Tests
To run tests, use the following command:
```
pytest
```
Make sure to run tests before submitting any changes.


## Contributing
Contributions are welcome! Please follow these guidelines:
1.) Fork the Repository: Use the GitHub interface to fork the repository to your own account.
2.) Create a Branch: Create a feature branch for your changes
```
git checkout -b feature/your-feature-name
```

3.) Commit Your Changes: Write descriptive commit messages.
```
git commit -m "Add feature X"
```

4.) Push to Your Fork: Push your changes to your forked repository.
```
git push origin feature/your-feature-name
```

5.) Submit a Pull Request: Go to the original repository on GitHub and submit a pull request.

Please see [CONTRIBUTING](CONTRIBUTING.md) for more details.
 
## Examples

You can find examples, guides and tutorials in the respective folders on [Goldman Sachs Developer](https://developer.gs.com/docs/gsquant/).



## Help

Please reach out to `gs-quant@gs.com` with any questions, comments or feedback.
