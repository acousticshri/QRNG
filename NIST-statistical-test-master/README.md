[![](https://www.ginar.io/wp-content/themes/ginar/assets/img/logo1.svg)](https://ginar.io)
# Statistical test
[![](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://github.com/ginarteam) [![](https://img.shields.io/badge/Telegram-Group-blue.svg)](https://t.me/GINAR_io) 


GINAR is a blockchain technology company specializing in providing a decentralized random number generator. Random Number Generation, or RNG, is a key component to applications that benefit from true randomness. GINAR is set to release a best-in-class decentralized.
- Random Number Generator (dRNG) that will change the financial, gambling, online gaming, and IOT industry by providing the fastest, most secure and easily verifiable service, ..

- For more detail about GINAR: Read our white-paper -> [![](https://img.shields.io/badge/docs-latest-af1a97.svg)](https://www.ginar.io/whitepaper-v2.0.pdf)

This is implementation of NIST's statistical test suite for Random Number Generator (RNG) that apply to GINAR RNG    

# NIST SP 800-22 Statistical Test Suite

  
> Generators suitable for use in cryptographic applications may need to meet stronger requirements than for other applications.  In particular, their outputs must be unpredictable in the absence of knowledge of the inputs.  Some criteria for characterizing and selecting appropriate generators are discussed in this document.  The subject of statistical testing and its relation to cryptanalysis is also discussed, and some recommended statistical tests are provided.  These tests may be useful as a first step in determining whether or not a generator is suitable for a particular cryptographic application.  However, no set of statistical tests can absolutely certify a generator as appropriate for usage in a particular application, i.e., statistical testing cannot serve as a substitute for cryptanalysis.  The design and cryptanalysis of generators is outside the scope of this paper.

[NIST SP 800-22 Statistical Test Suite](https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-22r1a.pdf)

### Installation
GINAR Random test requires  **Python 2.7** to run.
First, you need to clone our repository and install some packages:

```sh
$ git clone https://github.com/ginarteam/randomness-tests.git
```
```sh
$ pip install requests
$ pip install numpy
$ pip install matplotlib
```
### Get data for random test

You need a dataset of random number for the test. We have built a function that help you get data from GINAR:
- Login your account  GINAR
- Initialize your session key
- Copy the init-session-key link (url)

(More detail, please visit our [documentation website](https://docs.ginar.io))

This test suite requires 8000 numbers as minimum. We recommend using 2000000 numbers.
### Run the test
```sh
$ cd randomness-tests
$ python test.py
```

### Output and visualization

The output of this test store in `results` folder.
`results` folder contains some `csv` and `png` files that is the ouput and column chart of every single test.

Sample of `csv`:

| n	| chi_sq | p-value | success |
| - | ------ | ------- | ------- |
|256|	3.875|	0.868221541877252|	True|
|256|	4.75|	0.783931686247815|	True|
|256	|5.5|	0.703039994468557|	True|
|256|	24.25|	0.002080662493339|	False|
|256|	5	|0.757576133133066|	True|
|256|	6.125|	0.633232282721816|	True|
|256|	9.375|	0.311655310694243|	True|
|256	|7.75|	0.458264157653297|	True|
|256|	10.25|	0.247915841547624|	True|

Sample of `png`:

![](https://raw.githubusercontent.com/ginarteam/randomness-tests/master/result/Figure_1.png)

### Report
Read [`test_report`](https://github.com/ginarteam/randomness-tests/blob/master/Test_Report.pdf) for more detail of Test Suite
