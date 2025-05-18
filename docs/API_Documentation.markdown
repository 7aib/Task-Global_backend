# Inventory Management API Documentation

This document outlines the API endpoints for the Inventory Management System, built with FastAPI. The API supports managing categories, products, inventory, and sales, along with providing a dashboard and revenue analytics.

## Base URL

```
http://<your-domain>/
```

- **Note**: For local development, use `http://127.0.0.1:8000/`.
- **Authentication**: No authentication is required for these endpoints (public access). Add authentication (e.g., JWT) for production use.

## Endpoints

### 1. Dashboard

- **Method**: GET
- **Path**: `/`
- **Description**: Retrieves a summary of the inventory management system, including total counts of categories, products, inventory items, sales, and the five most recent sales.
- **Parameters**: None
- **Request Body**: None
- **Responses**:
  - **200 OK**: Returns the dashboard summary.
  - **500 Internal Server Error**: Unexpected server error.
- **Example Request**:
  ```
  GET http://127.0.0.1:8000/
  ```
- **Example Response**:
  ```json
  {
    "message": "Welcome to the Inventory Management System",
    "summary": {
      "categories": 10,
      "products": 50,
      "inventory_items": 45,
      "sales": 100
    },
    "latest_sales": [
      {
        "id": 1,
        "product_id": 5,
        "quantity": 1,
        "total_price": 29.99,
        "channel": "Amazon",
        "sale_date": "2025-05-17T10:00:00"
      },
      ...
    ]
  }
  ```

### 2. Create Category

- **Method**: POST
- **Path**: `/categories/`
- **Description**: Creates a new category.
- **Parameters**: None
- **Request Body**:
  ```json
  {
    "name": "string",
    "description": "string" // optional
  }
  ```
- **Responses**:
  - **200 OK**: Category created successfully.
  - **422 Unprocessable Entity**: Invalid input data (e.g., missing name).
- **Example Request**:
  ```
  POST http://127.0.0.1:8000/categories/
  Content-Type: application/json

  {
    "name": "Electronics",
    "description": "Gadgets and devices"
  }
  ```
- **Example Response**:
  ```json
  {
    "id": 1,
    "name": "Electronics",
    "description": "Gadgets and devices",
    "is_deleted": false
  }
  ```

### 3. Get All Categories

- **Method**: GET
- **Path**: `/categories/`
- **Description**: Retrieves a list of all non-deleted categories.
- **Parameters**: None
- **Request Body**: None
- **Responses**:
  - **200 OK**: List of categories.
  - **500 Internal Server Error**: Unexpected server error.
- **Example Request**:
  ```
  GET http://127.0.0.1:8000/categories/
  ```
- **Example Response**:
  ```json
  [
    {
      "id": 1,
      "name": "Electronics",
      "description": "Gadgets and devices",
      "is_deleted": false
    },
    ...
  ]
  ```

### 4. Get Category by ID

- **Method**: GET
- **Path**: `/categories/{category_id}`
- **Description**: Retrieves a specific category by its ID.
- **Parameters**:
  - `category_id` (int, path): The ID of the category.
- **Request Body**: None
- **Responses**:
  - **200 OK**: Category details.
  - **404 Not Found**: Category not found or soft-deleted.
- **Example Request**:
  ```
  GET http://127.0.0.1:8000/categories/1
  ```
- **Example Response**:
  ```json
  {
    "id": 1,
    "name": "Electronics",
    "description": "Gadgets and devices",
    "is_deleted": false
  }
  ```

### 5. Create Product

- **Method**: POST
- **Path**: `/products/`
- **Description**: Creates a new product and initializes its inventory with a stock of 1.
- **Parameters**: None
- **Request Body**:
  ```json
  {
    "name": "string",
    "description": "string", // optional
    "price": float,
    "category_id": int
  }
  ```
- **Responses**:
  - **200 OK**: Product created successfully.
  - **422 Unprocessable Entity**: Invalid input data (e.g., negative price, invalid category_id).
- **Example Request**:
  ```
  POST http://127.0.0.1:8000/products/
  Content-Type: application/json

  {
    "name": "Smartphone",
    "description": "Latest model",
    "price": 599.99,
    "category_id": 1
  }
  ```
- **Example Response**:
  ```json
  {
    "id": 1,
    "name": "Smartphone",
    "description": "Latest model",
    "price": 599.99,
    "category_id": 1,
    "is_deleted": false
  }
  ```

### 6. Get All Products

- **Method**: GET
- **Path**: `/products/`
- **Description**: Retrieves a list of all non-deleted products.
- **Parameters**: None
- **Request Body**: None
- **Responses**:
  - **200 OK**: List of products.
  - **500 Internal Server Error**: Unexpected server error.
- **Example Request**:
  ```
  GET http://127.0.0.1:8000/products/
  ```
- **Example Response**:
  ```json
  [
    {
      "id": 1,
      "name": "Smartphone",
      "description": "Latest model",
      "price": 599.99,
      "category_id": 1,
      "is_deleted": false
    },
    ...
  ]
  ```

### 7. Get Product by ID

- **Method**: GET
- **Path**: `/products/{product_id}`
- **Description**: Retrieves a specific product by its ID.
- **Parameters**:
  - `product_id` (int, path): The ID of the product.
- **Request Body**: None
- **Responses**:
  - **200 OK**: Product details.
  - **404 Not Found**: Product not found or soft-deleted.
- **Example Request**:
  ```
  GET http://127.0.0.1:8000/products/1
  ```
- **Example Response**:
  ```json
  {
    "id": 1,
    "name": "Smartphone",
    "description": "Latest model",
    "price": 599.99,
    "category_id": 1,
    "is_deleted": false
  }
  ```

### 8. Delete Product

- **Method**: DELETE
- **Path**: `/products/{product_id}`
- **Description**: Soft-deletes a product by marking it as `is_deleted=true`.
- **Parameters**:
  - `product_id` (int, path): The ID of the product.
- **Request Body**: None
- **Responses**:
  - **200 OK**: Product soft-deleted successfully.
  - **404 Not Found**: Product not found or already soft-deleted.
- **Example Request**:
  ```
  DELETE http://127.0.0.1:8000/products/1
  ```
- **Example Response**:
  ```json
  {
    "message": "Product soft-deleted"
  }
  ```

### 9. Create Inventory

- **Method**: POST
- **Path**: `/inventory/`
- **Description**: Creates a new inventory entry for a product.
- **Parameters**: None
- **Request Body**:
  ```json
  {
    "product_id": int,
    "stock": int
  }
  ```
- **Responses**:
  - **200 OK**: Inventory entry created successfully.
  - **422 Unprocessable Entity**: Invalid input data (e.g., negative stock, invalid product_id).
- **Example Request**:
  ```
  POST http://127.0.0.1:8000/inventory/
  Content-Type: application/json

  {
    "product_id": 1,
    "stock": 100
  }
  ```
- **Example Response**:
  ```json
  {
    "id": 1,
    "product_id": 1,
    "stock": 100,
    "is_deleted": false
  }
  ```

### 10. Get All Inventory

- **Method**: GET
- **Path**: `/inventory/`
- **Description**: Retrieves a list of all non-deleted inventory items.
- **Parameters**: None
- **Request Body**: None
- **Responses**:
  - **200 OK**: List of inventory items.
  - **500 Internal Server Error**: Unexpected server error.
- **Example Request**:
  ```
  GET http://127.0.0.1:8000/inventory/
  ```
- **Example Response**:
  ```json
  [
    {
      "id": 1,
      "product_id": 1,
      "stock": 100,
      "is_deleted": false
    },
    ...
  ]
  ```

### 11. Get Inventory by ID

- **Method**: GET
- **Path**: `/inventory/{inventory_id}`
- **Description**: Retrieves a specific inventory item by its ID.
- **Parameters**:
  - `inventory_id` (int, path): The ID of the inventory item.
- **Request Body**: None
- **Responses**:
  - **200 OK**: Inventory item details.
  - **404 Not Found**: Inventory item not found or soft-deleted.
- **Example Request**:
  ```
  GET http://127.0.0.1:8000/inventory/1
  ```
- **Example Response**:
  ```json
  {
    "id": 1,
    "product_id": 1,
    "stock": 100,
    "is_deleted": false
  }
  ```

### 12. Create Sale

- **Method**: POST
- **Path**: `/sales/{product_id}`
- **Description**: Creates a new sale for a product, reducing its inventory stock by 1 (assumes quantity is 1 for simplicity).
- **Parameters**:
  - `product_id` (int, path): The ID of the product being sold.
- **Request Body**:
  ```json
  {
    "channel": "string", // e.g., "Amazon", "Walmart"
    "customer_email": "string" // optional
  }
  ```
- **Responses**:
  - **200 OK**: Sale created successfully.
  - **400 Bad Request**: Product out of stock.
  - **404 Not Found**: Product not found or soft-deleted.
  - **422 Unprocessable Entity**: Invalid input data.
- **Example Request**:
  ```
  POST http://127.0.0.1:8000/sales/1
  Content-Type: application/json

  {
    "channel": "Amazon",
    "customer_email": "customer@example.com"
  }
  ```
- **Example Response**:
  ```json
  {
    "id": 1,
    "product_id": 1,
    "quantity": 1,
    "total_price": 599.99,
    "sale_date": "2025-05-17T10:00:00",
    "channel": "Amazon",
    "customer_email": "customer@example.com",
    "is_deleted": false
  }
  ```

### 13. Get All Sales

- **Method**: GET
- **Path**: `/sales/`
- **Description**: Retrieves a list of sales, optionally filtered by date range, product ID, or category ID.
- **Parameters**:
  - `start_date` (string, query, optional): Filter sales from this date (ISO 8601, e.g., `2025-05-01T00:00:00`).
  - `end_date` (string, query, optional): Filter sales until this date (ISO 8601).
  - `product_id` (int, query, optional): Filter sales by product ID.
  - `category_id` (int, query, optional): Filter sales by category ID.
- **Request Body**: None
- **Responses**:
  - **200 OK**: List of sales.
  - **500 Internal Server Error**: Unexpected server error.
- **Example Request**:
  ```
  GET http://127.0.0.1:8000/sales/?start_date=2025-05-01T00:00:00&product_id=1
  ```
- **Example Response**:
  ```json
  [
    {
      "id": 1,
      "product_id": 1,
      "quantity": 1,
      "total_price": 599.99,
      "sale_date": "2025-05-17T10:00:00",
      "channel": "Amazon"
    },
    ...
  ]
  ```

### 14. Revenue Comparison

- **Method**: GET
- **Path**: `/sales/comparison/`
- **Description**: Retrieves a revenue comparison between the current period and the previous period, grouped by a specified period (daily, weekly, monthly, or annual).
- **Parameters**:
  - `period` (string, query, optional): Period for grouping (`daily`, `weekly`, `monthly`, `annual`). Defaults to `weekly`.
- **Request Body**: None
- **Responses**:
  - **200 OK**: List of revenue comparisons.
  - **422 Unprocessable Entity**: Invalid period value.
  - **500 Internal Server Error**: Unexpected server error.
- **Example Request**:
  ```
  GET http://127.0.0.1:8000/sales/comparison/?period=weekly
  ```
- **Example Response**:
  ```json
  [
    {
      "current_period": "2025-20",
      "current_revenue": 1599.97,
      "previous_period": "2025-19",
      "previous_revenue": 1299.98,
      "percentage_change": 23.08
    },
    ...
  ]
  ```

### 15. Get Sale by ID

- **Method**: GET
- **Path**: `/sales/{sale_id}`
- **Description**: Retrieves a specific sale by its ID.
- **Parameters**:
  - `sale_id` (int, path): The ID of the sale.
- **Request Body**: None
- **Responses**:
  - **200 OK**: Sale details.
  - **404 Not Found**: Sale not found or soft-deleted.
- **Example Request**:
  ```
  GET http://127.0.0.1:8000/sales/1
  ```
- **Example Response**:
  ```json
  {
    "id": 1,
    "product_id": 1,
    "quantity": 1,
    "total_price": 599.99,
    "sale_date": "2025-05-17T10:00:00",
    "channel": "Amazon",
    "customer_email": "customer@example.com",
    "is_deleted": false
  }
  ```

## Error Handling

- **400 Bad Request**: Invalid request (e.g., insufficient stock for a sale).
- **404 Not Found**: Resource not found or soft-deleted (e.g., category, product, inventory, or sale).
- **422 Unprocessable Entity**: Invalid input data (e.g., missing required fields, incorrect data types).
- **500 Internal Server Error**: Unexpected server error (e.g., database connection issues).

## Notes

- **Soft Deletion**: All endpoints use soft deletion, marking records as `is_deleted=true` instead of physically deleting them from the database.
- **Sale Assumptions**: The `POST /sales/{product_id}` endpoint assumes a sale quantity of 1 and uses the product’s price as the total price for simplicity.
- **Database**: The API uses MySQL with SQLAlchemy ORM for database operations (though SQLite is mentioned in the README for local development).
- **FastAPI Features**: Endpoints leverage FastAPI’s automatic Swagger UI for interactive testing at `/docs`.
- **Time Zone**: All dates are in ISO 8601 format, assumed to be in UTC unless specified.