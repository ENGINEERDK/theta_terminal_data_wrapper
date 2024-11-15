# thetadata-api-python

This repo implements an unofficial Python wrapper for the [ThetaData REST API](https://http-docs.thetadata.us/docs/theta-data-rest-api-v2/4g9ms9h4009k0-getting-started).


## Context
The original [thetadata-python](https://github.com/ThetaData-API/thetadata-python) library is deprecated and it's preferred to use the REST API directly. 

Their documentation provides Python examples for the REST API that are useful and comprehensive and you'll find these on every endpoint page ([example](https://http-docs.thetadata.us/docs/theta-data-rest-api-v2/a38vp739baoch-quote-snapshot)). This library is a simple wrapper on those examples into neat classes and functions that anyone can download and use. It provides 2 additional conveniences:

1. Integration with pandas, so data is returned to your program directly in a DataFrame.
2. A CLI (command-line-interface) wrapper for downloading data directly without writing any code yourself

## Usage

> ### Make sure [ThetaTerminal](https://http-docs.thetadata.us/docs/theta-data-rest-api-v2/4g9ms9h4009k0-getting-started#what-is-theta-terminal-and-why-do-i-need-it) is running - nothing will work without it!

This library currently provides 3 classes for core operations: 
* `ThetaDataStocksHistorical`
* `ThetaDataStocksSnapshot`
* `ThetaDataOptions`

Here's an example of using the snapshot object to get current market quotes:

```
stocks_snapshot = ThetaDataStocksSnapshot(log_level="INFO", output_dir="./output")
quotes_df = stocks_snapshot.get_quotes("AAPL")
print(quotes_df.head())
```

Several code examples are available [here](https://github.com/pythonfortraders/thetadata-api-python/tree/main/examples).

There's also a command line interface available in `cli`. You can use it as follows: 

```
(pft) ➜  cli git:(main) python main.py 
                                                                                                                                     
 Usage: main.py [OPTIONS] COMMAND [ARGS]...                                                                                 
                                                                                                                                     
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                                           │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.                    │
│ --help                        Show this message and exit.                                                                         │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ options                                                                                                                           │
│ stocks                                                                                                                            │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
``` 

Subcommands nest downwards naturally. For example, let's say you want to get historical OHLC data for a stock:
```
(pft) ➜  cli git:(main) python thetadata_cli.py stocks historical ohlc AAPL 20240101 20240201
⠸ Loading data...Data retrieved successfully
```
This will save the data as a local CSV named `ohlc_AAPL_20240101_20240201.csv`. Many examples of CLI usage can be found [here](https://github.com/pythonfortraders/thetadata-api-python/blob/08ec0160da2519d5a0de73d8ec29ab8dd0c8d98c/cli/thetadata_cli.py#L1-L78).

## Features

1. Starts the Theta Terminal connection in backgroud automatically.[Not supported now]
2. Downloads the data in CSV files using below commands.

## Example Commands

Example usage commands:
Copy and execute the commands below in your terminal directly from project root, CSV data will be saved in project root.

### List roots Data:
#### List all roots:
1. option 2. stock 3. index
   `python main.py roots data stock`
   `python main.py roots data option`

### Stocks Historical Data:

#### Get end-of-day report:
   
   `python main.py stocks historical eod-report AAPL 20240101 20240131`

#### Get quotes:

   `python main.py stocks historical quotes MSFT 20240101 20240131 --interval 3600000`

### Stocks Snapshot Data:

#### Get real-time quotes:
   `python main.py stocks snapshot quotes AAPL`

#### Get real-time OHLC:
   `python main.py stocks snapshot ohlc NVDA`

#### Get real-time trades:
   `python main.py stocks snapshot trades TSLA`

### Options Data:
### Historical:
#### Get historical EOD report:
   `python main.py options historical eod-report AAPL 20240119 170000 C 20240101 20240131`

#### Get historical quotes:
   `python main.py options historical quotes AAPL 20240119 170000 C 20240101 20240131`

#### Get historical trades:
   `python main.py options historical trades AAPL 20240119 170000 C 20240101 20240131`

#### Get historical trade quote:
   `python main.py options historical trade-quote AAPL 20240119 170000 C 20240101 20240131`

#### Get historical Greeks:
   `python main.py options historical greeks AAPL 20240119 170000 C 20240101 20240131`

#### Get historical third-order Greeks:
   `python main.py options historical greeks-third-order AAPL 20240119 170000 C 20240101 20240131`

#### Get historical trade Greeks:
   `python main.py options historical trade-greeks AAPL 20240119 170000 C 20240101 20240131`

#### Get historical trade Greeks third order:
   `python main.py options historical trade-greeks-third-order AAPL 20240119 170000 C 20240101 20240131`

### Bulk:
#### Get bulk EOD:
   `python main.py options bulk eod AAPL 20240119 20240101 20240131`

#### Get bulk OHLC:
   `python main.py options bulk ohlc AAPL 20240119 20240101 20240131`

#### Get bulk trade:
   `python main.py options bulk trade AAPL 20240119 20240101 20240131`

#### Get bulk trade quote:
   `python main.py options bulk trade-quote AAPL 20240119 20240101 20240131`

#### Get bulk trade Greeks:
   `python main.py options bulk trade-greeks AAPL 20240119 20240101 20240131`

### Snapshot:
#### Get quote snapshot:
   `python main.py options snapshot quote AAPL 20240119 170000 C`

#### Get OHLC snapshot:
   `python main.py options snapshot ohlc AAPL 20240119 C 170000`

#### Get bulk quote snapshot:
   `python main.py options snapshot bulk-quote AAPL 20240119`

#### Get bulk OHLC snapshot:
   `python main.py options snapshot bulk-ohlc AAPL 20240119`

#### Get bulk open interest snapshot:
   `python main.py options snapshot bulk-open-interest AAPL 20240119`


## Disclaimer
Currently work in progress for cloasing the theta Terminal connection.

Workaround - 
1. After work done, execute the last query again to close the connection.