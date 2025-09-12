#!/usr/bin/env python3
"""
Simple test script to verify the AI Trip Planner application works
"""
import os
from dotenv import load_dotenv

def test_imports():
    """Test that all main imports work"""
    try:
        from Agent.agentic_workflow import GraphBuilder
        from main import app
        from utils.model_loaders import ModelLoader
        from tools.weather_info_tool import WeatherInfoTool
        from tools.place_search_tool import LocationInfoTool
        from tools.currency_converter_tool import CurrencyConverterTool
        from tools.arithematic_operations_tool import ArithematicOperationsTool
        print("✅ All imports successful!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_config_loading():
    """Test config loading"""
    try:
        from utils.config_loader import load_config
        config = load_config()
        print("✅ Config loading successful!")
        print(f"Config keys: {list(config.keys())}")
        return True
    except Exception as e:
        print(f"❌ Config loading error: {e}")
        return False

def test_model_loader():
    """Test model loader without API keys"""
    try:
        from utils.model_loaders import ModelLoader
        model_loader = ModelLoader(model_provider="deepseek")
        print("✅ ModelLoader initialization successful!")
        return True
    except Exception as e:
        print(f"❌ ModelLoader error: {e}")
        return False

def test_graph_builder_init():
    """Test graph builder initialization without API keys"""
    try:
        from Agent.agentic_workflow import GraphBuilder
        # This will likely fail without API keys, but we're testing structure
        graph = GraphBuilder(model_provider="deepseek")
        print("✅ GraphBuilder initialization successful!")
        return True
    except Exception as e:
        print(f"❌ GraphBuilder error: {e}")
        return False

def check_env_setup():
    """Check if environment is set up"""
    load_dotenv()
    
    required_keys = [
        'OPENAI_API_KEY',
        'WEATHER_API_KEY',
        'SERPAPI_API_KEY',
        'TAVILY_API_KEY',
        'EXCHANGE_API_KEY'
    ]
    
    missing_keys = []
    for key in required_keys:
        if not os.getenv(key):
            missing_keys.append(key)
    
    if missing_keys:
        print(f"⚠️  Missing environment variables: {missing_keys}")
        print("Please copy .env.example to .env and add your API keys")
        return False
    else:
        print("✅ All environment variables are set!")
        return True

def main():
    print("🚀 Testing AI Trip Planner Application")
    print("=" * 50)
    
    tests = [
        ("Import Tests", test_imports),
        ("Config Loading", test_config_loading),
        ("Model Loader", test_model_loader),
        ("Environment Setup", check_env_setup),
        ("Graph Builder", test_graph_builder_init),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔧 Running {test_name}...")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY:")
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("\n🎉 All tests passed! The application structure is working correctly.")
        print("You can now run the application with:")
        print("  uvicorn main:app --host 0.0.0.0 --port 8000 --reload")
        print("  streamlit run streamlit_app.py")
    else:
        print(f"\n⚠️  {len(tests) - passed} test(s) failed. Please check the issues above.")

if __name__ == "__main__":
    main()