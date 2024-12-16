# Shopping Cart

A successful promotional campaign can bring many advantages to businesses looking to acquire new customers, increase sales, or clear out stock. Our goal is to create a shopping cart system with a promotional campaign and differentiated pricing based on user type.

### **Promotions:**

1. 🏷️ **Get 3 for the Price of 2**:
    
    Customers who add multiple products to their cart will receive the third product for free. The free product will always be the lowest-priced item.
    
    - Buy 1, pay for 1.
    - Buy 2, pay for 2.
    - Buy 3, pay for 2 (lowest-priced item is free).
    - Buy 4, pay for 3, and so on.
2. 👑 **VIP Discount**:
    
    VIP customers enjoy a **15% discount** on all purchases. However, VIP customers **cannot combine this discount with the "Get 3 for the Price of 2" promotion**.
    

The system must **automatically calculate and suggest the best pricing option** (either using the VIP discount or the "Get 3 for 2" promotion) based on the user's cart contents and user type (VIP or common).

---

## **Key Requirements**

- The API should be able to **Add** and **Remove** items from the shopping cart.
- The API should identify whether the customer is **VIP** or **common**.
- The API should calculate the **total price** based on:
    - The **"Get 3 for 2" promotion** for common users.
    - The **VIP discount** (15%) for VIP customers.
    - For VIP customers, the API should decide whether it's better to apply the 15% discount or the "Get 3 for 2" promotion, and recommend the best deal.

---

### **Product Price Table**

| Product | Price (USD) |
| --- | --- |
| T-shirt | 35.99 |
| Jeans | 65.50 |
| Dress | 80.75 |

---

### **Sample Scenarios**

**Scenario 1**:

A common customer adds 3 t-shirts to the cart.

- **Expected total**: USD 71.98
    - (Using "Get 3 for 2", the customer pays for 2 t-shirts, and 1 is free).

**Scenario 2**:

A common customer adds 2 t-shirts and 2 jeans.

- **Expected total**: USD 137.49
    - (The free item is the t-shirt since it's the cheapest item).

**Scenario 3**:

A VIP customer adds 3 dresses to the cart.

- **VIP Discount**: USD 205.91
    - (15% discount on the total, so 242.25 - 36.34).
- **Get 3 for 2**: USD 161.50
    - (The customer only pays for 2 dresses).
- **Recommendation**: Use "Get 3 for 2" (cheaper than the VIP discount).

**Scenario 4**:

A VIP customer adds 2 jeans and 2 dresses.

- **VIP Discount**: USD 249.57
    - (15% off the total, so 293.00 - 43.43).
- **Get 3 for 2**: USD 211.25
    - (The free item is the jeans since it’s cheaper).
- **Recommendation**: Use "Get 3 for 2" (cheaper than the VIP discount).

**Scenario 5**:

A VIP customer adds 4 t-shirts and 1 jeans to the cart.

- **VIP Discount**:
    
    The total price before the discount is:
    
    - 4 T-shirts = 4 × 35.99 = USD 143.96
    - 1 Jeans = USD 65.50
    - **Total before discount** = USD 209.46
    - Applying the 15% VIP discount:209.46 - (15% of 209.46) = 209.46 - 31.42 = **USD 178.04**
- **Get 3 for 2**:
    
    Using the "Get 3 for 2" promotion, the free item will be a t-shirt (the lowest-priced item).
    
    The calculation will be:
    
    - 4 T-shirts (with 1 free) = Pay for 3 T-shirts = 3 × 35.99 = USD 107.97
    - 1 Jeans = USD 65.50
    - **Total with promotion** = 107.97 + 65.50 = **USD 173.47**
- **Recommendation**:
    
    The "Get 3 for 2" promotion gives a total of USD 173.47, while the VIP discount gives a total of USD 178.04.
    
    **Recommendation**: In this case, it's better for the VIP customer to use the **"Get 3 for 2" promotion** because it results in a lower total price.
    

---

## **Documentation Requirements**

Please provide a `README` that includes:

- Instructions on how to **run the project**.
- A description of the **architecture** and **design decisions** implemented.