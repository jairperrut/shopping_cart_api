- [Sumamry](#sumamry)
- [🚀 **Running the Application**](#-running-the-application-with-docker-compose)
- [📐 **Architecture and Design Decisions Implemented**](#description-of-the-architecture-and-design-decisions-implemented)
    - [✨ **1. Overview**](#-1-overview)
    - [🏗️ **2. Architecture**](#️-2-architecture)
    - [🎨 **3. Design Decisions**](#-3-design-decisions)
    - [🧩 **4. Key Components**](#-4-key-components)
    - [🎯 **5. Design Advantages**](#-5-design-advantages)
    - [🔄 **6. Improvements for Production**](#-6-improvements-for-production)
    - [🏁 **7. Conclusion**](#-7-conclusion)

# 🚀 **Running the Application with Docker Compose**

This document provides step-by-step instructions to build and run the application, as well as to execute tests, using Docker Compose.

---

## ✅ **Prerequisites**

- 🐋 [Docker](https://docs.docker.com/get-docker/) installed on your system.
- 🛠️ [Docker Compose](https://docs.docker.com/compose/install/) installed.

---

## ▶️ **Getting Started**

Clone this repository:
   ```bash
   git clone https://github.com/jairperrut/shopping_cart_api
   cd shopping_cart_api
   ```

### 👥 **Customer Types**
- The type of customer (e.g., `VIP` or `COMMON`) is configured in the `.env` file.  
  This value directly affects the discount strategies available for the shopping cart.

---

### 🛠️ **Building and Running the Application**
To build and start the application, use the following commands:

```bash
docker-compose up --build app
```

#### 🌐 **Accessing the API**
- **API Base URL:** `http://localhost:8000` 
- **API Documentation:** Visit `http://localhost:8000/docs` in your web browser to explore documentation via Swagger UI and test the API.
##### 🔑 **API Endpoints**
- `POST /v1/cart/items`: Adds an item to the cart.
```bash
curl -X 'POST' \
  'http://localhost:8000/v1/cart/items' \
  -d '{
  "product_name": str
}'
```
- `DELETE /v1/cart/items`: Removes an item from the cart.
```bash
curl -X 'DELETE' \
  'http://localhost:8000/v1/cart/items' \
  -d '{
  "product_name": str
}'
```

#### Avaliable Products:
     T-shirt
     Dress
     Jeans
---

### 🧪 **2. Running Tests**
To execute the test suite, use the following command:

```bash
docker-compose up --build tests
```

---

## 🛑 **Stopping the Application**
To stop the running containers, use the following command:

```bash
docker-compose down
```
or
press `CTRL + C` on terminal

---

## ⚠️ **Troubleshooting**

### 🔌 **1. Port Conflicts**
If the application fails to start due to port conflicts:
- Check if the ports specified in the `docker-compose.yml` file are already in use.
- Update the port configuration in the `docker-compose.yml` file if necessary.

### 🐋 **2. Docker Daemon**
Ensure the Docker daemon is running on your system:
- On Linux: Start the Docker service using `sudo systemctl start docker`.
- On macOS/Windows: Verify the Docker Desktop application is running.

---


# 📐 **Description of the Architecture and Design Decisions Implemented**

### ✨ **1. Overview**

The application is a shopping cart system implemented using Python, FastAPI, and a clean architecture approach. It incorporates principles of Domain-Driven Design (DDD) to ensure modularity, scalability, and maintainability. The design emphasizes separation of concerns and facilitates the addition of new features, such as discount strategies, with minimal code changes.

This project was developed based on the challenge described in [CHALLENGE.md](CHALLENGE.md).

---

### 🏗️ **2. Architecture**

#### 🧱 **2.1 Clean Architecture**
The project adheres to the clean architecture pattern, which separates the application into four main layers:

- 🏛️ **Domain Layer**: Contains the core business logic and rules. It is independent of any external frameworks or libraries. Key components include:
  - `Cart`: Represents the shopping cart entity.
  - `CartItem`: Represents the relation of the prodcuts and quantity.
  - `Product`: Represents the shopping cart entity.
  - `CustomerType`: Enum for distinguishing between common and VIP customers.
  - `CalculateStrategy`: Abstract class for defining discount rules.

- 🛠️ **Application Layer**: Handles use cases that orchestrate domain objects. Each use case represents a specific application action, such as adding an item to the cart or calculating the total price.
  - `AddItemToCart`
  - `RemoveItemFromCart`
  - `CalculateCart`

- ⚙️ **Infrastructure Layer**: Implements external dependencies like repositories. Examples include:
  - `InMemoryCartRepository`
  - `InMemoryProductRepository`

- 🌐 **Interface Layer**: Defines the web API using FastAPI. Routes interact with use cases and return data in a RESTful manner.

#### 💉 **2.2 Dependency Injection**
FastAPI’s `Depends` is used to inject dependencies, such as repositories, into routes. This promotes testability and flexibility by allowing different implementations to be swapped in as needed.

---

### 🎨 **3. Design Decisions**

#### 🗂️ **3.1 In-Memory Repositories**
- In-memory repositories (`InMemoryCartRepository` and `InMemoryProductRepository`) are used as default implementations for data handling. These are ideal for prototyping and testing but can be replaced by persistent repositories in the future.
   - **Products Repository**: Initialized with sample data:
     - 👕 `T-shirt` - $35.99
     - 👗 `Dress` - $80.75
     - 👖 `Jeans` - $65.50
   - **Cart Repository**: Stores the cart's items and customer type.

#### 💸 **3.2 Discount Calculation**

**Challenge**: Implement a flexible system for applying discount strategies, ensuring new rules can be added without significant refactoring.

**Solution**:
- **Strategy Pattern**:
  - The `CalculateStrategy` abstract class defines a standard interface for all strategies.
  - Concrete strategies like `VIPCalculateStrategy`, `Get3For2CalculateStrategy` and `FullPriceCalculateStrategy` implement this interface and encapsulate specific discount logic.

- **Validation**: Each strategy includes a `is_applicable` method to determine whether it applies to the current cart context.

- **CalculateFactory**:
  - Automatically loads strategies using a factory method that dynamically discovers and initializes subclasses of `CalculateStrategy`.

#### **3.3 Use Cases as Orchestrators**
Use cases, such as `AddItemToCart`, are responsible for managing domain operations. They ensure the separation of business rules from API layers.

#### **3.4 Testability**
- **In-Memory Repositories**:
  - Simulate database behavior during development and testing without requiring external services.

- **Pytest Fixtures**:
  - Dependency injection via `TestClient` and repository overrides ensures isolated and repeatable tests.

#### **3.5 Modular Route Definitions**
FastAPI’s `APIRouter` is used to group related endpoints, keeping the codebase organized and allowing for future extension without modifying existing routes.

---

### 🧩 **4. Key Components**

#### 📦 **4.1 Domain Models**
- **Cart**: Tracks details with **CartItem**, and customer type.
- **CartItem**: Tracks items and quantities.
- **Product**: Represents items available for purchase.
- **CustomerType**: Enum for common and VIP customers.

#### 🗄️ **4.2 Repositories**
- **InMemoryCartRepository**: Stores cart data in memory, adhering to the repository interface.
- **InMemoryProductRepository**: Stores products data in memory. Provides product data for use cases.

#### 📋 **4.3 Use Cases**
- **AddItemToCart**: Validates and adds an item to the cart.
- **RemoveItemFromCart**: Validates and removes an item from the cart.
- **CalculateCart**: Applies all discount strategies, calculates totals, and identifies the best deal.

#### 🔀 **4.4 Strategies**
- **Get3For2CalculateStrategy**: Implements the "Buy 3, Pay for 2" promotion.
- **VIPCalculateStrategy**: Applies a 15% discount for VIP customers.
- **FullPriceCalculateStrategy**: Implements the calculation whithout promotions.

---

### 🎯 **5. Design Advantages**

#### ➕ **5.1 Extensibility**
- New discount strategies can be added by implementing the `CalculateStrategy` interface and ensuring their logic is self-contained.
- The `CalculateFactory` dynamically discovers and uses strategies, avoiding manual updates to lists or logic.

#### ✅ **5.2 Testability**
- Clear separation of concerns ensures each layer can be tested independently.
- Use of in-memory repositories allows for fast and isolated unit tests.

#### 🔧 **5.3 Maintainability**
- Clean architecture enforces modularity, reducing the risk of breaking changes.
- The `CalculateFactory` minimize changes required for adding or updating features.

#### 📋 **5.4 Schema Definitions**
- Data transferred via the API is defined using `dataclasses`, closely mirroring domain objects. This ensures clarity and consistency in input/output interfaces.

---

### 🔄 **6. Improvements for Production** 

While the current prototype is functional, the following enhancements would make the application more robust, scalable, and suitable for production:

#### 🗄️ **6.1 Database Integration** 
  - Replace in-memory repositories with a persistent database, such as PostgreSQL or MySQL.
  - Use an ORM like SQLAlchemy to manage database interactions efficiently.
  - Add migrations using tools like Alembic to handle schema changes.
#### 🆔 **6.2 Use IDs for Products** 
  - Currently, products are referenced by name, which is not scalable or reliable.
  - Introduce unique identifiers (e.g., UUIDs or incremental IDs) for products and use these IDs in API requests and responses.
  - This prevents issues with duplicate product names and simplifies updates or deletions.
#### 🛍️ **6.3 User-Centric Cart** 
  - The cart is currently global, shared across the entire application.
  - Associate each cart with a specific user to support multiple users simultaneously.
  - Implementing authentication and session management to identify users.
#### 🏷️ **6.4 Dynamic Discount Management** 
  - Instead of setting discounts for VIPs in the `.env` file, implement a dynamic discount management system to enable updates without redeploying the application.

#### ❌ **6.5 Improved Error Handling** 
  - Standardize API responses to return meaningful error codes and messages.

#### 📈 **6.6 Observability and Monitoring** 
  - Add structured logging using tools like ELK Stack.
  - Monitor performance with APM tools like New Relic, Datadog or Kibana.
  - Include health check endpoints and metrics using tools like Prometheus.

---

### 🏁 **7. Conclusion** 
The application’s architecture and design reflect best practices in modern Python development. By combining clean architecture, DDD principles, and patterns like Strategy and Dependency Injection, the system achieves flexibility, scalability, and robustness, while remaining easy to extend and maintain.
