## Driving Test Data Platform 

A full end-to-end data engineering project that simulates how driving test results
can be collected, processed, stored, analyzed, and visualized for operational
and business insights.

This project is designed for learning real-world data systems.

## Project Overview

This platform processes driving test results (PASS / FAIL), stores them in a SQL
database, runs analytical transformations using Apache Spark, and prepares the data
for visualization via a web dashboard.

Each record represents:
- A driving test attempt
- The test location (city)
- The examiner
- Pass or fail result
- Number of errors

## System Architecture
CSV Data
↓
Spark ETL (etl.py)
↓
SQL Server Database
↓
Backend Access Layer (database.py)
↓
Application / Dashboard (app.py)

## Project Structure

driving-test-data-platform/
│
├── spark/
│ └── etl.py # Spark ETL pipeline
│
├── app.py # Application entry point
├── database.py # Database access layer
├── README.md # Project documentation

---

## Technologies Used

- Python– Core programming language
- Apache Spark (PySpark) – ETL and analytics
- SQL Server – Relational data storage
- Git & GitHub – Version control
- Streamlit (planned) – Web dashboard
- Cloud deployment (planned) – Azure / AWS

---

## Data Pipeline Details

###  Extract
- Raw driving test data is read from CSV files using Spark

###  Transform
- Data cleaning (trimming strings, fixing types)
- Feature engineering (PassFlag column)
- Aggregations:
  - Pass rate by city

###  Load
- Cleaned data is written to SQL Server
- Database functions allow querying and inserting records

## Key Concepts Demonstrated

- ETL pipeline design
- Separation of concerns
- Data aggregation & analytics
- Backend database abstraction
- Real-world data modeling
- Version control best practices

## Example Insights Generated

- Pass rate by city
- Identification of lowest and highest pass-rate locations

## Future Enhancements

- Interactive Streamlit dashboard
- REST API for data access
- Cloud deployment (Azure SQL + Azure App Service)

## How to Run the Project

1. Clone the repository:
   ```bash
   git clone https://github.com/yasmeennagpal/icbc-driving-test-data-system.git

