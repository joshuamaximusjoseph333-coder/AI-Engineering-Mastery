# Project 01 — Data Investigation Report

## 1. Investigation Objective
The objective of this investigation is to examine the order and customer datasets used by the Engineering Workbench and identify meaningful patterns using data profiling, descriptive statistics, and relational SQL analysis.

The investigation focuses on:

- Assessing the quality and structure of the available data.
- Understanding the distribution and variation of product prices.
- Identifying potential statistical outliers.
- Examining product purchase quantities.
- Comparing payment method usage.
- Analyzing customer ordering activity.
- Identifying customers without matching orders.
- Comparing revenue generated across cities.

The findings are based only on the current Project 01 datasets and should be interpreted within the limitations of the available data.

## 2. Dataset Overview
The investigation uses two related CSV datasets.

### Orders Dataset

Source:

`data/raw/orders_week2.csv`

The orders dataset contains 10 order records and 7 columns:

- `order_id`
- `customer_id`
- `product`
- `quantity`
- `price`
- `order_date`
- `payment_method`

Each row represents an order record.

### Customers Dataset

Source:

`data/raw/customers_week2.csv`

The customer dataset contains customer information including:

- `customer_id`
- `customer_name`
- `city`

The two datasets are logically related through `customer_id`.

```text
customers
    │
    │ customer_id
    ↓
orders
```

## 3. Data Quality Findings
The orders dataset was examined using the Engineering Workbench validation and profiling layers before performing deeper statistical and SQL analysis.

The current dataset contains:

```text
Rows:       10
Columns:     7
Duplicates:  0
```
## 4. Price and Statistical Analysis
The `price` column was examined using descriptive statistics and IQR-based outlier detection.

### Price Summary

| Statistic | Value |
|---|---:|
| Mean | ₹14,200 |
| Median | ₹3,000 |
| Minimum | ₹1,000 |
| Maximum | ₹50,000 |
| Range | ₹49,000 |
| Standard Deviation | ₹19,611.79 |
| Q1 | ₹2,000 |
| Q3 | ₹15,000 |
| Skewness | 1.486 |
| Skew Direction | Right-skewed |

The mean price of ₹14,200 is substantially higher than the median price of ₹3,000.

This indicates that higher-priced observations are pulling the arithmetic mean upward. The positive skewness value of approximately `1.486` supports the conclusion that the price distribution is right-skewed.

The standard deviation of approximately ₹19,611.79 also indicates substantial variation in prices within the current dataset.

### Outlier Analysis

The Interquartile Range (IQR) method produced:

| Measure | Value |
|---|---:|
| Q1 | ₹2,000 |
| Q3 | ₹15,000 |
| IQR | ₹13,000 |
| Lower Bound | -₹17,500 |
| Upper Bound | ₹34,500 |

Two observations with a price of ₹50,000 exceed the calculated upper bound and are therefore identified as potential statistical outliers.

These observations correspond to laptop prices. A price of ₹50,000 is plausible for this product category, so the observations should not automatically be treated as data errors or removed.

The outlier results should therefore be interpreted as signals for investigation rather than automatic evidence of invalid data.

## 5. Product Analysis
Product activity was analyzed by calculating the total quantity purchased for each product.

| Product | Total Quantity |
|---|---:|
| Webcam | 5 |
| Mouse | 3 |
| Keyboard | 3 |
| Monitor | 2 |
| Laptop | 2 |

Webcam has the highest total purchased quantity in the current dataset, with 5 units.

Mouse and Keyboard each account for 3 units, while Monitor and Laptop each account for 2 units.

These results describe product purchase quantity only. They should not be interpreted as product profitability or overall product performance because the analysis does not include product costs or profit margins.

## 6. Payment Method Analysis
Payment method usage was analyzed by counting the number of orders associated with each payment method.

| Payment Method | Number of Orders |
|---|---:|
| UPI | 4 |
| Card | 4 |
| Cash | 2 |

UPI and Card are tied as the most frequently occurring payment methods in the current dataset, each appearing in 4 of the 10 orders.

Cash appears in 2 orders.

The current dataset therefore shows equal order counts for UPI and Card. Because the dataset contains only 10 orders, these results should not be generalized into broader customer payment preferences without additional data.

## 7. Customer Analysis
Customer ordering activity was analyzed by combining the `customers` and `orders` tables using relational SQL.

### Orders per Customer

| Customer | Number of Orders |
|---|---:|
| Priya | 3 |
| Arjun | 2 |
| Rahul | 2 |
| Aisha | 2 |
| Neha | 1 |
| Kiran | 0 |

Priya has the highest order count in the current dataset, with 3 orders.

Arjun, Rahul, and Aisha each have 2 orders, while Neha has 1 order.

Kiran has no matching orders in the current orders dataset.

A `LEFT JOIN` was used so that customers without matching orders were preserved in the analysis. This allowed Kiran to remain in the result with an order count of zero.

The order-count results describe customer ordering frequency within the current dataset. They do not by themselves determine customer value, profitability, loyalty, or long-term activity.

## 8. Geographic Revenue Analysis
Revenue was analyzed by combining customer location information with order data and aggregating the results by city.

| City | Revenue |
|---|---:|
| Chennai | ₹52,000 |
| Kochi | ₹51,000 |
| Bengaluru | ₹26,000 |
| Hyderabad | ₹21,000 |
| Mumbai | ₹4,000 |

Chennai generated the highest revenue in the current dataset at ₹52,000, followed closely by Kochi at ₹51,000.

Bengaluru generated ₹26,000, Hyderabad generated ₹21,000, and Mumbai generated ₹4,000.

These figures describe revenue represented in the current dataset only. Because the dataset is small and has limited coverage, the results are not sufficient to conclude that Chennai is the strongest overall market or that additional business investment should be directed there.

A broader geographic business decision would require additional evidence across more orders, customers, and time periods, along with other relevant business metrics.

## 9. Key Findings
The investigation produced the following key findings:

1. **No missing values or duplicate rows were detected in the orders dataset.**  
   The current dataset contains 10 order records across 7 columns and passed the validation checks implemented by the Engineering Workbench.

2. **The price distribution is right-skewed.**  
   The mean price is ₹14,200, while the median is ₹3,000. The calculated skewness of approximately 1.486 indicates positive/right skew, with higher-priced observations pulling the mean upward.

3. **Two ₹50,000 price observations were identified as potential statistical outliers.**  
   These values exceed the IQR upper bound of ₹34,500. However, they correspond to plausible laptop prices and should not automatically be treated as invalid data.

4. **Webcam has the highest total purchased quantity in the current dataset.**  
   A total of 5 webcam units were purchased, followed by Mouse and Keyboard with 3 units each.

5. **UPI and Card are tied as the most frequently occurring payment methods.**  
   Each appears in 4 of the 10 orders, while Cash appears in 2.

6. **Priya has the highest order count in the current dataset.**  
   Priya placed 3 orders. Kiran is present in the customer dataset but has no matching orders in the current orders dataset.

7. **Chennai generated the highest revenue represented in the current dataset.**  
   Chennai generated ₹52,000, followed closely by Kochi at ₹51,000.

## 10. Limitations
The findings in this report should be interpreted within the limitations of the current Project 01 datasets.

### Small Dataset

The orders dataset contains only 10 records. Patterns observed in such a small sample may not represent broader customer or business behavior.

### Limited Customer Coverage

Only a small number of customers are represented. Customer-level conclusions should therefore not be generalized to a larger customer population.

### Limited Time Coverage

The current investigation is based only on the order dates available in the dataset. It does not provide enough historical coverage to identify long-term trends, seasonality, or changes in customer behavior over time.

### Limited Product Coverage

Only five products are represented in the current orders dataset. Product-level findings therefore apply only to this limited sample.

### Revenue Is Not Profit

The geographic analysis measures revenue represented by the available order data. The dataset does not contain product costs, operating expenses, or profit margins.

Therefore, revenue results should not be interpreted as profitability.

### Order Frequency Is Not Customer Value

The number of orders placed by a customer measures ordering frequency within the current dataset.

It does not by itself measure customer profitability, lifetime value, loyalty, or total business importance.

### Statistical Outliers Are Not Automatically Errors

The IQR method identifies statistically unusual observations but does not determine whether those observations are incorrect.

Potential outliers require investigation and business context before any correction or removal decision is made.

### Validation Has Defined Boundaries

The Engineering Workbench verifies the structural and value rules currently implemented by the application.

Passing these checks does not guarantee that every value accurately represents a real-world transaction.

## 11. Recommendations and Next Steps

Based on the current investigation and its limitations, the following next steps would strengthen future analysis:

1. **Collect a larger order dataset.**  
   Additional records would provide stronger evidence for identifying product, customer, payment, and geographic patterns.

2. **Analyze a longer time period.**  
   Historical data would allow trends, seasonality, growth, and changes in customer behavior to be investigated.

3. **Add product cost information.**  
   Combining selling prices with product costs would allow profit and profit-margin analysis instead of relying only on revenue.

4. **Expand customer analysis.**  
   Future analysis could calculate customer spending, average order value, repeat-purchase behavior, and eventually customer lifetime value.

5. **Expand product analysis.**  
   Product quantity can be combined with revenue and cost information to distinguish sales volume from financial performance.

6. **Investigate geographic performance using more data.**  
   City-level revenue should be examined across a larger number of orders and time periods before making geographic business decisions.

7. **Continue investigating statistical outliers rather than automatically removing them.**  
   Outliers should be validated against product and business context before any data-cleaning decision is made.

8. **Extend the Engineering Workbench into a reusable reporting service.**  
   The existing ingestion, validation, profiling, statistical, and SQL layers provide a foundation for the production-oriented work planned in the next stage of Project 01.