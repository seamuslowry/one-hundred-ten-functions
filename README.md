[![Code Quality](https://github.com/seamuslowry/hundred-and-ten-serverless/actions/workflows/lint.yaml/badge.svg?branch=main)](https://github.com/seamuslowry/hundred-and-ten-serverless/actions/workflows/lint.yaml)
[![100% Coverage](https://github.com/seamuslowry/hundred-and-ten-serverless/actions/workflows/coverage.yaml/badge.svg?branch=main)](https://github.com/seamuslowry/hundred-and-ten-serverless/actions/workflows/coverage.yaml)

# Hundred and Ten Serverless

An Azure Functions exposing an API for the game One Hundred Ten

## Getting Started

To run the application locally, run

```sh
docker compose up -d --build
```

This should create a mongo DB container that the API will connect to and expose all endpoints on `localhost:7071`.
