# e-comm-warehouse
A sample E-Commerce Warehouse System

# Participants
1. Anirban Sinha
2. Aditya Singh Rathore
3. Vinod Kanwar

# ER Diagram For Source Schema
```mermaid
erDiagram
    Categories {
        string category_id PK
        string category_name
    }
    Customers {
        string customer_id PK
        string customer_name
        string customer_email
        string customer_city
        string customer_state
    }
    Geolocation {
        string geolocation_zip_code_prefix
        float geolocation_lat
        float geolocation_lng
        string geolocation_city
        string geolocation_state
    }
    OrderItems {
        string order_id FK
        string product_id FK
        string seller_id FK
        float price
        float freight_value
    }
    OrderPayments {
        string order_id FK
        int payment_sequential
        string payment_type
        int payment_installments
        float payment_value
    }
    Orders {
        string order_id PK
        string customer_id FK
        string order_status
        datetime order_purchase_timestamp
        datetime order_approved_at
    }
    Products {
        string product_id PK
        string product_category FK
        string product_name
        string product_description
        float product_price
    }
    Reviews {
        string review_id PK
        string order_id FK
        int review_score
        string review_comment_title
        string review_comment_message
    }
    Sellers {
        string seller_id PK
        string seller_name
        string seller_city
        string seller_state
    }

    Categories ||--o{ Products: "has"
    Customers ||--o{ Orders: "places"
    Orders ||--o{ OrderItems: "contains"
    Orders ||--o{ OrderPayments: "has"
    Products ||--o{ OrderItems: "is part of"
    Sellers ||--o{ OrderItems: "provides"
    Orders ||--o{ Reviews: "has"
    Geolocation ||--o{ Customers: "located in"
    Geolocation ||--o{ Sellers: "located in"

```

# ER Diagram For OLAP Schema
```mermaid
erDiagram
    SalesFact {
        bigint sales_id PK
        int customer_id FK
        int product_id FK
        int seller_id FK
        int category_id FK
        date time_id FK
        numeric price
        numeric freight_value
        numeric payment_value
    }
    CustomersDim {
        int customer_id PK
        string customer_name
        string customer_city
        string customer_state
    }
    ProductsDim {
        int product_id PK
        string product_name
        string product_category
    }
    SellersDim {
        int seller_id PK
        string seller_name
        string seller_city
        string seller_state
    }
    CategoriesDim {
        int category_id PK
        string category_name
    }
    TimeDim {
        date time_id PK
        int year
        int month
        int day
    }

    SalesFact ||--o{ CustomersDim : "belongs to"
    SalesFact ||--o{ ProductsDim : "contains"
    SalesFact ||--o{ SellersDim : "sold by"
    SalesFact ||--o{ CategoriesDim : "categorized as"
    SalesFact ||--o{ TimeDim : "occurred on"
```