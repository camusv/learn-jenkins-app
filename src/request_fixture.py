# Pytest Request Fixture - Methods and Attributes

import pytest

# This file demonstrates all key methods and attributes of pytest's request fixture

@pytest.fixture
def demonstrate_request_methods(request):
    """
    This fixture demonstrates all the important methods and attributes
    available on pytest's built-in request fixture.
    """
    
    # ------ Core Attributes ------
    
    # request.param - Access parameters when fixture is parameterized
    # Only available if the fixture is parameterized
    if hasattr(request, 'param'):
        param_value = request.param
    
    # request.fixturename - The name of the current fixture
    fixture_name = request.fixturename  # Returns 'demonstrate_request_methods'
    
    # request.scope - The scope of the current fixture ('function', 'class', 'module', 'session')
    fixture_scope = request.scope  # Typically 'function' for most fixtures
    
    # ------ Test Function Information ------
    
    # request.function - The test function object that requested the fixture
    test_func = request.function
    test_func_name = request.function.__name__
    
    # request.cls - The class object if the test is a method in a test class (None otherwise)
    test_class = request.cls  # None if not in a test class
    
    # request.instance - The instance of the test class (None if test is not in a class)
    test_instance = request.instance  # None if not in a test class
    
    # request.module - The module object where the test function is defined
    test_module = request.module
    test_module_name = request.module.__name__
    
    # request.path - Path to the test module as a string
    module_path = request.path
    
    # request.fspath - Path to the test module as a py.path.local object
    file_path = request.fspath
    
    # request.keywords - Dictionary of keywords/markers for the test function
    test_keywords = request.keywords
    
    # request.node - The underlying collection node for the test
    test_node = request.node
    test_node_name = request.node.name
    
    # ------ Configuration Information ------
    
    # request.config - The pytest config object
    config = request.config
    
    # request.config.getoption() - Get command line options
    verbosity = request.config.getoption('--verbose', default=False)
    
    # request.config.rootdir - Root directory of the test run
    root_dir = request.config.rootdir
    
    # ------ Session and Context Information ------
    
    # request.session - The pytest session object
    session = request.session
    
    # ------ Methods for Fixture Lifecycle Management ------
    
    # request.addfinalizer(func) - Add a function to be called when the fixture is torn down
    def cleanup_function():
        print("Cleaning up resources")
    
    request.addfinalizer(cleanup_function)
    
    # request.node.add_marker() - Dynamically add a marker to the test
    request.node.add_marker(pytest.mark.xfail(reason="Demonstrating dynamic markers"))
    
    # request.getfixturevalue(name) - Get the value of another fixture
    # Equivalent to requesting a fixture as a parameter
    try:
        tmp_path_value = request.getfixturevalue('tmp_path')
    except Exception:
        # The fixture might not be available in all contexts
        tmp_path_value = None
    
    # ------ Context Helping Methods ------
    
    # request.node.get_closest_marker() - Get the closest marker of a given name
    skip_marker = request.node.get_closest_marker('skip')
    
    # request.node.listextrakeywords() - List extra keywords for parametrization
    extra_keywords = request.node.listextrakeywords() if hasattr(request.node, 'listextrakeywords') else {}
    
    # ------ Working with Parametrization ------
    
    # request.node.callspec - Access to the "call specification" of a parametrized test
    if hasattr(request.node, 'callspec'):
        call_spec = request.node.callspec
        param_names = call_spec.metafunc.funcargnames if hasattr(call_spec, 'metafunc') else []
        param_values = call_spec.params if hasattr(call_spec, 'params') else {}
    else:
        call_spec = None
        param_names = []
        param_values = {}
    
    # Return a dictionary with all the request properties for demonstration
    return {
        "fixture_name": fixture_name,
        "fixture_scope": fixture_scope,
        "test_func_name": test_func_name,
        "test_module_name": test_module_name,
        "test_node_name": test_node_name,
        # Include other values as needed for demonstration
    }


def test_request_methods(demonstrate_request_methods):
    """Test demonstrating request methods using the fixture above."""
    result = demonstrate_request_methods
    
    # Assertions to verify the request information
    assert result["fixture_name"] == "demonstrate_request_methods"
    assert result["fixture_scope"] in ["function", "class", "module", "session"]
    assert result["test_func_name"] == "test_request_methods"
    assert "test_" in result["test_module_name"]
    assert result["test_node_name"] == "test_request_methods"


# Example using parameterized fixtures to demonstrate request.param
@pytest.fixture(params=["scenario1", "scenario2", "scenario3"])
def scenario(request):
    """A parameterized fixture demonstrating request.param usage."""
    return {
        "name": request.param,
        "fixture_name": request.fixturename,
        "test_name": request.node.name,
    }


def test_parameterized_fixture(scenario):
    """Test demonstrating parameterized fixtures with request."""
    assert scenario["name"] in ["scenario1", "scenario2", "scenario3"]
    assert scenario["fixture_name"] == "scenario"
    assert scenario["test_name"].startswith("test_parameterized_fixture")


# Example using request.getfixturevalue
@pytest.fixture
def fixture_user():
    """A simple fixture providing user data."""
    return {"username": "testuser", "id": 123}


@pytest.fixture
def advanced_fixture(request):
    """A fixture that gets other fixture values using request.getfixturevalue."""
    # Get the value of another fixture dynamically
    user = request.getfixturevalue("fixture_user")
    
    # Extend the user data with additional information
    return {
        **user,
        "is_admin": False,
        "accessed_by": request.fixturename
    }


def test_getfixturevalue(advanced_fixture):
    """Test demonstrating request.getfixturevalue usage."""
    assert advanced_fixture["username"] == "testuser"
    assert advanced_fixture["id"] == 123
    assert advanced_fixture["is_admin"] is False
    assert advanced_fixture["accessed_by"] == "advanced_fixture"


# Example demonstrating dynamic fixture selection based on markers
@pytest.fixture
def data_source(request):
    """
    A fixture that provides different data sources based on test markers.
    """
    # Check if test is marked with a specific marker
    mock_marker = request.node.get_closest_marker("mock_data")
    if mock_marker:
        return {"type": "mock", "data": [1, 2, 3, 4, 5]}
    
    real_marker = request.node.get_closest_marker("real_data")
    if real_marker:
        return {"type": "real", "data": [10, 20, 30, 40, 50]}
    
    # Default case
    return {"type": "default", "data": [0, 0, 0]}


@pytest.mark.mock_data
def test_with_mock_data(data_source):
    """Test using mock data through markers and request.node.get_closest_marker."""
    assert data_source["type"] == "mock"
    assert data_source["data"] == [1, 2, 3, 4, 5]


@pytest.mark.real_data
def test_with_real_data(data_source):
    """Test using real data through markers and request.node.get_closest_marker."""
    assert data_source["type"] == "real"
    assert data_source["data"] == [10, 20, 30, 40, 50]


def test_with_default_data(data_source):
    """Test using default data (no specific marker)."""
    assert data_source["type"] == "default"
    assert data_source["data"] == [0, 0, 0]


# Example using request.addfinalizer for setup/teardown
@pytest.fixture
def managed_resource(request):
    """A fixture demonstrating resource management with addfinalizer."""
    # Setup: Create a resource
    resource = {"name": "test_resource", "status": "active"}
    print(f"\nResource created: {resource['name']}")
    
    # Define teardown function
    def teardown():
        resource["status"] = "inactive"
        print(f"\nResource released: {resource['name']}")
    
    # Register finalizer
    request.addfinalizer(teardown)
    
    return resource


def test_managed_resource(managed_resource):
    """Test demonstrating resource management with addfinalizer."""
    assert managed_resource["status"] == "active"
    # Test operations with the resource
    managed_resource["data"] = "test data"
    assert "data" in managed_resource
    # When test completes, teardown will be called automatically