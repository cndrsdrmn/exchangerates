# Exchange Rates Crawl with Scrapy

This Scrapy project aims to provide a simple and efficient way to crawl exchange rates, specifically focusing on Bank Indonesia transaction rates. The project is designed to be easily deployable on AWS Lambda using Docker.

## Prerequisites

Before you begin, make sure you have the following installed:

- Python 3.x
- Docker

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/cndrsdrmn/exchangerates.git
   cd exchangerates
   ```

2. Create a virtual environment and activate it:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running Locally

To run the Scrapy spider locally and store the results in a JSON file, use the following command:

```bash
scrapy crawl bank_indonesia_transaction_rate -o output.json
```

### Dockerizing the Scrapy Spider

Build the Docker image using the provided Dockerfile:

```bash
docker build -t exchangerates .
```

Run the Docker container:

```bash
docker run -it --rm -p 9000:8080 exchangerates
```

Run command for trigger the crawler:

```shell
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'
```

## Contributing

Feel free to contribute to this project by submitting issues or pull requests. Your feedback and contributions are highly appreciated.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
