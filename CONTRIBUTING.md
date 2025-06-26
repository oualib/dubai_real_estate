# Contributing to Dubai Real Estate Database

Thank you for your interest in contributing to the Dubai Real Estate Database project! We welcome contributions from the community.

## 🚀 Quick Start for Contributors

### 1. Development Setup

```bash
# Clone the repository
git clone https://github.com/oualib/dubai_real_estate.git
cd dubai_real_estate

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

### 2. Set Up ClickHouse for Development

You'll need a ClickHouse instance for testing. Quick options:

**🆓 [ClickHouse Cloud - 1 Month Free Trial](https://clickhouse.com/cloud)**
- Perfect for development and testing
- No setup required - ready in minutes
- Automatic scaling and backups

**Local Installation:**
```bash
# Using Docker (recommended for development)
docker run -d --name clickhouse-dev \
  -p 8123:8123 \
  -p 9000:9000 \
  clickhouse/clickhouse-server

# Or install locally on your system
# See: https://clickhouse.com/docs/en/install
```

### 3. Create Development Connection

```python
from dubai_real_estate.connection import create_connection

# For ClickHouse Cloud (recommended)
create_connection(
    "dev", 
    "client",
    host="your-dev-instance.clickhouse.cloud",
    port=8443,
    username="default",
    password="your-password",
    secure=True,
    set_auto=True
)

# For local Docker instance
create_connection(
    "dev", 
    "client", 
    host="localhost",
    port=8123,
    username="default",
    password="",
    set_auto=True
)
```

### 4. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=dubai_real_estate

# Run specific test file
pytest tests/test_connection.py

# Run tests that don't require ClickHouse
pytest -m "not integration"
```

## 📝 Contribution Types

We welcome several types of contributions:

### 🐛 Bug Reports
- Use the issue template
- Include minimal reproduction steps
- Specify your environment (Python version, OS, ClickHouse version, etc.)

### ✨ Feature Requests
- Describe the use case clearly
- Explain why it would be valuable
- Consider backward compatibility

### 🔧 Code Contributions
- SQL functions for data processing
- Performance improvements
- New ClickHouse integrations
- Documentation improvements

### 📊 Data Quality
- Data validation rules
- Quality checks
- Documentation of data issues

## 🛠️ Development Guidelines

### Code Style

```bash
# Format code
black dubai_real_estate/
isort dubai_real_estate/

# Lint code
flake8 dubai_real_estate/
mypy dubai_real_estate/
```

### Testing

```python
# Add tests for new features
def test_new_feature():
    # Arrange
    connection = create_test_connection()
    
    # Act
    result = new_feature(connection)
    
    # Assert
    assert result.is_valid()
```

### SQL Functions

When adding new SQL functions:

```sql
-- Format: CATEGORY/FUNCTION_NAME.sql
-- Example: FORMAT/FORMAT_CURRENCY.sql

CREATE OR REPLACE FUNCTION FORMAT_CURRENCY(amount Nullable(Float64))
RETURNS String
AS $$
    CASE 
        WHEN amount IS NULL THEN 'N/A'
        WHEN amount = 0 THEN 'Free'
        ELSE concat('AED ', formatReadableQuantity(amount))
    END
$$;
```

## 📋 Pull Request Process

### 1. Branch Naming
- `feature/feature-name` - New features
- `fix/bug-description` - Bug fixes
- `docs/documentation-update` - Documentation only
- `refactor/component-name` - Code refactoring

### 2. Commit Messages
```
feat: add support for real-time data streaming
fix: resolve connection timeout in cloud environments
docs: update installation guide for ClickHouse Cloud
refactor: simplify credential storage logic
```

### 3. Pull Request Template
- Clear description of changes
- Link related issues
- Include tests for new functionality
- Update documentation if needed

## 📊 Working with Real Data

### Sample Queries for Testing

```python
# Test transaction data integrity
def test_transaction_data_quality():
    """Test data quality for 1.5M+ transactions"""
    query = """
    SELECT 
        COUNT(*) as total,
        COUNT(DISTINCT transaction_id) as unique_transactions,
        COUNT(CASE WHEN actual_worth > 0 THEN 1 END) as transactions_with_value,
        MIN(instance_date) as earliest_date,
        MAX(instance_date) as latest_date
    FROM dld_transactions
    """
    result = execute_query(query)
    assert result[0]['total'] > 1400000  # 1.5M+ transactions
    assert result[0]['unique_transactions'] == result[0]['total']  # All unique
    assert result[0]['earliest_date'] >= '2002-01-01'  # Historical data
    assert result[0]['latest_date'] <= '2025-12-31'  # Current data

# Test geographical data coverage  
def test_area_coverage():
    """Test coverage across Dubai areas"""
    query = """
    SELECT 
        COUNT(DISTINCT area_name_english) as total_areas,
        COUNT(CASE WHEN area_name_english = 'Downtown Dubai' THEN 1 END) as downtown_count,
        COUNT(CASE WHEN area_name_english = 'Palm Jumeirah' THEN 1 END) as palm_count
    FROM dld_transactions
    WHERE area_name_english IS NOT NULL
    """
    result = execute_query(query)
    assert result[0]['total_areas'] > 200  # 200+ distinct areas
    assert result[0]['downtown_count'] > 1000  # Popular areas have data
    assert result[0]['palm_count'] > 1000  # Luxury areas covered
```

## 🧪 Testing Strategy

### Unit Tests
```python
# Test individual functions
def test_format_date():
    assert FORMAT_DATE('2023-01-01') == '01 Jan 2023'
```

### Integration Tests
```python
# Test complete workflows with real data
def test_full_installation():
    conn = create_connection("test", "client", host="localhost")
    result = install_database()
    assert result['success'] == True
    
    # Verify data integrity
    cursor = conn.execute("SELECT COUNT(*) FROM dld_transactions")
    count = cursor.fetchone()[0]
    assert count > 1000000  # Should have 1M+ transactions

def test_real_data_queries():
    # Test complex analytical queries
    query = """
    SELECT 
        area_name_english,
        COUNT(*) as transactions,
        AVG(actual_worth) as avg_price
    FROM dld_transactions 
    WHERE actual_worth > 0 
    GROUP BY area_name_english
    HAVING transactions > 1000
    ORDER BY avg_price DESC
    """
    result = execute_query(query)
    assert len(result) > 50  # Should return many areas
```

### Performance Tests
```python
# Test query performance with real data volumes
def test_query_performance():
    # Test with 1.5M+ transaction records
    start_time = time.time()
    query = """
    SELECT 
        year(instance_date) as year,
        COUNT(*) as transactions,
        AVG(actual_worth) as avg_amount
    FROM dld_transactions 
    WHERE actual_worth > 0
    GROUP BY year
    ORDER BY year DESC
    """
    result = execute_complex_query(query)
    execution_time = time.time() - start_time
    assert execution_time < 10.0  # Should complete within 10 seconds
    assert len(result) > 20  # Should cover 20+ years of data

def test_large_dataset_memory():
    # Test memory usage with 13M+ total records
    import psutil
    process = psutil.Process()
    initial_memory = process.memory_info().rss
    
    # Load large dataset
    load_full_database()
    
    final_memory = process.memory_info().rss
    memory_used = (final_memory - initial_memory) / 1024 / 1024 / 1024  # GB
    assert memory_used < 15.0  # Should use less than 15GB
```

## 📚 Documentation

### Code Documentation
```python
def install_database(
    database_name: str = DEFAULT_DATABASE,
    include_functions: bool = True,
    **kwargs
) -> Dict[str, Any]:
    """Complete database installation using auto connection.
    
    Args:
        database_name: Target database name (default: 'dubai_real_estate')
        include_functions: Whether to install SQL functions
        **kwargs: Additional installation options
        
    Returns:
        Dict with complete installation results and statistics
        
    Example:
        >>> result = install_database()
        >>> print(f"Success: {result['success']}")
    """
```

### SQL Function Documentation
```sql
-- Function: FORMAT_CURRENCY
-- Category: FORMAT
-- Description: Format numeric values as currency with AED prefix
-- Parameters:
--   amount (Nullable(Float64)): Amount to format
-- Returns: String
-- Example: FORMAT_CURRENCY(1500000) -> 'AED 1.50 million'
-- Real usage: FORMAT_CURRENCY(actual_worth) for transaction amounts
```

## 🚨 Common Issues

### Connection Problems
```python
# Always test connections
try:
    conn = create_connection("test", "client", host="localhost")
    conn.connect()
    assert conn.is_connected()
finally:
    conn.disconnect()
```

### Memory Usage with Large Datasets
```python
# Use generators for large datasets
def process_large_dataset():
    for batch in chunked_data(batch_size=10000):
        yield process_batch(batch)

# Monitor memory usage
import psutil
process = psutil.Process()
print(f"Memory usage: {process.memory_info().rss / 1024 / 1024:.1f} MB")
```

### ClickHouse Specific Issues
```python
# Handle ClickHouse connection timeouts
def robust_query(query, max_retries=3):
    for attempt in range(max_retries):
        try:
            return connection.execute(query)
        except TimeoutError:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            raise
```

### Error Handling
```python
# Provide clear error messages
try:
    result = risky_operation()
except SpecificError as e:
    raise InstallationError(
        f"Failed to install {component}: {e}\n"
        f"Try: pip install missing-dependency"
    ) from e
```

## 📞 Getting Help

- **Questions**: Open a GitHub Discussion
- **Bugs**: Create an Issue with reproduction steps
- **Feature Ideas**: Start with a Discussion before coding
- **Urgent Issues**: Tag maintainers in the issue
- **ClickHouse Help**: [ClickHouse Community](https://clickhouse.com/docs/en/whats-new/community)

## 🎯 Priority Areas

We especially welcome contributions in:

1. **ClickHouse optimization** - Query optimization, indexing strategies
2. **Data validation** - Quality checks, consistency rules
3. **SQL functions** - New formatting, mapping, and calculation functions
4. **Performance tuning** - Large dataset handling, memory optimization
5. **Documentation** - Examples, tutorials, API documentation
6. **Testing** - Edge cases, performance tests, integration tests

## ✅ Checklist Before Submitting

- [ ] Code follows style guidelines (black, isort)
- [ ] Tests pass locally
- [ ] New functionality has tests
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] No sensitive information in code
- [ ] ClickHouse connection tested
- [ ] Performance impact considered

Thank you for contributing to making Dubai's real estate data more accessible! 🏙️