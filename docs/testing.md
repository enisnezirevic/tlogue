# **Pytest Naming Conventions**

## **Test File Naming**
Test files should adhere to the following conventions. Each file should:

- Begin with the prefix **`test_`**.
- Be named after the file or module containing the functionality being tested.

### **Example:**
- **Logic file**: `models.py`  
- **Test file**: `test_models.py`

---

## **Test Function Naming**
Test functions should use descriptive names that clearly communicate their purpose. The naming pattern should highlight:
1. **The operation being tested**.
2. **The conditions under which it is being tested**.
3. **The expected outcome**.

### **Naming Pattern**:
```python
def test_<operation>_<condition>_should_<expected_behaviour>():
```

### **Examples**:
- Testing login functionality:
    ```python
    def test_login_with_valid_credentials_should_return_success():
    ```
  or
    ```python
    def test_login_with_valid_credentials_should_return_200_response():
    ```

- Testing registration with invalid fields:
    ```python
    def test_register_with_invalid_fields_should_raise_error():
    ```
  or
    ```python
    def test_register_with_invalid_fields_should_raise_404_error():
    ```